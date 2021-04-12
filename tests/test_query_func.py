import unittest
import datetime
import pathlib


import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from database import NEODatabase
from extract import load_neos, load_approaches
from filters import create_filters


ROOT = pathlib.Path(__file__).cwd().parent
data_csv = ROOT / 'data' / 'neos-2020.csv'
data_json = ROOT / 'data' / 'cad-2020.json'


class QueryTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.neos = load_neos(data_csv)
		cls.approaches = load_approaches(data_json)
		cls.db = NEODatabase(cls.neos, cls.approaches)

	# tests regarding date
	def test_query_all(self):
		'''First, test that data > 0
		   Second, test that hollow filters
		   give same result as ordinary data'''
		data = self.approaches
		self.assertGreater(len(data), 0)

		filters = create_filters()
		data_two = list(self.db.query(filters))
		# list() is crucial as data_two receives
		# <generator object..>
		self.assertEqual(data, data_two)

	def test_results_march(self):
		date = datetime.date(2020, 3, 2)
		data = [x for x in self.approaches
				if x.time.date() == date]
		self.assertGreater(len(data), 0)

		filters = create_filters(date=date)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_results_april(self):
		date = datetime.date(2020, 4, 1)
		data = [x for x in self.approaches
				if date <= x.time.date()]
		self.assertGreater(len(data), 0)

		filters = create_filters(start_date=date)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_results_july(self):
		date = datetime.date(2020, 6, 30)
		data = [x for x in self.approaches
				if x.time.date() <= date]
		self.assertGreater(len(data), 0)

		filters = create_filters(end_date=date)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_result_exact_march(self):
		start = datetime.date(2020, 3, 1)
		end = datetime.date(2020, 3, 31)

		data = [x for x in self.approaches
				if start <= x.time.date() <= end]
		self.assertGreater(len(data), 0)

		filters = create_filters(start_date=start, end_date=end)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_wrong_dates(self):
		start = datetime.date(2020, 8, 23)
		end = datetime.date(2020, 2, 17)

		data = []
		filters = create_filters(start_date=start, end_date=end)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_multiple_dates(self):
		date = datetime.date(2020, 3, 2)
		start = datetime.date(2020, 2, 1)
		end = datetime.date(2020, 4, 1)

		data = [x for x in self.approaches
				if x.time.date() == date]
		self.assertGreater(len(data), 0)

		filters = create_filters(date=date, start_date=start, end_date=end)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	# tests regarding distance
	def test_max_distance(self):
		dist = 0.4
		data = [x for x in self.approaches
				if x.distance <= dist]
		self.assertGreater(len(data), 0)

		filters = create_filters(distance_max=dist)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_min_distance(self):
		dist = 0.1
		data = [x for x in self.approaches
				if x.distance >= dist]
		self.assertGreater(len(data), 0)

		filters = create_filters(distance_min=dist)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_two_distances(self):
		min_dist = 0.1
		max_dist = 0.4
		data = [x for x in self.approaches
				if min_dist <= x.distance <= max_dist]
		self.assertGreater(len(data), 0)

		filters = create_filters(distance_min=min_dist, distance_max=max_dist)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_erroneous_distance(self):
		min_dist = 0.4
		max_dist = 0.1
		data = []

		filters = create_filters(distance_min=min_dist, distance_max=max_dist)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	# tests regarding velocity
	def test_max_velocity(self):
		max_vel = 20
		data = [x for x in self.approaches
				if x.velocity <= max_vel]
		self.assertGreater(len(data), 0)

		filters = create_filters(velocity_max=max_vel)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_min_velocity(self):
		min_vel = 10
		data = [x for x in self.approaches
				if x.velocity >= min_vel]
		self.assertGreater(len(data), 0)

		filters = create_filters(velocity_min=min_vel)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_two_velocity(self):
		min_vel = 10
		max_vel = 20
		data = [x for x in self.approaches
				if min_vel <= x.velocity <= max_vel]
		self.assertGreater(len(data), 0)

		filters = create_filters(velocity_min=min_vel, velocity_max=max_vel)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_erroneous_velocity(self):
		min_vel = 20
		max_vel = 10
		data = []

		filters = create_filters(velocity_max=max_vel, velocity_min=min_vel)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	# tests regarding diameter
	def test_max_diameter(self):
		max_diam = 1.5
		data = [x for x in self.approaches
				if x.neo.diameter <= max_diam]
		self.assertGreater(len(data), 0)

		filters = create_filters(diameter_max=max_diam)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_min_diameter(self):
		min_diam = 0.5
		data = [x for x in self.approaches
				if x.neo.diameter >= min_diam]
		self.assertGreater(len(data), 0)

		filters = create_filters(diameter_min=min_diam)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_min_max_diam(self):
		min_diam = 0.5
		max_diam = 1.5
		data = [x for x in self.approaches
				if min_diam <= x.neo.diameter <= max_diam]
		self.assertGreater(len(data), 0)

		filters = create_filters(diameter_max=max_diam, diameter_min=min_diam)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_erroneous_diameter(self):
		min_diam = 1.5
		max_diam = 0.5

		data = []
		filters = create_filters(diameter_min=min_diam, diameter_max=max_diam)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	# tests regarding hazardous
	def test_hazardous(self):
		data = [x for x in self.approaches
				if x.neo.hazardous]
		self.assertGreater(len(data), 0)

		filters = create_filters(hazardous=True)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_not_hazardous(self):
		data = [x for x in self.approaches
				if not x.neo.hazardous]
		self.assertGreater(len(data), 0)

		filters = create_filters(hazardous=False)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	# combination of filters
	def test_march_max_distance(self):
		date = datetime.date(2020, 3, 2)
		distance = 0.4
		data = [x for x in self.approaches
				if x.time.date() == date
				and x.distance <= distance]
		self.assertGreater(len(data), 0)

		filters = create_filters(distance_max=distance, date=date)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_march_min_distance(self):
		date = datetime.date(2020, 3, 2)
		distance = 0.1
		data = [x for x in self.approaches
				if x.time.date() == date
				and x.distance >= distance]
		self.assertGreater(len(data), 0)

		filters = create_filters(distance_min=distance, date=date)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_two_date_distances(self):
		min_date = datetime.date(2020, 3, 1)
		max_date = datetime.date(2020, 3, 31)
		min_dist = 0.1
		max_dist = 0.4
		data = [x for x in self.approaches
				if min_date <= x.time.date() <= max_date
				and min_dist <= x.distance <= max_dist]

		self.assertGreater(len(data), 0)

		filters = create_filters(
								start_date=min_date, end_date=max_date,
								distance_min=min_dist, distance_max=max_dist)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_dates_distances_max_vel(self):
		start_date = datetime.date(2020, 3, 1)
		end_date = datetime.date(2020, 3, 31)
		min_dist = 0.1
		max_dist = 0.4
		max_velocity = 20
		data = [x for x in self.approaches
				if min_dist <= x.distance <= max_dist
				and start_date <= x.time.date() <= end_date
				and x.velocity <= max_velocity]

		self.assertGreater(len(data), 0)

		filters = create_filters(
								start_date=start_date, end_date=end_date,
								distance_min=min_dist, distance_max=max_dist,
								velocity_max=max_velocity)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_dates_distances_velocities(self):
		start_date = datetime.date(2020, 3, 1)
		end_date = datetime.date(2020, 3, 31)
		min_dist = 0.1
		max_dist = 0.4
		max_velocity = 20
		min_velocity = 10
		data = [x for x in self.approaches
				if min_dist <= x.distance <= max_dist
				and start_date <= x.time.date() <= end_date
				and min_velocity <= x.velocity <= max_velocity]
		self.assertGreater(len(data), 0)

		filters = create_filters(
								start_date=start_date, end_date=end_date,
								distance_min=min_dist, distance_max=max_dist,
								velocity_max=max_velocity, velocity_min=min_velocity)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_dates_distances_velocities_max_diameter(self):
		start_date = datetime.date(2020, 3, 1)
		end_date = datetime.date(2020, 5, 31)
		min_dist = 0.05
		max_dist = 0.5
		max_velocity = 25
		min_velocity = 5
		max_diameter = 1.5
		data = [x for x in self.approaches
				if min_dist <= x.distance <= max_dist
				and start_date <= x.time.date() <= end_date
				and min_velocity <= x.velocity <= max_velocity
				and x.neo.diameter <= max_diameter]
		self.assertGreater(len(data), 0)

		filters = create_filters(
								start_date=start_date, end_date=end_date,
								distance_min=min_dist, distance_max=max_dist,
								velocity_max=max_velocity, velocity_min=min_velocity,
								diameter_max=max_diameter)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_dates_distances_velocities_min_diameter(self):
		start_date = datetime.date(2020, 3, 1)
		end_date = datetime.date(2020, 5, 31)
		min_dist = 0.05
		max_dist = 0.5
		max_velocity = 25
		min_velocity = 5
		max_diameter = 1.5
		min_diameter = 0.5
		data = [x for x in self.approaches
				if min_dist <= x.distance <= max_dist
				and start_date <= x.time.date() <= end_date
				and min_velocity <= x.velocity <= max_velocity
				and min_diameter <= x.neo.diameter <= max_diameter]
		self.assertGreater(len(data), 0)

		filters = create_filters(
								start_date=start_date, end_date=end_date,
								distance_min=min_dist, distance_max=max_dist,
								velocity_max=max_velocity, velocity_min=min_velocity,
								diameter_max=max_diameter, diameter_min=min_diameter)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_dates_distances_velocities_min_diameter_hazardous(self):
		start_date = datetime.date(2020, 3, 1)
		end_date = datetime.date(2020, 5, 31)
		min_dist = 0.05
		max_dist = 0.5
		max_velocity = 25
		min_velocity = 5
		max_diameter = 1.5
		min_diameter = 0.5
		data = [x for x in self.approaches
				if min_dist <= x.distance <= max_dist
				and start_date <= x.time.date() <= end_date
				and min_velocity <= x.velocity <= max_velocity
				and min_diameter <= x.neo.diameter <= max_diameter
				and x.neo.hazardous]
		self.assertGreater(len(data), 0)

		filters = create_filters(
								start_date=start_date, end_date=end_date,
								distance_min=min_dist, distance_max=max_dist,
								velocity_max=max_velocity, velocity_min=min_velocity,
								diameter_max=max_diameter, diameter_min=min_diameter,
								hazardous=True)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)

	def test_dates_distances_velocities_min_diameter_not_hazardous(self):
		start_date = datetime.date(2020, 3, 1)
		end_date = datetime.date(2020, 5, 31)
		min_dist = 0.05
		max_dist = 0.5
		max_velocity = 25
		min_velocity = 5
		max_diameter = 1.5
		min_diameter = 0.5
		data = [x for x in self.approaches
				if min_dist <= x.distance <= max_dist
				and start_date <= x.time.date() <= end_date
				and min_velocity <= x.velocity <= max_velocity
				and min_diameter <= x.neo.diameter <= max_diameter
				and not x.neo.hazardous]
		self.assertGreater(len(data), 0)

		filters = create_filters(
								start_date=start_date, end_date=end_date,
								distance_min=min_dist, distance_max=max_dist,
								velocity_max=max_velocity, velocity_min=min_velocity,
								diameter_max=max_diameter, diameter_min=min_diameter,
								hazardous=False)
		data_two = list(self.db.query(filters))
		self.assertEqual(data, data_two)


if __name__ == '__main__':
	unittest.main()
