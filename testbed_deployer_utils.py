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
import re

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
 
	def __init__(self, name, net, cost=1, hello_int=5, area="0.0.0.0"):

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

	allowed_name = ["cro","peo","ctr","swi","cer", "rou", "euh"]

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
			lhs = link[0][:3]
			rhs = link[1][:3]
			
			a = re.search(r'cro\d+$', link[0])
			b = re.search(r'peo\d+$', link[0])
			c = re.search(r'ctr\d+$', link[0])
			d = re.search(r'swi\d+$', link[0])
			e = re.search(r'cer\d+$', link[0])
			f = re.search(r'rou\d+$', link[0])
			g = re.search(r'euh\d+$', link[0])
			
			if a is None and b is None and c is None and d is None and e is None and f is None and g is None:
				print "ERROR Not Allowed Name (%s,%s)" %(link[0],link[1])
				sys.exit(-2)

			h = re.search(r'cro\d+$', link[1])
			i = re.search(r'peo\d+$', link[1])
			l = re.search(r'ctr\d+$', link[1])
			m = re.search(r'swi\d+$', link[1])
			n = re.search(r'cer\d+$', link[1])
			o = re.search(r'rou\d+$', link[1])
			p = re.search(r'euh\d+$', link[1])
			
			if h is None and i is None and l is None and m is None and n is None and o is None and p is None:
				print "ERROR Not Allowed Name (%s,%s)" %(link[0],link[1])
				sys.exit(-2)
				
			ipLHS = None
			ipRHS = None
			ingrType = None
			ingrData = None
			OSPFnet="0.0.0.0/32"

			if d is None:
				ipLHS = hosts.pop(0).__str__()
			if m is None:
				ipRHS = hosts.pop(0).__str__()
			if (b is not None or i is not None) and (e is not None or n is not None):
				ingrType = "INGRB"
				ingrData = None
			if ipLHS is not None or ipRHS is not None:
				OSPFnet = net.__str__()

			linkproperties = LinkProperties(ipLHS, ipRHS, ingrType, ingrData, OSPFnet)
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
		
		e = re.search(r'cer\d+$', vll[0])
			
		if e is None:
			print "Error Both Hand Side != from Customer Edge Router (%s,%s)" %(vll[0],vll[1])
			sys.exit(-2)

		e = re.search(r'cer\d+$', vll[1])
			
		if e is None:
			print "Error Both Hand Side != from Customer Edge Router (%s,%s)" %(vll[0],vll[1])
			sys.exit(-2)

		
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

			c = re.search(r'ctr\d+$', node)
			d = re.search(r'swi\d+$', node)
			e = re.search(r'cer\d+$', node)
			f = re.search(r'euh\d+$', node)
			
			if c is None and d is None and e is None and f is None:
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
		self.ingr = IngressData(ingrType, ingrData)
		self.net = net

	def __str__(self):
		return "{'ipLHS':'%s', 'ipRHS':'%s', 'ingr':'%s', 'net':'%s'}" %(self.ipLHS, self.ipRHS, self.ingr, self.net)

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

class IngressData(object):

	def __init__(self, ingrtype, ingrdata):
		self.type = ingrtype
		self.data = ingrdata
	
	def __str__(self):
		return "{'type':'%s', 'data':'%s'}" %(self.type, self.data)
