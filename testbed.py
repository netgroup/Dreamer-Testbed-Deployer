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
from testbed_node import *
from mapping_parser import *
from testbed_deployer_utils import *
from ingress_classification import *
import copy
import os

class Testbed(object):

	def __init__(self):
		self.user = None
		self.pwd = None
		self.nameToNode = {}
		self.tunneling = None
		self.vniBase = 1

	def getNodeByName(self, key):
		return self.nameToNode[key]

	def newVNI(self):
		ret = self.vniBase
		self.vniBase = self.vniBase + 1
		return ret

class TestbedRouter(Testbed):
	
	def __init__(self):
		Testbed.__init__(self)
		self.routs = []
		self.l2sws = []
		self.euhs = []
		self.ospfnets = []
		self.routerinfo = []
		self.euhsinfo = []
		self.l2swinfo = []
		self.ospfBase = 1
		self.nameToOSPFNet = {}

	def addRouter(self, name, nodeproperties):
		if len(self.routerinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Router"
			sys.exit(-2)
		rou = self.routerinfo[0]
		rou.name = name
		self.routerinfo.remove(rou)
		router = Router(rou, self.vlan, self.user, self.pwd, self.tunneling, nodeproperties.loopback)
		self.routs.append(router)
		self.nameToNode[router.name] = router
		return router

	def addL2Switch(self, name):
		if len(self.l2swsinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of L2Sw"
			sys.exit(-2)
		l2sw = self.l2swsinfo[0]
		l2sw.name = name
		self.l2swsinfo.remove(l2sw)
		l2switch = L2Switch(l2sw, self.vlan, self.user, self.pwd, self.tunneling)
		self.l2sws.append(l2switch)
		self.nameToNode[l2switch.name] = l2switch
		return l2switch

	def addEuh(self, name):
		if len(self.euhsinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Host"
			sys.exit(-2)
		euh = self.euhsinfo[0]
		euh.name = name
		self.euhsinfo.remove(euh)
		euh = Host(euh, self.vlan, self.user, self.pwd, self.tunneling)
		self.euhs.append(euh)
		self.nameToNode[euh.name] = euh
		return euh

	def addLink(self, lhs, rhs, linkproperty):
		
		lhs = self.getNodeByName(lhs)	
		rhs = self.getNodeByName(rhs)
	

		(lhs_eth, lhs_eth_ip) = lhs.next_eth()
		(rhs_eth, rhs_eth_ip) = rhs.next_eth()
		
		
		lhs_tap_port = lhs.newTapPort()
		rhs_tap_port = rhs.newTapPort()

		ospf_net = self.addOSPFNet(linkproperty.net)
		lhs_ip = linkproperty.ipLHS
		rhs_ip = linkproperty.ipRHS
		lhs_ospf_net = copy.deepcopy(ospf_net)
		rhs_ospf_net = copy.deepcopy(ospf_net)
		vni = self.newVNI()

		(lhs_vi, lhs_tap, lhs_ospf_net) = lhs.addIntf([rhs_eth_ip, lhs_eth, lhs_tap_port, rhs_tap_port, lhs_ospf_net, lhs_ip, rhs_ip, vni])
		(rhs_vi, rhs_tap, rhs_ospf_net) = rhs.addIntf([lhs_eth_ip, rhs_eth, rhs_tap_port, lhs_tap_port, rhs_ospf_net, rhs_ip, lhs_ip, vni])
		
		return [(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)]

	def newOSPFNetName(self):
		ret = self.ospfBase
		self.ospfBase = self.ospfBase + 1
		return "NET%s" % ret
		
	def addOSPFNet(self, ip):
		found = False
		for ospfnet in self.ospfnets:
			if ip == ospfnet.net:
				found = True
				break
		if found == False:
			name = self.newOSPFNetName()
			net = OSPFNetwork(name, ip)
			self.ospfnets.append(net)
			self.nameToOSPFNet[name] = net
		else:
			net = ospfnet 
		return net

	def generateMGMTCfg(self):
		header =open('headerMGMT.txt','r')
		management = open('management.sh','w')
		lines = header.readlines()
		for line in lines:
			management.write(line)
		management.write("declare -a DSH_GROUPS=(ROUTER EUH L2SW)\n")
		router = "declare -a ROUTER=(" + " ".join("%s" % rout.mgt_ip for rout in self.routs)+ ")\n"
		euh = "declare -a EUH=(" + " ".join("%s" % euh.mgt_ip for euh in self.euhs) + ")\n"
		l2sw = "declare -a L2SW=(" + " ".join("%s" % l2sw.mgt_ip for l2sw in self.l2sws) + ")\n"
		machine = "declare -a NODE_LIST=(" + " ".join("%s" % node.mgt_ip for name, node in self.nameToNode.iteritems()) + ")\n"	
		management.write(router)
		management.write(euh)
		management.write(l2sw)
		management.write(machine)

class TestbedOSHI( Testbed ):
	
	def __init__(self):
		Testbed.__init__(self)
		self.oshs = []
		self.aoss = []
		self.euhs = []
		self.ctrls = []
		self.l2sws = []
		self.ospfnets = []
		self.coex = None
		self.aosinfo = []
		self.oshinfo = []
		self.ctrlsinfo = []
		self.euhsinfo = []
		self.l2swsinfo = []
		self.nameToOSPFNet = {}
		self.oshiToControllers = {}
		self.euhToAOS = {}
		self.vllcfgline = []
		self.ospfBase = 1

	def addOshi(self, name, nodeproperties):
		if len(self.oshinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Oshi"
			sys.exit(-2)
		osh = self.oshinfo[0]
		osh.name = name
		self.oshinfo.remove(osh)
		oshi = Oshi(osh, self.vlan, self.user, self.pwd, self.tunneling, nodeproperties.loopback)
		self.oshs.append(oshi)
		self.nameToNode[oshi.name] = oshi
		return oshi

	def addAoshi(self, name, nodeproperties):
		if len(self.aosinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Aoshi"
			sys.exit(-2)
		aos = self.aosinfo[0]
		aos.name = name
		self.aosinfo.remove(aos)
		aoshi = Oshi(aos, self.vlan, self.user, self.pwd, self.tunneling, nodeproperties.loopback)
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
		ctrl = Controller(ctrl, self.vlan, port, self.user, self.pwd, self.tunneling)
		self.ctrls.append(ctrl)
		self.nameToNode[ctrl.name] = ctrl
		return ctrl

	def addEuh(self, name):
		if len(self.euhsinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Host"
			sys.exit(-2)
		euh = self.euhsinfo[0]
		euh.name = name
		self.euhsinfo.remove(euh)
		euh = Host(euh, self.vlan, self.user, self.pwd, self.tunneling)
		self.euhs.append(euh)
		self.nameToNode[euh.name] = euh
		return euh

	def addL2Switch(self, name):
		if len(self.l2swsinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of L2Sw"
			sys.exit(-2)
		l2sw = self.l2swsinfo[0]
		l2sw.name = name
		self.l2swsinfo.remove(l2sw)
		l2switch = L2Switch(l2sw, self.vlan, self.user, self.pwd, self.tunneling)
		self.l2sws.append(l2switch)
		self.nameToNode[l2switch.name] = l2switch
		return l2switch
		
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
			print "Warning No Controller Added - Information Will Not Be Generated"
		
	def addLink(self, lhs, rhs, linkproperties):
		
		lhs = self.getNodeByName(lhs)	
		rhs = self.getNodeByName(rhs)
	

		(lhs_eth, lhs_eth_ip) = lhs.next_eth()
		(rhs_eth, rhs_eth_ip) = rhs.next_eth()
		
		
		lhs_tap_port = lhs.newTapPort()
		rhs_tap_port = rhs.newTapPort()
		
		ospf_net = self.addOSPFNet(linkproperties.net)
		lhs_ip = linkproperties.ipLHS
		rhs_ip = linkproperties.ipRHS
		lhs_ospf_net = copy.deepcopy(ospf_net)
		rhs_ospf_net = copy.deepcopy(ospf_net)
		vni = self.newVNI()

		(lhs_vi, lhs_tap, lhs_ospf_net) = lhs.addIntf([rhs_eth_ip, lhs_eth, lhs_tap_port, rhs_tap_port, lhs_ospf_net, lhs_ip, rhs_ip, vni])
		(rhs_vi, rhs_tap, rhs_ospf_net) = rhs.addIntf([lhs_eth_ip, rhs_eth, rhs_tap_port, lhs_tap_port, rhs_ospf_net, rhs_ip, lhs_ip, vni])
		
		if ('aos' in lhs.name or 'aos' in rhs.name) and ('euh' in lhs.name or 'euh' in rhs.name):
			if 'aos' in lhs.name:
				AOS = lhs.name
				EUH = rhs.name
				ingress = self.getIngress(linkproperties.ingrType, lhs_tap, lhs_vi, linkproperties.ingrData)
			else:
				AOS = rhs.name
				EUH = lhs.name
				ingress = self.getIngress(linkproperties.ingrType, rhs_tap, rhs_vi, linkproperties.ingrData)
			self.euhToAOS[EUH] = AOS
			self.addIngressClassification(EUH, AOS, ingress)

		return [(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)]

	def getIngress(self, typeof, tap, vi, params):
			if typeof == "INGRB":
				return IngrB(self.coex, tap, vi)

	def addVLL(self, lhs_euh, rhs_euh, vllproperties):

		lhs_aos = self.euhToAOS[lhs_euh]
		rhs_aos = self.euhToAOS[rhs_euh]
	
		lhs_euh = self.getNodeByName(lhs_euh)	
		rhs_euh = self.getNodeByName(rhs_euh)
		lhs_aos = self.getNodeByName(lhs_aos)	
		rhs_aos = self.getNodeByName(rhs_aos)

		(lhs_euh_eth, lhs_euh_eth_ip) = lhs_euh.next_eth()
		(lhs_aos_eth, lhs_aos_eth_ip) = lhs_aos.next_eth()
		
		
		lhs_euh_tap_port = lhs_euh.newTapPort()
		lhs_aos_tap_port = lhs_aos.newTapPort()
		

		lhs_euh_ospf_net = self.addOSPFNet(vllproperties.net)
		lhs_euh_ip = vllproperties.ipLHS
		lhs_aos_ip = "0.0.0.0"
		vni = self.newVNI()
			
				
		
		(lhs_euh_vi, lhs_euh_tap, temp) = lhs_euh.addIntf([lhs_aos_eth_ip, lhs_euh_eth, lhs_euh_tap_port, lhs_aos_tap_port, lhs_euh_ospf_net, lhs_euh_ip, lhs_aos_ip, vni])
		(lhs_aos_vi, lhs_aos_tap, lhs_aos_ospf_net) = lhs_aos.addIntf([lhs_euh_eth_ip, lhs_aos_eth, lhs_aos_tap_port, lhs_euh_tap_port, None, lhs_aos_ip, lhs_euh_ip, vni])

		(rhs_euh_eth, rhs_euh_eth_ip) = rhs_euh.next_eth()
		(rhs_aos_eth, rhs_aos_eth_ip) = rhs_aos.next_eth()
		
		
		rhs_euh_tap_port = rhs_euh.newTapPort()
		rhs_aos_tap_port = rhs_aos.newTapPort()

		rhs_euh_ospf_net = copy.deepcopy(lhs_euh_ospf_net)
		rhs_euh_ip = vllproperties.ipRHS
		rhs_aos_ip = "0.0.0.0"
		vni = self.newVNI()

		(rhs_euh_vi, rhs_euh_tap, temp) = rhs_euh.addIntf([rhs_aos_eth_ip, rhs_euh_eth, rhs_euh_tap_port, rhs_aos_tap_port, rhs_euh_ospf_net, rhs_euh_ip, rhs_aos_ip, vni])
		(rhs_aos_vi, rhs_aos_tap, rhs_aos_ospf_net) = rhs_aos.addIntf([rhs_euh_eth_ip, rhs_aos_eth, rhs_aos_tap_port, rhs_euh_tap_port, None, rhs_aos_ip, rhs_euh_ip, vni])

		self.addLineToCFG(lhs_aos.dpid, lhs_aos_tap, rhs_aos.dpid, rhs_aos_tap)

	def addLineToCFG(self, lhs_dpid, lhs_tap, rhs_dpid, rhs_tap):
		lhs_dpid = ':'.join(s.encode('hex') for s in lhs_dpid.decode('hex'))
		rhs_dpid = ':'.join(s.encode('hex') for s in rhs_dpid.decode('hex'))
		self.vllcfgline.append(("%s|%s|%s|%s|0|0|\n" %(lhs_dpid, rhs_dpid, lhs_tap.name, rhs_tap.name)))
		
	def newOSPFNetName(self):
		ret = self.ospfBase
		self.ospfBase = self.ospfBase + 1
		return "NET%s" % ret
	
	def addOSPFNet(self, ip):
		found = False
		for ospfnet in self.ospfnets:
			if ip == ospfnet.net:
				found = True
				break
		if found == False:
			name = self.newOSPFNetName()
			net = OSPFNetwork(name, ip)
			self.ospfnets.append(net)
			self.nameToOSPFNet[name] = net
		else:
			net = ospfnet 
		return net

	# Check if a structure is empty
	def is_empty(struct):
		if struct:
		    return False
		else:
		    return True

	# XXX Depends on type of testbed
	def configure(self):
		raise NotImplementedError("Abstract Method")
	
	def generateLMErules(self):
		header =open('headerLME.txt','r')
		testbed = open('lmerules.sh','w')
		lines = header.readlines()
		for line in lines:
			testbed.write(line)
		testbed.close()
		for osh in self.oshs:
			osh.generateLMErules(self.coex)
		for aosh in self.aoss:
			aosh.generateLMErules(self.coex)

	def generateMGMTCfg(self):
		header =open('headerMGMT.txt','r')
		management = open('management.sh','w')
		lines = header.readlines()
		for line in lines:
			management.write(line)
		management.write("declare -a DSH_GROUPS=(OSHI EUH CTRL L2SW)\n")
		temp = []
		for osh in self.oshs:
			temp.append(osh)
		for aos in self.aoss:
			temp.append(aos)
		oshi = "declare -a OSHI=(" + " ".join("%s" % osh.mgt_ip for osh in temp) + ")\n"
		euh = "declare -a EUH=(" + " ".join("%s" % euh.mgt_ip for euh in self.euhs) + ")\n"
		ctrl = "declare -a CTRL=(" + " ".join("%s" % ctrl.mgt_ip for ctrl in self.ctrls) + ")\n"
		l2sw = "declare -a L2SW=(" + " ".join("%s" % l2sw.mgt_ip for l2sw in self.l2sws) + ")\n"
		machine = "declare -a NODE_LIST=(" + " ".join("%s" % node.mgt_ip for name, node in self.nameToNode.iteritems()) + ")\n"	
		management.write(oshi)
		management.write(euh)
		management.write(ctrl)
		management.write(l2sw)
		management.write(machine)

	def generateVLLCfg(self, path):
		dbpath = path + "vlls.json"
		if(os.path.exists(dbpath)):
			if self.verbose:			
				print "*** Remove Vlls DB File"
			os.remove(path + "vlls.json")
		cfg = open(path + 'vll_pusher.cfg','w')
		for line in self.vllcfgline:
			cfg.write(line)
		cfg.close()

	def addCoexistenceMechanism(self, coex):
		if self.coex != None:
			print "Error Coex mechanism already created"
			sys.exit(-1)
		self.coex = coex

	def addIngressClassification(self, cedge, aoshi, ingress):
		cedge = self.getNodeByName(cedge)	
		aoshi = self.getNodeByName(aoshi)
		aoshi.addIngress(ingress)
		# TODO management cedge

# XXX configure() depends On Luca Prete' s Bash Script
class TestbedRouterGOFF( TestbedRouter ):
	def __init__(self, tunneling, ipnet, verbose=True):
		TestbedRouter.__init__(self)
		self.parser = MappingParserRouterTestbed(path_json = "router_goff_mapping.map", verbose = verbose)
		(self.routerinfo, self.l2swsinfo, self.euhsinfo) = self.parser.getNodesInfo()
		self.vlan = self.parser.vlan
		self.verbose = verbose
		self.user = self.parser.user
		self.pwd = self.parser.pwd
		self.ipnet = ipnet
		self.tunneling = tunneling	
	
	def configure(self):
		header =open('header.txt','r')
		testbed = open('testbed.sh','w')
		lines = header.readlines()
		for line in lines:
			testbed.write(line)
		testbed.write("# general configuration - start\n")
		testbed.write("TESTBED=GOFF\n")
		testbed.write("TUNNELING=%s\n" % self.tunneling)
		testbed.write("# general configuration - end\n")
		testbed.close()
		for router in self.routs:
			router.configure([self.ipnet])	
		for l2switch in self.l2sws:
			l2switch.configure()	
		for euh in self.euhs:
			euh.configure([self.ipnet])
					
# XXX configure() depends On Luca Prete' s Bash Script
class TestbedOSHIGOFF( TestbedOSHI ):
	
	def __init__(self, tunneling, ipnet, verbose=True):
		TestbedOSHI.__init__(self)
		self.parser = MappingParserOSHITestbed(path_json = "oshi_goff_mapping.map", verbose = verbose)
		(self.oshinfo, self.aosinfo, self.l2swsinfo, self.ctrlsinfo, self.euhsinfo) = self.parser.getNodesInfo()
		self.vlan = self.parser.vlan
		self.verbose = verbose
		self.user = self.parser.user
		self.pwd = self.parser.pwd
		self.ipnet = ipnet
		self.tunneling = tunneling

	
	def configure(self):
		self.roundrobinallocation()
		header =open('header.txt','r')
		testbed = open('testbed.sh','w')
		lines = header.readlines()
		for line in lines:
			testbed.write(line)
		testbed.write("# general configuration - start\n")
		testbed.write("TESTBED=GOFF\n")
		testbed.write("TUNNELING=%s\n" % self.tunneling)
		if self.coex == None:
			print "Error No Coexistence Mechanism Created"
			sys.exit(-2)
		testbed.write(self.coex.serialize())
		testbed.write("# general configuration - end\n")
		testbed.close()
		for osh in self.oshs:
			osh.configure([self.ipnet])
		for aosh in self.aoss:
			aosh.configure([self.ipnet])
		for l2switch in self.l2sws:
			l2switch.configure()	
		for euh in self.euhs:
			euh.configure([self.ipnet])
		for ctrl in self.ctrls:
			ctrl.configure([self.ipnet])

# XXX configure() depends On Luca Prete' s Bash Script
class TestbedRouterOFELIA( TestbedRouter ):

	# Init Function
	def __init__( self, tunneling, ipnet, verbose=True):	
		TestbedRouter.__init__(self)
		self.parser = MappingParserRouterTestbed(path_json = "router_ofelia_mapping.map", verbose = verbose)
		(self.routerinfo, self.l2swsinfo, self.euhsinfo) = self.parser.getNodesInfo()
		self.vlan = self.parser.vlan
		self.verbose = verbose
		self.ipnet = ipnet
		#XXX START MGMT INFO
		self.mgmtnet = "10.216.0.0/255.255.0.0"
		self.mgmtgw = "10.216.32.1"
		self.mgmtintf = "eth0"
		#XXX END MGMT INFO		
		self.user = self.parser.user
		self.pwd = self.parser.pwd
		self.tunneling = tunneling

	def configure(self):
		header =open('header.txt','r')
		testbed = open('testbed.sh','w')
		lines = header.readlines()
		for line in lines:
			testbed.write(line)
		mgmtnetdata = (self.mgmtnet.split("/"))
		mgmtnet = mgmtnetdata[0]
		mgmtmask = mgmtnetdata[1]
		testbed.write("# general configuration - start\n")
		testbed.write("TESTBED=OFELIA\n")
		testbed.write("TUNNELING=%s\n" % self.tunneling)
		testbed.write("declare -a MGMTNET=(%s %s %s %s)\n" %(mgmtnet, mgmtmask, self.mgmtgw, self.mgmtintf))		
		testbed.write("# general configuration - end\n")
		testbed.close()
		for router in self.routs:
			router.configure([self.ipnet])
		for l2switch in self.l2sws:
			l2switch.configure()	
		for euh in self.euhs:
			euh.configure([self.ipnet])

# XXX configure() depends On Luca Prete' s Bash Script
class TestbedOSHIOFELIA( TestbedOSHI ):

	# Init Function
	def __init__( self, tunneling, ipnet, verbose=True):
		TestbedOSHI.__init__(self)
		self.parser = MappingParserOSHITestbed(path_json = "oshi_ofelia_mapping.map", verbose = verbose)
		(self.oshinfo, self.aosinfo, self.l2swsinfo, self.ctrlsinfo, self.euhsinfo) = self.parser.getNodesInfo()
		self.vlan = self.parser.vlan
		self.verbose = verbose
		self.ipnet = ipnet
		#XXX START MGMT INFO
		self.mgmtnet = "10.216.0.0/255.255.0.0"
		self.mgmtgw = "10.216.32.1"
		self.mgmtintf = "eth0"
		#XXX END MGMT INFO		
		self.user = self.parser.user
		self.pwd = self.parser.pwd
		self.tunneling = tunneling
	
	def configure(self):
		self.roundrobinallocation()
		header =open('header.txt','r')
		testbed = open('testbed.sh','w')
		lines = header.readlines()
		for line in lines:
			testbed.write(line)
		mgmtnetdata = (self.mgmtnet.split("/"))
		mgmtnet = mgmtnetdata[0]
		mgmtmask = mgmtnetdata[1]
		testbed.write("# general configuration - start\n")
		testbed.write("TESTBED=OFELIA\n")
		testbed.write("TUNNELING=%s\n" % self.tunneling)
		if self.coex == None:
			print "Error No Coexistence Mechanism Created"
			sys.exit(-2)
		testbed.write(self.coex.serialize())
		testbed.write("declare -a MGMTNET=(%s %s %s %s)\n" %(mgmtnet, mgmtmask, self.mgmtgw, self.mgmtintf))		
		testbed.write("# general configuration - end\n")
		testbed.close()
		for osh in self.oshs:
			osh.configure([self.ipnet])
		for aosh in self.aoss:
			aosh.configure([self.ipnet])
		for l2switch in self.l2sws:
			l2switch.configure()
		for euh in self.euhs:
			euh.configure([self.ipnet])
		for ctrl in self.ctrls:
			ctrl.configure([self.ipnet])
