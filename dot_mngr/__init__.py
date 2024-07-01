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

DIR_RSC			= os.path.join(DIR_BASE, "rsc")
DIR_REPO		= os.path.join(DIR_CONFIG, "repo")
DIR_CACHE		= os.path.join(DIR_CONFIG, "cache")
DIR_LOG			= os.path.join(DIR_CONFIG, "log")

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

ENV = dict()


try:
	with open(ENV_FILE, 'r') as f:
		config_string = '[s]\n' + f.read()
	env = configparser.ConfigParser()
	env.read_string(config_string)

	ENV = env["s"]
except FileNotFoundError as e:
	pass

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

# EXCEPTION

from	.exception				import RepoError

# UTILS
from 	.utils.regex			import regex				as r
from	.utils.ansi				import ansi					as a
from	.utils.git				import Git

from 	.utils.progress_bar		import ProgressBar
from 	.utils					import url_handler
from 	.utils					import unicode				as u

from	.utils._print			import _print				as p

from 	.utils._os				import Os

from 	.utils._json			import Json

# CLI PARSING
from 	.parsing				import Parsing

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
