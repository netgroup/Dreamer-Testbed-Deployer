#!/usr/bin/python

"""
Utility Class For TestbedDeployer

author: Pier Luigi Ventre (pl.ventre@gmail.com)
author: Giuseppe Siracusano (a_siracusano@tin.it)
author: Stefano Salsano (stefano.salsano@uniroma2.it)

"""

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
	
	ipBaseOSPF=[10, 0, 0, 0]
	netbitOSPF=24
 
	def __init__(self, name, cost=1, hello_int=1, area="0.0.0.0"):
		self.subnet = self.next_netAddress()
		self.cost = cost
		self.hello_int = hello_int
		self.area = area
		self.name = name
	
	# XXX Change With ipBaseOSPF and netbitOSPF
	def next_netAddress(self):
		self.ipBaseOSPF[2] = (self.ipBaseOSPF[2] + 1) % 256
		if self.ipBaseOSPF[2] == 255:
			print "Net Address SoldOut"
			sys.exit(-2)
		return [self.ipBaseOSPF[0], self.ipBaseOSPF[1], self.ipBaseOSPF[2], 0 ]

	def serialize(self):
		return "declare -a %s=(%s.%s.%s.0/%s %s)\n" %(self.name, self.subnet[0], self.subnet[1], self.subnet[2], self.netbitOSPF, self.area)
	
	def __str__(self):
		return "{'name':'%s', 'net':'%s.%s.%s.0/%s', 'area':'%s'}" %(self.name, self.subnet[0], self.subnet[1], self.subnet[2], self.netbitOSPF, self.area)



