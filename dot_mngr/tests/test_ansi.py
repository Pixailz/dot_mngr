import unittest

from dot_mngr.tests.utils import add_to_suite
from dot_mngr.tests.ansi import Ansi as AnsiTest
from dot_mngr.utils.ansi import Ansi

class TestAnsi(unittest.TestCase):
	def setUp(self):
		self.a = Ansi()
		self.t_a = AnsiTest(False)
		self.na = Ansi()
		self.na.remove_ansi()
		self.t_na = AnsiTest(True)

	def wrapper_ansi(self, var, no_ansi=False):
		if no_ansi:
			tested_var = self.na.__dict__[var]
			expected_var = self.t_na.__dict__[var]
		else:
			tested_var = self.a.__dict__[var]
			expected_var = self.t_a.__dict__[var]
		self.assertIsInstance(tested_var, str, "Tested variable should be a string")
		self.assertIsInstance(expected_var, str, "Expected variable should be a string")
		self.assertEqual(tested_var, expected_var, "Is not equal")

	def testAnsiAllKeys(self):
		a_keys = self.a.__dict__.keys()
		na_keys = self.na.__dict__.keys()
		t_a_keys = self.t_a.__dict__.keys()
		t_na_keys = self.t_na.__dict__.keys()

		len_a = len(a_keys)
		len_na = len(na_keys)
		len_t_a = len(t_a_keys)
		len_t_na = len(t_na_keys)

		self.assertEqual(len_a, len_na, "Wrong number of keys")
		self.assertEqual(len_t_a, len_t_na, "Wrong number of keys")

		for key in a_keys:
			self.wrapper_ansi(key)
		for key in na_keys:
			self.wrapper_ansi(key, True)

TEST_UTILS_ANSI = [
	# Base
	"testAnsiAllKeys",
]

def suite(suite):
	return add_to_suite(suite, TestAnsi, TEST_UTILS_ANSI)

if __name__ == "__main__":
	unittest.main()
