#!/usr/bin/python

"""
Utility Class For TestbedDeployer

author: Pier Luigi Ventre (pl.ventre@gmail.com)
author: Giuseppe Siracusano (a_siracusano@tin.it)
author: Stefano Salsano (stefano.salsano@uniroma2.it)

"""

class endIP:

	def __init__(self, name, remoteIP, localIntf):
		self.name = name
		self.remoteIP = remoteIP
		self.localIntf = localIntf

	def serialize(self):
		return "declare -a %s=(%s %s)" %(name, remoteIP, localIntf)


class OSPFNetwork:
	
	ipBaseOSPF=[10, 0, 0, 0]
	netbitOSPF=24
 
	def __init__(self, name, ctrl, cost=1, hello_int=2, area="0.0.0.0"):
		if ctrl:
			self.subnet = [10, 0, 0, 0]
		else :
			self.subnet = self.next_netAddress()
		self.cost = cost
		self.hello_int = hello_int
		self.area = area
		self.name = name
	
	# XXX Change With ipBaseOSPF and netbitOSPF
	def next_netAddress(self):
		self.ipBaseOSPF[2] = (self.ipBaseTestbed[2] + 1) % 256
		if self.ipBaseTestbed[2] == 255:
			print "Net Address SoldOut"
			sys.exit(-2)
		return (self.ipBaseTestbed[0], self.ipBaseTestbed[1], self.ipBaseTestbed[2], 0 )

	def serialize(self):
		return "declare -a %s=(%s.%s.%s.0/%s %s)" %(name, self.subnet[0], self.subnet[1], self.subnet[2], self.netbitOSPF, self.area)





