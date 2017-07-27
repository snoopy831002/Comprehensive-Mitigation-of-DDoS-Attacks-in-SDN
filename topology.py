#!/usr/bin/python
 
"""

"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, IVSSwitch, UserSwitch
from mininet.link import Link, TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
 
def topology():
 
    "Create a network."
    net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
 
    print "*** Creating nodes"
    s1 = net.addSwitch( 's1', listenPort=6673, mac='00:00:00:00:00:01' )
    c2 = net.addController( 'c2' , ip='127.0.0.1' , port=6633 )
    h3 = net.addHost( 'h3', mac='00:00:00:00:00:03', ip='10.0.0.3/8' )
    h4 = net.addHost( 'h4', mac='00:00:00:00:00:04', ip='10.0.0.4/8' )
    h5 = net.addHost( 'h5', mac='00:00:00:00:00:05', ip='10.0.0.5/8' )
    
 
    print "*** Creating links"
    net.addLink(h5, s1)
    net.addLink(s1, h4)
    net.addLink(h3, s1)
 
    print "*** Starting network"
    net.build()
    c2.start()
    s1.start( [c2] )

 
    print "*** Running CLI"
    CLI( net )
 
    print "*** Stopping network"
    net.stop()
 
if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()