'''
Created on Jul 13, 2010

@author: Daniel
'''

from distutils.core import setup
from platform import architecture
import sys

import py2exe  # @UnusedImport


sys.argv.append('py2exe')

opts = {
  "py2exe": {
    "compressed": 1,
    "optimize": 2,
    "bundle_files": 2,
    "dist_dir": r"..\dist_%s" % architecture()[0],
    "packages": ["dbhash", "decimal"],
    "excludes": ['Tkinter', 'tcl'],
    "dll_excludes": ['w9xpopen.exe',
                     'mswsock.dll',
                     'powrprof.dll',
                     'MPR.dll',
                     'MSVCP90.dll']
  }
}


class Target:
  def __init__(self, **kw):
    self.__dict__.update(kw)
    self.version = '0.0.1.0'
    self.company_name = '<Insert Company Name>'
    self.copyright = '<Copyright Notice>'
    self.name = '<service name>'
    self.description = '<Service Description>'

instance = Target(service = ['ServiceTemplate'],
                  modules = ['ServiceTemplate'],
                  create_exe = True,
                  create_dll = True)

setup(options = opts,
      zipfile = "library.bin",
      service = [instance])

