from dot_mngr import r

class Ansi():
	def	__init__(self) -> None:

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

		self.RSTBOL	= f"{self.CSI}0;22m"
		self.RSTITA	= f"{self.CSI}0;23m"
		self.RSTUND	= f"{self.CSI}0;24m"
		self.RSTBLI	= f"{self.CSI}0;25m"

		# COMPOSITE

		## PRINT FUNCTION HEADER
		self.SEP	= f" "
		self.P_INFO = f"[{self.BOL}{self.BLU}*{self.RSTBOL}]"
		self.P_WARN = f"[{self.BOL}{self.ORA}!{self.RSTBOL}]"
		self.P_PASS = f"[{self.BOL}{self.GRE}+{self.RSTBOL}]"
		self.P_FAIL = f"[{self.BOL}{self.RED}-{self.RSTBOL}]"
		self.P_TITL = f"[{self.YEL}{self.BOL}#{self.RSTBOL}]"
		self.P_DRY_RUN = f"[{self.CYA}{self.UND}~{self.RSTUND}]"
		self.P_CMD_OUT = f"[{self.GRE}{self.BOL}>{self.RSTBOL}]"
		self.P_CMD_ERR = f"[{self.RED}{self.BOL}>{self.RSTBOL}]"
		self.P_REF = f"[{self.RED}@{self.RSTITA}]"
		## HELP META
		self.HM_PATH = f"{self.RED}PATH{self.RST}"
		self.HM_INT = f"{self.RED}INT{self.RST}"

	def	remove_ansi(self) -> None:
		for key in self.__dict__.keys():
			if key in ["ESC", "CSI"]:
				self.__dict__[key] = ""
			else:
				self.__dict__[key] = r.ransi.sub("", self.__dict__[key])

ansi = Ansi()
