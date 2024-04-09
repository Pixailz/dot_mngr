import unittest

def	add_to_suite(suite, to_class, to_add):
	for test in to_add:
		suite.addTest(to_class(test))
	return suite
