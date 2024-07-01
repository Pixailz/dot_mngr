import os
import re
import sys
import copy
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
import configparser

from concurrent.futures import ThreadPoolExecutor, wait
from importlib import metadata as md
from timeit import default_timer as timer

from pprint import pprint

BEGIN_TS = timer()
ELAPSED_LVL = 0

def p_elapsed(msg=""):
	global ELAPSED_LVL
	ELAPSED_LVL += 1

	elapsed_lvl = f"\x1b[2m{ELAPSED_LVL:02d}\x1b[22m"
	elapsed_time = f"\x1b[4m{timer() - BEGIN_TS:.3f}\x1b[24m"
	print(f"[{elapsed_lvl}][{elapsed_time}] {msg}")

# PARSED ARGS
## GLOBAL
DRY_RUN			= False
PREFIX			= "/usr"
NB_PROC			= os.cpu_count()

# UPDATE
WRITE_HTML		= False

# INSTALL
DO_CHECK		= True
DO_CHROOT		= False # TODO Implement chroot

HOST_TRIPLET	= subprocess.run(
	"gcc -dumpmachine",
	shell=True,
	capture_output=True
).stdout.decode("utf-8").strip("\n")

METADATA		= dict(md.metadata("dot_mngr"))

CWD				= os.getcwd()
# DIR_BASE		= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DIR_BASE		= os.path.dirname(os.path.realpath(__file__))
HOME			= os.environ.get("HOME", None)

DIR_CONFIG		= os.environ.get("XDG_CONFIG_HOME", None)
if DIR_CONFIG is None:
	DIR_CONFIG = os.path.realpath(os.path.join(HOME, ".config/"))

DIR_CONFIG		= os.path.join(DIR_CONFIG, "dot_mngr")

DIR_REPO		= os.path.join(DIR_CONFIG, "repo")
DIR_CACHE		= os.path.join(DIR_BASE, "cache")
DIR_LOG			= os.path.join(DIR_BASE, "log")

FILE_META		= "meta.json"
FILE_COMMAND	= "command.py"

TERM_COLS, TERM_ROWS = os.get_terminal_size()

PROMPT_RIGHT_SIZE = 60
PROMPT_PROGRESS_BAR_SIZE = PROMPT_RIGHT_SIZE - 10

# LOADING ENV
ENV_FILE = os.path.join(DIR_CONFIG, ".env")

def	shrink_path(path: str):
	if path.startswith(CWD):
		return path.replace(CWD, ".")
	if path.startswith(HOME):
		return path.replace(HOME, "~")
	return path

try:
	with open(ENV_FILE, 'r') as f:
		config_string = '[s]\n' + f.read()
except FileNotFoundError as e:
	print(f"{shrink_path(ENV_FILE)} not found, and relaunch dot_mngr")
	sys.exit(130)

env = configparser.ConfigParser()
env.read_string(config_string)

ENV = env["s"]

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

# PACKAGES = [
# 	"a", "b", "c", "d", "e", "f", "g"
# ]

# EXCEPTION

from	.exception				import RepoError

# UTILS
from 	.utils.regex			import regex				as r
from	.utils.ansi				import ansi					as a

# CLI PARSING
from 	.parsing				import Parsing

from 	.utils.progress_bar		import ProgressBar
from 	.utils					import url_handler
from 	.utils					import unicode				as u

from	.utils._print			import _print				as p

from 	.utils._os				import Os

from 	.utils._json			import Json


# SCRAP
from 	.scrap					import scrap

# COMMAND
from 	.command				import default_configure
from 	.command				import default_compile
from 	.command				import default_check
from 	.command				import default_install
from 	.command				import default_uninstall
from 	.command				import default_suite
from 	.command				import a_cmd

# PACKAGE
from	.package				import Package

# REPOSITORY
from	.repository				import Repository

# CONFIG
from 	.config					import conf
