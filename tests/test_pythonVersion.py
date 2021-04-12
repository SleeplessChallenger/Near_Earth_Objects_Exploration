import unittest
import sys


class VersionTest(unittest.TestCase):
	'''Python version check-up'''
	def test_version(self):
		self.assertTrue(sys.version_info > (3, 5), f"major: {sys.version_info.major}, "
												   f"minor: {sys.version_info.minor}, "
												   f"micro: {sys.version_info.micro}"
													)

# sys.version_info(major=3, minor=7, micro=9, releaselevel='final', serial=0)

if __name__ == '__main__':
	unittest.main()
