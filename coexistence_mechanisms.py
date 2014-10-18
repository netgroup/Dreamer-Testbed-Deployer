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
# Coexistence mechanisms.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
# XXX Depends On Dreamer-Setup-Script

import sys

class CoexistenceMechanism (object):

	prio_std_rules = 300
	prio_special_rules = 301
	prio_max = 32768
	
	def __init__(self, eths, vis, name, typeof):
		self.eths = eths
		self.vis = vis
		self.name = name
		self.type = typeof

class CoexA(CoexistenceMechanism):

	tableIP = 1
	tableSBP = 0
	
	def __init__(self, vlan_id, eths, vis, name):
		if vlan_id > 4095:
			print("ERROR VLAN ID Not Valid\n")
			sys.exit(-2)
		self.vlanIP = vlan_id
		CoexistenceMechanism.__init__(self, eths, vis, name, "COEXA")

	def serialize(self):
		return "declare -a COEX=(%s %s)\n" % (self.type, self.vlanIP)	

	def serializeRules(self):

		rules = ""

		rules = rules + 'ovs-ofctl add-flow %s "table=0,hard_timeout=0,priority=%s,dl_vlan=%s,actions=resubmit(,%s)"\n' %(self.name, 
		self.prio_std_rules, self.vlanIP, self.tableIP)
		
		for eth, vi in zip(self.eths, self.vis):
			rules = rules + 'ovs-ofctl add-flow %s "table=%s,hard_timeout=0,priority=%s,in_port=%s,action=output:%s"\n' %(self.name, self.tableIP, 
			self.prio_std_rules, eth, vi)
			rules = rules + 'ovs-ofctl add-flow %s "table=%s,hard_timeout=0,priority=%s,in_port=%s,action=output:%s"\n' %(self.name, self.tableIP, 
			self.prio_std_rules, vi, eth)
    	
		rules = rules + 'ovs-ofctl add-flow %s "table=%s,hard_timeout=0,priority=%s,dl_type=0x88cc,action=controller"\n' %(self.name, self.tableIP, 
		self.prio_special_rules)
		rules = rules + 'ovs-ofctl add-flow %s "table=%s,hard_timeout=0,priority=%s,dl_type=0x8942,action=controller"\n' %(self.name, self.tableIP, 
		self.prio_special_rules)

		return rules

class CoexA_13(CoexA):

	
	def __init__(self, vlan_id, eths, vis, name):
		CoexA.__init__(self, vlan_id, eths, vis, name)
	
	def serializeRules(self):

		rules = ""

		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=0,hard_timeout=0,priority=%s,dl_vlan=%s,actions=goto_table:%s"\n' %(self.name, 
		self.prio_std_rules, self.vlanIP, self.tableIP)
		
		for eth, vi in zip(self.eths, self.vis):
			rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=%s,hard_timeout=0,priority=%s,in_port=%s,action=output:%s"\n' %(self.name, 
			self.tableIP, self.prio_std_rules, eth, vi)
			rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=%s,hard_timeout=0,priority=%s,in_port=%s,action=output:%s"\n' %(self.name, 
			self.tableIP, self.prio_std_rules, vi, eth)
    	
		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=%s,hard_timeout=0,priority=%s,dl_type=0x88cc,action=controller"\n' %(self.name, 
		self.tableIP, self.prio_special_rules)
		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=%s,hard_timeout=0,priority=%s,dl_type=0x8942,action=controller"\n' %(self.name, 
		self.tableIP, self.prio_special_rules)

		return rules

class CoexB(CoexistenceMechanism):
	
	tableIP = 1
	tableSBP = 0	

	def __init__(self, eths, vis, name):
		CoexistenceMechanism.__init__(self, eths, vis, name, "COEXB")

	def serialize(self):
		return "declare -a COEX=(%s %s)\n" % (self.type, 0)

	def serializeRules(self):

		rules = ""

		rules = rules + 'ovs-ofctl add-flow %s "table=0,hard_timeout=0,priority=%s,dl_vlan=%s,actions=resubmit(,%s)"\n' %(self.name, self.prio_std_rules,
		"0xffff", self.tableIP)

		for eth, vi in zip(self.eths, self.vis):
			rules = rules + 'ovs-ofctl add-flow %s "table=%s,hard_timeout=0,priority=%s,in_port=%s,action=output:%s"\n' %(self.name, self.tableIP, 
			self.prio_std_rules, eth, vi)
			rules = rules + 'ovs-ofctl add-flow %s "table=%s,hard_timeout=0,priority=%s,in_port=%s,action=output:%s"\n' %(self.name, self.tableIP, 
			self.prio_std_rules, vi, eth)

		rules = rules + 'ovs-ofctl add-flow %s "table=%s,hard_timeout=0,priority=%s,dl_type=0x88cc,action=controller"\n' %(self.name, self.tableIP, 
		self.prio_special_rules)
		rules = rules + 'ovs-ofctl add-flow %s "table=%s,hard_timeout=0,priority=%s,dl_type=0x8942,action=controller"\n' %(self.name, self.tableIP, 
		self.prio_special_rules)		

		return rules

class CoexB_13(CoexB):
		
	def __init__(self, eths, vis, name):
		CoexB.__init__(self, eths, vis, name)

	def serializeRules(self):

		rules = ""

		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=0,hard_timeout=0,priority=%s,dl_vlan=%s,actions=goto_table:%s"\n' %(self.name, 
		self.prio_std_rules, "0xffff", self.tableIP)

		for eth, vi in zip(self.eths, self.vis):
			rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=%s,hard_timeout=0,priority=%s,in_port=%s,action=output:%s"\n' %(self.name, 
			self.tableIP, self.prio_std_rules, eth, vi)
			rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=%s,hard_timeout=0,priority=%s,in_port=%s,action=output:%s"\n' %(self.name, 
			self.tableIP, self.prio_std_rules, vi, eth)

		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=%s,hard_timeout=0,priority=%s,dl_type=0x88cc,action=controller"\n' %(self.name, 
		self.tableIP, self.prio_special_rules)
		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=%s,hard_timeout=0,priority=%s,dl_type=0x8942,action=controller"\n' %(self.name, 
		self.tableIP, self.prio_special_rules)		

		return rules

class CoexH(CoexistenceMechanism):
	
	tableIP=0
	tableSBP = 1
	MPLS_UNICAST = "0x8847"
	MPLS_MULTICAST = "0x8848"

	def __init__(self, eths, vis, name):
		CoexistenceMechanism.__init__(self, eths, vis, name, "COEXH")

	def serialize(self):
		return "declare -a COEX=(%s %s)\n" % (self.type, 0)

	def serializeRules(self):

		rules = ""

		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=0,hard_timeout=0,priority=%s,dl_type=%s,actions=goto_table:%s"\n' %(self.name, 
		self.prio_max, self.MPLS_UNICAST, self.tableSBP)
		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=0,hard_timeout=0,priority=%s,dl_type=%s,actions=goto_table:%s"\n' %(self.name, 
		self.prio_max, self.MPLS_MULTICAST, self.tableSBP)

		for eth, vi in zip(self.eths, self.vis):
			rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=0,hard_timeout=0,priority=%s,in_port=%s,action=output:%s"\n' %(self.name, 
			self.prio_std_rules, eth, vi)
			rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=0,hard_timeout=0,priority=%s,in_port=%s,action=output:%s"\n' %(self.name, 
			self.prio_std_rules, vi, eth)

		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=0,hard_timeout=0,priority=%s,dl_type=0x88cc,action=controller"\n' %(self.name, 
		self.prio_special_rules)
		rules = rules + 'ovs-ofctl -O OpenFlow13 add-flow %s "table=0,hard_timeout=0,priority=%s,dl_type=0x8942,action=controller"\n' %(self.name,
		self.prio_special_rules)		

		return rules

class CoexFactory(object):

	coex_types=["COEXA", "COEXB", "COEXH"]

	def getCoex(self, coex_type, coex_data, in_eths, in_vis, name, OF_V):
		if coex_type not in self.coex_types:
			print("ERROR %s not supported" % coex_type)
			sys.exit(-2)

		eths = []
		vis = []
		
		for i in range(0, len(in_eths)):

			eths.append(in_eths[i].name)
			vis.append(in_vis[i].name)

			# Because the PW access is different
			if i >= len(in_vis):		
				break				

		if coex_type == "COEXA":
			if OF_V == None:
				return CoexA(coex_data, eths, vis, name)
			elif OF_V == "OpenFlow13":
				return CoexA_13(coex_data, eths, vis, name)

		if coex_type == "COEXB":
			if OF_V == None:
				return CoexB(eths, vis, name)
			elif OF_V == "OpenFlow13":
				return CoexB_13(eths, vis, name)

		if coex_type == "COEXH":
			if OF_V == None:
				print("ERROR %s is not supported with OpenFlow 1.0" % coex_type)
				sys.exit(-2)
			elif OF_V == "OpenFlow13":
				return CoexH(eths, vis, name)
