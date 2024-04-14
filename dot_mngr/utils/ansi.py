from dot_mngr import *

class Ansi():
	def	__init__(
			self,
			no_ansi : bool = NO_ANSI
		) -> None:

		# ESCAPE SEQUENCE
		self.ESC = "\x1b"
		self.CSI = f"{self.ESC}["

		# COLOR
		self.BLA = f"{self.CSI}30m"
		self.RED = f"{self.CSI}31m"
		self.GRE = f"{self.CSI}32m"
		self.YEL = f"{self.CSI}33m"
		self.BLU = f"{self.CSI}34m"
		self.PUR = f"{self.CSI}35m"
		self.CYA = f"{self.CSI}36m"
		self.ORA = f"{self.CSI}38;5;208m"

		# MODIFIER
		self.BOL	= f"{self.CSI}1m"
		self.ITA	= f"{self.CSI}3m"
		self.UND	= f"{self.CSI}4m"
		self.BLI	= f"{self.CSI}5m"

		self.RST	= f"{self.CSI}0m"
		self.RBOL	= f"{self.CSI}22m"
		self.RITA	= f"{self.CSI}23m"
		self.RUND	= f"{self.CSI}24m"
		self.RBLI	= f"{self.CSI}25m"

		if no_ansi:
			self.remove_ansi()

		# COMPOSITE
		self.SEP	= f" "
		self.P_INFO = f"[{self.BLU}*{self.RST}]"
		self.P_WARN = f"[{self.ORA}!{self.RST}]"
		self.P_PASS = f"[{self.GRE}+{self.RST}]"
		self.P_FAIL = f"[{self.RED}-{self.RST}]"

	def	remove_ansi(
			self
		) -> None:
		for key in self.__dict__.keys():
			self.__dict__[key] = ""

ansi = Ansi()
