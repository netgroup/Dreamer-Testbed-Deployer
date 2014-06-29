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
# Deployer Utils.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
# XXX Depends On Dreamer-Setup-Script

from netaddr import *
from ipaddress import *
import sys

class EndIP:

	def __init__(self, name, remoteIP, localIntf):
		self.name = name
		self.remoteIP = remoteIP
		self.localIntf = localIntf

	def serialize(self):
		return "declare -a %s=(%s %s)\n" %(self.name, self.remoteIP, self.localIntf)

	def __str__(self):
        	return "{'name':'%s', 'endip':'%s' 'localintf':'%s'}" %(self.name, self.remoteIP, self.localIntf)

class OSPFNetwork:
 
	def __init__(self, name, net, cost=1, hello_int=1, area="0.0.0.0"):
		self.net = net
		data = net.split("/")
		#bytes = data[0].split(".")
		self.netbitOSPF = int(data[1])
		i = 0
		self.subnet = []
		#for byte in bytes:
		#	self.subnet.append(int(byte))
		#	i = i + 1
		self.cost = cost
		self.hello_int = hello_int
		self.area = area
		self.name = name

	def serialize(self):
		return "declare -a %s=(%s %s)\n" %(self.name, self.net, self.area)
	
	def __str__(self):
		return "{'name':'%s', 'net':'%s', 'area':'%s'}" %(self.name, self.net, self.area)

class LoopbackAllocator(object):

	def __init__(self):	
		print "*** Calculating Available Loopback Addresses"
		self.loopbacknet = (IPv4Network(("172.16.0.0/255.240.0.0").decode('unicode-escape')))
		self.hosts = list(self.loopbacknet.hosts())
	
	def next_hostAddress(self):
		host = self.hosts.pop(0)
		return host.__str__()
	

class NetAllocator(object):

	ipnet = "10.0.0.0/255.0.0.0".decode('unicode-escape')
	
	def __init__(self, generate):
		if generate == True:		
			print "*** Calculating Available IP Networks"
			self.ipnet = (IPv4Network(self.ipnet))
			self.iternets = self.ipnet.subnets(new_prefix=24)
			self.iternets24 = self.iternets.next().subnets(new_prefix=24)
	
	def next_netAddress(self):
		DONE = False
		#print list(self.iternets24)
		while DONE == False :	
			try:						
				try:
					net = self.iternets24.next()
					DONE = True
				except StopIteration:
					#print "Error Change SuperSubnet"
					self.iternets24 = self.iternets.next().subnets(new_prefix=24)
			except StopIteration:
				print "Error IP Net SoldOut"
				sys.exit(-2)
		return net

class OFELIANetAllocator(NetAllocator):
	
	mgmtnet = "10.216.0.0/255.255.0.0".decode('unicode-escape')	

	def __init__(self):
		NetAllocator.__init__(self, False)
		self.mgmtnet = (IPv4Network(self.mgmtnet))
		self.ipnet = (IPv4Network(self.ipnet))
		if self.ipnet.overlaps(self.mgmtnet):
			print "*** Overlap Among IPNet and ManagementNet"
			print "*** Calculating Available IP network"
			self.iternets = self.ipnet.address_exclude(self.mgmtnet)
		else:
			self.iternets = self.ipnet.subnets(new_prefix=24)
		self.iternets24 = self.iternets.next().subnets(new_prefix=24)

class PropertiesGenerator(object):

	def __init__(self, testbed):
		self.verbose = False
		if testbed == "OFELIA":
			self.netAllocator = OFELIANetAllocator()
		else:
			self.netAllocator = NetAllocator(True)
		self.loopbackAllocator = LoopbackAllocator()

	def getLinksProperties(self, links):
		output = []
		net = self.netAllocator.next_netAddress()
		if self.verbose == True:		
			print net
		hosts = list(net.hosts())	
		if self.verbose == True:			
			print hosts
		for link in links:
			if self.verbose == True:		
				print "(%s,%s)" % (link[0], link[1])
			ipLHS = None
			ipRHS = None
			ingrType = None
			ingrData = None
			if 'l2sw' not in link[0]:
				ipLHS = hosts.pop(0).__str__()
			if 'l2sw' not in link[1]:
				ipRHS = hosts.pop(0).__str__()
			if ('aos' in link[0] or 'aos' in link[1]) and ('euh' in link[0] or 'euh' in link[1]):
				ingrType = "INGRB"
				ingrData = None
			linkproperties = LinkProperties(ipLHS, ipRHS, ingrType, ingrData, net.__str__())
			if self.verbose == True:			
				print linkproperties
			output.append(linkproperties)
		return output

	def getVLLsProperties(self, vll):
		net = self.netAllocator.next_netAddress()
		if self.verbose == True:		
			print net
		hosts = list(net.hosts())				
		if self.verbose == True:
			print hosts		
			print "(%s,%s)" % (vll[0], vll[1])
		if 'euh' not in vll[0] and 'euh' not in vll[1]:
			print "Error Both != from EUH"
			print sys.exit(-2)
		ipLHS = hosts.pop(0).__str__()
		ipRHS = hosts.pop(0).__str__()
		
		vllproperties = VLLProperties(ipLHS, ipRHS, net.__str__())
		if self.verbose == True:			
			print vllproperties
		return vllproperties
		
	def getVerticesProperties(self, nodes):
		output = []
		for node in nodes:
			if self.verbose == True:
				print node
			host = None
			if 'l2sw' not in node:
				host = self.loopbackAllocator.next_hostAddress()
			vertexproperties = VertexProperties(host)
			if self.verbose == True:
				print vertexproperties
			output.append(vertexproperties)
		return output
	
class LinkProperties(object):

	def __init__(self, ipLHS, ipRHS, ingrType, ingrData, net):
		self.ipLHS = ipLHS
		self.ipRHS = ipRHS
		self.ingrType = ingrType
		self.ingrData = ingrData
		self.net = net

	def __str__(self):
		return "{'ipLHS':'%s', 'ipRHS':'%s', 'ingrType':'%s', 'ingrData':'%s', 'net':'%s'}" %(self.ipLHS, self.ipRHS, self.ingrType, self.ingrData, self.net)

class VLLProperties(object):

	def __init__(self, ipLHS, ipRHS, net):
		self.ipLHS = ipLHS
		self.ipRHS = ipRHS
		self.net = net

	def __str__(self):
		return "{'ipLHS':'%s', 'ipRHS':'%s', 'net':'%s'}" %(self.ipLHS, self.ipRHS, self.net)

class VertexProperties(object):
	
	def __init__(self, loopback):
		self.loopback = loopback

	def __str__(self):
		return "{'loopback':'%s'}" %(self.loopback)

"""if __name__ == '__main__':

	nodes = ["osh1", "osh2", "l2sw3", "osh4"]
	links = [("osh1", "l2sw3"), ("l2sw3", "osh2"), ("osh4", "l2sw3")]
	generator = PropertiesGenerator("OFELIA")
	vproperties = generator.getVerticesProperties(nodes)
	lproperties = generator.getLinksProperties(links)
	i = 0
	for node in nodes:
		print "Node: %s - Properties: %s" %( node, vproperties[i])
		i = i + 1	
	i = 0
	for link in links:
		print "Link: (%s, %s) - Properties: %s" %( link[0], link[1], lproperties[i])
		i = i + 1

	
	nodes = ["aos4", "euh5"]
	links = [("aos4", "euh5")]
	vproperties = generator.getVerticesProperties(nodes)
	lproperties = generator.getLinksProperties(links)
	i = 0
	for node in nodes:
		print "Node: %s - Properties: %s" %( node, vproperties[i])
		i = i + 1
	i = 0
	for link in links:
		print "Link: (%s, %s) - Properties: %s" %( link[0], link[1], lproperties[i])
		i = i + 1

	vlls = [("euh5", "euh6")]
	vllproperties = []
	for vll in vlls:
		vllproperties.append(generator.getVLLProperties(vll))
	i = 0
	for vll in vlls:
		print "VLL: (%s, %s) - Properties: %s" %( vll[0], vll[1], vllproperties[i])
		i = i + 1"""
	


