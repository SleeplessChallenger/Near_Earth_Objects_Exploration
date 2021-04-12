import unittest
import pathlib
import os
import csv, json
from collections import deque


ROOT = pathlib.Path(__file__).cwd().parent


class FilesTest(unittest.TestCase):
	def setUp(self):
		self.root = ROOT
		self.data_root = self.root / 'data'
		self.neos = self.data_root / 'neos.csv'
		self.json = self.data_root / 'cad.json'

	def test_existance(self):
		'''Check that files exist'''
		self.assertTrue(self.neos.exists())
		self.assertTrue(self.json.exists())

	def test_readable(self):
		'''Check that files can be read'''
		self.assertTrue(os.access(self.neos, os.R_OK))
		self.assertTrue(os.access(self.json, os.R_OK))

	def test_not_empty(self):
		'''Check that files are not empty'''
		try:
			self.assertTrue(self.neos.stat().st_size > 0, 'CSV file is empty!')
			self.assertTrue(self.json.stat().st_size > 0, 'JSON file ie empty')
		except OSError:
			self.fail('OSError. Check directories or paths')

	def test_files_format(self):
		'''At first check CSV file, then JSON one'''
		try:
			with self.neos.open() as file:
				deque(csv.reader(file), maxlen=0)
				# If maxlen is not specified or is None, deques may grow to an arbitrary length.
				# Otherwise, the deque is bounded to the specified maximum length.
				# Once a bounded length deque is full, when new items are added,
				# a corresponding number of items are discarded from the opposite end. 
		except csv.Error as err:
			# `from err` allows to chain errors => preserve traceback
			raise self.failureException(f"{self.neos} is of wrong format!") from err

		try:
			with self.json.open() as file:
				json.load(file)
			# load() is for loading file
			# loads() is for converting it into python list
			json.loads(self.json.read_text())
		except json.JSONDecodeError as err:
			raise self.failureException(f"{self.json} is of wrong format or something else") from err


if __name__ == '__main__':
	unittest.main()
