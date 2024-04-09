import os
import argparse
import enum
import datetime

from importlib import metadata as md

NO_ANSI		= False
LOG_FILE	= None
METADATA	= md.metadata("dot_mngr")

CWD			= os.getcwd()
DIR_BASE	= os.path.dirname(os.path.realpath(__file__))

from	.utils.ansi				import ansi					as a
from	.utils.print			import _print				as p
from 	.utils					import unicode				as u

from 	.cli.main				import CliMain
