from dot_mngr.tests import NO_ANSI

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
		## BASE
		self.SEP	= f" "
		self.P_INFO = f"[{self.BLU}*{self.RST}]"
		self.P_WARN = f"[{self.ORA}!{self.RST}]"
		self.P_PASS = f"[{self.GRE}+{self.RST}]"
		self.P_FAIL = f"[{self.RED}-{self.RST}]"
		self.P_TITL = f"[{self.YEL}{self.BOL}#{self.RST}{self.RBOL}]"
		self.P_DRY_RUN = f"[{self.CYA}{self.UND}dry-run{self.RST}{self.RUND}]"
		self.P_CMD_OUT = f"[{self.GRE}{self.BOL}>{self.RST}{self.RBOL}]"
		self.P_CMD_ERR = f"[{self.RED}{self.BOL}>{self.RST}{self.RBOL}]"

		## TEST
		self.SEP1 = f"{self.BOL}{self.CYA}{'=' * 80}{self.RST}{self.RBOL}"
		self.SEP2 = f"{self.BOL}{self.YEL}{'-' * 80}{self.RST}{self.RBOL}"

		self.WAIT = f" {self.CYA}...{self.RST} "

		self.FAIL_L = f"{self.BOL}{self.RED}Fail{self.RST}{self.RBOL}"
		self.FAIL_S = f"{self.BOL}{self.RED}F{self.RST}{self.RBOL}"

		self.ERRO_L = f"{self.ORA}Error{self.RST}"
		self.ERRO_S = f"{self.ORA}E{self.RST}"

		self.PASS_L=f"{self.GRE}ok{self.RST}"
		self.PASS_S=f"{self.GRE}.{self.RST}"

		self.SKIP_L = f"{self.PUR}Skipped{self.RST} "
		self.SKIP_S = f"{self.PUR}s{self.RST}"

		self.EXPE_FAIL_L = f"{self.BLU}Expected Failure{self.RST}"
		self.EXPE_FAIL_S = f"{self.BLU}f{self.RST}"

		self.UNEX_PASS_L = f"{self.CYA}Unexpected Success{self.RST}"
		self.UNEX_PASS_S = f"{self.CYA}u{self.RST}"

		self.RES_FAIL = f"{self.BOL}{self.RED}FAILED{self.RST}{self.RBOL}"
		self.RES_PASS = f"{self.BOL}{self.GRE}OK{self.RST}{self.RBOL}"
		self.RES_NO_TEST = f"{self.BOL}{self.YEL}NO TESTS RAN{self.RST}{self.RBOL}"

		# FORMAT
		self.FMTB_NB_TEST = f"{self.BOL}{self.GRE}"
		self.FMTE_NB_TEST = f"{self.RST}{self.RBOL}"

		self.FMTB_TIME_TAKEN = f"{self.BOL}{self.ORA}"
		self.FMTE_TIME_TAKEN = f"{self.RST}{self.RBOL}"

		self.FMTB_METHOD = f"{self.YEL}"
		self.FMTE_METHOD = f"{self.RST}"

	def	remove_ansi(
			self
		) -> None:
		for key in self.__dict__.keys():
			self.__dict__[key] = ""

ansi = Ansi()
