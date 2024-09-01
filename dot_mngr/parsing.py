from dot_mngr import os
from dot_mngr import argparse

from dot_mngr import a
from dot_mngr import Check
from dot_mngr import METADATA as MD
import dot_mngr as dm

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
			"--nproc",
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
			"--prefix", "-p",
			type=str,
			help="set PREFIX to the given value",
			dest="glob_prefix",
			metavar=a.HM_PATH,
		)

		self.parser.add_argument(
			"--root-path", "-P",
			type=str,
			help="set ROOT_PATH to the given value",
			dest="glob_root_path",
			metavar=a.HM_PATH,
		)

		self.parser.add_argument(
			"--target-triplet", "-T",
			type=str,
			help="set the linux triplet target",
			dest="glob_target_triplet",
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

		update.add_argument(
			"update_package",
			type=str,
			nargs="*",
			default=[],
			help="the package to update",
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
			dest="inst_disable_check",
		)

		install.add_argument(
			"--extract-folder", "-X",
			type=str,
			help="set the folder to extract the package",
			dest="inst_extract_folder",
		)

		install.add_argument(
			"--force-install", "-F",
			type=bool,
			help="force installation of already installed packages",
			dest="inst_force_install",
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

	# UTILS
	def get_default(self, k_env, k_get, default):
		env = os.getenv(k_env, None)
		get = getattr(self.args, k_get, None)
		if get is not None:
			return get
		elif env is not None:
			return env
		else:
			return default

	# POST PARSING
	def post_parse(self):
		self.post_parse_prefix()
		self.post_parse_root_path()
		self.post_parse_dry_run()
		self.post_parse_no_ansi()
		self.post_parse_nproc()
		self.post_parse_triplet()

		self.post_parse_install()

		self.post_parse_update()

	def post_parse_prefix(self):
		prefix = self.get_default("PREFIX", "glob_prefix", dm.PREFIX)
		use_home_dir = self.get_default("USE_HOME", "glob_use_home", None)

		if prefix:
			dm.PREFIX = prefix
		elif use_home_dir:
			env = os.environ
			if env.get("XDG_DATA_HOME", None):
				dm.PREFIX = env["XDG_DATA_HOME"]
			else:
				dm.PREFIX = f"{env['HOME']}/.local"

	def post_parse_root_path(self):
		dm.ROOT_PATH = self.get_default(
			"ROOT_PATH", "glob_root_path", dm.ROOT_PATH
		)

	def post_parse_dry_run(self):
		dm.DRY_RUN = self.get_default("DRY_RUN", "glob_dry_run", dm.DRY_RUN)

	def post_parse_no_ansi(self):
		if self.get_default("NO_ANSI", "glob_no_ansi", False):
			a.remove_ansi()

	def post_parse_nproc(self):
		tmp = self.get_default("NB_PROC", "glob_nproc", -1)

		if tmp > 0 and tmp < dm.NB_PROC:
			dm.NB_PROC = tmp

	def post_parse_triplet(self):
		tmp = self.get_default(
			"TARGET_TRIPLET", "glob_target_triplet", dm.TARGET_TRIPLET
		)

		if tmp is not None:
			dm.TARGET_TRIPLET = tmp

		triplet = dm.TARGET_TRIPLET.split("-")
		dm.ARCH = triplet[0]

	def post_parse_update(self):
		self.post_parse_update_write_html()

	def post_parse_update_write_html(self):
		dm.WRITE_HTML = self.get_default(
			"WRITE_HTML", "upda_write_html", dm.WRITE_HTML
		)

	def post_parse_install(self):
		self.post_parse_install_disable_check()
		self.post_parse_install_extract_folder()
		self.post_parse_install_force_install()

	def post_parse_install_disable_check(self):
		dm.DO_CHECK =self.get_default(
			"DO_CHECK", "inst_disable_check", dm.DO_CHECK
		)
		if Check.IsFalse(dm.DO_CHECK):
			dm.DO_CHECK = False
		else:
			dm.DO_CHECK = True

	def post_parse_install_extract_folder(self):
		tmp = self.get_default(
			"EXTRACT_FOLDER", "inst_extract_folder", dm.DIR_CACHE
		)
		if tmp is not None:
			dm.DIR_CACHE = tmp

	def post_parse_install_force_install(self):
		dm.FORCE_INSTALL = self.get_default(
			"FORCE_INSTALL", "inst_force_install", dm.FORCE_INSTALL
		)
		if Check.IsFalse(dm.FORCE_INSTALL):
			dm.FORCE_INSTALL = False
		else:
			dm.FORCE_INSTALL = True
