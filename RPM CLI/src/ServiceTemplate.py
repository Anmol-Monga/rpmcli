'''
Created on Mar 3, 2011

@author: daniel
'''
import win32serviceutil
import win32event
import sys

class Launcher(win32serviceutil.ServiceFramework):
  _svc_name_ = "<insert service name>"

  _svc_display_name_ = "<insert display name>"

  def __init__(self, args):
    win32serviceutil.ServiceFramework.__init__(self, args)

    self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

  def SvcStop(self):
    sys.stopservice = True

  def SvcDoRun(self):
    # Call a Main() like function here.
    pass
