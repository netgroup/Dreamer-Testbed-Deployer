#!/usr/bin/python

class TestbedOFELIA( object ):

	# Init Function
	def __init__( self, path_mapping = "Mapping.json", ipBaseOSPF=[10, 0, 1, 0],
		netbitOSPF=8, ipBaseTestbed=[192,168, 0, 0], netbitTestbed=16, verbose=True):

        self.parser = MappingParserOFELIA(path_mapping, verbose)
	(self.oshinfo, self.aosinfo, self.euhsinfo) = self.parser.getNodesInfo()
	self.vlan = self.parser.vlan
	self.ipBaseOSPF = ipBaseOSPF
	self.netbitOSPF = 8
	self.ipBaseTestbed = ipBaseTestbed
	self.netbitTestbed = 16
	self.verbose = True

        self.oshs = []
        self.aoss = []
	self.euhs = []
	self.controllers = []

        self.nameToNode = {}  # name to Node objects
	
	def addOshi(self, name):

	def addAoshi(self, name):

	def addEuh(self, name):
	



