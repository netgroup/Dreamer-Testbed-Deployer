#!/usr/bin/python

"""

author: Pier Luigi Ventre (pl.ventre@gmail.com)
author: Giuseppe Siracusano (a_siracusano@tin.it)
author: Stefano Salsano (stefano.salsano@uniroma2.it)

"""

class Intf:
	
	def __init__(self, name):
		self.name = name

class EthIntf(Intf):
	
	def __init__(self, name, ip, netbit, netmask):
		Intf.__init__(self,name)
		self.ip = ip
		self.netbit = netbit
		self.netmask = netmask
	
	def serialize(self):
		return "declare -a %s=(%s %s.%s.%s.%s)\n" % (self.name, self.ip, self.netmask[0], self.netmask[1], self.netmask[2], self.netmask[3])

	def __str__(self):
		return "{'name':'%s', 'ip':'%s/%s', 'netmask':'%s.%s.%s.%s'}" %(self.name, self.ip, self. netbit, self.netmask[0], self.netmask[1], self.netmask[2], self.netmask[3])

class TapIntf(Intf):
	
	def __init__(self, name, localport, remoteport, endipname):
		Intf.__init__(self,name)
		self.name = name
		self.localport = localport
		self.remoteport = remoteport
		self.endipname = endipname
	
	def serialize(self):
		return "declare -a %s=(%s %s %s)\n" % (self.name, self.localport, self.remoteport, self.endipname)
	
	def __str__(self):
		return "{'name':'%s', 'localport':'%s', 'remoteport':'%s', 'endip':'%s'}" % (self.name, self.localport, self.remoteport, self.endipname)

class TapIPIntf(TapIntf):
	
	def __init__(self, name, localport, remoteport, endipname, ip, netbit):
		TapIntf.__init__(self,name, localport, remoteport, endipname)
		self.ip = ip
		self.netbit = netbit

	def serialize(self):
		return "declare -a %s=(%s %s %s/%s %s)\n" % (self.name, self.localport, self.remoteport, self.ip, self.netbit, self.endipname)
	
	def __str__(self):
		return "{'name':'%s', 'localport':'%s', 'remoteport':'%s', 'ip:':'%s/%s', 'endip':'%s'}" % (self.name, self.localport, self.remoteport, self.ip, self.netbit, self.endipname)

class ViIntf(Intf):
	
	def __init__(self, name, ip, netbit, hello_int, cost):
		Intf.__init__(self,name)
		self.ip = ip
		self.netbit = netbit
		self.hello_int = hello_int
		self.cost = cost
	
	def serialize(self):
		return "declare -a %s=(%s/%s %s %s)\n" %(self.name, self.ip, self.netbit, self.cost, self.hello_int)

	def __str__(self):
		return "{'name':'%s', 'ip':'%s', 'netbit':'%s', 'hello_int':'%s', 'cost':'%s'}" % (self.name, self.ip, self.netbit, self.cost, self.hello_int)

class LoIntf(Intf):
	
	def __init__(self, ip, name="LOOPBACK", netbit=32, hello_int=1, cost=1):
		Intf.__init__(self,name)
		self.ip = ip
		self.netbit = netbit
		self.hello_int = hello_int
		self.cost = cost
	
	def serialize(self):
		return "declare -a %s=(%s/%s %s %s)\n" %(self.name, self.ip, self.netbit, self.cost, self.hello_int)

	def __str__(self):
		return "{'name':'%s', 'ip':'%s', 'netbit':'%s', 'hello_int':'%s', 'cost':'%s'}" % (self.name, self.ip, self.netbit, self.cost, self.hello_int)








