#!/usr/bin/python

import os
import json
import sys

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
			print "*** Error No vlan Data"
			sys.exit(-2)
		self.vlan = self.json_data['vlan']
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

