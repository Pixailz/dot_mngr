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
import subprocess
import configparser

from concurrent.futures import ThreadPoolExecutor, wait
from importlib import metadata as md
from timeit import default_timer as timer

from pprint import pprint

BEGIN_TS = timer()
ELAPSED_LVL = 0

# PARSED ARGS
DEBUG			= True
## GLOBAL
DRY_RUN			= False
PREFIX			= "/usr"
ROOT_PATH		= ""
NB_PROC			= os.cpu_count()
XORG_PREFIX		= ""
XORG_CONFIG		= ""

## UPDATE
WRITE_HTML		= False

## INSTALL
DO_CHECK		= True
DO_CHROOT		= False
FORCE_INSTALL	= False

TARGET_TRIPLET	= subprocess.run(
	"/bin/gcc -dumpmachine",
	shell=True,
	capture_output=True
).stdout.decode("utf-8").strip("\n")

METADATA		= dict(md.metadata("dot_mngr"))
REPO_SEP		= "@"

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

TERM_COLS, TERM_ROWS		= shutil.get_terminal_size(fallback=(120, 50))

PROMPT_RIGHT_SIZE			= 60
PROMPT_PROGRESS_BAR_SIZE	= PROMPT_RIGHT_SIZE - 10

# LOADING ENV
ENV_FILE = os.path.join(DIR_CONFIG, ".env")

ENV = dict()

PATH = os.getenv("PATH")
if PATH is None:
	PATH = ["/bin", "/sbin"]
else:
	PATH = PATH.split(":")

try:
	with open(ENV_FILE, 'r') as f:
		config_string = '[s]\n' + f.read()
	env = configparser.ConfigParser()
	env.read_string(config_string)

	ENV = env["s"]
except FileNotFoundError as e:
	pass

# CTYPE
from	.utils.ctype				import CTYPE
# Check
from	._check.main				import Check

# KERNEL
from 	.utils.kernel				import Kernel

# EXCEPTION
from	.utils.exception			import RepoError

# UTILS
from 	._os						import Os

from 	._json						import Json

from 	.utils.regex				import regex				as r
from	.utils.ansi					import ansi					as a
from	.utils.git					import Git

from	._print						import _print				as p

from 	.utils.progress_bar			import ProgressBar
from	.utils						import url_handler
from	.utils						import unicode as u

# CLI PARSING
from 	.utils.parsing				import Parsing

# SCRAP
from 	.utils.scrap				import scrap

# COMMAND
from	.utils.command_kernel		import default_kernel_configure_kernel
from	.utils.command_kernel		import default_kernel_configure
from	.utils.command_kernel		import default_kernel_compile
from	.utils.command_kernel		import default_kernel_install
from 	.utils.command				import default_configure
from 	.utils.command				import default_compile
from 	.utils.command				import default_check
from 	.utils.command				import default_install
from 	.utils.command				import default_uninstall
from 	.utils.command				import default_suite
from 	.utils.command				import a_cmd

# PACKAGE
from	.package.utils				import get_real_name
from	.package.main				import Package

# REPOSITORY
from	.utils.repository			import Repository

# CONFIG
from 	.config.main				import conf
from	.config.utils				import extract_file_from_package
from	.config.utils				import get_version_from_package
from	.config.utils				import download_package
