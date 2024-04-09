import unittest

from dot_mngr.tests.custom_runner import CustomTestRunner
from dot_mngr.tests.test_ansi import suite as suite_ansi

from pprint import pprint

def	TestUtils():
	suite = unittest.TestSuite()
	suite_ansi(suite)
	runner = CustomTestRunner(
		descriptions="Testing all the utils from dot_mngr",
	)
	runner.run(suite)

if __name__ == "__main__":
	TestUtils()
