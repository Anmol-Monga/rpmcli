#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe  # @UnusedImport
import sys
from platform import architecture

if 'py2exe' not in sys.argv:
  sys.argv.append('py2exe')

options = {"py2exe": {
    "compressed":    1,
    "optimize":      2,
    "bundle_files":  2,
    "dist_dir": "../standalones_%s" % architecture()[0],
    "excludes": ['Tkinter', 'tcl'],
    "dll_excludes": ['w9xpopen.exe']
  }
}

if __name__ == '__main__':
  setup(
    console = ['queuesuspend.py', 'resetsequence.py', 'jobadd.py'],
    zipfile = 'library.bin',
    options = options)
