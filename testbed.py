#!/usr/bin/python

##############################################################################################
# Copyright (C) 2014 Pier Luigi Ventre - (Consortium GARR and University of Rome "Tor Vergata")
# Copyright (C) 2014 Giuseppe Siracusano, Stefano Salsano - (CNIT and University of Rome "Tor Vergata")
# www.garr.it - www.uniroma2.it/netgroup - www.cnit.it
#
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Testbed Class.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
# XXX Depends On Luca Prete Script

import sys
from testbed_node import Oshi, Controller, Host
from mapping_parser import MappingParserOFELIA
from testbed_deployer_utils import OSPFNetwork, IPNetAllocator
import copy
import os

class Testbed( object ):
	
	def __init__(self):
		self.user = None
		self.pwd = None
		self.nameToNode = {}	

# XXX configure() depends On Luca Prete' s Bash Script
# TODO Introduce integrity check
class TestbedOFELIA( Testbed ):

	# Init Function
	def __init__( self, path_mapping="Mapping.json", verbose=True):
		Testbed.__init__(self)
		self.parser = MappingParserOFELIA(path_mapping, verbose)
		(self.oshinfo, self.aosinfo, self.ctrlsinfo, self.euhsinfo) = self.parser.getNodesInfo()
		self.vlan = self.parser.vlan
		self.verbose = True
		self.ospfBase = 1
		self.ipNetAllocator = IPNetAllocator(self.parser.mgmtnet, self.parser.ipnet)

		self.user = self.parser.user
		self.pwd = self.parser.pwd

		self.oshs = []
		self.aoss = []
		self.euhs = []
		self.ctrls = []
		self.ospfnets = []
		
		self.nameToOSPFNet = {}
		self.oshiToControllers = {}
	
	def addOshi(self, name):
		if len(self.oshinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Oshi"
			sys.exit(-2)
		osh = self.oshinfo[0]
		osh.name = name
		self.oshinfo.remove(osh)
		oshi = Oshi(osh, self.vlan, self.parser.user, self.parser.pwd)
		self.oshs.append(oshi)
		self.nameToNode[oshi.name] = oshi
		return oshi

	def addAoshi(self, name):
		if len(self.aosinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Aoshi"
			sys.exit(-2)
		aos = self.aosinfo[0]
		aos.name = name
		self.aosinfo.remove(aos)
		aoshi = Oshi(aos, self.vlan, self.parser.user, self.parser.pwd)
		self.aoss.append(aoshi)
		self.nameToNode[aoshi.name] = aoshi
		return aoshi
	
	def addController(self, name, port):
		if len(self.ctrlsinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Controller"
			sys.exit(-2)
		ctrl = self.ctrlsinfo[0]
		ctrl.name = name
		self.ctrlsinfo.remove(ctrl)
		ctrl = Controller(ctrl, self.vlan, port, self.parser.user, self.parser.pwd)
		self.ctrls.append(ctrl)
		self.nameToNode[ctrl.name] = ctrl
		return ctrl

	def addEuh(self, name):
		if len(self.euhsinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Controller"
			sys.exit(-2)
		euh = self.euhsinfo[0]
		euh.name = name
		self.euhsinfo.remove(euh)
		euh = Host(euh, self.vlan, self.parser.user, self.parser.pwd)
		self.euhs.append(euh)
		self.nameToNode[euh.name] = euh
		return euh
		

	def getNodeByName(self, key):
		return self.nameToNode[key]
	
	# Allocation OF OVS equipment, We Use A RR Behavior;
	def roundrobinallocation(self):
		ctrl_to_allocate = []
		for ctrl in self.ctrls:
			if len(ctrl.ips) > 0:
				ctrl_to_allocate.append(ctrl)
		if len(ctrl_to_allocate) == 1:
			for osh in self.oshs:
				osh.setControllers([ctrl_to_allocate[0].ips[0]], [ctrl_to_allocate[0].port])
			for aos in self.aoss:
				aos.setControllers([ctrl_to_allocate[0].ips[0]], [ctrl_to_allocate[0].port])

		elif len(ctrl_to_allocate) >= 2:
			i = 0
			j = 0
			for osh in self.oshs:
				i = i % len(ctrl_to_allocate)
				j = (i + 1) % len(ctrl_to_allocate)
				ip_1 = ctrl_to_allocate[i].ips[0]
				ip_2 = ctrl_to_allocate[j].ips[0]
				p_1 = ctrl_to_allocate[i].port
				p_2 = ctrl_to_allocate[j].port
				osh.setControllers([ip_1, ip_2], [p_1, p_2])
				i = i + 1
			i = 0
			j = 0
			for aos in self.aoss:
				i = i % len(ctrl_to_allocate)
				j = (i + 1) % len(ctrl_to_allocate)
				ip_1 = ctrl_to_allocate[i].ips[0]
				ip_2 = ctrl_to_allocate[j].ips[0]
				p_1 = ctrl_to_allocate[i].port
				p_2 = ctrl_to_allocate[j].port
				aos.setControllers([ip_1, ip_2], [p_1, p_2])
				i = i + 1
		else:
			print "Error No Controller Added - Information Will Not Be Generated"
		
	def addPPLink(self, lhs, rhs):
		
		lhs = self.getNodeByName(lhs)	
		rhs = self.getNodeByName(rhs)

		(lhs_eth, lhs_eth_ip) = lhs.next_eth()
		(rhs_eth, rhs_eth_ip) = rhs.next_eth()
		
		
		lhs_tap_port = lhs.newTapPort()
		rhs_tap_port = rhs.newTapPort()
		
		ospf_net = self.addOSPFNet()
		lhs_ip = self.next_hostAddress(ospf_net)
		rhs_ip = self.next_hostAddress(ospf_net)
		lhs_ospf_net = copy.deepcopy(ospf_net)
		rhs_ospf_net = copy.deepcopy(ospf_net)

		(lhs_vi, lhs_tap, lhs_ospf_net) = lhs.addIntf([rhs_eth_ip, lhs_eth, lhs_tap_port, rhs_tap_port, lhs_ospf_net, lhs_ip, rhs_ip])
		(rhs_vi, rhs_tap, rhs_ospf_net) = rhs.addIntf([lhs_eth_ip, rhs_eth, rhs_tap_port, lhs_tap_port, rhs_ospf_net, rhs_ip, lhs_ip])

		return [(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)]

		
	def newOSPFNetName(self):
		
		ret = self.ospfBase
		self.ospfBase = self.ospfBase + 1
		return "NET%s" % ret
		
	def addOSPFNet(self):
		name = self.newOSPFNetName()
		net = OSPFNetwork(name, self.ipNetAllocator.next_netAddress())
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
		
		mgmtnet = (self.parser.mgmtnet.split("/"))[0]
		testbed.write("# general configuration - start\n")
		testbed.write("MGMTNET=%s\n" % mgmtnet)
		testbed.write("# general configuration - end\n")
		testbed.close()
		for key, host in self.nameToNode.iteritems():
			host.configure(self.parser.ipnet)

	#def start(self):
	#	for osh in self.oshs:
	#		osh.start()

	#def stop(self):
	#	for osh in self.oshs:
	#		osh.stop()
