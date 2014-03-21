#!/usr/bin/python

import os
import json
import sys
from netaddr import *
from ipaddress import *
from time import sleep

class MappingParserOFELIA:

	# Init Function, load json_data from path_json
	def __init__(self, path_json, verbose=False):
		self.verbose = verbose
		self.oshis = []
		self.aoshis = []
		self.euhs = []
		self.ctrls = []
		self.vlan = None
		self.user = None
		self.pwd = None
		self.mgmtnet = None
		self.ipnet = None
		self.testbednet = None
		self.loopbacknet = None
		if self.verbose:
			print "*** MappingParser.__init__:"
		if os.path.exists(path_json) == False:
			print "Error Topo File Not Found"
			sys.exit(-2)
		json_file=open(path_json)
		self.json_data = json.load(json_file)
		json_file.close()
		if self.verbose:
			print "*** JSON Data Loaded:"
			print json.dumps(self.json_data, sort_keys=True, indent=4)

	# Parse Function, retrieves from json data : vlan_info (necessary for OFELIA testbed),
	# second retrieves the oshi info from json data, then the aoshi info, finally the euhs
	# info.
	def parse_data(self):
		self.load_info()
	
	def getNodesInfo(self):
		self.parse_data()
		return (self.oshis, self.aoshis, self.ctrls, self.euhs)
	
	def load_info(self):
		if self.verbose:
			print "*** Retrieve Nodes"
		if 'username' not in self.json_data:
			print "*** Error No Username Data"
			sys.exit(-2)
		self.user = self.json_data['username']
		if 'password' not in self.json_data:
			print "*** Error No Password Data"
			sys.exit(-2)
		self.pwd = self.json_data['password']
		if 'vlan' not in self.json_data:
			print "*** Error No Vlan Data"
			sys.exit(-2)
		self.vlan = self.json_data['vlan']
		if 'mgmtnet' not in self.json_data:
			print "*** Error No Management Net Data"
			sys.exit(-2)
		self.mgmtnet = self.json_data['mgmtnet']
		if 'ipnet' not in self.json_data:
			print "*** Error No IP Net Data"
			sys.exit(-2)
		self.ipnet = self.json_data['ipnet']
		#if 'testbednet' not in self.json_data:
		#	print "*** Error No Testbed Net Data"
		#	sys.exit(-2)
		#self.testbednet = self.json_data['testbednet']
		#if 'loopbacknet' not in self.json_data:
		#	print "*** Error No Loopback Net Data"
		#	sys.exit(-2)
		#self.loopbacknet = self.json_data['loopbacknet']
		if 'core' in self.json_data:
			oshies = self.json_data['core']
			for oshi in oshies:
				self.oshis.append(NODInfo(oshi[0], oshi[1]))
		if 'access' in self.json_data:
			aoshies = self.json_data['access']
			for aoshi in aoshies:
				self.aoshis.append(NODInfo(aoshi[0], aoshi[1]))
		if 'ctrl' in self.json_data:
			controllers = self.json_data['ctrl']
			for controller in controllers:
				self.ctrls.append(NODInfo(controller[0], controller[1]))
		if 'euh' in self.json_data:
			euhos = self.json_data['euh']
			for euh in euhos:
				self.euhs.append(NODInfo(euh[0], euh[1]))
			
		if self.verbose:		
			print "*** OSHI:"
			for osh in self.oshis:
				print "*** Name %s - Mgt IP %s - Intfs %s" %(osh.name, osh.mgt_ip, osh.intfs)
			print "*** AOSHI:"
			for aos in self.aoshis:
				print "*** Name %s - Mgt IP %s - Intfs %s" %(aos.name, aos.mgt_ip, aos.intfs)
			print "*** CONTROLLER:"
			for ctrl in self.ctrls:
				print "*** Name %s - Mgt IP %s - Intfs %s" %(ctrl.name, ctrl.mgt_ip, ctrl.intfs)
			print "*** EUH:"
			for euh in self.euhs:
				print "*** Name %s - Mgt IP %s - Intfs %s" %(euh.name, euh.mgt_ip, euh.intfs)
	

class NODInfo:
	
	def __init__(self, mgt_ip, intfs):
		self.mgt_ip = mgt_ip
		self.intfs = intfs
		self.name = None

if __name__ == '__main__':
	parser = MappingParserOFELIA("ofelia_mapping.map")
	parser.load_info()
	net = []
	mgmtnet = (IPv4Network(parser.mgmtnet))
	ipnet = (IPv4Network(parser.ipnet))
	"""testbednet = (IPv4Network(parser.testbednet))
	loopbacknet = (IPv4Network(parser.loopbacknet))
	if ipnet.overlaps(mgmtnet):
		print "Overlap Among IPNet and ManagementNet"
		print "Calculating Available IP network"
		DONE = False
		iternets = ipnet.address_exclude(mgmtnet)
		iternets24 = iternets.next().subnets(new_prefix=24)
		while DONE == False :	
			try:						
				try:
					net = iternets24.next()
					print net
				except StopIteration:
					print "Error Change SuperSubnet"
					sleep(5)
					iternets24 = iternets.next().subnets(new_prefix=24)
			except StopIteration:
				print "Error IP Net SoldOut"
				sys.exit(-2)
		
	if testbednet.overlaps(mgmtnet):
		print "Overlap Among TestbedNet and ManagementNet"
		print "Calculating Available Testbed IP"
		DONE = False
		iternets = testbednet.address_exclude(mgmtnet)
		iterhosts = iternets.next().hosts()
		while DONE == False :	
			try:						
				try:
					host = iterhosts.next()
					while "192.168.0" in host.__str__():
						host = iterhosts.next()
					print host
					print host.
				except StopIteration:
					print "Error Change SuperSubnet"
					iternets2 = list(testbednet.address_exclude(mgmtnet))
					print iternets2
					sleep(5)
					iterhosts = iternets.next().hosts()
			except StopIteration:
				print "Error IP Testbed SoldOut"
				sys.exit(-2)
	if loopbacknet.overlaps(mgmtnet):
		print "Overlap Among LoopbackNet and ManagementNet"
		print "Calculating Available Loopback IP"
		DONE = False
		iternets = loopbacknet.address_exclude(mgmtnet)
		iterloopbacks = iternets.next().hosts()
		while DONE == False :	
			try:						
				try:
					loopback = iterloopbacks.next()
					print loopback
				except StopIteration:
					print "Error Change SuperSubnet"
					iternets2 = list(loopbacknet.address_exclude(mgmtnet))
					print iternets2
					sleep(5)
					iterloopbacks = iternets.next().hosts()
			except StopIteration:
				print "Error IP Loopback SoldOut"
				sys.exit(-2)
	"""
	iternets = list(ipnet.subnets(new_prefix=24))
	iternets24 = list(ipnet.subnets(new_prefix=24).next().subnets(new_prefix=24))
	print iternets[0]
	print iternets24[0]



