from dot_mngr import os
from dot_mngr import argparse

from dot_mngr import a
from dot_mngr import METADATA as MD
import dot_mngr as dm

# PARSED ARGS
## GLOBAL
DRY_RUN			= False
PREFIX			= "/usr"

## UPDATE
WRITE_HTML		= False

class Parsing():
	def __init__(self):
		# BASE
		ver = f"Developed by {a.BOL}{MD['Author']}{a.RBOL} ({MD['Version']})"

		self.parser = argparse.ArgumentParser(
			prog=f"{a.BOL}{MD['Name']}{a.RBOL}",
			description=MD['Summary'],
			epilog=
				f"{ver}\n"
				f"{a.UND}{MD['Home-page']}{a.RUND}\n",
			formatter_class=argparse.RawDescriptionHelpFormatter
		)

		self.parser.add_argument(
			"--version", "-V",
			action="version",
			version=f"%(prog)s, {ver}",
		)

		# THREADING
		self.parser.add_argument(
			"--no-thread",
			action="store_true",
			help="do not use threading",
			default=False,
			dest="glob_no_thread",
		)

		self.parser.add_argument(
			"--nrpoc",
			type=int,
			help="set the number of processes to use",
			default=dm.NB_PROC,
			dest="glob_nproc",
			metavar=a.HM_INT,
		)

		# COMPILATION / INSTALLATION CONFIG
		self.parser.add_argument(
			"--use-home", "-H",
			action="store_true",
			help="set PREFIX to $XDG_DATA_HOME if set, else $HOME/.local",
			default=False,
			dest="glob_use_home",
		)

		self.parser.add_argument(
			"--use-prefix", "-p",
			type=str,
			help="set PREFIX to the given value",
			dest="glob_use_prefix",
			metavar=a.HM_PATH,
		)

		# LOGING / STYLE
		self.parser.add_argument(
			"--no-ansi", "-A",
			action="store_true",
			help="disable ANSI escape codes",
			default=False,
			dest="glob_no_ansi",
		)

		# DEBUG
		self.parser.add_argument(
			"--dry-run", "-D",
			action="store_true",
			help="do not install anything, just show what would be done",
			default=False,
			dest="glob_dry_run",
		)

		# SUBCOMMANDS
		self.subparsers = self.parser.add_subparsers(
			title="Commands",
			dest="command",
			required=False,
		)

		self.add_command_update()
		self.add_command_install()
		self.add_command_info()

		# PARSING
		self.args = self.parser.parse_args()

		# POST PARSING
		self.post_parse()

	def add_command_update(self):
		update = self.subparsers.add_parser(
			"update",
			help="update packages list",
		)

		update.add_argument(
			"--write-html",
			action="store_true",
			help="write the scraped HTML file",
			default=False,
			dest="upda_write_html",
		)

	def add_command_install(self):
		install = self.subparsers.add_parser(
			"install",
			help="install a package",
		)

		install.add_argument(
			"--disable-check",
			action="store_false",
			help="disable the check step for installation",
			default=True,
			dest="inst_disable_check",
		)

		install.add_argument(
			"inst_package",
			type=str,
			nargs="+",
			help="the package to install",
		)

	def add_command_info(self):
		info = self.subparsers.add_parser(
			"info",
			help="show information about a package"
		)
		info.add_argument(
			"info_package",
			type=str,
			nargs="*",
			help="the package to get information about",
		)

	def post_parse(self):
		self.post_parse_prefix()
		self.post_parse_dry_run()
		self.post_parse_no_ansi()
		self.post_parse_nproc()

		self.post_parse_install()

		self.post_parse_update()

	def post_parse_prefix(self):
		use_prefix = getattr(self.args, "glob_use_prefix", None)
		use_home_dir = getattr(self.args, "glob_use_home", None)

		if use_prefix:
			dm.PREFIX = use_prefix
		elif use_home_dir:
			env = os.environ
			if env.get("XDG_DATA_HOME", None):
				dm.PREFIX = env["XDG_DATA_HOME"]
			else:
				dm.PREFIX = f"{env['HOME']}/.local"

	def post_parse_dry_run(self):
		dm.DRY_RUN = getattr(self.args, "glob_dry_run", dm.DRY_RUN)

	def post_parse_no_ansi(self):
		if getattr(self.args, "glob_no_ansi", False):
			a.remove_ansi()

	def post_parse_nproc(self):
		tmp  = getattr(self.args, "glob_nproc", -1)

		if tmp > 0 and tmp < dm.NB_PROC:
			dm.NB_PROC = tmp

	def post_parse_update(self):
		self.post_parse_update_write_html()

	def post_parse_update_write_html(self):
		dm.WRITE_HTML = getattr(self.args, "upda_write_html", dm.WRITE_HTML)

	def post_parse_install(self):
		self.post_parse_install_disable_check()

	def post_parse_install_disable_check(self):
		dm.DO_CHECK = getattr(self.args, "inst_disable_check", dm.DO_CHECK)
