import os
import sys

from rssscan.__about__ import __version__

LIB_ROOT = os.path.dirname(os.path.realpath(__file__))
LIB_VENDOR = os.sep.join([LIB_ROOT, 'vendor'])
sys.path.insert(0, LIB_VENDOR)