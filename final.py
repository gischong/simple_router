#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    #h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='1.1.1.1/24', defaultRoute="h1-eth0")
    #h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='2.2.2.2/24', defaultRoute="h2-eth0")
    
    h10 = self.addHost('h1',mac='00:00:00:00:00:01',ip='10.0.1.10/24', defaultRoute="h1-eth0") #Host10
    h20 = self.addHost('h2',mac='00:00:00:00:00:02',ip='10.0.2.20/24', defaultRoute="h2-eth0") #Host20
    h30 = self.addHost('h3',mac='00:00:00:00:00:03',ip='10.0.3.30/24', defaultRoute="h3-eth0") #Host30
    trusted = self.addHost('h4',mac='00:00:00:00:00:04',ip='104.82.214.112/24', defaultRoute="h4-eth0") #Trusted Host
    untrusted = self.addHost('h5',mac='00:00:00:00:00:05',ip='156.134.2.12/24', defaultRoute="h5-eth0") #Untrusted Host
    server = self.addHost('h6',mac='00:00:00:00:00:06',ip='10.0.4.10/24', defaultRoute="h6-eth0") #Server

    # Create a switch. No changes here from Lab 1.
    s1 = self.addSwitch('s1') #Floor 1 Switch
    s2 = self.addSwitch('s2') #Floor 2 Switch
    s3 = self.addSwitch('s3') #Floor 3 Switch
    s4 = self.addSwitch('s4') #Core Switch
    s5 = self.addSwitch('s5') #Data Center Switch

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
    #self.addLink(s1,h1, port1=8, port2=0)
    #self.addLink(s1,h2, port1=9, port2=0)

    #Adding links between switches and hosts
    self.addLink(s1,h10, port1=8, port2=0) #Links h10 -> Floor 1 Switch
    self.addLink(s2,h20, port1=8, port2=0) #Links h20 -> Floor 2 Switch
    self.addLink(s3,h30, port1=8, port2=0) #Links h30 -> Floor 3 Switch
    self.addLink(s4,trusted, port1=8, port2=0) #Links trusted -> Core
    self.addLink(s4,untrusted, port1=9, port2=0) #Links untrusted -> Core
    self.addLink(s5,server, port1=8, port2=0) #Links server -> Data Center

    #Adding links between switches
    self.addLink(s1,s4, port1=1, port2=1) #Links Floor 1 Switch -> Core
    self.addLink(s2,s4, port1=1, port2=2) #Links Floor 2 Switch -> Core
    self.addLink(s3,s4, port1=1, port2=3) #Links Floor 3 Switch -> Core
    self.addLink(s5,s4, port1=1, port2=4) #Links Data Center -> Core

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
