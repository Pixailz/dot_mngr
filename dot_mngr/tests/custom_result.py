import unittest

from dot_mngr.tests.ansi import ansi as a

class CustomTestResult(unittest.TestResult):
	"""A test result class that can print formatted text results to a stream.
	With color
	"""

	separator1 = a.SEP1
	separator2 = a.SEP2

	def __init__(self, stream, descriptions, verbosity, *, durations=None):
		"""Construct a TextTestResult. Subclasses should accept **kwargs
		to ensure compatibility as the interface changes."""
		super(CustomTestResult, self).__init__(stream, descriptions, verbosity)
		self.stream = stream
		self.showAll = verbosity > 1
		self.dots = verbosity == 1
		self.descriptions = descriptions
		self._newline = True
		self.durations = durations

	def getDescription(self, test):
		doc_first_line = test.shortDescription()
		if self.descriptions and doc_first_line:
			return '\n'.join((str(test), doc_first_line))
		else:
			method_name = str(test).split(" ")[0]
			method_full = str(test).split(" ")[1].strip("()")
			return f"{a.FMTB_METHOD}{method_name}{a.FMTE_METHOD}{a.SEP}" \
				f"{a.UND}{method_full}{a.RUND}"
			# return str(test)

	def startTest(self, test):
		super(CustomTestResult, self).startTest(test)
		if self.showAll:
			self.stream.write(self.getDescription(test))
			self.stream.write(a.WAIT)
			self.stream.flush()
			self._newline = False

	def _write_status(self, test, status):
		is_subtest = isinstance(test, unittest.case._SubTest)
		if is_subtest or self._newline:
			if not self._newline:
				self.stream.writeln()
			if is_subtest:
				self.stream.write("  ")
			self.stream.write(self.getDescription(test))
			self.stream.write(a.WAIT)
		self.stream.writeln(status)
		self.stream.flush()
		self._newline = True

	def addSubTest(self, test, subtest, err):
		if err is not None:
			if self.showAll:
				if issubclass(err[0], subtest.failureException):
					self._write_status(subtest, a.FAIL_L)
				else:
					self._write_status(subtest, a.ERRO_L)
			elif self.dots:
				if issubclass(err[0], subtest.failureException):
					self.stream.write(a.FAIL_S)
				else:
					self.stream.write(a.ERRO_S)
				self.stream.flush()
		super(CustomTestResult, self).addSubTest(test, subtest, err)

	def addSuccess(self, test):
		super(CustomTestResult, self).addSuccess(test)
		if self.showAll:
			self._write_status(test, a.PASS_L)
		elif self.dots:
			self.stream.write(a.PASS_S)
			self.stream.flush()

	def addError(self, test, err):
		super(CustomTestResult, self).addError(test, err)
		if self.showAll:
			self._write_status(test, a.ERRO_L)
		elif self.dots:
			self.stream.write(a.ERRO_S)
			self.stream.flush()

	def addFailure(self, test, err):
		super(CustomTestResult, self).addFailure(test, err)
		if self.showAll:
			self._write_status(test, a.FAIL_L)
		elif self.dots:
			self.stream.write(a.FAIL_S)
			self.stream.flush()

	def addSkip(self, test, reason):
		super(CustomTestResult, self).addSkip(test, reason)
		if self.showAll:
			self._write_status(test, "{} {0!r}".format(a.SKIP_L, reason))
		elif self.dots:
			self.stream.write(a.SKIP_S)
			self.stream.flush()

	def addExpectedFailure(self, test, err):
		super(CustomTestResult, self).addSkip(test)
		if self.showAll:
			self.stream.writeln(a.EXPE_FAIL_L)
			self.stream.flush()
		elif self.dots:
			self.stream.write(a.EXPE_FAIL_S)
			self.stream.flush()

	def addUnexpectedSuccess(self, test):
		super(CustomTestResult, self).addUnexpectedSuccess(test)
		if self.showAll:
			self.stream.writeln(a.UNEX_PASS_L)
			self.stream.flush()
		elif self.dots:
			self.stream.write(a.UNEX_PASS_S)
			self.stream.flush()

	def printErrors(self):
		if self.dots or self.showAll:
			self.stream.writeln()
			self.stream.flush()
		self.printErrorList(a.ERRO_L, self.errors)
		self.printErrorList(a.FAIL_L, self.failures)
		unexpectedSuccesses = getattr(self, 'unexpectedSuccesses', ())
		if unexpectedSuccesses:
			self.stream.writeln(self.separator1)
			for test in unexpectedSuccesses:
				self.stream.writeln(f"UNEXPECTED SUCCESS: " \
					"{self.getDescription(test)}")
			self.stream.flush()

	def printErrorList(self, flavour, errors):
		for test, err in errors:
			self.stream.writeln(self.separator1)
			self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
			self.stream.writeln(self.separator2)
			self.stream.writeln("%s" % err)
			self.stream.flush()
