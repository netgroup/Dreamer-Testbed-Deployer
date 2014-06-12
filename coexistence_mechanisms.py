#!/usr/bin/python

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
