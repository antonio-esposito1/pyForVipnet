from ncclient import manager
import shelve
import time
import subprocess
import threading
import paramiko

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



class AttrDisplay:
    "Provides an inheritable display overload method that shows instances with their class names and a name=value pair for each attribute stored on the instances itself (but not attrs inherited from its classes). Can be mixed into any class, and will work on any instance."
    
    def gatherAttrs(self):
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append('%s=%s' % (key, getattr(self, key)))
        return ', '.join(attrs)
    
    def __repr__(self):
        return '[%s: %s]' % (self.__class__.__name__, self.gatherAttrs())


class Device(AttrDisplay):
  "Questa classe descrive un device"
  def __init__(self, devicename, hostname, port, username, password):
    self.devicename = devicename
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password

  def connectnetconf(self):
      "questo metodo restituisce il collegamento netconf al device in campo "
      return manager.connect(host=self.hostname, port=self.port, username=self.username, password=self.password, hostkey_verify=False, device_params={}, allow_agent=False, look_for_keys=False)
      #return manager.connect(host=self.devicename, port=2222, username=self.username, password=self.password, hostkey_verify=False)

class XR_VPE(Device):
   def __init__(self, devicename, hostname, port, username, password):
      Device.__init__(self, devicename, hostname, port, username, password)
    
   def __repr__(self):
        return '[%s: %s]' % (self.devicename, self.gatherAttrs())

def netconfrequest(subtree_filter, device):

    #crea una string str_nc_get_reply contenete la risposta xml del device
    return device.get(('subtree', subtree_filter))

def netconf_requests_isis_neighbors(device):
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
   nc_get_reply = netconfrequest(stringaxml, device.connectnetconf())
   isis_neighbors = []
   xmlns = "http://cisco.com/ns/yang/Cisco-IOS-XR-clns-isis-oper"
   neighbors = nc_get_reply.data.findall(f'.//{{{xmlns}}}neighbor')
   for neighbor in neighbors:
     temp = {}
     temp['system-id'] = neighbor.find(f'{{{xmlns}}}system-id').text
     temp['interface-name'] = neighbor.find(f'{{{xmlns}}}interface-name').text
     temp['neighbor-state'] = neighbor.find(f'{{{xmlns}}}neighbor-state').text
     temp['neighbor-circuit-type'] = neighbor.find(f'{{{xmlns}}}neighbor-circuit-type').text
     isis_neighbors.append(temp)
   device.isis_neighbors = isis_neighbors
   #print(device.isis_neighbors)
   return device.isis_neighbors

def netconf_requests_bgp_vpnv4_unicast_neighbors(device):
   stringaxml = """
          <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-oper">
        <instances>
          <instance>
            <instance-active>
              <default-vrf>
                <afs>
                  <af>
                    <af-name>vpnv4-unicast</af-name>
                    <neighbor-af-table>
                      <neighbor>
                        <neighbor-address/>
                        <description/>
                        <remote-as/>
                        <connection-state/>
                        <af-data>
                          <af-name>vpnv4</af-name>
                          <prefixes-accepted/>
                          <prefixes-advertised/>
                        </af-data>
                      </neighbor>
                    </neighbor-af-table>
                  </af>
                </afs>
              </default-vrf>
            </instance-active>
          </instance>
        </instances>
      </bgp>
          """
   nc_get_reply = netconfrequest(stringaxml, device.connectnetconf())
   bgp_vpnv4_unicast_neighbors = []
   xmlns = "http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-oper"
   neighbors = nc_get_reply.data.findall(f'.//{{{xmlns}}}neighbor')
   for neighbor in neighbors:
     temp = {}
     temp['neighbor-address'] = neighbor.find(f'{{{xmlns}}}neighbor-address').text
     temp['description'] = neighbor.find(f'{{{xmlns}}}description').text
     temp['remote-as'] = neighbor.find(f'{{{xmlns}}}remote-as').text
     temp['connection-state'] = neighbor.find(f'{{{xmlns}}}connection-state').text
     bgp_vpnv4_unicast_neighbors.append(temp)
   device.bgp_vpnv4_unicast_neighbors = bgp_vpnv4_unicast_neighbors
   #print(device.bgp_vpnv4_unicast_neighbor)
   return device.bgp_vpnv4_unicast_neighbors


if __name__ == '__main__':
  deviceList = ['anvpe025', 'anvpe026']
  tunnel = SshTunnel(2222, 830, 'espositoa1','anvpe025')
  tunnel.start()
  anvpe025 = XR_VPE('anvpe025', 'localhost', '2222', 'espositoa1', 'SaericeGiacca81_21')
  netconf_requests_isis_neighbors(anvpe025)
  netconf_requests_bgp_vpnv4_unicast_neighbors(anvpe025)
  
  #time.sleep(3)
  
  tunnel = SshTunnel(2223, 830, 'espositoa1','anvpe026')
  tunnel.start()
  anvpe026 = XR_VPE('anvpe026', 'localhost', '2223', 'espositoa1', 'SaericeGiacca81_21')
  netconf_requests_isis_neighbors(anvpe026)
  netconf_requests_bgp_vpnv4_unicast_neighbors(anvpe026)
  
  timestr = time.strftime("%Y%m%d-%H%M%S")
  db = shelve.open('devicedb-' + timestr)
  for obj in (anvpe025, anvpe026):
     db[obj.devicename] = obj
  db.close()


    

  
  
  
  
  # print(db['mivpe015'])
  # db.close()
  #print(tabulate(list(db['mivpe015']['isis-neighbors']()), headers, tablefmt="fancy_grid"))
