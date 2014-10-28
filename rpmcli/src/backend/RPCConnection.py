'''
Created on Mar 8, 2011

@author: daniel
'''

from telnetlib import Telnet
import json

class RPCConnection(object, Telnet):
  def __init__(self, host = 'localhost', port = 9198, auto = True):
    Telnet.__init__(self)
    self.host, self.port, self.connected = host, port, False
    if auto:
      self._connect()

  def _connect(self):
    self.open(self.host, self.port)
    self.connected = True

  def _disconnect(self):
    self.close()
    self.connected = False

  def __enter__(self):
    self._connect()
    return self

  def __exit__(self, etype, value, traceback):
    self._disconnect()

  def send(self, adict):
    self.write(json.dumps(adict))

  def recv(self):
    resp = self.read_until('\n')
    self.msg(resp)
    try:
      return json.loads(resp)
    except Exception, e:
      print e
      print repr(resp)
      return resp

  def comm(self, adict):
    self.send(adict)
    return self.recv()

  def write(self, buffer):
    """Write a string to the socket.

    Can block if the connection is blocked.  May raise
    socket.error if the connection is closed.

     - Note this is overridden from the Telnet class to prevent IAC (\xFF)
       duplication which is unnecessary for this connection.
    """
    self.msg("send %r", buffer)
    self.sock.sendall(buffer)



if __name__ == "__main__":
  with RPCConnection() as conn:
    print conn.comm({'command': 'make-uuid'})
