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
# Usage Example Of The Testbed Deployer.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
# XXX Depends On Luca Prete Script

import argparse
import sys
from testbed import TestbedOFELIA
from testbed_cli import TestbedCLI
from topo_parser import TestbedTopoParser
import os

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# XXX VLL Pusher Param
vll_path = "" #"../vll_pusher_for_floodlights/"	


# XXX Create a Core Mesh Network, with "param" OSHI and 1 Controllers
def topo1(param):
	print "*** Test1"
	testbed = TestbedOFELIA("ofelia_mapping.map", verbose=False)
	print "*** Create Core Network"
	oshis = []
	for i in range(param):
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
	#TestbedCLI(testbed)

# XXX First Create a Core Mesh Network, second for each coshi create an aoshi, link them and create the Controller.
# Finally Print The Internal Object of TestBed	
def topo2(param):
	print "*** Test2"
	testbed = TestbedOFELIA("ofelia_mapping.map", verbose=False)
	print "*** Create Core Network"
	oshis = []
	for i in range(param):
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
	for i in range(param):
		aoshi = testbed.addAoshi("aos%s" % (i+4))
		l = testbed.addPPLink(testbed.oshs[i].name, aoshi.name)
		print "*** Connect", testbed.oshs[i].name, "To", aoshi.name
	
	print "*** Configure Testbed"	
	testbed.configure()
	#TestbedCLI(testbed)

# XXX Build Topology From topo.json generated through TopologyDesigner
def topo3(param):
	verbose = True
	if verbose:
		print "*** Build Topology From Parsed File"
	parser = TestbedTopoParser(param, verbose=True)
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
	#TestbedCLI(testbed)

# XXX Test4 Build Topology From topo.json generated through TopologyDesigner And Build Configuration File For Classification Function
# and for VLL pusher
# TODO Generation Configuration File For Classification Function
# TODO Properly Generation of testbed.sh for the VLL

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


def topo4(param):

	LHS_tunnel = ['euh2']#,'euh2', 'euh3','euh4','euh5','euh6','euh7']	
	RHS_tunnel = ['euh3']#,'euh3', 'euh4','euh5','euh6','euh7','euh1']	

	verbose = True
	if verbose:
		print "*** Build Topology From Parsed File"
	parser = TestbedTopoParser(param, verbose=False)
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
	
	print "*** Configure Testbed"
	testbed.configure()
	#TestbedCLI(testbed)

def buildTopoFromNx(topo, args):
	if topo == 'e_r':
		data = args.split(",")
		args = []
		args.append(int(data[0]))
		args.append(float(data[1]))
		if len(args) >= 2:
			if args [0] > 10 or args[1] > 1:
				print "Warning Parameter Too High For Erdos Renyi", "Nodes %s" % args[0], "Interconnection Probability %s" % args[1]
				print "Using Default Parameter"
				args[0] = 5
				args[1] = 0.8
		else :
			args[0] = 5
			args[1] = 0.8
		print "Erdos Renyi", "Nodes %s" % args[0], "Interconnection Probability %s" % args[1]
		e_r(args[0], args[1])

	print "Error NX Wrong Parameter"
	sys.exit(-2) 

def e_r(n, p):
	g = nx.erdos_renyi_graph(n,p)
	"Create An Erdos Reny Topo"
	"Creating OSHI"

	print "*** Test2"
	testbed = TestbedOFELIA("ofelia_mapping.map", verbose=False)
	print "*** Create Core Network"
	oshis = []
	for n in g.nodes():
		n = n + 1
		oshi = testbed.addOshi('osh%s' % (n))
		oshis.append(oshi)

	for (n1, n2) in g.edges():
		n1 = n1 + 1
		n2 = n2 + 1
		lhs = ('osh%s' % n1)
		rhs = ('osh%s' % n2)
		l = testbed.addPPLink(lhs, rhs)
		print "*** Connect", lhs, "To", rhs 

	print "*** Create Controllers"
	for i in range(1):
		ctrl = testbed.addController("ctrl%s" % (i+1),"6633")
		l = testbed.addPPLink(testbed.oshs[i].name, ctrl.name)
		print "*** Connect", testbed.oshs[i].name, "To", ctrl.name
		
	print "*** Create Access Network"   
	for i in range(n):
		aoshi = testbed.addAoshi("aos%s" % (i+n+1))
		l = testbed.addPPLink(testbed.oshs[i].name, aoshi.name)
		print "*** Connect", testbed.oshs[i].name, "To", aoshi.name
   
	for i in range(n):
		euh = testbed.addEuh("euh%s" % (i+1))
		l = testbed.addPPLink(testbed.aoss[i].name, euh.name)
		print "*** Connect", testbed.aoss[i].name, "To", euh.name

	# We generate the topo's png
	pos = nx.circular_layout(g)
        nx.draw(g, pos)
        plt.savefig("topo.png")

	print "*** Configure Testbed"	
	testbed.configure()
	#TestbedCLI(testbed)	

def parse_cmd_line():
	parser = argparse.ArgumentParser(description='Mininet Deployer')
	parser.add_argument('--topology', dest='topoInfo', action='store', default='topo1:3', help='Topology Info topo:param see readme for further details')
	args = parser.parse_args()	
	if len(sys.argv)==1:
    		parser.print_help()
    		sys.exit(1)
	data = args.topoInfo.split(":")	
	return (data[0], data[1])

def check_precondition():
	if vll_path == "":
		print "Error Set Environment Variable At The Beginning Of File"
		sys.exit(-2)

if __name__ == '__main__':
	check_precondition()
	(topo, param) = parse_cmd_line()
	if topo == 'topo1':
		print "*** Create Core Mesh[%s] Network" % param
		topo1(int(param))
	elif topo == 'topo2':
		print "*** Create Core Mesh[%s] Network And Simple Access" % param
		topo2(int(param))
	elif topo == 'topo3':
		print "*** Create Topology Without Services From File:", param
		topo3(param)
	elif topo == 'topo4':
		print "*** Create Topology With Services From File:", param
		topo4(param)
	else:
		print "*** Create Topology From Networkx:", topo, param
		buildTopoFromNx(topo, param)
