#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jun 10, 2013

@author: daniel
'''
from backend.RPCConnection import RPCConnection
from code import interact
from contextlib import closing
import shelve

class RPM(object):
  methodspec = dict(
    ('queue-get', ('queue-id', 'queue-name')),
    ('queue-add', ('queue-name',)),
    ('queue-modify', ('queue-id', 'queue-name'))
  )
  def __init__(self, host = 'localhost', port = 9198):
    self.conn = RPCConnection(host, port)
    self.auth()

  def auth(self):
    with closing(shelve.open('constants')) as store:
      self.rpckey = store.get('rpckey', '')
      if not self.rpckey:
        store['rpckey'] = self.rpckey = raw_input('Please enter your RPC Key: ')
    self.app_key()
    self.loadcmds()

  def loadcmds(self):
    for name in self.command('list-all-rpc')['commands']:
      if name in self.methodspec:
        argnames = self.methodspec[name]
        
      if not hasattr(self, name):
        def f(cmd = name):
          return self.command(cmd)
        self.__dict__[name.replace('-', '_')] = f

  def app_key(self):
    return self.command('app-key', key = self.rpckey)

  def command(self, cmd, **kwargs):
    return self.conn.comm(dict(command = cmd, **kwargs))


if __name__ == '__main__':
  r = RPM()
  interact(local = globals())
