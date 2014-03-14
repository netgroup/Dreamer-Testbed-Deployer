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
from testbed_node import Oshi
from mapping_parser import MappingParserOFELIA
from testbed_deployer_utils import OSPFNetwork
import copy

# XXX configure() depends On Luca Prete' s Bash Script
# TODO Introduce integrity check
class TestbedOFELIA( object ):

	# Init Function
	def __init__( self, path_mapping="Mapping.json", verbose=True):

		self.parser = MappingParserOFELIA(path_mapping, verbose)
		(self.oshinfo, self.aosinfo, self.euhsinfo) = self.parser.getNodesInfo()
		self.vlan = self.parser.vlan
		self.verbose = True
		self.ospfBase = 1

		self.oshs = []
		self.aoss = []
		self.euhs = []
		self.controllers = []
		self.ospfnets = []

		self.nameToNode = {}
		self.nameToOSPFNet = {}
		self.oshiToControllers = {}
	
	def addOshi(self):
		if len(self.oshinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Topology"
			sys.exit(-2)
		if self.verbose:
			print "Add Oshi %s" % self.oshinfo[0].name
		osh = self.oshinfo[0]
		self.oshinfo.remove(osh)
		oshi = Oshi(osh, self.vlan)
		self.oshs.append(oshi)
		self.nameToNode[oshi.name] = oshi
		return oshi

	def addAoshi(self):
		if self.verbose:
			print "Add Aoshi %s" % self.aosinfo[0].name

	def addEuh(self):
		if self.verbose:
			print "Add Euh %s" % self.euhsinfo[0].name

	def getNodeByName(self, key):
		if self.verbose:
			print "Retrieve Node %s" % key
		return self.nameToNode[key]
	
	# TODO Integrity Check of ctrls
	# ctrls = ['ip1:port1', 'ip2:port2', ...]
	def setController(oshi, ctrls):
		if self.verbose:
			print "Set For %s The Controllers %s" % (oshi, ctrls)
		oshi = self.getNodeByName(oshi)
		oshi.setController(ctrls)
		self.oshiToControllers[oshi.name] = ctrls
	
	# XXX Attenzione se sono host fare addHostLink(oshi, host) e controllo se lhs e' oshi
	# TODO Check is lhs is (oshi or aoshi) and rhs is (oshi or aoshi)
	def addLink(self, lhs, rhs):
		if self.verbose:
			print "Add Link (%s, %s)" %(lhs, rhs)
		lhs = self.getNodeByName(lhs)	
		rhs = self.getNodeByName(rhs)

		(lhs_eth, lhs_eth_ip) = lhs.next_eth()
		(rhs_eth, rhs_eth_ip) = rhs.next_eth()
		lhs_endip = lhs.addEndIP(rhs_eth_ip, lhs_eth)
		rhs_endip = rhs_addEndIp(lhs_eth_ip, rhs_eth)
		lhs_tap_port = lhs.newTapPort()
		rhs_tap_port = rhs.newTapPort()
		lhs_tap = lhs.addTap(lhs_tap_port, rhs_tap_port, lhs_endip.name)
		rhs_tap = rhs.addTap(rhs_tap_port, lhs_tap_port, rhs_endip.name)

		ospf_net = self.addOSPFNet(self, isCtrlLink=False)
		lhs_ip = self.next_hostAddress(ospf_net)
		rhs_ip = self.next_hostAddress(ospf_net)
		lhs_ospf_name = lhs.newOSPFNetName()
		rhs_ospf_name = rhs.newOSPFNetName()
		lhs_ospf_net = copy.deepcopy(ospf_net)
		lhs_ospf_net.name = lhs_ospf_name
		lhs.addOSPFNet(lhs_ospf_net)
		rhs_ospf_net = copy.deepcopy(ospf_net)
		rhs_ospf_net.name = rhs_ospf_name
		rhs.addOSPFNet(rhs_ospf_net)
		lhs_vi = lhs.addVi(lhs_ip, lhs_ospf_net.netbitOSPF, lsh_ospf_net.hello_int, lhs_ospf_net.cost)
		rhs_vi = rhs.addVi(rhs_ip, rhs_ospf_net.netbitOSPF, rhs_ospf_net.hello_int, rhs_ospf_net.cost)
		
	
	def newOSPFNetName(self):
		if self.verbose:
			print "Creating New OSPFNet %s" % s
		ret = self.ospfBase
		self.ospfBase = self.ospfBase + 1
		return ret
		
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
	
	def configure():
		for osh in self.oshs:
			osh.configure()

	#def start():

	#def stop():

if __name__ == '__main__':
	"""testbed = TestbedOFELIA("ofelia_mapping.json", verbose=False)
	testbed.addOshi()
	osh = testbed.getNodeByName('osh1')
	print osh.name, osh.mgt_ip, osh.loopback, osh.vlan
	for eth in osh.eths:
		print eth.name, eth.ip + "/" + str(eth.netbit), eth.serialize()
	testbed.addOshi()
	osh2 = testbed.getNodeByName('osh2')
	print osh2.name, osh2.mgt_ip, osh2.loopback, osh2.vlan
	for eth in osh2.eths:
		print eth.name, eth.ip + "/" + str(eth.netbit), eth.serialize()
	"""
	ctrls = ['ip port', 'ip port', 'ip port']
	i = 1
	names = []
	serialized_line = ""
	for ctrl in ctrls:
		name = "ctrl" + str(i)
		names.append(name)
		serialized_line = serialized_line + ("declare -a %s=(%s)\n" %(name, ctrl))			
		i = i + 1			
	ret = "declare -a CTRL=(" + " ".join(names) + ")\n" + serialized_line
	print (ret),


