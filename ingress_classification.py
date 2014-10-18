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
# Ingress classification functions.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
# XXX Depends On Dreamer-Setup-Script

import sys

class IngressClassification (object):
	
	prio_std_rules = 300
	
	def __init__(self, eth, vi, name, typeof):
		self.eth = eth
		self.vi = vi
		self.name = name
		self.type = typeof

class IngrB_CoexA(IngressClassification):

	tableIP =1

	def __init__(self, eth, vi, coexData, name):
		IngressClassification.__init__(self, eth, vi, name, "INGRB")
		self.vlanIP = coexData
	
	def serialize(self):

		rules = ""
		
		rules = rules + 'ovs-ofctl add-flow %s "table=0,hard_timeout=0,priority=%s,in_port=%s,actions=mod_vlan_vid:%s,resubmit(,%s)"\n' %(self.name, 
		self.prio_std_rules, self.eth, self.vlanIP, self.tableIP)
		rules = rules + 'ovs-ofctl add-flow %s "table=%s,hard_timeout=0,priority=%s,in_port=%s,actions=strip_vlan,output:%s"\n' %(self.name, 
		self.tableIP, self.prio_std_rules, self.vi, self.eth)

		return rules

class IngrB_CoexA_13(IngrB_CoexA):

	def __init__(self, eth, vi, coexData, name):
		IngrB_CoexA.__init__(self, eth, vi, coexData, name)
	
	def serialize(self):

		rules = ""
		
		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=0,hard_timeout=0,priority=%s,in_port=%s,actions=mod_vlan_vid:%s,goto_table:%s"\n' %(self.name, self.prio_std_rules, self.eth, self.vlanIP, self.tableIP)
		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=%s,hard_timeout=0,priority=%s,in_port=%s,actions=strip_vlan,output:%s"\n' %(self.name, self.tableIP, self.prio_std_rules, self.vi, self.eth)

		return rules		

class IngrB_CoexB(IngressClassification):

	def __init__(self, eth, vi, name):
		IngressClassification.__init__(self, eth, vi, name, "INGRB")
	
	def serialize(self):

		rules = ""

		return rules

class IngrB_CoexH(IngressClassification):

	def __init__(self, eth, vi, name):
		IngressClassification.__init__(self, eth, vi, name, "INGRB")
	
	def serialize(self):

		rules = ""

		return rules

class IngressFactory(object):

	coex_types=["COEXA", "COEXB", "COEXH"]
	ingress_types=["INGRB"]

	def getIngr(self, coex_type, coex_data, ingress_type, ingress_data, eth, vi, name, OF_V):

		eth = eth.name
		vi = vi.name

		if coex_type not in self.coex_types:
			print("ERROR %s not supported" % coex_type)
			sys.exit(-2)

		if ingress_type not in self.ingress_types:
			print("ERROR %s not supported" % ingress_type)
			sys.exit(-2)
		
		if coex_type == "COEXA" and ingress_type == "INGRB":
			if OF_V == None:
				return IngrB_CoexA(eth, vi, coex_data, name)
			elif OF_V == "OpenFlow13":
				return IngrB_CoexA_13(eth, vi, coex_data, name)

		if coex_type == "COEXB" and ingress_type == "INGRB":
			return IngrB_CoexB(eth, vi, name)

		if coex_type == "COEXH" and ingress_type == "INGRB":
			if OF_V == None:
				print("ERROR %s is not supported by OpenFlow 1.0" % coex_type)
				sys.exit(-2)
			elif OF_V == "OpenFlow13":
				return IngrB_CoexH(eth, vi, name)
