#!/usr/bin/python

"""
Based On Mininet API
thanks to: Bob Lantz (rlantz@cs.stanford.edu), Brandon Heller (brandonh@stanford.edu)
thanks to all Dreamer Team, especially to Luca Prete (preteluca@gmail.com) for the bash scripts;

author: Pier Luigi Ventre (pl.ventre@gmail.com)
author: Giuseppe Siracusano (a_siracusano@tin.it)
author: Stefano Salsano (stefano.salsano@uniroma2.it)

"""
import re
from abc import ABCMeta, abstractmethod
from testbed_intf import EthIntf, LoIntf, TapIntf, ViIntf
from testbed_deployer_utils import EndIP
from testbed_deployer_utils import OSPFNetwork

#TODO Integration with psShell
# TODO Integrity Check, before starting the creation of the testbed.sh

class Node:
	
	ipBaseTestbed=[192,168, 1, 0]
	netbitTestbed=16
	netmaskTestbed=[255, 255, 0, 0]
	
	def __init__( self, NODInfo):
		self.name = NODInfo.name
		self.mgt_ip = NODInfo.mgt_ip
		self.eths = []
		self.nameToEths = {}
		for eth in NODInfo.intfs:
			eth_intf = EthIntf(eth, self.next_testbedAddress(), self.netbitTestbed, self.netmaskTestbed)
			self.eths.append(eth_intf)
			self.nameToEths[eth] = eth_intf

	def next_testbedAddress(self):
		self.ipBaseTestbed[3] = (self.ipBaseTestbed[3] + 1) % 256
		if self.ipBaseTestbed[3] == 0:
			self.ipBaseTestbed[2] = (self.ipBaseTestbed[2] + 1) % 256
		if self.ipBaseTestbed[2] == 255 and self.ipBaseTestbed[3] == 255:
			print "Ip Testbed Address Sold Out"
			sys.exit(-2)
		return "%s.%s.%s.%s" %(self.ipBaseTestbed[0], self.ipBaseTestbed[1], self.ipBaseTestbed[2], self.ipBaseTestbed[3])

	def start(self):
		raise NotImplementedError("TODO")

	def stop(self):
		raise NotImplementedError("TODO")

	def configure(self):
		raise NotImplementedError("TODO")
	
	def cmd(self, cmds):		
		raise NotImplementedError("TODO")

class Controller(Node):

	def __init__( self, NODInfo, port, vlan):
		Node.__init__(self, NODInfo)
		self.port = port
		self.ips = []

	def addIP(self, ip):
		if ip not in ips:
			self.ips.append(ip) 

class Oshi(Node):

	loopbackBaseTestbed = [172, 168, 0, 0]
	dpidLen = 16

	def __init__( self, NODInfo, vlan):
		Node.__init__(self, NODInfo)
		self.dpid = self.defaultDpid()
		self.loopback = LoIntf(ip=self.next_loopbackAddress())
		self.vlan = vlan
		self.endips = []
		self.nameToEndIps = {}
		self.taps = []
		self.nameToTaps = {}
		self.vis = []
		self.nameToVis = {}
		self.ctrls = []
		self.ospfnets = []
		self.nameToNets = {}
		
		self.endIPBase = 1
		self.tapBase = 1
		self.viBase = 1
		self.ethIndex = 0
		self.tapPortBase = 1190
		self.ospfNetBase = 1


	def defaultDpid( self ):
		"Derive dpid from switch name, s1 -> 1"
		try:
			dpid = int( re.findall( r'\d+', self.name )[ 0 ] )
			dpid = hex( dpid )[ 2: ]
			dpid = '0' * ( self.dpidLen - len( dpid ) ) + dpid
			return dpid
		except IndexError:
			raise Exception( 'Unable to derive default datapath ID - '
							 'please either specify a dpid or use a '
							 'canonical switch name such as s23.' )	
	
	def setControllers(self, controllers):
		for controller in controllers:
			(ip,port) = controller.split(":")
			key = ip + " " + port
			if key in self.ctrls:
				continue
			self.ctrls.append(key)
	
	def newOSPFNetName(self):
		ret = self.ospfNetBase
		self.ospfNetBase = self.ospfNetBase + 1
		return "NET%s" % ret		
		
	def addOSPFNet(self, net):
		name = self.newOSPFNetName()
		net.name = name
		self.ospfnets.append(net)
		self.nameToNets[name] = net
		return net
	
	def newViName(self):
		ret = self.viBase
		self.viBase = self.viBase + 1
		return "vi%s" % ret
	
	def addVi(self, ip, netbit, hello_int, cost):
		name = self.newViName()
		vi = ViIntf(name, ip, netbit, hello_int, cost)
		self.vis.append(vi)
		self.nameToVis[name] = vi
		return vi 		
	
	def newTapName(self):
		ret = self.tapBase
		self.tapBase = self.tapBase + 1
		return "tap%s" % ret
	
	def newTapPort(self):
		self.tapPortBase = self.tapPortBase + 1
		return self.tapPortBase
	
	def addTap(self, localport, remoteport, endipname):
		name = self.newTapName()
		tap = TapIntf(name, localport, remoteport, endipname)
		self.taps.append(tap)
		self.nameToTaps[name] = tap
		return tap
 
	def next_eth(self):
		ret = (self.eths[self.ethIndex].name, self.eths[self.ethIndex].ip)
		self.ethIndex = (self.ethIndex + 1) % len(self.eths) 		
		return ret

	def addEndIP(self, remoteIP, localIntf):
		name = self.newEndIPName()
		endip = EndIP(name, remoteIP, localIntf)
		self.endips.append(endip)
		self.nameToEndIps[name] = endip
		return endip
		
	def newEndIPName(self):
		ret = self.endIPBase
		self.endIPBase = self.endIPBase + 1
		return "endip%s" % ret

	def next_loopbackAddress(self):
		self.loopbackBaseTestbed[3] = (self.loopbackBaseTestbed[3] + 1) % 256
		if self.loopbackBaseTestbed[3] == 0:
			self.loopbackBaseTestbed[2] = (self.loopbackBaseTestbed[2] + 1) % 256
		if self.loopbackBaseTestbed[2] == 255 and self.loopbackBaseTestbed[3] == 255:
			print "Loopback Address Sold Out"
			sys.exit(-2)
		return "%s.%s.%s.%s" %(self.loopbackBaseTestbed[0], self.loopbackBaseTestbed[1], self.loopbackBaseTestbed[2], self.loopbackBaseTestbed[3])

	# XXX Probably we have to change keys
	def controllersSerialization(self):
		i = 1
		names = []
		serialized_line = ""
		for ctrl in self.ctrls:
			name = "ctrl" + str(i)
			names.append(name)
			serialized_line = serialized_line + ("declare -a %s=(%s)\n" %(name, ctrl))			
			i = i + 1			
		ret = "declare -a CTRL=(" + " ".join(names) + ")\n" + serialized_line
		return ret

	def ethsSerialization(self):
		return "declare -a INTERFACES=(" + " ".join("%s" % eth.name for eth in self.eths) + ")\n"

	def tapsSerialization(self):
		return "declare -a TAP=(" + " ".join("%s" % tap.name for tap in self.taps) + ")\n"
	
	def visSerialization(self):
		return "declare -a QUAGGAINT=(" + " ".join("%s" % vi.name for vi in self.vis) + ")\n"

	def ospfnetsSerialization(self):
		return "declare -a OSPFNET=(" + " ".join("%s" % net.name for net in self.ospfnets) + ")\n"

	def configure(self):
		testbed = open('testbed.sh','a')
		testbed.write("# %s - start\n" % self.mgt_ip)
		testbed.write("HOST=%s\n" % self.name)
		testbed.write("ROUTERPWD=dreamer\n")
		testbed.write("DPID=%s\n" % self.dpid)
		testbed.write("SLICEVLAN=%s\n" % self.vlan)
		testbed.write("BRIDGENAME=br-dreamer\n")
		testbed.write(self.controllersSerialization())
		testbed.write(self.loopback.serialize())
		testbed.write(self.ethsSerialization())
		for eth in self.eths:
			testbed.write(eth.serialize())
		testbed.write(self.tapsSerialization())
		for tap in self.taps:
			testbed.write(tap.serialize())
		for endip in self.endips:
			testbed.write(endip.serialize())
		testbed.write(self.visSerialization())
		for vi in self.vis:
			testbed.write(vi.serialize())
		testbed.write(self.ospfnetsSerialization())
		for net in self.ospfnets:
			testbed.write(net.serialize())
		testbed.write("# %s - end\n" % self.mgt_ip)
		testbed.close()

	#def start():

	#def stop():

	#def cmd():
	
	


