from django.test import TestCase
from django.utils import timezone
from ourcalendar.logic.event_comparison import Interval


class IntervalTestCase(TestCase):
    def setUp(self):
        self.t0 = timezone.now()
        self.t1 = self.t0 + timezone.timedelta(hours=1)
        self.t2 = self.t0 + timezone.timedelta(hours=2)
        self.t3 = self.t0 + timezone.timedelta(hours=3)
        self.t4 = self.t0 + timezone.timedelta(hours=4)

        times = [self.t0, self.t1, self.t2, self.t3, self.t4]

        # Generate the ranges
        for start in range(4):
            for end in range(4):
                try:
                    setattr(self, 't%s_t%s' % (start, end),
                            Interval(times[start], times[end]))
                except ValueError:
                    pass

    def test_validation(self):
        # Test if class validation works
        Interval(self.t0, self.t1)
        Interval(self.t0, self.t0)

        with self.assertRaises(ValueError):
            Interval(self.t1, self.t0)

    def test_operators(self):
        self.assertEqual(self.t0_t1, self.t0_t1)
        self.assertNotEqual(self.t0_t0, self.t1_t2)
        self.assertLess(self.t0_t1, self.t1_t2)
        self.assertLessEqual(self.t0_t1, self.t0_t0)
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

    def test_union(self):
        # Normal case
        self.assertItemsEqual(Interval.union_list([
            self.t0_t1, self.t1_t2, self.t2_t3,
        ]), [
            self.t0_t3,
        ])

        # Single interval case
        self.assertItemsEqual(Interval.union_list([
            self.t0_t3,
        ]), [
            self.t0_t3,
        ])

        # FIXME
        self.assertItemsEqual(Interval.union_list([
            self.t0_t1, self.t2_t3,
        ]), [
            self.t0_t1, self.t2_t3,
        ])
