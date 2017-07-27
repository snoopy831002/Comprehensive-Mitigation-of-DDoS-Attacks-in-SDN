from socket import socket, AF_PACKET, SOCK_RAW
 
from impacket import ImpactPacket
from impacket import ImpactDecoder
from impacket.ImpactPacket import TCPOption
from time import sleep
import random
 
def string2tuple(string):
    if string.find(':') >= 0:
       return [int(x) for x in string.split(':')]
    else:
       return [int(x) for x in string.split('.')]
 
def randomMAC():
    mac = (
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) )
    return mac
 
#Generate arp packets with randomly 
#s = socket(AF_INET, SOCK_RAW)
s = socket(AF_PACKET, SOCK_RAW) 
s.bind(("h4-eth0", 0x0806))
 
pktid = 0;
while(pktid <= 100000000):
    eth = ImpactPacket.Ethernet()
    forged_mac = randomMAC()
    eth.set_ether_shost(randomMAC())
    eth.set_ether_dhost(randomMAC())
    eth.set_ether_type(0x0806)
    print "send packet #", pktid,"with src_mac:", ':'.join(map(lambda x: "%02x" % x, forged_mac))
    arp = ImpactPacket.ARP() # create the arp packet that will be inside of layer 1
    arp.set_ar_hrd(0x0001) #  set hardware type to  ARPHRD ETHER  (ethernet)
    arp.set_ar_op(0x01) # Set tyoe to Arp Reply (0x02 = Reply, 0x04 = RevReply, 0x03 = RevRequest)
    arp.set_ar_pro(0x800) # 2048 (Set to standard IP protocol) 
    arp.set_ar_hln(6) # Length should be 6 (octaves of mac address)
    arp.set_ar_pln(4) # should be 4 (octaves of i.p. address)
    #arp.set_ar_spa(string2tuple("10.0.0.253")) # Set source I.P. in arp reply.
    #arp.set_ar_tpa(string2tuple("10.0.0.254")) # Set target I.P. in arp reply.
    #arp.set_ar_tha([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]) # Target of the packet, could be broadcast
    #arp.set_ar_sha(forged_mac) # Source of the packet (this is our own MAC, so they can reply to us)
 
    eth.contains(arp) # Encapsulate the arp packet, wrap the ethernet layer 1 packet around it.
    pkt=eth.get_packet()
    s.send(pkt)
    pktid = pktid + 1
    sleep(0.001)