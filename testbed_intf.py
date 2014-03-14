#!/usr/bin/python

"""
Based On Mininet API
thanks to: Bob Lantz (rlantz@cs.stanford.edu), Brandon Heller (brandonh@stanford.edu)
thanks to all Dreamer Team, especially to Luca Prete (preteluca@gmail.com) for the bash scripts;

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

class TapIntf(Intf):
	
	def __init__(self, name, localport, remoteport, endipname):
		Intf.__init__(self,name)
		self.ip = ip
		self.localport = localport
		self.remoteport = remoteport
		self.endipname = endipname
	
	def serialize(self):
		return "declare -a %s=(%s %s %s)\n" % (self.localport, self.remoteport, self.endipname)

class ViIntf(Intf):
	
	def __init__(self, name, ip, netbit, hello_int, cost):
		Intf.__init__(self,name)
		self.ip = ip
		self.netbit = netbit
		self.hello_int = hello_int
		self.cost = cost
	
	def serialize(self):
		return "declare -a %s=(%s/%s %s %s)\n" %(self.name, self.ip, self.netbit, self.hello_int, self.cost)

class LoIntf(Intf):
	
	def __init__(self, ip, name="LOOPBACK", netbit=32, hello_int=1, cost=1):
		Intf.__init__(self,name)
		self.ip = ip
		self.netbit = netbit
		self.hello_int = hello_int
		self.cost = cost
	
	def serialize(self):
		return "declare -a %s=(%s/%s %s %s)\n" %(self.name, self.ip, self.netbit, self.hello_int, self.cost)









