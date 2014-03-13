#!/usr/bin/python

import os
import json
import sys
from topo_parser_utils import Subnet
from topo_parser_utils import TestbedSubnet

class TopoParser:

	# Init Function, load json_data from path_json
	def __init__(self, path_json, verbose=False):
		self.verbose = verbose
		self.oshis = []
		self.aoshis = []
		self.l2sws = []
		self.euhs = []
		self.pplinks = []
		self.l2links = []
		self.ppsubnets = []
		self.l2subnets = []
		self.subnetclass = Subnet
		if self.verbose:
			print "*** __init__:"
		if os.path.exists(path_json) == False:
			print "Error Topo File Not Found"
			sys.exit(-2)
		json_file=open(path_json)
		self.json_data = json.load(json_file)
		json_file.close()
		if self.verbose:
			print "*** JSON Data Loaded:"
			#print json.dumps(self.json_data, sort_keys=True, indent=4)

	# Parse Function, first retrieves the vertices from json data,
	# second retrieves the links from json data, finally create the
	# subnets (PPsubnet, Core L2Subnet, Access L2Subnet)
	def parse_data(self):
		self.load_vertex()
		self.load_links()
		self.create_subnet()
	
	def getsubnets(self):
		self.parse_data()
		return (self.ppsubnets, self.l2subnets)

	# Parses vertex from json_data, renames the node in 'vertices' and in 'edges', 
	# and divides them in: oshi (Core Oshi), aoshi (Access Oshi), l2sws (Legacy L2 switch)
	# and euhs (End User Host). 
	# TODO Parse Nodes Properties
	def load_vertex(self):
		if self.verbose:
			print "*** Retrieve Vertex"
		vertices = self.json_data['vertices']
		edges = self.json_data['edges']
		for vertex in vertices:
			if 'COSH' in vertex:
				data = vertex.split('#')
				name = "osh" + str(len(self.oshis) + len(self.aoshis) + 1)
				self.oshis.append(name) 
			elif 'AOSH' in vertex:
				data = vertex.split('#')
				name = "aos" + str(len(self.oshis) + len(self.aoshis) + 1)
				self.aoshis.append(name)
			elif 'L2SW' in vertex:
				data = vertex.split('#')
				name = "sw" + str(len(self.l2sws) + 1)
				self.l2sws.append(name)
			elif 'EUH' in vertex:
				data = vertex.split('#')
				name = "euh" + str(len(self.euhs) + 1)
				self.euhs.append(name)
			for edge in edges:
				i = 0
				for side in edge:
					if vertex in side:
						edge[i] = name
					i = i + 1
		if self.verbose:		
			print "*** OSHI:", self.oshis
			print "*** AOSHI:", self.aoshis
			print "*** L2SW:", self.l2sws
			print "*** EUH:", self.euhs

	# Parses link from json_data, then divides them in L2Links (Switched Links)
	# and PPLinks (Point To Point Links)
	# TODO Parse Links Properties
	def load_links(self):
		if self.verbose:
			print "*** Retrieve Links"
		edges = self.json_data['edges']
		for edge in edges:
			if 'sw' in edge[0] or 'sw' in edge[1]:
				self.l2links.append((edge[0], edge[1]))
			else:
				self.pplinks.append((edge[0], edge[1]))
		if self.verbose:
			print "*** L2links:", self.l2links
			print "*** PPlinks:", self.pplinks
	
	# From the parsed Links, creates the associates Subnet, then divides them in
	# L2subnet and PPsubnets
	def create_subnet(self):
		# Creates the ppsubnets
		for pplink in self.pplinks:
			s = self.subnetclass()
			s.appendLink(pplink)
			if 'euh' in pplink[0] or 'euh' in pplink[1]:
				s.type = "ACCESS"
			self.ppsubnets.append(s)
		# Eliminates all links
		self.pplinks = []
		if self.verbose:
			i = 0
			print "*** Subnets:"
			for subnet in self.ppsubnets:
				print "*** PP Subnet(%s) - Type %s: Nodes %s - Links %s" %(i + 1, subnet.type, subnet.nodes, subnet.links)
				i = i + 1
		# Creates the l2subnets
		tmp = []
		for sw in self.l2sws:
			tmp.append(sw)
			s = self.subnetclass()
			while len(tmp) > 0:
				current = tmp[0]
				if 'euh' in current:
					s.type = "ACCESS"
				tmp.pop(0)
				(hops, links) = self.getNextHopAndLinks(current)
				for hop in hops:
					tmp.append(hop)
				for link in links:
					s.appendLink(link)
			if len(s.links) > 0:
				self.l2subnets.append(s)	
		if self.verbose:
			i = 0
			print "*** Subnets:"
			for subnet in self.l2subnets:
				print "*** L2 Subnet(%s) - Type %s: Nodes %s - Links %s" %(i + 1, subnet.type, subnet.nodes, subnet.links)
				i = i + 1

	# Utility Function, provides node's next hop and links (to the nexthop)
	# we use it to rebuild from scratch a l2subnets, XXX it deletes the l2links
	# once we rebuild the subnet
	def getNextHopAndLinks(self,node):
		ret_links = []
		ret_node = []
		tmp = []
		if 'euh' in node or 'aos' in node or 'osh' in node:
			return ([],[])
		for link in self.l2links:
			if link[0] == node or link[1] == node:
				ret_links.append(link)
				if link[0] == node:
					ret_node.append(link[1])
				if link[1] == node:
					ret_node.append(link[0])
				tmp.append(link)
		for link in tmp:
			self.l2links.remove(link)
		return (ret_node, ret_links)

# Parser For Testbed Deployer
class TestbedTopoParser(TopoParser):

		def __init__(self, path_json, verbose=False):
        		TopoParser.__init__(self, path_json, verbose=False)
			self.subnetclass = TestbedSubnet
