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
	
	def __init__(self, typeof, value):
		self.type = typeof
		self.value = value

class CoexA(CoexistenceMechanism):
	
	def __init__(self, value):
		if value > 4095:
			print "Error VLAN ID Not Valid"
			sys.exit(-1)
		CoexistenceMechanism.__init__(self, "COEXA", value)
	
	def serialize(self):
		return "declare -a COEX=(%s %s)\n" % (self.type, self.value)


class CoexB(CoexistenceMechanism):
	
	def __init__(self):
		CoexistenceMechanism.__init__(self, "COEXB", 0)

	def serialize(self):
		return "declare -a COEX=(%s %s)\n" % (self.type, self.value)
