#!/usr/bin/python

"""
Based On Mininet API
thanks to: Bob Lantz (rlantz@cs.stanford.edu), Brandon Heller (brandonh@stanford.edu)
thanks to all Dreamer Team, especially to Luca Prete (preteluca@gmail.com) for the bash scripts;

author: Pier Luigi Ventre (pl.ventre@gmail.com)
author: Giuseppe Siracusano (a_siracusano@tin.it)
author: Stefano Salsano (stefano.salsano@uniroma2.it)

"""

import sys
from testbed_node import Oshi, Controller
from mapping_parser import MappingParserOFELIA
from testbed_deployer_utils import OSPFNetwork
import copy

# XXX configure() depends On Luca Prete' s Bash Script
# TODO Introduce integrity check
class TestbedOFELIA( object ):

	# Init Function
	def __init__( self, path_mapping="Mapping.json", verbose=True):

		self.parser = MappingParserOFELIA(path_mapping, verbose)
		(self.oshinfo, self.aosinfo, self.ctrlsinfo, self.euhsinfo) = self.parser.getNodesInfo()
		self.vlan = self.parser.vlan
		self.verbose = True
		self.ospfBase = 1

		self.oshs = []
		self.aoss = []
		self.euhs = []
		self.ctrls = []
		self.ospfnets = []

		self.nameToNode = {}
		self.nameToOSPFNet = {}
		self.oshiToControllers = {}
	
	def addOshi(self):
		if len(self.oshinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Oshi"
			sys.exit(-2)
		osh = self.oshinfo[0]
		self.oshinfo.remove(osh)
		oshi = Oshi(osh, self.vlan)
		self.oshs.append(oshi)
		self.nameToNode[oshi.name] = oshi
		return oshi

	def addAoshi(self):
		if len(self.aosinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Aoshi"
			sys.exit(-2)
		aos = self.aosinfo[0]
		self.aosinfo.remove(aos)
		aoshi = Oshi(aos, self.vlan)
		self.aoss.append(aoshi)
		self.nameToNode[aoshi.name] = aoshi
		return aoshi
	
	def addController(self, port):
		if len(self.ctrlsinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Controller"
			sys.exit(-2)
		ctrl = self.ctrlsinfo[0]
		self.ctrlsinfo.remove(ctrl)
		ctrl = Controller(ctrl, port, self.vlan)
		self.ctrls.append(ctrl)
		self.nameToNode[ctrl.name] = ctrl
		return ctrl

	def addEuh(self):
		if self.verbose:
			print "*** Add Euh %s" % self.euhsinfo[0].name

	def getNodeByName(self, key):
		return self.nameToNode[key]
	
	# Allocation OF OVS equipment, We Use A RR Behavior;
	def roundrobinallocation(self):
		ctrl_to_allocate = []
		for ctrl in self.ctrls:
			if len(ctrl.ips) > 0:
				ctrl_to_allocate.append(ctrl)

		if len(ctrl_to_allocate) >= 1:
			for osh in self.oshs:
				osh.setController(ctrl_to_allocate[0].ips[0], ctrl_to_allocate[0].port)
			for aosh in self.aoss:
				aos.setController(ctrl_to_allocate[0].ips[0], ctrl_to_allocate[0].port)

		elif len(ctrl_to_allocate) >= 2:
			i = 0
			j = 0
			for osh in self.oshs:
				i = i % len(ctrl_to_allocate)
				j = (i + 1) % len(ctrl_to_allocate)
				osh.setController(ctrl_to_allocate[i].ips[0], ctrl_to_allocate[i].port)
				# Backup Controller
				osh.setController(ctrl_to_allocate[j].ips[0], ctrl_to_allocate[j].port)
				i = i + 1
		else:
			print "Error No Controller Added - Informatino Will Not Be Generated"
		
	# TODO Check is lhs is (oshi or aoshi) and rhs is (oshi or aoshi)
	def addLink(self, lhs, rhs):
		
		lhs = self.getNodeByName(lhs)	
		rhs = self.getNodeByName(rhs)

		(lhs_eth, lhs_eth_ip) = lhs.next_eth()
		(rhs_eth, rhs_eth_ip) = rhs.next_eth()
		lhs_endip = lhs.addEndIP(rhs_eth_ip, lhs_eth)
		rhs_endip = rhs.addEndIP(lhs_eth_ip, rhs_eth)
		lhs_tap_port = lhs.newTapPort()
		rhs_tap_port = rhs.newTapPort()
		lhs_tap = lhs.addTap(lhs_tap_port, rhs_tap_port, lhs_endip.name)
		rhs_tap = rhs.addTap(rhs_tap_port, lhs_tap_port, rhs_endip.name)

		ospf_net = self.addOSPFNet(ctrl=False)
		lhs_ip = self.next_hostAddress(ospf_net)
		rhs_ip = self.next_hostAddress(ospf_net)
		lhs_ospf_net = copy.deepcopy(ospf_net)
		rhs_ospf_net = copy.deepcopy(ospf_net)
		lhs.addOSPFNet(lhs_ospf_net)
		rhs.addOSPFNet(rhs_ospf_net)
		lhs_vi = lhs.addVi(lhs_ip, lhs_ospf_net.netbitOSPF, lhs_ospf_net.hello_int, lhs_ospf_net.cost)
		rhs_vi = rhs.addVi(rhs_ip, rhs_ospf_net.netbitOSPF, rhs_ospf_net.hello_int, rhs_ospf_net.cost)
		
	
	def newOSPFNetName(self):
		
		ret = self.ospfBase
		self.ospfBase = self.ospfBase + 1
		return "NET%s" % ret
		
	def addOSPFNet(self, ctrl):
		name = self.newOSPFNetName()
		net = OSPFNetwork(name, ctrl)
		self.ospfnets.append(net)
		self.nameToOSPFNet[name] = net
		return net

	# XXX Change With ipBaseOSPF and netbitOSPF
	def next_hostAddress(self, net):
		net.subnet[3] = (net.subnet[3] + 1) % 256
		if net.subnet[3] == 255:
			print "Ip Address Sold Out"
			sys.exit(-2)
		return "%s.%s.%s.%s" %(net.subnet[0], net.subnet[1], net.subnet[2], net.subnet[3])

	# Check if a structure is empty
	def is_empty(struct):
		if struct:
		    return False
		else:
		    return True
	
	def configure(self):
		self.roundrobinallocation()
		header =open('header.txt','r')
		testbed = open('testbed.sh','w')
		lines = header.readlines()
		for line in lines:
			testbed.write(line)
		testbed.close()
		for osh in self.oshs:
			osh.configure()
		for aos in self.aoss:
			aos.configure()

	def start(self):
		for osh in self.oshs:
			osh.start()

	def stop(self):
		for osh in self.oshs:
			osh.stop()

# XXX Test1 Create a Mesh Triangular Network And Print The Internal Object of TestBed
def test1():
	print "*** Test1"
	testbed = TestbedOFELIA("ofelia_mapping.json", verbose=False)
	print "*** Create Core Networks"
	oshis = []
	for i in range(3):
		oshi = testbed.addOshi()
		for lhs in oshis:
			l = testbed.addLink(lhs.name, oshi.name)
			print "*** Connect", lhs.name, "To", oshi.name 
		oshis.append(oshi)
	testbed.configure()
	print "###########################"
	print "*** Internal TestBed"
	print "*** NameToNode", testbed.nameToNode
	print "*** NameToOSPFNet", testbed.nameToOSPFNet
	print "*** OshiToControllers", testbed.oshiToControllers
	print "###########################"
	for osh in testbed.oshs:
		print "*** OSHI:", osh.name
		for key, value in osh.nameToEths.iteritems():
			print "*** Eth", key, value
		for key, value in osh.nameToEndIps.iteritems():
			print "*** EndIP", key, value
		for key, value in osh.nameToTaps.iteritems():
			print "*** Tap", key, value
		for key, value in osh.nameToVis.iteritems():
			print "*** Vi", key, value
		for key, value in osh.nameToNets.iteritems():
			print "*** Announced Net", key, value
		print "*** EndIPBase", osh.endIPBase
		print "*** TapBase", osh.tapBase
		print "*** ViBase", osh.viBase
		print "*** EthIndex", osh.ethIndex
		print "*** TapPortBase", osh.tapPortBase
		print "*** OSPFBase", osh.ospfNetBase
		print "###########################"
	print "###########################"
	for controller in testbed.ctrls:
		print "*** Ctrl", controller
	print "###########################"
	for net in testbed.ospfnets:
		print "*** Testbed OSPFNET", net

# XXX Test2 First Create a Mesh Triangular Core Network, second for each coshi create an aoshi, link them and create the Controller.
# Finally Print The Internal Object of TestBed	
def test2():
	print "*** Test2"
	testbed = TestbedOFELIA("ofelia_mapping.json", verbose=False)
	print "*** Create Core Network"
	oshis = []
	for i in range(3):
		oshi = testbed.addOshi()
		for lhs in oshis:
			l = testbed.addLink(lhs.name, oshi.name)
			print "*** Connect", lhs.name, "To",oshi.name
		oshis.append(oshi)
	print "*** Create Controllers"
	for i in range(2):
		ctrl = testbed.addController("6633")
		# l = testbed.addLink(testbed.oshs[i].name, aoshi.name)
		# print "*** Connect", testbed.oshs[i].name, "To", ctrl.name
		
	print "*** Create Access Network"   
	for i in range(3):
		aoshi = testbed.addAoshi()
		l = testbed.addLink(testbed.oshs[i].name, aoshi.name)
		print "*** Connect", testbed.oshs[i].name, "To", aoshi.name
		
	testbed.configure()

	print "###########################"
	print "*** Internal TestBed"
	print "*** NameToNode", testbed.nameToNode
	print "*** NameToOSPFNet", testbed.nameToOSPFNet
	print "*** OshiToControllers", testbed.oshiToControllers
	print "###########################"
	for osh in testbed.oshs:
		print "*** OSHI:", osh.name
		for key, value in osh.nameToEths.iteritems():
			print "*** Eth", key, value
		for key, value in osh.nameToEndIps.iteritems():
			print "*** EndIP", key, value
		for key, value in osh.nameToTaps.iteritems():
			print "*** Tap", key, value
		for key, value in osh.nameToVis.iteritems():
			print "*** Vi", key, value
		for key, value in osh.nameToNets.iteritems():
			print "*** Announced Net", key, value
		print "*** EndIPBase", osh.endIPBase
		print "*** TapBase", osh.tapBase
		print "*** ViBase", osh.viBase
		print "*** EthIndex", osh.ethIndex
		print "*** TapPortBase", osh.tapPortBase
		print "*** OSPFBase", osh.ospfNetBase
		print "###########################"
	print "###########################"
	for aos in testbed.aoss:
		print "*** AOSHI:", aos.name
		for key, value in aos.nameToEths.iteritems():
			print "*** Eth", key, value
		for key, value in aos.nameToEndIps.iteritems():
			print "*** EndIP", key, value
		for key, value in aos.nameToTaps.iteritems():
			print "*** Tap", key, value
		for key, value in aos.nameToVis.iteritems():
			print "*** Vi", key, value
		for key, value in aos.nameToNets.iteritems():
			print "*** Announced Net", key, value
		print "*** EndIPBase", aos.endIPBase
		print "*** TapBase", aos.tapBase
		print "*** ViBase", aos.viBase
		print "*** EthIndex", aos.ethIndex
		print "*** TapPortBase", aos.tapPortBase
		print "*** OSPFBase", aos.ospfNetBase
		print "###########################"
	for ctrl in testbed.ctrls:
		print "*** Ctrl", ctrl.name
		for key, value in ctrl.nameToEths.iteritems():
			print "*** Eth", key, value
		print "*** IP", ctrl.ips
		print "*** Port", ctrl.port
	print "###########################"
	for net in testbed.ospfnets:
		print "*** Testbed OSPFNET", net

if __name__ == '__main__':
	test1()
	#test2()

	

	# Cemetery of Code
	# ctrls = ['ip1:port1', 'ip2:port2', ...]
	#def setControllers(self, oshi, ctrls):
		#oshi = self.getNodeByName(oshi)
		#oshi.setControllers(ctrls)
		#self.oshiToControllers[oshi.name] = ctrls
	
	

