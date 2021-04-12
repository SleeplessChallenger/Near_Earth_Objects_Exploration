import unittest
import collections
import pathlib
import unittest.mock
import contextlib
import io
import csv
import json
import datetime


import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


from database import NEODatabase
from extract import load_neos, load_approaches
from write import write_to_csv, write_to_json


ROOT = pathlib.Path(__file__).cwd().parent
data_csv = ROOT / 'data' / 'neos-2020.csv'
data_json = ROOT / 'data' / 'cad-2020.json'


def retrieve_data(lim):
	csv_data = list(load_neos(data_csv))
	json_data = list(load_approaches(data_json))

	NEODatabase(csv_data, json_data)
	return json_data[:lim]


# about StringIO() vs open():
# https://stackoverflow.com/questions/50418448/io-stringio-vs-open-in-python-3/50418544

# about UncloseableStringIO() -ISH operation:
# https://stackoverflow.com/questions/30510282/reopening-a-closed-stringio-object-in-python-3

# about getvalue() and seek():
# https://webkul.com/blog/using-io-for-creating-file-object/

@contextlib.contextmanager
def UncloseableStringIO(value=''):
	buf = io.StringIO(value)
	buf._close = buf.close
	buf.close = lambda: False
	yield buf
	buf.close = buf._close
	delattr(buf, '_close')
	buf.close()


# In two classes below 'patch' is used as a
# decorator which takes required param/s which
# will be patched. In our case it is 'write.py'
# module and 'open()' function. 'setUpClass' has
# a param that will be the mocking object passed to the tests. 
# Next, we use altered 'context manager' as we need to modify
# the open/close stuff.
# with 'open()' as buf: .
# content from the context manager is attached to that mocking object
class CSVTest(unittest.TestCase):
	@classmethod
	@unittest.mock.patch('write.open')
	def setUpClass(cls, mock_file):
		results = retrieve_data(6)

		with UncloseableStringIO() as buf:
			mock_file.return_value = buf

			try:
				write_to_csv(results, None)
			except csv.Error as err:
				raise cls.failureException('Problems with writing data to csv') from err
			except ValueError as err:
				raise cls.failureException('Some error when writing data to csv') from err
			else:
				buf.seek(0)
				cls.value = buf.getvalue()

	def test_csv_data_formed_good(self):
		buf = io.StringIO(self.value)
		# buf is in list format
		try:
			# take the output and discard it immediately
			collections.deque(csv.DictReader(buf), maxlen=0)
		except csv.Error as err:
			raise self.failureException('write_to_csv gives wrong output') from err

	def test_csv_data_has_header(self):
		try:
			self.assertTrue(csv.Sniffer().has_header(self.value))
		except csv.Error as err:
			raise self.failureException('Unable to retrieve headers') from err

	def test_csv_file_has_six_rows(self):
		buf = io.StringIO(self.value)

		try:
			reader = csv.DictReader(buf)
			rows = list(reader)
		except csv.Error as err:
			raise self.failureException('write_to_csv gives wrong output') from err
		self.assertEqual(len(rows), 6)
		self.assertIsInstance(rows, collections.abc.Sequence)

	def test_csv_file_headers_right(self):
		buf = io.StringIO(self.value)

		try:
			reader = csv.DictReader(buf)
			rows = list(reader)
		except csv.Error as err:
			raise self.failureException('write_to_csv gives wrong output') from err

		fieldnames = ['datetime_utc', 'distance_au', 'velocity_km_s', 'designation',
					  'name', 'diameter_km', 'potentially_hazardous']
		self.assertGreater(len(rows), 0)
		self.assertListEqual(list(fieldnames), list(rows[0].keys()))


class JSONTest(unittest.TestCase):
	@classmethod
	@unittest.mock.patch('write.open')
	def setUpClass(cls, mock_file):
		results = retrieve_data(7)

		with UncloseableStringIO() as buf:
			mock_file.return_value = buf

			try:
				write_to_json(results, None)
			except csv.Error as err:
				raise cls.failureException('write_to_json gives wrong output') from err
			except ValueError as err:
				raise cls.failureException('Some error when writing data to json') from err
			else:
				buf.seek(0)
				cls.value = buf.getvalue()

	def test_json_data_formed_good(self):
		buf = io.StringIO(self.value)
		# buf is dict in list
		try:
			json.load(buf)
		except json.JSONDecodeError as err:
			raise self.failureException('write_to_json gives wrong output') from err

	def test_json_data_is_sequence(self):
		buf = io.StringIO(self.value)

		try:
			data = json.load(buf)
		except json.JSONDecodeError as err:
			raise self.failureException('write_to_json gives invalid format of the document') from err
		self.assertIsInstance(data, collections.abc.Sequence)
		self.assertIsInstance(data[0], collections.abc.Collection)

	def test_json_data_has_seven(self):
		buf = io.StringIO(self.value)

		try:
			data = json.load(buf)
		except json.JSONDecodeError as err:
			raise self.failureException('write_to_json gives invalid format of the document') from err
		self.assertEqual(len(data), 7)

	def test_json_data_is_mapping(self):
		buf = io.StringIO(self.value)

		try:
			data = json.load(buf)
		except json.JSONDecodeError as err:
			raise self.failureException('write_to_json gives invalid format of the document') from err
		data = data[0]
		self.assertIsInstance(data, collections.abc.Mapping)

	def test_json_data_has_nested_data(self):
		buf = io.StringIO(self.value)

		try:
			data = json.load(buf)
		except json.JSONDecodeError as err:
			raise self.failureException('write_to_json gives invalid format of the document') from err

		data_two = data[0]
		self.assertIn('datetime_utc', data_two)
		self.assertIn('distance_au', data_two)
		self.assertIn('velocity_km_s', data_two)
		self.assertIn('neo', data_two)

		data_neo = data_two.get('neo')
		self.assertIn('designation', data_neo)
		self.assertIn('name', data_neo)
		self.assertIn('diameter_km', data_neo)
		self.assertIn('potentially_hazardous', data_neo)

	def test_json_decodes_correct_types(self):
		buf = io.StringIO(self.value)

		try:
			data = json.load(buf)
		except json.JSONDecodeError as err:
			raise self.failureException('write_to_json gives invalid format of the document') from err

		# appraoches first
		approach = data[0]
		try:
			datetime.datetime.strptime(approach.get('datetime_utc'), '%Y-%m-%d %H:%M')
		except ValueError:
			self.fail("The 'datetime_utc' isn't in YYYY-MM-DD HH:MM`")
		self.assertIsInstance(approach.get('distance_au'), float)
		self.assertIsInstance(approach.get('velocity_km_s'), float)

		#next is neo
		self.assertIsInstance(approach.get('neo').get('designation'), str)
		self.assertNotEqual(approach.get('neo').get('name'), 'None')
		if approach.get('neo').get('name'):
			self.assertIsInstance(approach.get('neo').get('name'), str)
		self.assertIsInstance(approach.get('neo').get('diameter_km'), float)
		self.assertIsInstance(approach.get('neo').get('potentially_hazardous'), bool)


if __name__ == '__main__':
	unittest.main()
