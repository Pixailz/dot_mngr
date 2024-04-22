import os
import re
import sys
import enum
import gzip
import json
import tarfile as tar
import urllib
import shutil
import argparse
import datetime
import importlib
import selectors
import subprocess

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from importlib import metadata as md

from pprint import pprint

NO_ANSI			= False
LOG_FILE		= None
WRITE_HTML		= False
DO_CHECK		= False
USE_LOCAL_HOME	= True
DO_CHROOT		= False # TODO Implement chroot
DRY_RUN			= False

HOST_TRIPLET	= subprocess.run(
	"gcc -dumpmachine",
	shell=True,
	capture_output=True
).stdout.decode("utf-8").strip("\n")

if USE_LOCAL_HOME:
	CNF_PREFIX	= os.path.expanduser("~/.local")
else:
	CNF_PREFIX	= "/usr"

METADATA		= md.metadata("dot_mngr")

CWD				= os.getcwd()
DIR_BASE		= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DIR_REPO		= os.path.join(DIR_BASE, "repo")
DIR_CACHE		= os.path.join(DIR_BASE, "cache")
DIR_LOG			= os.path.join(DIR_BASE, "log")

FILE_META		= "meta.json"
FILE_COMMAND	= "command.py"

TERM_COLS, TERM_ROWS = os.get_terminal_size()

PROMPT_RIGHT_SIZE = 60
PROMPT_PROGRESS_BAR_SIZE = PROMPT_RIGHT_SIZE - 10

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
# PACKAGES = [
# 	"acl",
# 	"flit-core",
# 	"e2fsprogs",
# 	"lfs-bootscripts",
# 	"libcap",
# 	"make-ca",
# 	"markup-safe",
# 	"ncurses",
# 	"pkgconf",
# 	"systemd",
# 	"sysvinit",
# 	"vim",
# 	"wheel",
# 	"xml-parser",
# 	"udev-lfs",
# ]

# PACKAGES = [
# 	# "bash",
# 	# "less",
# 	# "linux",
# 	"bc"
# 	# "acl"
# ]

from	.utils.ansi				import ansi					as a
from 	.utils.regex			import regex				as r
from 	.utils.progress_bar		import ProgressBar
from 	.utils					import url_handler
from 	.utils					import unicode				as u

from	.utils._print			import _print				as p

from 	.utils._os				import mkdir
from 	.utils._os				import take
from 	.utils._json			import json_load

from 	.cli.main				import CliMain

from 	.scrap					import scrap
from	.package				import Package
from 	.config					import conf

conf.load_packages()
