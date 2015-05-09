class Interval:
    """
    A representation of an time range that you can compare with another
    Interval, and perform operations like Union on.
    """
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
    def union(intervals):
        """
        Returns the union of a list of intervals.
        :param events: The list of intervals to union
        :return:
        """
        # Sort descending, use as a stack
        interval_stack = sorted((i.interval for i in intervals), reverse=True)

        # Set up the return value
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
