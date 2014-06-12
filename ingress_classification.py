#!/usr/bin/python

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
