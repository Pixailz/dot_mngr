from dot_mngr import *

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

		print(to_print + str(string), end=end)

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
			string : str,
			exiting : bool = True
		):
		self.print(string, a.P_FAIL)
		if exiting:
			sys.exit(1)

	def	title(
			self,
			string : str
		):
		self.print(string, a.P_TITL)

	def	dr(
			self,
			string : str
		):
		self.print(string, a.P_DRY_RUN)

	def raw(
			self,
			string : str
		):
		self.print(string, end="")

	def cmdo(
			self,
			string : str
		):
		self.print(string, a.P_CMD_OUT)

	def cmde(
			self,
			string : str
		):
		self.print(string, a.P_CMD_ERR)

	@staticmethod
	def col(cols):
		string = str()
		for c in cols:
			tmp = c[0] or ""
			string += tmp.ljust(c[1] - 1) + " "
		return string


_print = Print()
