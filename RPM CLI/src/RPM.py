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
  """
    The RPM Class encapsulates an RPC Connection to a server
    running RPM Remote Print Manager.
  """

  methodspec = {
    'action-add': {'atype': 'action-type'},
    'action-device-id': {'aid': 'action-id'},
    'action-get': {'aid': 'action-id'},
    'action-get-devmode': {'aid': 'action-id'},
    'action-get-queue': {'aid': 'action-id'},
    'action-list': {'qid': 'queue-id', 'qname': 'queue-name'},
    'action-list-fields': {'atype': 'action-type'},
    'action-modify': {'aid': 'action-id'},
    'action-refresh': {'aid': 'action-id'},
    'action-refresh-all': {'qid': 'queue-id'},
    'action-remove': {'aid': 'action-id'},
    'action-remove-all': {'qid': 'queue-id', 'qname': 'queue-name'},
    'action-set-devmode': {'aid': 'action-id', 'devmode': 'devmode'},
    'action-set-type': {'atype': 'action-type', 'aid': 'action-id'},
    'app-status': {'option': 'option'},
    'callback-add': {'callback': 'callback'},
    'callback-call': {'tag': 'callback-tag'},
    'callback-remove': {'callback': 'callback'},
    'device-add': {'path': 'path', 'dtype': 'device-type'},
    'device-alarm': {'did': 'device-id'},
    'device-error': {'did': 'device-id', 'err': 'error'},
    'device-get': {'did': 'device-id'},
    'device-get-path': {'path': 'path'},
    'device-get-state': {'did': 'device-id'},
    'device-get-status': {'did': 'device-id'},
    'device-get-user': {'did': 'device-id'},
    'device-modify': {'did': 'device-id'},
    'device-refresh': {'did': 'device-id'},
    'device-release': {'did': 'device-id'},
    'device-remove': {'did': 'device-id'},
    'device-remove-path': {'path': 'path'},
    'device-reserve': {'did': 'device-id'},
    'device-set-state': {'did': 'device-id', 'state': 'state'},
    'device-set-status': {'did': 'device-id', 'status': 'status'},
    'device-set-user': {'did': 'device-id', 'user': 'user'},
    'files-get': {'path': 'path'},
    'folder-create': {'path': 'path', 'name': 'leaf'},
    'job-add': {'path': 'job-path'},
    'job-cancel': {'jid': 'job-id'},
    'job-clear-error': {'jid': 'job-id'},
    'job-copy': {'jid': 'job-id'},
    'job-file-str': {'jid': 'job-id', 'mask': 'string'},
    'job-find': {'name': 'name'},
    'job-get': {'jid': 'job-id'},
    'job-get-error': {'jid': 'job-id'},
    'job-get-path': {'jid': 'job-id'},
    'job-hold': {'jid': 'job-id', 'state': 'hold'},
    'job-modify': {'jid': 'job-id'},
    'job-move': {'jid': 'job-id'},
    'job-remove': {'jid': 'job-id'},
    'job-rename': {'jid': 'job-id', 'jname': 'job-name'},
    'job-reprint': {'jid': 'job-id'},
    'logon-batch-add': {'uid': 'user-id'},
    'network-host-2-ip': {'host': 'host'},
    'network-ip-2-host': {'ip': 'ip'},
    'network-is-ip': {'ip': 'ip'},
    'port-refresh': {'port': 'port'},
    'port-remove': {'ports': 'ports'},
    'printer-devmode': {'printer': 'printer'},
    'queue-add': {'qname': 'queue-name'},
    'queue-eligible': {'qid': 'queue-id', 'qname': 'queue-name'},
    'queue-enable': {'qid': 'queue-id', 'state': 'enable'},
    'queue-exists': {'qid': 'queue-id', 'qname': 'queue-name'},
    'queue-find': {'name': 'name'},
    'queue-get': {'qid': 'queue-id', 'qname': 'queue-name'},
    'queue-hold': {'qid': 'queue-id', 'state': 'hold'},
    'queue-id': {'qname': 'queue-name'},
    'queue-is -archiving': {'qid': 'queue-id'},
    'queue-is -enabled': {'qid': 'queue-id', 'qname': 'queue-name'},
    'queue-is -held': {'qid': 'queue-id', 'qname': 'queue-name'},
    'queue-is -suspended': {'qid': 'queue-id', 'qname': 'queue-name'},
    'queue-jobs': {'qid': 'queue-id', 'qname': 'queue-name'},
    'queue-modify': {'qid': 'queue-id', 'qname': 'queue-name'},
    'queue-name': {'qid': 'queue-id'},
    'queue-purge': {'qid': 'queue-id'},
    'queue-refresh': {'qid': 'queue-id'},
    'queue-remove': {'qid': 'queue-id'},
    'queue-remove-archive': {'qid': 'queue-id'},
    'queue-rename': {'newname': 'newname'},
    'queue-reprint': {'qid': 'queue-id', 'qname': 'queue-name'},
    'queue-seqno': {'qid': 'queue-id', 'qname': 'queue-name'},
    'queue-set-archive': {'qid': 'queue-id', 'policy': 'delete-jobs'},
    'queue-suspend': {'qid': 'queue-id', 'state': 'suspend'},
    'scheduler2-job-action-status': {'jid': 'job-id', 'aid': 'action-id'},
    'scheduler2-job-status': {'jid': 'job-id'},
    'settings-get': {'category': 'category', 'attr': 'attr'},
    'settings-list': {'category': 'category'},
    'settings-refresh-category': {'category': 'category'},
    'settings-remove': {'category': 'category', 'attr': 'attr'},
    'settings-remove-category': {'category': 'category'},
    'settings-set': {'category': 'category', 'attr': 'attr', 'val': 'value'},
    'socket-add-listener': {'port': 'port', 'proto': 'protocol'},
    'socket-get-port': {'port': 'port'},
    'socket-modify-listener': {'port': 'port', 'proto': 'protocol'},
    'socket-port-start': {'port': 'port'},
    'socket-port-stop': {'port': 'port'},
    'spool-alarm': {'path': 'dir'},
    'spool-exist': {'path': 'path'},
    'spool-set-dir': {'path': 'dir'},
    'spool-set-temp': {'path': 'dir'},
    'spool-unique-path': {'path': 'dir', 'name': 'file'},
    'transform-add': {'ttype': 'transform-type'},
    'transform-get': {'tid': 'transform-id'},
    'transform-list': {'qid': 'queue-id', 'qname': 'queue-name'},
    'transform-list-fields': {'ttype': 'transform-type'},
    'transform-modify': {'tid': 'transform-id'},
    'transform-refresh': {'tid': 'transform-id'},
    'transform-refresh-all': {'qid': 'queue-id'},
    'transform-remove': {'tid': 'transform-id'},
    'transform-remove-all': {'qid': 'queue-id', 'qname': 'queue-name'},
    'user-add': {'user': 'user', 'pwd': 'password', 'domain': 'domain'},
    'user-get': {'uid': 'user-id'},
    'user-modify': {'uid': 'user-id', 'uname': 'user-name'},
    'user-refresh': {'uid': 'user-id'},
    'user-remove': {'uid': 'user-id'},
    'user-reset': {'uids': 'user-ids'}
  }
  addkwargs = {'action-add',
               'action-modify',
               'device-add',
               'device-modify',
               'job-add',
               'job-find',
               'job-modify',
               'port-modify',
               'queue-find',
               'queue-modify',
               'socket-modify-listener',
               'transform-add',
               'transform-modify',
               'user-modify'}

  def __init__(self, host = 'localhost', port = 9198):
    self.host = host
    self.port = port
    self.conn = RPCConnection(host, port)
    self.auth()
    self.loadcmds()

  def auth(self):
    with closing(shelve.open('constants')) as store:
      self.rpckey = store.get('%s-%d-%s' % (self.host, self.port, 'rpckey'), '')
      while True:
        authorized = self.app_key()
        if authorized['success']:
          return authorized
        print authorized['message']
        store['rpckey'] = self.rpckey = raw_input('Please enter your RPC Key: ')

  def loadcmds(self):
    for cmd in self.command('list-all-rpc')['commands']:
      method = cmd.replace('-', '_')
      if hasattr(self, method):
        continue
      if cmd in self.methodspec:
        def func(self, cmd = cmd, **kwargs):
          params = {rpcname: kwargs[argname]
                      for argname, rpcname in self.methodspec[cmd].items()
                        if argname in kwargs}
          if cmd in self.addkwargs:
            params.update(kwargs)
          return self.command(cmd, **params)
        argstr = '\n'.join(map(': '.join, sorted(self.methodspec[cmd].items())))
        if cmd in self.addkwargs:
          argstr += '\n**kwargs: Additional unlisted parameters allowed.'
        func.__doc__ = "Method: %s\n -- Valid Keywords --\n%s" % (cmd, argstr)
      else:
        def func(self, cmd = cmd):
          return self.command(cmd)
        func.__doc__ = "Method: %s\n -- No Additional Keywords --" % cmd
      func.__name__ = str(method)
      # hyphens aren't valid in python syntax, but they're 
      # accessible via getattr if necessary.
      setattr(RPM, cmd, func)
      setattr(RPM, method, func)

  def app_key(self):
    return self.command('app-key', key = self.rpckey)

  def command(self, cmd, **kwargs):
    return self.conn.comm(dict(command = cmd, **kwargs))

if __name__ == '__main__':
  r = RPM()
  interact(local = globals())
