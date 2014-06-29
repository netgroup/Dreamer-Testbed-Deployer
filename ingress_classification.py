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

class IngressClassification (object):
	
	def __init__(self, typeof):
		self.type = typeof

class IngrB(IngressClassification):
	
	def __init__(self, coex, tapintf, viintf):		
		IngressClassification.__init__(self, "INGRB")	
		self.coex = coex
		self.tapintf = tapintf
		self.viintf = viintf

	def serialize(self):
		ret = ""
		if self.coex.type == "COEXA":
			ret = "ovs-ofctl add-flow br-dreamer \"table=0,hard_timeout=0,priority=300,in_port=%s,actions=mod_vlan_vid:%s,resubmit(,1)\"" %(self.tapintf.name, self.coex.value)
			ret = ret + "\n"
			ret = ret + "ovs-ofctl add-flow br-dreamer \"table=1,hard_timeout=0,priority=300,in_port=%s,actions=strip_vlan,output:%s\"" % (self.viintf.name, self.tapintf.name)
			ret =  ret + "\n"
		return ret
