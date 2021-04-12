import unittest
import pathlib
import math

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from extract import load_neos, load_approaches
from database import NEODatabase

ROOT = pathlib.Path(__file__).cwd().parent
data_csv = ROOT / 'data' / 'neos-2020.csv'
data_json = ROOT / 'data' / 'cad-2020.json'


class ModelsTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.neos = load_neos(data_csv)
		cls.approaches = load_approaches(data_json)
		cls.db = NEODatabase(cls.neos, cls.approaches)

	def test_every_neo_attribute(self):
		for obj in self.neos:
			self.assertTrue(hasattr(obj, 'approaches'))

	def test_attribute_not_none(self):
		for approach in self.approaches:
			self.assertIsNotNone(approach.neo)

	def test_neo_by_designation(self):
		# first
		temp = self.db.get_neo_by_designation('1865')
		self.assertIsNotNone(temp)
		self.assertEqual(temp.designation, '1865')
		self.assertEqual(temp.name, 'Cerberus')
		self.assertEqual(temp.diameter, 1.2)
		self.assertEqual(temp.hazardous, False)
		# second
		temp = self.db.get_neo_by_designation('2101')
		self.assertIsNotNone(temp)
		self.assertEqual(temp.designation, '2101')
		self.assertEqual(temp.name, 'Adonis')
		self.assertEqual(temp.diameter, 0.60)
		self.assertEqual(temp.hazardous, True)
		# third
		temp = self.db.get_neo_by_designation('2102')
		self.assertIsNotNone(temp)
		self.assertEqual(temp.designation, '2102')
		self.assertEqual(temp.name, 'Tantalus')
		self.assertEqual(temp.diameter, 1.649)
		self.assertEqual(temp.hazardous, True)

	def test_neo_no_name(self):
		# first
		temp = self.db.get_neo_by_designation('2020 BS')
		self.assertIsNotNone(temp)
		self.assertEqual(temp.designation, '2020 BS')
		self.assertEqual(temp.name, None)
		self.assertTrue(math.isnan(temp.diameter))
		self.assertEqual(temp.hazardous, False)

		# second
		temp = self.db.get_neo_by_designation('2020 PY1')
		self.assertIsNotNone(temp)
		self.assertEqual(temp.designation, '2020 PY1')
		self.assertEqual(temp.name, None)
		self.assertTrue(math.isnan(temp.diameter))
		self.assertEqual(temp.hazardous, False)

	def test_check_non_existing(self):
		none_neo = self.db.get_neo_by_designation('some_random')
		self.assertIsNone(none_neo)

	def test_get_neo_by_name(self):
		# first
		temp = self.db.get_neo_by_name('Lemmon')
		self.assertIsNotNone(temp)
		self.assertEqual(temp.designation, '2013 TL117')
		self.assertEqual(temp.name, 'Lemmon')
		self.assertTrue(math.isnan(temp.diameter))
		self.assertEqual(temp.hazardous, False)

		# second
		temp = self.db.get_neo_by_name('Jormungandr')
		self.assertIsNotNone(temp)
		self.assertEqual(temp.designation, '471926')
		self.assertEqual(temp.name, 'Jormungandr')
		self.assertTrue(math.isnan(temp.diameter))
		self.assertEqual(temp.hazardous, True)

	def test_check_non_name_existing(self):
		none_obj = self.db.get_neo_by_name('some_random_name')
		self.assertIsNone(none_obj)


if __name__ == '__main__':
	unittest.main()
