# Implementing a Simple Router on a Network

# Description
  - Construction of a simplified company network topology using Mininet
  - Implementing firewall rules with a Pox controller for communication between un/trusted hosts and the server

# What's it built with?
  - Python
    -Mininet- a network emulator - https://github.com/mininet/mininet/wiki/Introduction-to-Mininet

# Topology
  - h10 = Host10, h20 = Host20, h30 = Host30, trusted = h4, untrusted = h5, server = h6
  - s1 = Floor 1 Switch, s2 = Floor 2 Switch, s3 = Floor 3 Switch, s4 = Core Swtich, s5 = Data Center Switch

#  Firewall Rules
|Rule|Description|
|---|---|
|Hosts 10/20/30|Allowed to communicate with any host, EXCEPT ICMP queries from untrusted host. ICMP from untrusted host must be blocked|
|Trusted Host|Allowed to communicate with any host/server|
|Untrusted Host|Should not be allowed to send ICMP traffic to Hosts 10/20/30, as well as IP traffic to server|
|Server|Should not accept IP traffic from untrusted host. Must accept all other traffic from other hosts|
# Expected Output from 'pingall'
  - h1 -> h2 h3 h4 X h6
  - h2 -> h1 h3 h4 X h6
  - h3 -> h1 h2 h4 X h6
  - h4 -> h1 h2 h3 h5 h6
  - h5 -> X X X h4 X
  - h6 -> h1 h2 h3 h4 X 

# Output Explanation
  - 26% - 22/30 received
  - Pingall sends out ICMP packets to test hosts, thus it was used to test if the logic of the controller was correct
  - h10, h20, h30, and the server cannot reach h5 because h5 is a untrusted host on the network
  - Vice versa, h5 cannot reach h10, h20, h30, or the server because the rules block ICMP packets sent from h5 to h10, h20, h30 and ANY incoming IP traffic  from h5 to the server
  - h4(a trusted host) can reach all the other host because the rules allowed it

# More Explanation
  - The POX controller helps "install" the rule into the switch so that the switch "remembers" what to do for a few seconds
  - Flood all non-IP traffic to find IPv4 packets(sends all non-IP traffic to outgoing nodes)
    - if IPv4 was NOT found - flood it with '.OFPP_FLOOD'(this floods all ports except the input port)
    - if IPv4 WAS found - check switch rules with the packet info(source/destination IP, traffic type, etc)
       - either allow or deny access to the packet through the switch