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
from testbed_cli import TestbedCLI
from topo_parser import TestbedTopoParser
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

	def start(self):
		for osh in self.oshs:
			osh.start()

	def stop(self):
		for osh in self.oshs:
			osh.stop()

# XXX Test1 Create a Mesh Triangular Network, with 3 OSHI and 1 Controllers And Print The Internal Object of TestBed
def test1():
	print "*** Test1"
	testbed = TestbedOFELIA("ofelia_mapping.map", verbose=False)
	print "*** Create Core Networks"
	oshis = []
	for i in range(3):
		oshi = testbed.addOshi("osh%s" % (i+1))
		
		oshis.append(oshi)
	i = 0

	for i in range(0, len(oshis)-1):
		for j in range(i + 1, len(oshis)):
			l = testbed.addPPLink(oshis[i].name, oshis[j].name)
			print "*** Connect", oshis[i].name, "To", oshis[j].name 
	
	print "*** Create Controllers"
	ctrl = testbed.addController('ctrl1', 6633)
	testbed.addPPLink(oshis[0].name, ctrl.name)

	print "*** Configure Testbed"
	testbed.configure()
	TestbedCLI(testbed)

# XXX Test2 First Create a Mesh Triangular Core Network, second for each coshi create an aoshi, link them and create the Controller.
# Finally Print The Internal Object of TestBed	
def test2():
	print "*** Test2"
	testbed = TestbedOFELIA("ofelia_mapping.map", verbose=False)
	print "*** Create Core Network"
	oshis = []
	for i in range(3):
		oshi = testbed.addOshi("osh%s" % (i+1))
		for lhs in oshis:
			l = testbed.addPPLink(lhs.name, oshi.name)
			print "*** Connect", lhs.name, "To",oshi.name
		oshis.append(oshi)
	print "*** Create Controllers"
	for i in range(1):
		ctrl = testbed.addController("ctrl%s" % (i+1),"6633")
		l = testbed.addPPLink(testbed.oshs[i].name, ctrl.name)
		print "*** Connect", testbed.oshs[i].name, "To", ctrl.name
		
	print "*** Create Access Network"   
	for i in range(3):
		aoshi = testbed.addAoshi("aos%s" % (i+4))
		l = testbed.addPPLink(testbed.oshs[i].name, aoshi.name)
		print "*** Connect", testbed.oshs[i].name, "To", aoshi.name
	
	print "*** Configure Testbed"	
	testbed.configure()
	TestbedCLI(testbed)

# XXX Test3 Build Topology From topo.json generated through TopologyDesigner
def test3():
	verbose = True
	if verbose:
		print "*** Build Topology From Parsed File"
	parser = TestbedTopoParser("topo5.json", verbose=True)
	(ppsubnets, l2subnets) = parser.getsubnets()
	set_oshis = parser.oshis
	set_aoshis = parser.aoshis
	set_l2sws = parser.l2sws
	set_euhs = parser.euhs
	testbed = TestbedOFELIA("ofelia_mapping.map", verbose = False)
	if verbose:
		print "*** Build OSHI"	
	for oshi in set_oshis:
		testbed.addOshi(oshi)
	if verbose:
		print "*** Build AOSHI"
	for aoshi in set_aoshis:
		testbed.addAoshi(aoshi)

	print "*** Build CONTROLLER"
	ctrl = testbed.addController("ctrl1", 6633)
	testbed.addPPLink(oshi, ctrl.name)

	if verbose:
		print "*** Build EUHS"
	for euh in set_euhs:
		testbed.addEuh(euh)	

	if verbose:	
		print "*** Create Core Networks Point To Point"
	i = 0
	for ppsubnet in ppsubnets:
		if ppsubnet.type == "CORE":
			links = ppsubnet.getOrderedLinks()
			if verbose:
				print "*** Subnet: Node %s - Links %s" %(ppsubnet.nodes, links)
			node1 = links[0][0]
			node2 = links[0][1]
			l = testbed.addPPLink(node1, node2)
			if verbose:			
				print "*** Connect", node1, "To", node2
		i = i + 1
	if verbose:	
		print "*** Create Access Networks Point To Point"
	i = 0
	for ppsubnet in ppsubnets:
		if ppsubnet.type == "ACCESS":
			links = ppsubnet.getOrderedLinks()
			if verbose:
				print "*** Subnet: Node %s - Links %s" %(ppsubnet.nodes, links)
			node1 = links[0][0]
			node2 = links[0][1]
			l = testbed.addPPLink(node1, node2)
			if verbose:			
				print "*** Connect", node1, "To", node2
		i = i + 1

	print "*** Configure Testbed"
	testbed.configure()
	TestbedCLI(testbed)

# XXX Test4 Build Topology From topo.json generated through TopologyDesigner And Build Configuration File For Classification Function
# and for VLL pusher

def conf_flows_ingress_egress_no_vlan_approach(oshi, i, intf):
	if CORE_APPROACH == 'B':
		print "*** Already Done Same Approach Between Core And Access"
	elif CORE_APPROACH == 'A':
		print "*** Add Rule For No Vlan Access Approach"
		VLAN_IP = 1 # Core Vlan	
		eth_intf = intf
		eth_port_number = convert_port_name_to_number(oshi.name, eth_intf)
		vi_intf = "vi%s" % strip_number(eth_intf)
		vi_port_number = convert_port_name_to_number(oshi.name, vi_intf)
		oshi.cmd("ovs-ofctl del-flows br-%s in_port=%s,dl_vlan=%s" % (oshi.name,eth_port_number,VLAN_IP))
		oshi.cmd("ovs-ofctl add-flow br-%s hard_timeout=0,priority=300,in_port=%s,dl_vlan=%s,actions=mod_vlan_vid:%s,output:%s" % (oshi.name,eth_port_number,"0xffff",VLAN_IP,vi_port_number))
		oshi.cmd("ovs-ofctl add-flow br-%s hard_timeout=0,priority=300,in_port=%s,dl_vlan=%s,actions=strip_vlan,output:%s" % (oshi.name,vi_port_number,VLAN_IP,eth_port_number)) 


def conf_flows_vlan_approach(oshi, eth_ports, vi_ports):
	print "*** Configuring Flows Classifier A For", oshi
	VLAN_IP = 1
	size = len(eth_ports)
	i = 0
	for i in range(size):
		oshi.cmd("ovs-ofctl add-flow br-" + oshi.name + " hard_timeout=0,priority=300,in_port=" + str(eth_ports[i])
		+ ",dl_vlan=" + str(VLAN_IP) + ",action=output:" + str(vi_ports[i]))
		oshi.cmd("ovs-ofctl add-flow br-" + oshi.name + " hard_timeout=0,priority=300,in_port=" + str(vi_ports[i])
		+ ",dl_vlan=" + str(VLAN_IP) + ",action=output:" + str(eth_ports[i]))
	oshi.cmd("ovs-ofctl add-flow br-" + oshi.name + " hard_timeout=0,priority=400,dl_type=0x88cc,action=controller")
	oshi.cmd("ovs-ofctl add-flow br-" + oshi.name + " hard_timeout=0,priority=400,dl_type=0x8942,action=controller")

def conf_flow_no_vlan_approach(oshi, eth_ports, vi_ports):
	print "*** Configuring Flows Classifier B For", oshi	
	size = len(eth_ports)
	i = 0
	oshi.cmd("ovs-ofctl add-flow br-" + oshi.name + " \"table=0,hard_timeout=0,priority=300,dl_vlan=0xffff,actions=resubmit(,1)\"")
	for i in range(size):
		oshi.cmd("ovs-ofctl add-flow br-" + oshi.name + " \"table=1,hard_timeout=0,priority=300,in_port=" + str(eth_ports[i])
		+ ",action=output:" + str(vi_ports[i]) + "\"")
		oshi.cmd("ovs-ofctl add-flow br-" + oshi.name + " \"table=1,hard_timeout=0,priority=300,in_port=" + str(vi_ports[i])
		+ ",action=output:" + str(eth_ports[i]) + "\"")
	oshi.cmd("ovs-ofctl add-flow br-" + oshi.name + " \"table=1,hard_timeout=0,priority=400,dl_type=0x88cc,action=controller\"")
	oshi.cmd("ovs-ofctl add-flow br-" + oshi.name + " \"table=1,hard_timeout=0,priority=400,dl_type=0x8942,action=controller\"")


def test4():

	LHS_tunnel = ['euh2']#,'euh2', 'euh3','euh4','euh5','euh6','euh7']	
	RHS_tunnel = ['euh3']#,'euh3', 'euh4','euh5','euh6','euh7','euh1']	

	verbose = True
	if verbose:
		print "*** Build Topology From Parsed File"
	parser = TestbedTopoParser("topo5.json", verbose=False)
	(ppsubnets, l2subnets) = parser.getsubnets()
	set_oshis = parser.oshis
	set_aoshis = parser.aoshis
	set_l2sws = parser.l2sws
	set_euhs = parser.euhs
	testbed = TestbedOFELIA("ofelia_mapping.map", verbose = False)
	if verbose:
		print "*** Build OSHI"	
	for oshi in set_oshis:
		testbed.addOshi(oshi)
	if verbose:
		print "*** Build AOSHI"
	for aoshi in set_aoshis:
		testbed.addAoshi(aoshi)	
	if verbose:
		print "*** Build CONTROLLER"
	ctrl = testbed.addController("ctrl1", 6633)
	testbed.addPPLink(oshi, ctrl.name)

	if verbose:
		print "*** Build EUHS"
	for euh in set_euhs:
		testbed.addEuh(euh)

	for i in range(0,len(LHS_tunnel)):
		host1 = LHS_tunnel[i]
		host2 = RHS_tunnel[i]
		if host1 not in set_euhs or host2 not in set_euhs:
			print "Error Misconfiguration Virtual Leased Line"
			print "Error Cannot Connect", host1, "To", host2
			sys.exit(2)
	

	if verbose:	
		print "*** Create Core Networks Point To Point"
	i = 0
	for ppsubnet in ppsubnets:
		if ppsubnet.type == "CORE":
			links = ppsubnet.getOrderedLinks()
			if verbose:
				print "*** Subnet: Node %s - Links %s" %(ppsubnet.nodes, links)
			node1 = links[0][0]
			node2 = links[0][1]
			l = testbed.addPPLink(node1, node2)
			if verbose:			
				print "*** Connect", node1, "To", node2
		i = i + 1
	if verbose:	
		print "*** Create Access Networks Point To Point"

	dpid_to_access_tap = {}
	host_to_aos = {}		
	default = ""

	i = 0
	for ppsubnet in ppsubnets:
		if ppsubnet.type == "ACCESS":
			links = ppsubnet.getOrderedLinks()
			for link in links:
				if verbose:
					print "*** Subnet: Node %s - Links %s" %(ppsubnet.nodes, links)
				node1 = link[0]
				node2 = link[1]
				[(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)] = testbed.addPPLink(node1, node2)
				if 'aos' in node1:
					intfs = dpid_to_access_tap.get(node1, default).split(",")
					if lhs_tap.name not in intfs:
						dpid_to_access_tap[node1] = dpid_to_access_tap.get(node1, default) + lhs_tap.name + ","
					if 'euh' in node2:
						host_to_aos[node2] = node1
					else:
						print "Errore Node2 Non e' host"
					 			
				elif 'aos' in node2:
					intfs = dpid_to_access_tap.get(node2, default).split(",")
					if rhs_tap.name not in intfs:
						dpid_to_access_tap[node2] = dpid_to_access_tap.get(node2, default) + rhs_tap.name + ","				
					if 'euh' in node1:
						host_to_aos[node1] = node2
					else:
						print "Errore Node2 Non e' host"
				if verbose:			
					print "*** Connect", node1, "To", node2
		i = i + 1

	print dpid_to_access_tap
	print host_to_aos

	"""CORE_APPROACH = "A"

	class_path = "./"
	print "*** Create Configuration File For Classification Function"
	path = class_path + "classifier.cfg"
	classifier_cfg = open(path,"w")		
		
	for osh in testbed.oshs:
		classifier_cfg.write("# %s - start" % osh.mgt_ip)
		if CORE_APPROACH == "A":
			conf_flows_vlan_approach(osh, classifier_cfg):
		else:
			conf_flows_no_vlan_approach(osh, classifier_cfg):

	for aos in testbed.aoss:
		if CORE_APPROACH == "A":
			conf_flows_vlan_approach(aos, classifier_cfg):
		else:
			conf_flows_no_vlan_approach(aos, classifier_cfg):
	"""		


	vll_path = "../sdn_controller_app/vll_pusher_for_floodlights/"	
	path = vll_path + "vlls.json"
	if(os.path.exists(path)):
		print "*** Remove Vlls DB File"
		os.remove(path)

	print "*** Create Configuration File For Vll Pusher"
	path = vll_path + "vll_pusher.cfg"
	vll_pusher_cfg = open(path,"w")	

	for i in range(0, len(LHS_tunnel)):
		host = LHS_tunnel[i]
		lhs_aos = host_to_aos[host]	
		[(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)] = testbed.addPPLink(host, lhs_aos)
		lhs_port = (rhs_tap.name)
		host = RHS_tunnel[i]
		rhs_aos = host_to_aos[RHS_tunnel[i]]	
		[(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)] = testbed.addPPLink(host, rhs_aos)
		rhs_port = (rhs_tap.name)
		vll_pusher_cfg.write("%s|%s|%s|%s|%d|%d|\n" % (lhs_aos, rhs_aos, lhs_port, rhs_port, 0, 0))

	vll_pusher_cfg.close()

	testbed.configure()


	

if __name__ == '__main__':
	#test1()
	#test2()
	#test3()
	test4()
