from datetime import datetime, timedelta
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from ourcalendar.models import Event

PHANTOMJS_BIN = './node_modules/phantomjs/bin/phantomjs'
TRITONLINK_URL = 'http://mytritonlink.ucsd.edu/'
USERNAME_NAME = 'urn:mace:ucsd.edu:sso:username'
PASSWORD_NAME = 'urn:mace:ucsd.edu:sso:password'
TIMEOUT = 10
LOGIN_ERROR_CLASS = 'error'
CLASSES_CONTAINER_ID = 'class_schedule'
CLASSES_ELEM = 'td'
CLASSES_CLASS = 'class'
MON = 'Monday'
TUE = 'Tuesday'
WED = 'Wednesday'
THU = 'Thursday'
FRI = 'Friday'
WEEK_DAYS = (MON, TUE, WED, THU, FRI)
DAYS_OF_WEEK = {day: idx for idx, day in enumerate(WEEK_DAYS)}
HRS_24 = 24
HRS_12 = 12
MAX_MIN = 59
MIN_MIN = 0
MAX_HR = 12
MIN_HR = 1
AM_PM_POS = -2


# For incorrect login info
class AuthenticationException(Exception):
    pass


# For TritonLink errors
class TritonLinkException(Exception):
    pass


def get_classes(username, password):
    """Gets the classes of a student attending UC San Diego from TritonLink.

    :param username: the username of the student
    :param password: the (raw) password of the student
    :return: a list of dicts, where each dict represents a class
        with fields: name, day, time, location
    """

    def chunk(l, size):
        return [l[i:i+size] for i in xrange(0, len(l), size)]

    driver = webdriver.PhantomJS(PHANTOMJS_BIN)
    driver.implicitly_wait(TIMEOUT)

    driver.get(TRITONLINK_URL)

    # Get redirected to login page
    login_url = driver.current_url

    # Send to elements
    e_username = driver.find_element_by_name(USERNAME_NAME)
    e_password = driver.find_element_by_name(PASSWORD_NAME)
    e_username.send_keys(username)
    e_password.send_keys(password)
    e_password.send_keys(Keys.RETURN)

    try:
        WebDriverWait(driver, TIMEOUT).until(
            lambda d: d.find_element_by_css_selector("#%s, .%s" %
                                                     (CLASSES_CONTAINER_ID, LOGIN_ERROR_CLASS)
                                                     )
        )

        # Check if logged in
        if driver.current_url == login_url:
            raise AuthenticationException

        bs_mtl = BeautifulSoup(driver.page_source)
    except TimeoutException:
        raise TritonLinkException("Request timed out")
    finally:
        driver.quit()

    # Parse TritonLink

    # Get all class elements by weekday
    try:
        bs_classes_container = bs_mtl.find_all(id=CLASSES_CONTAINER_ID)[0]
    except IndexError:
        raise TritonLinkException("Classes container not found")

    bs_classes = bs_classes_container.find_all(CLASSES_ELEM)
    by_weekday = zip(*chunk(bs_classes, len(WEEK_DAYS)))

    # Process each td
    classes = []
    for class_day, day in zip(WEEK_DAYS, by_weekday):
        for clazz in day:
            try:
                class_info = clazz.find_all(class_=CLASSES_CLASS)[0]
            # If empty, skip
            except IndexError:
                continue

            class_time, class_name, class_loc = list(class_info.stripped_strings)
            classes.append({
                'name': class_name,
                'day': class_day,
                'time': class_time,
                'location': class_loc,
            })

    return classes


def create_event(user, cls):
    """Creates an event on the user's calendar with the given class information.

    :param user: the UserProfile whose calendar the events will be created on
    :param cls: a dict containing class information, with fields: name, day, time, location
    :return: the Event object created (or retrieved)
    """

    name = cls['name']
    day_of_week = cls['day']
    time = cls['time']
    location = cls['location']

    start_time, end_time = [extract_time(t.strip()) for t in time.split('-')]

    # Get datetime for next occurrence of day of week, starting from today
    # TODO specify start and end time of current UC San Diego quarter
    # TODO create recurring events instead of one-off
    date = next_day_of_week(datetime.now().replace(second=0, microsecond=0),
                            DAYS_OF_WEEK[day_of_week])
    start = date.replace(hour=start_time[0], minute=start_time[1])
    end = date.replace(hour=end_time[0], minute=end_time[1])

    # Prevents creation of already-imported events through hashing of class info
    event, created = Event.objects.get_or_create(
        calendar=user.calendars.get(title='Default'),
        import_hash=hash(frozenset(cls.items()))
    )

    event.title = name
    event.start = start
    event.end = end
    event.location = location
    event.description = "Imported by TritonSync"
    event.save()

    return event


def next_day_of_week(current, day_of_week):
    """Returns a datetime of the next day of the week.

    :param current: the starting datetime
    :param day_of_week: an int corresponding to the day of the week.
        Monday = 0, ... , Friday = 4
    :return: the datetime of the first day of the week after (or on) current datetime
    """

    while current.weekday() != day_of_week:
        current += timedelta(1)
    return current


# TODO remove magic numbers
def extract_time(time):
    """Extracts the 24-hour (hours, minutes) from a 12-hour time string.

    :param time: a time string in the format HH:MM(am|AM|pm|PM), e.g. "4:20pm"
    :return: tuple of ints (hours, minutes) translated to 24-hour time
    """

    # Ensure time string is in correct format
    time_regex = re.compile("^\d{1,2}:\d{2}(am|AM|pm|PM)$")
    if not time_regex.match(time):
        raise ValueError("Time (%s) is not in format HH:MM(am|AM|pm|PM)" % time)

    am_pm = time[AM_PM_POS:]
    hours, minutes = map(int, time[:AM_PM_POS].split(':'))

    # Error checking
    if hours not in range(MIN_HR, MAX_HR + 1):
        raise ValueError("Hours (%d) is not between [%d, %d]" % (hours, MIN_HR, MAX_HR))
    if minutes not in range(MIN_MIN, MAX_MIN + 1):
        raise ValueError("Minutes (%d) is not between [%d, %d]" % (minutes, MIN_MIN, MAX_MIN))

    # Apply 12-hour to 24-hour time corrections
    hours %= HRS_12
    if am_pm == 'pm' or am_pm == 'PM':
        hours = (hours + HRS_12) % HRS_24

    return hours, minutes


def import_schedule(user, classes):
    """Imports a schedule of classes into a given user's calendar.

    :param user: a UserProfile, whose calendar to import the events into
    :param classes: a list of dicts, where each dict represents a class
        with fields: name, day, time, location
    :return: None
    """

    for cls in classes:
        create_event(user, cls)