# -*- coding: ascii -*-


"""Pragmatic.Pragmatic: provides entry point main()."""


__version__ = "0.0.15"

from . import Stuff
from .Registry import Registry
from .ArgParser import ParseArgs, Test
from .GetRelease import Get
import os
import pathlib


def Update():
	Get('LLVM', 'llvm-0.1')
	Get('PragmaticPlugin', '0.1')


def Main():
	print(f"Running pragmatic version {__version__}.")

	dir = os.path.dirname(os.path.realpath(__file__))
	dataDir = os.path.join(dir, 'data')
	if (not pathlib.Path(dataDir).exists()):
		Update()

	ParseArgs()