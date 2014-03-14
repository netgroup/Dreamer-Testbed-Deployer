#!/usr/bin/python

from testbed import Testbed
from topo_parser import TestbedTopoParser

oshis = []
aoshis = []
switches = []
hosts = []
ctrls = []

def buildTopoFromFile(param):
	global oshis
	global aoshis
	global switches
	global hosts
	global ctrls

	if verbose:
		print "*** Build Topology From Parsed File"
	parser = TopoParser(param, verbose=False)
	(ppsubnets, l2subnets) = parser.getsubnets()
	set_oshis = parser.oshis
	set_aoshis = parser.aoshis
	set_l2sws = parser.l2sws
	set_euhs = parser.euhs
	hosts_in_rn = []
	testbed = Testbed()
	if verbose:
		print "*** Build OSHI"	
	for oshi in set_oshis:
		osh = net.addHost(oshi)
		oshis.append(osh)
	if verbose:
		print "*** Build AOSHI"
	for aoshi in set_aoshis:
		aos = net.addHost(aoshi)
		aoshis.append(aos)
	if verbose:
		print "*** Build L2SWS"
	for l2sw in set_l2sws:
		sw = net.addSwitch(l2sw)
		switches.append(sw)
		hosts_in_rn.append(sw)
	if verbose:
		print "*** Build EUHS"
	for euh in set_euhs:
		net.addHost(euh)
		hosts.append(euh)	
	if verbose:	
		print "*** Create Core Networks Point To Point"
	i = 0
	for ppsubnet in ppsubnets:
		if ppsubnet.type == "CORE":
			if verbose:
				print "*** Subnet: Node %s - Links %s" %(ppsubnet.nodes, ppsubnet.links)
			node1 = net.getNodeByName(ppsubnet.links[0][0])
			node2 = net.getNodeByName(ppsubnet.links[0][1])
			l = net.addLink(node1, node2)
			nets.append(OSPFNetwork(intfs=[l.intf1.name,l.intf2.name], ctrl=False))
			if verbose:			
				print "*** Connect", node1.name, "To", node2.name
		i = i + 1
	if verbose:	
		print "*** Create Core Networks Switched"
	for l2subnet in l2subnets:
		if l2subnet.type == "CORE":
			if verbose:
				print "*** Subnet: Node %s - Links %s" % (ppsubnet.nodes, ppsubnet.links)
			intfs = []
			for link in l2subnet.links:
				node1 = net.getNodeByName(link[0])
				node2 = net.getNodeByName(link[1])
				l = net.addLink(node1, node2)
				if verbose:			
					print "*** Connect", node1.name, "To", node2.name
				if 'sw' not in link[0] and 'sw' in link[1]:
					intfs.append(l.intf1.name)
				elif 'sw' in link[0] and 'sw' not in link[1]:
					intfs.append(l.intf2.name)
				elif 'sw' in link[0] and 'sw' in link[1]:
					continue
				else:
					print "Error Switched Networks - Both EndPoint != SW"
					sys.exit(-2)
			nets.append(OSPFNetwork(intfs, ctrl=False))
		i = i + 1
	if verbose:	
		print "*** Create Access Networks Point To Point"
	i = 0
	for ppsubnet in ppsubnets:
		if ppsubnet.type == "ACCESS":
			# XXX The Order now is important
			"""if verbose:
				print "*** Subnet: Node %s - Links %s" %(ppsubnet.nodes, ppsubnet.links)
			node1 = net.getNodeByName(ppsubnet.links[0][0])
			node2 = net.getNodeByName(ppsubnet.links[0][1])
			l = net.addLink(node1, node2)
			nets.append(OSPFNetwork(intfs=[l.intf1.name,l.intf2.name], ctrl=False))
			if verbose:			
				print "*** Connect", node1.name, "To", node2.name"""
			print "Error Not Managed For Now"
			sys.exit(-2)
		i = i + 1
	if verbose:	
		print "*** Create Acces Networks Switched"
	for l2subnet in l2subnets:
		if l2subnet.type == "ACCESS":
			l2net = L2AccessNetwork(classification = 'B')
			if verbose:
				print "*** Subnet: Node %s - Links %s" % (l2subnet.nodes, l2subnet.links)
				print "*** Create L2 Access Network - Classification", l2net.classification	
			intfs = []
			# XXX The Order now is important
			ord_links = l2subnet.getOrderedLinks()
			for link in ord_links:
				node1 = net.getNodeByName(link[0])
				node2 = net.getNodeByName(link[1])
				l = net.addLink(node1, node2)
				l2net.addLink(l)
				if verbose:			
					print "*** Connect", node1.name, "To", node2.name
				if 'sw' not in link[0] and 'sw' in link[1]:
					intfs.append(l.intf1.name)
				elif 'sw' in link[0] and 'sw' not in link[1]:
					intfs.append(l.intf2.name)
				elif 'sw' in link[0] and 'sw' in link[1]:
					continue
				else:
					print "Error Switched Networks - Both EndPoint != SW"
					sys.exit(-2)
			nets.append(OSPFNetwork(intfs, ctrl=False))
			L2nets.append(l2net)
		i = i + 1	
	
	print "*** Creating controller"
	c1 = RemoteController( 'c1', ip=ctrls_ip[0], port=ctrls_port[0])
	ctrls.append(c1)
	hosts_in_rn.append(c1)

	# Connect the controller to the network
	print "*** Connect", osh.name, "To Controller"
	l = net.addLink(osh, c1)
	nets.append(OSPFNetwork(intfs=[l.intf1.name, l.intf2.name], ctrl=True))
	
	# Only needed for hosts in root namespace
	fixIntf(hosts_in_rn)

	# Utility function		
	check_host()
	
	for i in range(0, len(LHS_tunnel)):
		tunnels.append(Tunnel())

	loopback[2]=sdn_lastnet

	print "*** Loopback Address Start From:", loopback 
	print "*** Tunnels LHS:", LHS_tunnel
	print "*** Tunnels RHS:", RHS_tunnel

	# Tunnels Setup
	IP_tunnel_setup()
	SDN_tunnel_setup(net)

	i = 0
	for tunnel in tunnels :	
		print "*** Tunnel %d, Subnet %s0, Intfs %s" % (i+1, tunnel.subnet, tunnel.intfs)
		i = i + 1

	i = 0
	for l2net in L2nets:
		print "***", l2net.name
		print "*** Nodes:", l2net.Nodes
		print "*** Links:", l2net.Links
		print "*** Intfs:", l2net.intfs
		i = i + 1
	
	print "*** AOSHI Tag:", AOSHI_TO_TAG
	print "*** Trunk Port Configuration:", TRUNK_TO_TAG
	print "*** Access Port Configuration:", ACCESS_TO_TAG
	print "*** LHS AOSHI:", LHS_tunnel_aoshi
	print "*** RHS AOSHI:", RHS_tunnel_aoshi
	print "*** LHS Port:", LHS_tunnel_port
	print "*** RHS Port:", RHS_tunnel_port


	for network in nets:
		print "*** OSPF Network:", network.subnet + "0,", str(network.intfs) + ",", "cost %s," % network.cost, "hello interval %s," % network.hello_int
	return net

if __name__ == '__main__':
	testbed = buildTestbedFromFile(param)

