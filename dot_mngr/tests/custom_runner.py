from unittest.runner import sys, time, warnings, \
	_WritelnDecorator, registerResult

from dot_mngr.tests.ansi import ansi as a
from dot_mngr.tests.custom_result import CustomTestResult

class CustomTestRunner(object):
    """A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    resultclass = CustomTestResult

    def __init__(self, stream=None, descriptions=True, verbosity=2,
                 failfast=False, buffer=False, resultclass=None, warnings=None,
                 *, tb_locals=False, durations=None):
        """Construct a TextTestRunner.

        Subclasses should accept **kwargs to ensure compatibility as the
        interface changes.
        """
        if stream is None:
            stream = sys.stderr
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        self.tb_locals = tb_locals
        self.durations = durations
        self.warnings = warnings
        if resultclass is not None:
            self.resultclass = resultclass

    def _makeResult(self):
        try:
            return self.resultclass(self.stream, self.descriptions,
                                    self.verbosity, durations=self.durations)
        except TypeError:
            # didn't accept the durations argument
            return self.resultclass(self.stream, self.descriptions,
                                    self.verbosity)

    def _printDurations(self, result):
        if not result.collectedDurations:
            return
        ls = sorted(result.collectedDurations, key=lambda x: x[1],
                    reverse=True)
        if self.durations > 0:
            ls = ls[:self.durations]
        self.stream.writeln("Slowest test durations")
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        hidden = False
        for test, elapsed in ls:
            if self.verbosity < 2 and elapsed < 0.001:
                hidden = True
                continue
            self.stream.writeln("%-10s %s" % ("%.3fs" % elapsed, test))
        if hidden:
            self.stream.writeln("\n(durations < 0.001s were hidden; "
                                "use -v to show these durations)")
        else:
            self.stream.writeln("")

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals
        with warnings.catch_warnings():
            if self.warnings:
                # if self.warnings is set, use it to filter all the warnings
                warnings.simplefilter(self.warnings)
            startTime = time.perf_counter()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()
            try:
                test(result)
            finally:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
            stopTime = time.perf_counter()
        timeTaken = stopTime - startTime
        result.printErrors()
        if self.durations is not None:
            self._printDurations(result)

        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)

        run = result.testsRun
        self.stream.writeln(f"Ran {a.FMTB_NB_TEST}{run}{a.FMTE_NB_TEST}"
							f" test{run != 1 and 's' or ''} in "
							"%s%.3f%ss" %
								(a.FMTB_TIME_TAKEN, timeTaken, a.FMTE_TIME_TAKEN))
        self.stream.writeln()

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
        if not result.wasSuccessful():
            self.stream.write(a.RES_FAIL)
            failed, errored = len(result.failures), len(result.errors)
            if failed:
                infos.append(f"failures={self.RED}{self.BOL}{failed}{self.RSTBOL}")
            if errored:
                infos.append(f"errors={self.ORA}{errored}{self.RST}")
        elif run == 0 and not skipped:
            self.stream.write(a.RES_NO_TEST)
        else:
            self.stream.write(a.RES_PASS)
        if skipped:
            infos.append(f"skipped={self.PUR}{skipped}{self.RST}")
        if expectedFails:
            infos.append(f"expected failures={self.BLU}{expectedFails}{self.RST}")
        if unexpectedSuccesses:
            infos.append(f"unexpected successes={self.CYA}{unexpectedSuccesses}{self.RST}")
        if infos:
            self.stream.writeln(" x(%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")
        self.stream.flush()
        return result
