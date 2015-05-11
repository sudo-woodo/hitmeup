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

    def test_validation(self):
        # Test if class validation works
        Interval(self.t0, self.t1)
        Interval(self.t0, self.t0)

        with self.assertRaises(ValueError):
            Interval(self.t1, self.t0)

    def test_operators(self):
        t0_t0 = Interval(self.t0, self.t0)
        t0_t1 = Interval(self.t0, self.t1)
        t0_t2 = Interval(self.t0, self.t2)
        t1_t2 = Interval(self.t1, self.t2)

        self.assertEqual(t0_t1, t0_t1)
        self.assertNotEqual(t0_t0, t1_t2)
        self.assertLess(t0_t1, t1_t2)
        self.assertLessEqual(t0_t1, t0_t0)
        self.assertLessEqual(t0_t1, t1_t2)
        self.assertGreater(t1_t2, t0_t2)
        self.assertGreaterEqual(t1_t2, t1_t2)
        self.assertGreaterEqual(t1_t2, t0_t2)

    def test_overlaps(self):
        t0_t1 = Interval(self.t0, self.t1)
        t0_t2 = Interval(self.t0, self.t2)
        t2_t3 = Interval(self.t2, self.t3)
        t1_t3 = Interval(self.t1, self.t3)

        self.assertFalse(t0_t1.overlaps(t2_t3))
        self.assertFalse(t2_t3.overlaps(t0_t1))
        self.assertTrue(t0_t2.overlaps(t2_t3))
        self.assertTrue(t2_t3.overlaps(t0_t2))
        self.assertTrue(t0_t2.overlaps(t1_t3))
        self.assertTrue(t1_t3.overlaps(t0_t2))

    def test_join(self):
        t0_t1 = Interval(self.t0, self.t1)
        t0_t2 = Interval(self.t0, self.t2)
        t2_t3 = Interval(self.t2, self.t3)
        t0_t3 = Interval(self.t0, self.t3)
        t1_t3 = Interval(self.t1, self.t3)

        self.assertEqual(t0_t1.join(t0_t2), t0_t2)
        self.assertEqual(t0_t2.join(t2_t3), t0_t3)
        self.assertEqual(t0_t2.join(t1_t3), t0_t3)
