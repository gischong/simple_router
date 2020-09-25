# Final Skeleton
#
# Hints/Reminders from Lab 4:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 4:
    #   - port_on_switch represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
    # Installs table entries, same as lab3
    msg = of.ofp_flow_mod() # used for "installing" rule into switch and for switch to "remember" it for a few seconds
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 25
    msg.hard_timeout = 50

    ip = packet.find('ipv4') #finds ipv4
    ICMP = packet.find('icmp') #finds icmp
 
    if ip is None: #if ip is not ipv4, then flood
       msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
       msg.data = packet_in
       self.connection.send(msg) 
       return

    #Floor 1 Switch
    # if packet has dst ip to Host10, then forward to port 8
    # if packet has src ip from Host10, then forward to port 1 -> leaving from Floor 1 Switch to Core switch
    if switch_id == 1:
       if ip.dstip == '10.0.1.10':
          #print("headed to h1")
          action = of.ofp_action_output(port = 8)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)
       if ip.srcip == '10.0.1.10':
          #print("leaving s1")
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)

    #Floor 2 Switch
    # if packet has dst ip to Host20, then forward to port 8
    # if packet has src ip from Host20, then forward to port 1 -> leaving from Floor 2 Switch to Core switch
    elif switch_id == 2:
       if ip.dstip == '10.0.2.20':
          #print("headed to h2")
          action = of.ofp_action_output(port = 8)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)
       if ip.srcip == '10.0.2.20':
          #print("leaving s2")
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)

    #Floor 3 Switch
    # if packet has dst ip to Host30, then forward to port 8
    # if packet has src ip from Host30, then forward to port 1 -> leaving from Floor 3 Switch to Core switch
    elif switch_id == 3:
       if ip.dstip == '10.0.3.30':
          #print("headed to h3")
          action = of.ofp_action_output(port = 8)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)
       if ip.srcip == '10.0.3.30':
          #print("leaving s3")
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)
    
    #Core Switch
    # if ICMP traffic is coming from untrusted host and dst ip is not to trusted host, drop the packet -> doesn't allow ICMP traffic to Host10/20/30 and Server
    # if src ip is from untrusted and dst ip is server, drop packet -> doesn't allow IP traffic to server
    # if dst ip is to switch #, then forward to port # -> leaving core to Floor # Switch, Data Center, Trusted Host, or Untrusted Host
    elif switch_id == 4:
       if ip.srcip == '156.134.2.12' and ICMP is not None:
          if ip.dstip != '104.82.214.112':
             #print("packet dropped")
             msg.data = packet_in
             self.connection.send(msg)
             return
       if ip.srcip == '156.134.2.12' and ip.dstip == '10.0.4.10':
          #print("packet dropped")
          msg.data = packet_in
          self.connection.send(msg)
          return
       elif ip.dstip == '10.0.1.10':
          #print("headed to s1")
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)   
       elif ip.dstip == '10.0.2.20':
          #print("headed to s2")
          action = of.ofp_action_output(port = 2)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)
       elif ip.dstip == '10.0.3.30':
          #print("headed to s3")
          action = of.ofp_action_output(port = 3)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)
       elif ip.dstip == '10.0.4.10':
          #print("headed to server")
          action = of.ofp_action_output(port = 4)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)
       elif ip.dstip == '104.82.214.112':
          #print("headed to trusted")
          action = of.ofp_action_output(port = 8)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)
       elif ip.dstip == '156.134.2.12':
          #print("headed to untrusted")
          action = of.ofp_action_output(port = 9)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)

    #Data Center Server Switch
    # if packet has src ip from untrusted host and dst ip to server, don't accept -> or if packet doesn't have src ip from untrusted host and dst ip to server, accept
    # if packet has src ip from server, then forward to port 1 -> leaving Data Center to Core Switch
    elif switch_id == 5:
       if ip.srcip != '156.134.2.12' and ip.dstip == '10.0.4.10':
          #print("all trusted packet headed to server")
          action = of.ofp_action_output(port = 8)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)
       if ip.srcip == '10.0.4.10':
          #print("leaving data center")
          action = of.ofp_action_output(port = 1)
          msg.actions.append(action)
          msg.data = packet_in
          self.connection.send(msg)

    #print "Hello, World!"

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
