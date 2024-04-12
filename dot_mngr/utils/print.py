import sys

from dot_mngr import a

PADDING = "   "

class	Print():

	def	__init__(
			self
		) -> None:
		self.set_lvl(0)

	def set_lvl(
			self,
			lvl : int
		):
		self.padding = lvl * PADDING

	def	print(
			self,
			string : str,
			hdr : str = "",
			end : str = "\n",
		) -> None:
		to_print = self.padding + hdr

		if len(hdr) > 0:
			to_print += a.SEP

		print(to_print + string, end=end)

	def	info(
			self,
			string : str
		):
		self.print(string, a.P_INFO)

	def	warn(
			self,
			string : str
		):
		self.print(string, a.P_WARN)

	def	success(
			self,
			string : str
		):
		self.print(string, a.P_PASS)

	def	fail(
			self,
			string : str
		):
		self.print(string, a.P_FAIL)
		sys.exit(1)

	def raw(
			self,
			string : str
		):
		self.print(string, end="")

_print = Print()
