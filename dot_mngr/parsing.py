from dot_mngr import argparse

from dot_mngr import a

from dot_mngr import METADATA as MD

class Parsing():
	def __init__(self):
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
			version=f"%(prog)s, {ver}"
		)

		self.parser.add_argument(
			"--no-thread",
			action="store_true",
			help="do not use threading",
			default=False
		)

		self.subparsers = self.parser.add_subparsers(
			title="Commands",
			dest="command",
			required=False,
		)

		self.add_command_update()
		self.add_command_install()
		self.add_command_info()

		self.args = self.parser.parse_args()

	def add_command_update(self):
		update = self.subparsers.add_parser(
			"update",
			help="update packages list"
		)

	def add_command_install(self):
		install = self.subparsers.add_parser(
			"install",
			help="install a package"
		)
		install.add_argument(
			"package",
			type=str,
			nargs="+",
			help="the package to install"
		)

	def add_command_info(self):
		info = self.subparsers.add_parser(
			"info",
			help="show information about a package"
		)
		info.add_argument(
			"package",
			type=str,
			nargs="*",
			help="the package to get information about"
		)

