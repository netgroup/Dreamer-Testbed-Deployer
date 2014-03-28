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
# XXX Depends On Luca Prete Script

from netaddr import *
from ipaddress import *

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
	
	#ipBaseOSPF=[10, 0, 0, 0]
	#netbitOSPF=24
 
	def __init__(self, name, net, cost=1, hello_int=1, area="0.0.0.0"):
		self.net = net
		data = net.split("/")
		bytes = data[0].split(".")
		self.netbitOSPF = int(data[1])
		i = 0
		self.subnet = []
		for byte in bytes:
			self.subnet.append(int(byte))
			i = i + 1
		self.cost = cost
		self.hello_int = hello_int
		self.area = area
		self.name = name
	
	# XXX Change With ipBaseOSPF and netbitOSPF
	# def next_netAddress(self):
		#self.ipBaseOSPF[2] = (self.ipBaseOSPF[2] + 1) % 256
		#if self.ipBaseOSPF[2] == 255:
		#	print "Net Address SoldOut"
		#	sys.exit(-2)
		#return [self.ipBaseOSPF[0], self.ipBaseOSPF[1], self.ipBaseOSPF[2], 0 ]

	def serialize(self):
		return "declare -a %s=(%s %s)\n" %(self.name, self.net, self.area)
	
	def __str__(self):
		return "{'name':'%s', 'net':'%s', 'area':'%s'}" %(self.name, self.net, self.area)

class IPNetAllocator:
	
	def __init__(self, mgmtnet, ipnet):
		self.mgmtnet = (IPv4Network(mgmtnet))
		self.ipnet = (IPv4Network(ipnet))
		if self.ipnet.overlaps(self.mgmtnet):
			print "*** Overlap Among IPNet and ManagementNet"
			print "*** Calculating Available IP network"
			self.iternets = self.ipnet.address_exclude(self.mgmtnet)
		else:
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
		return net.__str__()

	

	
		







