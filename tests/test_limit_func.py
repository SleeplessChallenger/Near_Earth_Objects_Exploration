import unittest
import collections

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from filters import limit


class LimitTest(unittest.TestCase):
	# iterator - object that can be iterated upon
	# iterable - the one that iterates
	def setUp(self):
		self.iterable = tuple(range(6))

	def test_iterable_limit(self):
		self.assertEqual(tuple(limit(self.iterable, 4)), (0, 1, 2, 3))
		self.assertEqual(tuple(limit(self.iterable, 6)), (0, 1, 2, 3, 4, 5))
		self.assertEqual(tuple(limit(self.iterable, 12)), (0, 1, 2, 3, 4, 5))

	def test_iterable_without_limit(self):
		self.assertEqual(tuple(limit(self.iterable)), (0, 1, 2, 3, 4, 5))
		self.assertEqual(tuple(limit(self.iterable, 0)), (0, 1, 2, 3, 4, 5))
		self.assertEqual(tuple(limit(self.iterable, None)), (0, 1, 2, 3, 4, 5))

	def test_iterator_limit(self):
		self.assertEqual(tuple(limit(iter(self.iterable), 2)), (0, 1))
		self.assertEqual(tuple(limit(iter(self.iterable), 6)), (0, 1, 2, 3, 4, 5))
		self.assertEqual(tuple(limit(iter(self.iterable), 17)), (0, 1, 2, 3, 4, 5))

	def test_iterator_without_limit(self):
		self.assertEqual(tuple(limit(iter(self.iterable), 0)), (0, 1, 2, 3, 4, 5)) 
		self.assertEqual(tuple(limit(iter(self.iterable))), (0, 1, 2, 3, 4, 5))
		self.assertEqual(tuple(limit(iter(self.iterable), None)), (0, 1, 2, 3, 4, 5))

	def test_limit_gives_iterable(self):
		self.assertIsInstance(limit(self.iterable, 4), collections.abc.Iterable)
		self.assertIsInstance(limit(self.iterable, 15), collections.abc.Iterable)
		self.assertIsInstance(limit(self.iterable, 0), collections.abc.Iterable)
		self.assertIsInstance(limit(self.iterable), collections.abc.Iterable)
		self.assertIsInstance(limit(self.iterable, None), collections.abc.Iterable)
		self.assertIsInstance(limit(self.iterable, 6), collections.abc.Iterable)


if __name__ == '__main__':
	unittest.main()
