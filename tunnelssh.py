import subprocess
import time
import threading
import paramiko
import time
from ncclient import manager

class SshTunnel(threading.Thread):
    def __init__(self, localport, remoteport, remoteuser, remotehost):
        threading.Thread.__init__(self)
        self.localport = localport      # Local port to listen to
        self.remoteport = remoteport    # Remote port on remotehost
        self.remoteuser = remoteuser    # Remote user on remotehost
        self.remotehost = remotehost    # What host do we send traffic to
        self.daemon = True              # So that thread will exit when
                                        # main non-daemon thread finishes

    def run(self):
        if subprocess.call([
            'ssh', '-N',
                   '-L', str(self.localport) + ':' + self.remotehost + ':' + str(self.remoteport), 'espositoa1@rmvhb021']):
            raise Exception ('ssh tunnel setup failed')


if __name__ == '__main__':
    stringaxml = """
          <isis xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-clns-isis-oper">
            <instances>
              <instance>
                <instance-name>CORE</instance-name>
                <neighbors>
                  <neighbor>
                    <system-id/>
                    <interface-name/>
                    <neighbor-state/>
                    <neighbor-circuit-type/>
                    <neighbor-media-type/>
                  </neighbor>
                </neighbors>
                <checkpoint-adjacencies>
              <checkpoint-adjacency>
                <system-id/>
              </checkpoint-adjacency>
            </checkpoint-adjacencies>
              </instance>
            </instances>
          </isis>
          """
    tunnel = SshTunnel(2222, 830, 'espositoa1','anvpe025')
    tunnel.start()
    device = manager.connect(host = 'localhost', port = 2222, username = 'espositoa1', password = 'SaericeGiacca81_21', hostkey_verify = False)
    
    nc_get_reply = device.get(('subtree', stringaxml))
        
    print(nc_get_reply)
    
    
    tunnel = SshTunnel(2223, 830, 'espositoa1','anvpe026')
    tunnel.start()
    device = manager.connect(host = 'localhost', port = 2223, username = 'espositoa1', password = 'SaericeGiacca81_21', hostkey_verify = False)
    nc_get_reply = device.get(('subtree', stringaxml))
    
    print(nc_get_reply)