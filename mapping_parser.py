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
# Mapping Parser.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
# XXX Depends On Luca Prete Script

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
		self.mgmtgw = None
		self.mgmtintf = None
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
		if 'mgmtgw' not in self.json_data:
			print "*** Error No Management Gateway Data"
			sys.exit(-2)
		self.mgmtgw = self.json_data['mgmtgw']
		if 'mgmtintf' not in self.json_data:
			print "*** Error No Management Interface Data"
			sys.exit(-2)
		self.mgmtintf = self.json_data['mgmtintf']
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
				self.oshis.append(NODInfo(oshi[0], oshi[1], self.mgmtnet, self.mgmtgw, self.mgmtintf))
		if 'access' in self.json_data:
			aoshies = self.json_data['access']
			for aoshi in aoshies:
				self.aoshis.append(NODInfo(aoshi[0], aoshi[1], self.mgmtnet, self.mgmtgw, self.mgmtintf))
		if 'ctrl' in self.json_data:
			controllers = self.json_data['ctrl']
			for controller in controllers:
				self.ctrls.append(NODInfo(controller[0], controller[1], self.mgmtnet, self.mgmtgw, self.mgmtintf))
		if 'euh' in self.json_data:
			euhos = self.json_data['euh']
			for euh in euhos:
				self.euhs.append(NODInfo(euh[0], euh[1], self.mgmtnet, self.mgmtgw, self.mgmtintf))
			
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
	
	def __init__(self, mgt_ip, intfs, mgmtnet, mgmtgw, mgmtintf):
		self.mgt_ip = mgt_ip
		self.intfs = intfs
		self.name = None
		self.mgt_net = mgmtnet
		self.mgt_gw = mgmtgw
		self.mgt_intf = mgmtintf
