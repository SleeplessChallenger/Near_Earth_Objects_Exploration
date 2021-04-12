import unittest
import pathlib
import collections
import datetime
import math


import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
# /Users/daniilslobodenuk/Desktop/Udacity/Near_Earth_Objects_Exploration/tests/../

from extract import load_neos, load_approaches
from models import NearEarthObject, CloseApproach


ROOT = pathlib.Path(__file__).cwd().parent
data_csv = ROOT / 'data' / 'neos-2020.csv'
data_json = ROOT / 'data' / 'cad-2020.json'


class NEOTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.csv_file = load_neos(data_csv)
		cls.neo_design = {x.designation: x for x in cls.csv_file}

	@classmethod
	def get_or_none(cls):
		'''receive neo and stop when end'''
		try:
			return next(iter(cls.csv_file))
		except StopIteration:
			return None

	# to test that retrieved data is collection [iterable, sized, container]
	def test_object_iterable(self):
		self.assertIsInstance(self.csv_file, collections.abc.Collection)

	def test_class_contain_object(self):
		neo = self.get_or_none()
		self.assertIsNotNone(neo)
		self.assertIsInstance(neo, NearEarthObject)

	def test_all_elements(self):
		self.assertEqual(len(self.csv_file), 4226)

	def test_first_element_in_params(self):
		self.assertIn('2019 SC8', self.neo_design)
		neo = self.neo_design.get('2019 SC8')
		self.assertEqual(neo.designation, '2019 SC8')
		self.assertEqual(neo.name, None)
		self.assertTrue(math.isnan(neo.diameter))
		self.assertEqual(neo.hazardous, False)

	def test_second_element_in_params(self):
		self.assertIn('4581', self.neo_design)
		neo = self.neo_design.get('4581')
		self.assertEqual(neo.designation, '4581')
		self.assertEqual(neo.name, 'Asclepius')
		self.assertTrue(math.isnan(neo.diameter))
		self.assertEqual(neo.hazardous, True)

	def test_third_element_in_params(self):
		self.assertIn('2101', self.neo_design)
		neo = self.neo_design.get('2101')
		self.assertEqual(neo.designation, '2101')
		self.assertEqual(neo.name, 'Adonis')
		self.assertEqual(neo.diameter, 0.6)
		self.assertEqual(neo.hazardous, True)


class APPRTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.json_file = load_approaches(data_json)

	@classmethod
	def get_or_none(cls):
		try:
			return next(iter(cls.json_file))
		except StopIteration:
			return None

	def test_object_iterable(self):
		self.assertIsInstance(self.json_file, collections.abc.Collection)
		# Collections in python are basically container
		# data types, namely lists, sets, tuples, dictionary. 

	def test_class_contain_object(self):
		approach = self.get_or_none()
		self.assertIsNotNone(approach)
		self.assertIsInstance(approach, CloseApproach)

	def test_all_elements(self):
		self.assertEqual(len(self.json_file), 4700)

	def test_date_format(self):
		approach = self.get_or_none()
		self.assertIsNotNone(approach)
		self.assertIsInstance(approach.time, datetime.datetime)

	def test_distance_type(self):
		approach = self.get_or_none()
		self.assertIsNotNone(approach)
		self.assertIsInstance(approach.distance, float)

	def test_velocity_type(self):
		approach = self.get_or_none()
		self.assertIsNotNone(approach)
		self.assertIsInstance(approach.velocity, float)


if __name__ == '__main__':
	unittest.main()
