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
        # An interval can't end before it starts
        if self.end < self.start:
            raise ValueError("Interval ends before it starts")

        self.start = start
        self.end = end

    # Compares by start time.
    def __lt__(self, other):
        return self.start < other.start
    def __le__(self, other):
        return self.start <= other.start
    def __gt__(self, other):
        return self.start > other.start
    def __ge__(self, other):
        return self.start >= other.start

    # Serializes the interval for fullcalendar
    def serialize(self):
        return {
            'start': self.start.strftime(getattr(settings, 'TIME_FMT',
                                                 self.DEFAULT_TIME_FMT)),
            'end': self.end.strftime(getattr(settings, 'TIME_FMT',
                                             self.DEFAULT_TIME_FMT)),
        }

    def overlaps(self, other):
        # Returns whether or not two intervals overlap.
        # i.e. if the intervals are disjoint.
        return self.end < other.start or self.start > other.end

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
    def union_list(cls, intervals):
        """
        Returns the union list of a list of intervals.
        :param intervals: The list of intervals to union
        :return: The list of intervals, union-list-ified
        """
        # Sort descending, use as a stack
        interval_stack = sorted((i.interval for i in intervals), reverse=True)

        # Set up the return stack
        union_stack = []
        union_stack.append(interval_stack.pop())

        # While stack not empty
        while interval_stack:
            # Get the last unioned interval and next un-unioned interval
            prev = union_stack.pop()
            next = interval_stack.pop()

            # Attempt to join
            try:
                union_stack.append(prev.join(next))

            # If we can't join, just push both to the union_stack
            except ValueError:
                union_stack.append(prev)
                union_stack.append(next)

        # We done, boyz
        return union_stack

    @classmethod
    def complement(cls, intervals, start, end):
        """
        Returns the complement of a list of intervals, provided a start
        boundary and an end boundary. If start or end occurs within
        the complement range, just use the complement range.
        :param intervals: The list of intervals to complement
        :param start: The start boundary of the complement
        :param end: The end boundary of the complement
        :return: The list of intervals, complemented
        """
        # Sort ascending, use as a queue
        interval_queue = sorted(i.interval for i in intervals)

        # Do the bounds check out?
        try:
            # Check the start bound
            if start < interval_queue[0].end:
                start_bound = start
            else:
                # Toss the first interval
                start_bound = interval_queue.pop(0).end

            # Check the end bound
            if end > interval_queue[-1].start:
                end_bound = end
            else:
                # Toss the last interval
                end_bound = interval_queue.pop().start

        # If we can't get anything, we have an empty interval list.
        # Complement of nothing start -> end.
        except IndexError:
            return Interval(start, end)

        # Set up the return stack
        complement_stack = []
        complement_stack.append(Interval(start_bound, interval_queue[0].start))

        while interval_queue:
            # Push Interval(cur.end, next.start)
            pass
