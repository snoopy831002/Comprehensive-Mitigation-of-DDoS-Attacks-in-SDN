# Copyright 2011 James McCauley
#
# This file is part of POX.
#
# POX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# POX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with POX.  If not, see <http://www.gnu.org/licenses/>.
 
"""
This is an L2 learning switch written directly against the OpenFlow library.
It is derived from one written live for an SDN crash course.
"""
 
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.util import str_to_bool
from collections import deque
import time
 
log = core.getLogger()
 
# We don't want to flood immediately when a switch connects.
FLOOD_DELAY = 5
# Limit max MAC address table size to be 1000
MAX_TABLE_SIZE = 100
 
class LearningSwitch (EventMixin):
 
  def __init__ (self, connection, transparent):
    # Switch we'll be adding L2 learning switch capabilities to
    self.connection = connection
    self.transparent = transparent
 
    # Our table
    self.macToPort = {}
    self.macHistory = deque()
 
    # We want to hear PacketIn messages, so we listen
    self.listenTo(connection)
 
    #log.debug("Initializing LearningSwitch, transparent=%s",
    #          str(self.transparent))
 
  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch to implement above algorithm.
    """
 
    packet = event.parse()
 
    def flood ():
      """ Floods the packet """
      if event.ofp.buffer_id == -1:
        log.warning("Not flooding unbuffered packet on %s",
                    dpidToStr(event.dpid)) # dipd is the id of switch
        return
      msg = of.ofp_packet_out()
      if time.time() - self.connection.connect_time > FLOOD_DELAY:
        # Only flood if we've been connected for a little while...
        #log.debug("%i: flood %s -> %s", event.dpid, packet.src, packet.dst)
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      else:
        pass
        #log.info("Holding down flood for %s", dpidToStr(event.dpid))
      msg.buffer_id = event.ofp.buffer_id
      msg.in_port = event.port
      self.connection.send(msg)
 
    def drop (duration = None):
      """
      Drops this packet and optionally installs a flow to continue
      dropping similar ones for a while
      """
      if duration is not None:
        if not isinstance(duration, tuple):
          duration = (duration,duration)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = duration[0]
        msg.hard_timeout = duration[1]
        msg.buffer_id = event.ofp.buffer_id
        self.connection.send(msg)
      elif event.ofp.buffer_id != -1:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)
 
    if( len(self.macToPort) >= MAX_TABLE_SIZE ):
        #evict oldest entry 
        evictEntry = self.macHistory.popleft()
        del self.macToPort[evictEntry]
        log.debug("!!! MAC Table overflowed -- remove old entry")
        #flood()
     
    self.macToPort[packet.src] = event.port #1
    self.macHistory.append(packet.src)

    #Drop if dest addr is a Bridge Filtered address or Ethertpe LLDP (skip this step if transparent == True)
    if not self.transparent:
      if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered(): # 2
        drop()
        return
 
    if packet.dst.isMulticast():
      flood() # 3a
    else:
      if packet.dst not in self.macToPort: # 4
        log.debug("Port for %s unknown -- flooding" % (packet.dst,))
        flood() # 4a
      else:
        port = self.macToPort[packet.dst]
        #drop packet if input port = output port
        if port == event.port: # 5
          # 5a
          log.warning("Same port for packet from %s -> %s on %s.  Drop." %
                      (packet.src, packet.dst, port), dpidToStr(event.dpid))
          drop(10)
          return
        #input port != output port -> install flow table entry
        log.debug("installing flow for %s.%i -> %s.%i" %
                  (packet.src, event.port, packet.dst, port))
        #msg = of.ofp_flow_mod()
        #msg.match = of.ofp_match.from_packet(packet)
        #msg.idle_timeout = 10
        #msg.hard_timeout = 30
        #msg.actions.append(of.ofp_action_output(port = port))
        msg = of.ofp_packet_out(in_port=event.port)
        if event.ofp.buffer_id != -1 and event.ofp.buffer_id is not None:
            msg.buffer_id = event.ofp.buffer_id # 6a
        else:
            if event.ofp.data:
                return
            msg.data = event.ofp.data
        msg.actions.append(of.ofp_action_output(port = port))
        self.connection.send(msg)
 
class l2_learning (EventMixin):
  """
  Waits for OpenFlow switches to connect and makes them learning switches.
  """
  def __init__ (self, transparent):
    self.listenTo(core.openflow)
    self.transparent = transparent
 
  def _handle_ConnectionUp (self, event):
    log.debug("Connection %s" % (event.connection,))
    LearningSwitch(event.connection, self.transparent)
 
 
def launch (transparent=False):
  """
  Starts an L2 learning switch.
  """
  core.registerNew(l2_learning, str_to_bool(transparent))