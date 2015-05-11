from django.test import TestCase
from django.utils import timezone
from ourcalendar.logic.intervals import Interval


class IntervalTestCase(TestCase):

    NUM_TIMES = 10

    def setUp(self):
        self.t0 = timezone.now()

        for i in range(1, self.NUM_TIMES):
            setattr(self, 't%s' % i, self.t0 + timezone.timedelta(hours=i))

        # Generate the ranges
        for start in range(self.NUM_TIMES):
            for end in range(self.NUM_TIMES):
                try:
                    setattr(self, 't%s_t%s' % (start, end),
                            Interval(
                                getattr(self, 't%s' % start),
                                getattr(self, 't%s' % end)
                            ))
                except ValueError:
                    pass

    def test_validation(self):
        # Normal interval
        Interval(self.t0, self.t1)

        # Empty interval
        with self.assertRaises(ValueError):
            Interval(self.t0, self.t0)

        # Starts before ends
        with self.assertRaises(ValueError):
            Interval(self.t1, self.t0)

    # Don't mind the "unresolve attribute references"
    # I'm doing some metaprogramming :^)

    def test_operators(self):
        self.assertEqual(self.t0_t1, self.t0_t1)
        self.assertNotEqual(self.t0_t1, self.t1_t2)
        self.assertLess(self.t0_t1, self.t1_t2)
        self.assertLessEqual(self.t0_t1, self.t0_t2)
        self.assertLessEqual(self.t0_t1, self.t1_t2)
        self.assertGreater(self.t1_t2, self.t0_t2)
        self.assertGreaterEqual(self.t1_t2, self.t1_t2)
        self.assertGreaterEqual(self.t1_t2, self.t0_t2)

    def test_overlaps(self):
        self.assertFalse(self.t0_t1.overlaps(self.t2_t3))
        self.assertFalse(self.t2_t3.overlaps(self.t0_t1))
        self.assertTrue(self.t0_t2.overlaps(self.t2_t3))
        self.assertTrue(self.t2_t3.overlaps(self.t0_t2))
        self.assertTrue(self.t0_t2.overlaps(self.t1_t3))
        self.assertTrue(self.t1_t3.overlaps(self.t0_t2))

    def test_join(self):
        self.assertEqual(self.t0_t1.join(self.t0_t2), self.t0_t2)
        self.assertEqual(self.t0_t2.join(self.t2_t3), self.t0_t3)
        self.assertEqual(self.t0_t2.join(self.t1_t3), self.t0_t3)

    def test_flatten(self):
        # No intervals
        self.assertEqual(Interval.flatten_intervals([]), [])

        # Single interval
        self.assertEqual(Interval.flatten_intervals([
            self.t0_t3,
        ]), [
            self.t0_t3,
        ])

        # Non-unionable intervals
        self.assertEqual(Interval.flatten_intervals([
            self.t0_t1, self.t2_t3,
        ]), [
            self.t0_t1, self.t2_t3,
        ])

        # Unionable intervals
        self.assertEqual(Interval.flatten_intervals([
            self.t0_t1, self.t1_t2, self.t3_t4,
        ]), [
            self.t0_t2, self.t3_t4,
        ])

        # Union to single interval
        self.assertEqual(Interval.flatten_intervals([
            self.t0_t1, self.t1_t2, self.t2_t3,
        ]), [
            self.t0_t3,
        ])

        # Identical intervals
        self.assertEqual(Interval.flatten_intervals([
            self.t0_t1, self.t0_t1,
        ]), [
            self.t0_t1,
        ])

    def test_complement(self):
        # Invalid start
        with self.assertRaises(ValueError):
            Interval.complement_intervals([self.t0_t3], Interval(self.t1, self.t4))

        # Invalid end
        with self.assertRaises(ValueError):
            Interval.complement_intervals([self.t1_t4], Interval(self.t0, self.t3))

        # No intervals
        self.assertEqual(Interval.complement_intervals([], Interval(self.t0, self.t4)),
            self.t0_t4)

        # One interval
        self.assertEqual(Interval.complement_intervals([
            self.t1_t3,
        ], Interval(self.t0, self.t4)),[
            self.t0_t1, self.t3_t4
        ])

        # Identical intervals
        self.assertEqual(Interval.complement_intervals([
            self.t1_t3, self.t1_t3
        ], Interval(self.t0, self.t4)),[
            self.t0_t1, self.t3_t4
        ])


        # Overlapping intervals
        self.assertEqual(Interval.complement_intervals([
            self.t2_t5, self.t4_t7
        ], Interval(self.t0, self.t9)),[
            self.t0_t2, self.t7_t9
        ])

        # Disjiont intervals
        self.assertEqual(Interval.complement_intervals([
            self.t2_t4, self.t6_t8
        ], Interval(self.t0, self.t9)),[
            self.t0_t2, self.t4_t6, self.t8_t9
        ])

        # All intervals
        self.assertEqual(Interval.complement_intervals([
            self.t0_t9,
        ], Interval(self.t0, self.t9)),[])
