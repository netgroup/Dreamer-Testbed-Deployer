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
# Testbed Deployer.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
# XXX Depends On Dreamer-Setup-Script

import argparse
import sys
import os

parser_path = "" #"../Dreamer-Topology-Parser-and-Validator/"
if parser_path == "":
	print "Error Set Environment Variable At The Beginning Of File"
	sys.exit(-2)

sys.path.append(parser_path)
from topo_parser import TopoParser

from testbed import *
from testbed_cli import TestbedCLI
from coexistence_mechanisms import *
from ingress_classification import *
from testbed_deployer_utils import *

# XXX Build Topology From topo.json generated through TopologyDesigner And Build Configuration File For Classification Function
# and for VLL pusher	
def topo(topology, testbed):

	verbose = True
	if verbose:
		print "*** Build Topology From Parsed File"
	parser = TopoParser(topology, verbose = False)
	(ppsubnets, l2subnets) = parser.getsubnets()
	vlls = parser.getVLLs()
	# XXX
	if parser.autogenerated == False:
		if verbose:
			print "*** No Autogenerated"

		generator = PropertiesGenerator(testbed)
		if verbose:
			print "*** Build Vertices Properties"
			oshis_properties = generator.getVerticesProperties(parser.oshis)
			aoshis_properties = generator.getVerticesProperties(parser.aoshis)
			l2sws_properties = generator.getVerticesProperties(parser.l2sws)
			euhs_properties = generator.getVerticesProperties(parser.euhs)

		if verbose:
			print "*** Build Point-To-Point Links Properties"
		pp_properties = []
		for ppsubnet in ppsubnets:
			pp_properties.append(generator.getLinksProperties(ppsubnet.links))
		
		if verbose:
			print "*** Build Switched Links Properties"
		l2_properties = []
		for l2subnet in l2subnets:
			l2_properties.append(generator.getLinksProperties(l2subnet.links))

		if verbose:
			print "*** Build VLLs Properties"
		vlls_properties = []
		for vll in vlls:
			vlls_properties.append(generator.getVLLsProperties(vll))
			

	set_oshis = parser.oshis
	set_aoshis = parser.aoshis
	set_l2sws = parser.l2sws
	set_euhs = parser.euhs

	factory = TestbedFactory(verbose)
	testbed = factory.getTestbedOSHI(testbed, parser.tunneling)

	if verbose:
		print "*** Build OSHI"
	i = 0	
	for oshi in set_oshis:
		testbed.addOshi(oshi, oshis_properties[i])
		if verbose:
			print "*** %s - %s" %(oshi, oshis_properties[i])
		i = i + 1

	if verbose:
		print "*** Build AOSHI"
	i = 0
	for aoshi in set_aoshis:
		testbed.addAoshi(aoshi, aoshis_properties[i])
		if verbose:
			print "*** %s - %s" %(aoshi, aoshis_properties[i])	
		i = i + 1

	if verbose:
		print "*** Build L2Switch"
	i = 0
	for l2switch in set_l2sws:
		testbed.addL2Switch(l2switch)	
		i = i + 1

	if verbose:
		print "*** Build CONTROLLER"
	ctrl = testbed.addController("ctrl1", 6633)	
	coex = CoexA(1)
	testbed.addCoexistenceMechanism(coex)
	linkproperties = generator.getLinksProperties((oshi, ctrl.name))
	[(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)] = testbed.addLink(oshi, ctrl.name, linkproperties[0])
	ingress = IngrB(coex, lhs_tap, lhs_vi)
	testbed.addIngressClassification(ctrl.name, oshi, ingress)
	if verbose:			
		print "*** Connect", ctrl.name, "To", oshi

	if verbose:
		print "*** Build CONTROLLER2"
	ctrl2 = testbed.addController("ctrl2", 6633)	
	oshi2 = set_oshis[0]
	linkproperties = generator.getLinksProperties((oshi2, ctrl2.name))
	[(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)] = testbed.addLink(oshi2, ctrl2.name, linkproperties[0])
	ingress2 = IngrB(coex, lhs_tap, lhs_vi)
	testbed.addIngressClassification(ctrl2.name, oshi2, ingress2)
	if verbose:			
		print "*** Connect", ctrl2.name, "To", oshi2

	if verbose:
		print "*** Build EUHS"
	for euh in set_euhs:
		testbed.addEuh(euh)

	if verbose:	
		print "*** Create Networks Point To Point"
	i = 0
	for ppsubnet in ppsubnets:
			links = ppsubnet.links
			if verbose:
				print "*** Subnet: Node %s - Links %s" %(ppsubnet.nodes, links)
			node1 = links[0][0]
			node2 = links[0][1]
			[(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)] = testbed.addLink(node1, node2, pp_properties[i][0])
			if verbose:			
				print "*** Connect", node1, "To", node2
				print "*** Link Properties", pp_properties[i][0]
			i = i + 1

	if verbose:	
		print "*** Create Switched Networks"
	j = 0
	for l2subnet in l2subnets:
			links = l2subnet.links
			if verbose:
					print "*** Subnet: Node %s - Links %s" %(l2subnet.nodes, links)
			i = 0
			for link in links:
				node1 = link[0]
				node2 = link[1]
				[(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)] = testbed.addLink(node1, node2, l2_properties[j][i])
				if verbose:			
					print "*** Connect", node1, "To", node2
					print "*** Link Properties", l2_properties[j][i]
				i = i + 1
			j = j + 1

	i = 0
	for vll in vlls:
		testbed.addVLL(vll[0], vll[1], vlls_properties[i])
		if verbose:			
			print "*** VLLs Properties", vlls_properties[i]
		i = i + 1	
	print "*** Generate testbed.sh"
	testbed.configure()
	print "*** Generate LME rules"
	testbed.generateLMErules()
	print "*** Generate VLL pusher cfg"
	testbed.generateVLLCfg()
	print "*** Generate management.sh"
	testbed.configureMGMT()

def parse_cmd_line():
	parser = argparse.ArgumentParser(description='Testbed Deployer')
	parser.add_argument('--topology', dest='topoInfo', action='store', default='topo:topo1.json', help='topo:param see README for further details')
	parser.add_argument('--testbed', dest='testbedInfo', action='store', default='testbed:OFELIA', help='testbed:param see README for further details')
	args = parser.parse_args()	
	if len(sys.argv)==1:
    		parser.print_help()
    		sys.exit(1)
	topo_data = args.topoInfo	
	testbed_data = args.testbedInfo
	return (topo_data, testbed_data)

if __name__ == '__main__':
	(topology, testbed) = parse_cmd_line()
	topo(topology, testbed)
