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
# XXX Depends Dreamer-Setup-Script

import os
import json
import sys
from netaddr import *
from ipaddress import *
from time import sleep

class MappingParser(object):

	base_path = "./mapping/"
	
	def __init__(self, path_json, verbose=False):
		self.verbose = verbose
		self.vlan = None
		self.user = None
		self.pwd = None
		self.euhs = []
		self.l2sws = []
		path_json = "%s%s" % (self.base_path, path_json)
		if self.verbose:
			print "*** MappingParser.__init__:"
		if os.path.exists(path_json) == False:
			print "Error Mapping File %s Not Found" % path_json
			sys.exit(-2)
		json_file=open(path_json)
		self.json_data = json.load(json_file)
		json_file.close()
		if self.verbose:
			print "*** JSON Data Loaded:"
			print json.dumps(self.json_data, sort_keys=True, indent=4)	
	
	# Parse Function, retrieves from json data: the oshi info,
	# then the aoshi info, finally the euhs info.
	def parse_data(self):
		self.load_info()
	
	def getNodesInfo(self):
		raise NotImplementedError("Abstract Method")

	def load_info(self):
		if self.verbose:
			print "*** Retrieve General Data"
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
		
		if self.verbose:
			print "*** Retrieve Nodes"
		if 'euh' in self.json_data:
			euhos = self.json_data['euh']
			for euh in euhos:
				self.euhs.append(NODInfo(euh[0], euh[1]))
		if 'l2sw' in self.json_data:
			l2swos = self.json_data['l2sw']
			for l2sw in l2swos:
				self.l2sws.append(NODInfo(l2sw[0], l2sw[1]))

		if self.verbose:		
			print "*** EUH:"
			for euh in self.euhs:
				print "*** Name %s - Mgt IP %s - Intfs %s" %(euh.name, euh.mgt_ip, euh.intfs)
		if self.verbose:		
			print "*** L2SW:"
			for l2sw in self.l2sws:
				print "*** Name %s - Mgt IP %s - Intfs %s" %(l2sw.name, l2sw.mgt_ip, l2sw.intfs)

class MappingParserRouterTestbed(MappingParser):

	# Init Function, load json_data from path_json
	def __init__(self, path_json="goff_mapping.map", verbose=False):
		MappingParser.__init__(self, path_json, verbose)
		self.routers = []
		if self.verbose:
			print "*** MappingParserGOFF.__init__:"

	def load_info(self):
		MappingParser.load_info(self)
		if 'router' in self.json_data:
			routers = self.json_data['router']
			for router in routers:
				self.routers.append(NODInfo(router[0], router[1]))

		if self.verbose:		
			print "*** Router:"
			for router in self.routers:
				print "*** Name %s - Mgt IP %s - Intfs %s" %(router.name, router.mgt_ip, router.intfs)

	def getNodesInfo(self):
		self.parse_data()
		return (self.routers, self.l2sws, self.euhs)

	

class MappingParserOSHITestbed(MappingParser):

	# Init Function, load json_data from path_json
	def __init__(self, path_json="goff_mapping.map", verbose=False):
		MappingParser.__init__(self, path_json, verbose)
		self.oshis = []
		self.aoshis = []
		self.ctrls = []
		if self.verbose:
			print "*** MappingParserOSHI.__init__:"

	def load_info(self):
		MappingParser.load_info(self)
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

	def getNodesInfo(self):
		self.parse_data()
		return (self.oshis, self.aoshis, self.l2sws, self.ctrls, self.euhs)

		

class NODInfo:
	
	def __init__(self, mgt_ip, intfs):
		self.mgt_ip = mgt_ip
		self.intfs = intfs
		self.name = None
