import os
import re
import enum
import gzip
import json
import argparse
import datetime
import urllib

from importlib import metadata as md

NO_ANSI		= False
LOG_FILE	= None
METADATA	= md.metadata("dot_mngr")

CWD			= os.getcwd()
DIR_BASE	= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DIR_REPO	= os.path.join(DIR_BASE, "repo")
DIR_CACHE	= os.path.join(DIR_BASE, "cache")

WRITE_HTML = True

TERM_COLS, TERM_ROWS = os.get_terminal_size()

_ENV_FILE_	= os.path.join(DIR_BASE, ".env")
# Load .env file
if os.path.exists(_ENV_FILE_):
	with open(_ENV_FILE_, "r") as f:
		try:
			ENV = json.load(f)
		except json.JSONDecodeError:
			ENV = None
else:
	ENV = None

PACKAGES	= [
	"acl", "attr", "autoconf", "automake",

	"bash", "bc", "binutils", "bison", "bzip2",

	"check", "coreutils", "cracklib", "cracklib-wordlist",

	"dbus", "diffutils",

	"e2fsprogs", "elfutils", "eudev", "expat", "expect",

	"file", "findutils", "flex", "flit-core",

	"gawk", "gcc", "gdbm", "gettext", "glibc", "gmp", "gperf", "grep", "groff",
	"grub", "gzip",

	"iana-etc", "inetutils", "intltool", "iproute2",

	"jinja2",

	"kbd", "kmod",

	"less", "lfs-bootscripts", "libcap", "libffi", "libpipeline", "libtasn1",
	"libtool", "libxcrypt", "linux",

	"m4", "make", "make-ca", "man-db", "man-pages", "markup-safe", "meson",
	"mpc", "mpfr",

	"ncurses", "ninja", "nspr", "nss",

	"openssl",

	"p11-kit", "patch", "perl", "pkgconf", "procps-ng", "psmisc", "python3",
	"python3-doc",

	"readline",

	"sed", "setuptools", "shadow", "sysklogd", "systemd", "systemd-man-pages",
	"sysvinit",

	"tar", "tcl", "tcl-doc", "terminus", "texinfo", "tzdata",

	"udev-lfs", "util-linux",

	"vim",

	"wheel",

	"xml-parser", "xz",

	"zlib", "zstd"
]

# PACKAGES = [
# 	"acl",				# apache
# 	"elfutils",			# apache_dir
# 	"iproute2",			# apache_no_sort
# 	"bc",				# github
# 	"e2fsprogs",		# github_tag
# 	"libxslt",			# gitlab
# 	"expect",			# fossies
# 	"tcl-doc",			# fossies_search
# 	"flit-core",		# pypi
# 	"intltool",			# website
# 	"util-linux",		# no_scrap
# 	"psmisc",			# sourceforge
# ]

# TODO Check why package downloader fail to properly pad, with those package
PACKAGES = [
	"acl",
	"flit-core",
	"e2fsprogs",
	"lfs-bootscripts",
	"libcap",
	"make-ca",
	"markup-safe",
	"ncurses",
	"pkgconf",
	"systemd",
	"sysvinit",
	"vim",
	"wheel",
	"xml-parser",
	"udev-lfs",
]

from	.utils.ansi				import ansi					as a
from	.utils.print			import _print				as p
from 	.utils.regex			import regex				as r
from 	.utils					import url_handler
from 	.utils					import unicode				as u

from 	.cli.main				import CliMain

from 	.scrap					import scrap
from 	.config					import config
