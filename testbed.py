#!/usr/bin/python


"""

author: Pier Luigi Ventre (pl.ventre@gmail.com)
author: Giuseppe Siracusano (a_siracusano@tin.it)
author: Stefano Salsano (stefano.salsano@uniroma2.it)

"""

import sys
from testbed_node import Oshi, Controller, Host
from mapping_parser import MappingParserOFELIA
from testbed_deployer_utils import OSPFNetwork
from testbed_cli import TestbedCLI
from topo_parser import TestbedTopoParser
import copy

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
			print "Error No Controller Added - Informatino Will Not Be Generated"
		
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

		(lhs_vi, lhs_tap, lhs_ospf_net) = lhs.addIntf([rhs_eth_ip, lhs_eth, lhs_tap_port, rhs_tap_port, lhs_ospf_net, lhs_ip])
		(rhs_vi, rhs_tap, rhs_ospf_net) = rhs.addIntf([lhs_eth_ip, rhs_eth, rhs_tap_port, lhs_tap_port, rhs_ospf_net, rhs_ip])

		return [(lhs_vi, rhs_vi), (lhs_tap, rhs_tap), (lhs_ospf_net, rhs_ospf_net)]

		
	def newOSPFNetName(self):
		
		ret = self.ospfBase
		self.ospfBase = self.ospfBase + 1
		return "NET%s" % ret
		
	def addOSPFNet(self):
		name = self.newOSPFNetName()
		net = OSPFNetwork(name)
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
		for key, host in self.nameToNode.iteritems():
			host.configure()

	def start(self):
		for osh in self.oshs:
			osh.start()

	def stop(self):
		for osh in self.oshs:
			osh.stop()

# XXX Test1 Create a Mesh Triangular Network, with 3 OSHI and 1 Controllers And Print The Internal Object of TestBed
def test1():
	print "*** Test1"
	testbed = TestbedOFELIA("ofelia_mapping.json", verbose=False)
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
	for controller in testbed.ctrls:
		print "*** Ctrl", controller.name
		for key, value in controller.nameToEths.iteritems():
			print "*** Eth", key, value
		for key, value in controller.nameToEndIps.iteritems():
			print "*** EndIP", key, value
		for key, value in controller.nameToTaps.iteritems():
			print "*** Tap", key, value
		print "*** Reachable IP", controller.ips
		print "*** Reachable Port", controller.port
		print "###########################"
	for net in testbed.ospfnets:
		print "*** Testbed OSPFNET", net
	
	print
	TestbedCLI(testbed)

# XXX Test2 First Create a Mesh Triangular Core Network, second for each coshi create an aoshi, link them and create the Controller.
# Finally Print The Internal Object of TestBed	
def test2():
	print "*** Test2"
	testbed = TestbedOFELIA("ofelia_mapping.json", verbose=False)
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
	for controller in testbed.ctrls:
		print "*** Ctrl", controller.name
		for key, value in controller.nameToEths.iteritems():
			print "*** Eth", key, value
		for key, value in controller.nameToEndIps.iteritems():
			print "*** EndIP", key, value
		for key, value in controller.nameToTaps.iteritems():
			print "*** Tap", key, value
		print "*** Reachable IP", controller.ips
		print "*** Reachable Port", controller.port
		print "###########################"
	for net in testbed.ospfnets:
		print "*** Testbed OSPFNET", net
	print
	TestbedCLI(testbed)

# XXX Test3 Build Topology From topo.json generated through TopologyDesigner
def test3():
	verbose = True
	if verbose:
		print "*** Build Topology From Parsed File"
	parser = TestbedTopoParser("topo.json", verbose=True)
	(ppsubnets, l2subnets) = parser.getsubnets()
	set_oshis = parser.oshis
	set_aoshis = parser.aoshis
	set_l2sws = parser.l2sws
	set_euhs = parser.euhs
	testbed = TestbedOFELIA("ofelia_mapping.json", verbose = False)
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
	for euh in testbed.euhs:
		print "*** EUH:", euh.name
		for key, value in euh.nameToEths.iteritems():
			print "*** Eth", key, value
		for key, value in euh.nameToEndIps.iteritems():
			print "*** EndIP", key, value
		for key, value in euh.nameToTaps.iteritems():
			print "*** Tap", key, value
		print "*** EndIPBase", euh.endIPBase
		print "*** TapBase", euh.tapBase
		print "*** EthIndex", euh.ethIndex
		print "*** TapPortBase", euh.tapPortBase
		print "###########################"
	for controller in testbed.ctrls:
		print "*** Ctrl", controller.name
		for key, value in controller.nameToEths.iteritems():
			print "*** Eth", key, value
		for key, value in controller.nameToEndIps.iteritems():
			print "*** EndIP", key, value
		for key, value in controller.nameToTaps.iteritems():
			print "*** Tap", key, value
		print "*** Reachable IP", controller.ips
		print "*** Reachable Port", controller.port
		print "*** EndIPBase", euh.endIPBase
		print "*** TapBase", euh.tapBase
		print "*** EthIndex", euh.ethIndex
		print "*** TapPortBase", euh.tapPortBase
		print "###########################"

	for net in testbed.ospfnets:
		print "*** Testbed OSPFNET", net

	print	
	TestbedCLI(testbed)

# XXX Test4 Build Topology Using Networkxx
"""def test4():
	g = nx.erdos_renyi_graph(6,0.8)
	net = testbed = TestbedOFELIA("ofelia_mapping.json", verbose = False)
	i = 0
	h = 0
	# This is the basic behavior, but we have to modify it in order to creare switched networks
	oshis = int(floor(len(g.nodes)))
	aoshis = len(g.nodes) - oshis
	for i in range(0, oshis):
		i = i + 1
		testbed.addOshi('osh%s' % (i))
	for i in range(oshis, len(g.nodes)):
		i = i + 1
		testbed.addAoshi('aos%s' % (i)))
	for (n1, n2) in g.edges():
		n1 = n1 + 1
		n2 = n1 + n2 + 1
		lhs = testbed.getNodeByName('osh%s' % n1)
		rhs = net.getNodeByName('osh%s' % n2)
		l = net.addLink(lhs, rhs)
		nets.append(OSPFNetwork(intfs=[l.intf1.name,l.intf2.name], ctrl=False))
		print "*** Connect", lhs, "To", rhs 

	hosts_in_rn = []
	c1 = RemoteController( 'c1', ip=ctrls_ip[0], port=ctrls_port[0])
	ctrls.append(c1)
	hosts_in_rn.append(c1)
	# Connecting the controller to the network 
	print "*** Connect %s" % oshi," To c1"
	l = net.addLink(oshi, c1)
	nets.append(OSPFNetwork(intfs=[l.intf1.name,l.intf2.name], ctrl=True, hello_int=5))
	
	# Only needed for hosts in root namespace
	fixIntf(hosts_in_rn)

	for network in nets:
		print "*** Create Network:", network.subnet + "0,", str(network.intfs) + ",", "cost %s," % network.cost, "hello interval %s," % network.hello_int

	# We generate the topo's png
	pos = nx.circular_layout(g)
        nx.draw(g, pos)
        plt.savefig("topo.png")
"""

if __name__ == '__main__':
	#test1()
	test2()
	#test3()
	

	# Cemetery of Code
	# ctrls = ['ip1:port1', 'ip2:port2', ...]
	#def setControllers(self, oshi, ctrls):
		#oshi = self.getNodeByName(oshi)
		#oshi.setControllers(ctrls)
		#self.oshiToControllers[oshi.name] = ctrls
	
	

