from django.conf import settings

class Interval:
    """
    A representation of an time range that you can compare with another
    Interval, and perform operations like Union on.
    """
    DEFAULT_TIME_FMT = '%Y-%m-%dT%H:%M:%S'

    def __init__(self, start, end):
        """
        :param start: The start time (datetime)
        :param end: The end time (datetime)
        """
        # An interval can't end before it starts or be empty
        if end <= start:
            raise ValueError("Interval ends before or when it starts")

        self.start = start
        self.end = end

    def __str__(self):
        return '[%s, %s]' % (self.start, self.end)

    def __repr__(self):
        return str(self)

    # Compares by start time.
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        return self.start < other.start
    def __le__(self, other):
        return self.start <= other.start
    def __gt__(self, other):
        return self.start > other.start
    def __ge__(self, other):
        return self.start >= other.start

    # Serializes the interval for fullcalendar
    @property
    def serialized(self):
        return {
            'start': self.start.strftime(getattr(settings, 'TIME_FMT',
                                                 self.DEFAULT_TIME_FMT)),
            'end': self.end.strftime(getattr(settings, 'TIME_FMT',
                                             self.DEFAULT_TIME_FMT)),
        }

    def overlaps(self, other):
        # Returns whether or not two intervals overlap.
        # i.e. if the intervals are not disjoint.
        return not (
            self.start > other.end or
            self.end < other.start)

    def join(self, other):
        # Joins two intervals.
        # Raises a ValueError if the intervals are disjoint.
        if not self.overlaps(other):
            raise ValueError("Intervals don't overlap")

        # Then take the smaller start, and the larger end.
        start = self.start if self.start < other.start else other.start
        end = self.end if self.end > other.end else other.end
        return Interval(start, end)

    @classmethod
    def flatten_intervals(cls, intervals):
        """
        Sorts and flattens a list of intervals:
        i.e. it joins any intervals that overlap,
        turning it into a disjoint list.

        :param intervals: The list of intervals to flatten
        :return: The list of intervals, flattened
        """
        # If too few intervals, no need to union
        if len(intervals) <= 1:
            return intervals

        # Sort descending, use as a stack
        interval_stack = sorted(intervals, reverse=True)

        # Set up the return stack
        flattened_stack = []
        flattened_stack.append(interval_stack.pop())

        # While stack not empty
        while interval_stack:
            # Get the last unioned interval and next un-unioned interval
            prev = flattened_stack.pop()
            next = interval_stack.pop()

            # Attempt to join
            try:
                flattened_stack.append(prev.join(next))

            # If we can't join, just push both to the flattened_stack
            except ValueError:
                flattened_stack.append(prev)
                flattened_stack.append(next)

        # We done, boyz
        return flattened_stack

    @classmethod
    def complement_intervals(cls, intervals, complement_range):
        """
        Returns the complement of a list of intervals, provided an Interval range.

        Raises a ValueError if Interval list is not fully contained in range.

        :param intervals: The list of intervals to complement
        :param complement_range: The Interval range over which to complement
        :return: The list of intervals, complemented
        """
        # If no intervals, just return an interval start -> end
        if len(intervals) == 0:
            return complement_range

        # Sort ascending, use as a queue
        interval_queue = cls.flatten_intervals(intervals)

        # Do the bounds check out?
        if complement_range.start > interval_queue[0].start:
            raise ValueError("Start contained in interval list")
        if complement_range.end < interval_queue[-1].end:
            raise ValueError("End contained in interval list")

        # Set up the return stack
        complement_stack = []

        # Only make an interval if nonempty
        try:
            complement_stack.append(Interval(complement_range.start,
                                             interval_queue[0].start))
        except ValueError:
            pass

        # While queue not empty
        while interval_queue:
            # Push Interval(cur_end, next_start)
            cur_end = interval_queue.pop(0).end

            try:
                next_start = interval_queue[0].start

            # We've reached the end
            except IndexError:
                next_start = complement_range.end

            # Only make an interval if nonempty
            try:
                complement_stack.append(Interval(cur_end, next_start))
            except ValueError:
                pass

        return complement_stack
