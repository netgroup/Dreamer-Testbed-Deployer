#!/usr/bin/python

# Utility Class Store The Set Of Links and Nodes In a Subnet
class Subnet: 
	def __init__(self, Type=None):
		self.nodes = []
		self.links = []
		self.verbose = True
		if Type == None:
			self.type = "CORE"
		else:
			self.type = "ACCESS"

	def appendLink(self, link):
		if link[0] not in self.nodes:
			self.nodes.append(link[0])
		if link[1] not in self.nodes:
			self.nodes.append(link[1])
		if link not in self.links:
			self.links.append(link)

	# Provides the links in a proper order (if the network is "Access"; this order is very important for now in Mininet)
	# the links are ordered, executing a deep-first search on L2Subnet, starting from the AOSHIS,
	# XXX At the end of visit, the links are removed
	def getOrderedLinks(self):
		if self.type == "ACCESS":
			links = self.deep_first_search()
		else:
			links = self.links
		return links

	# Retrieves all the AOS
	def getAOS(self):
		ret_aos = []
		for node in self.nodes:
			if 'aos' in node and node not in ret_aos:
				ret_aos.append(node)
		return ret_aos

	# Executes a deep-first search on L2Subnet
	def deep_first_search(self):
		if self.verbose:
			print "*** Explore Subnet - Type %s: Nodes %s - Links %s" % (self.type, self.nodes, self.links)
		nodes = self.getAOS()
		ret_links = []
		links = []
		while len(nodes) > 0:
			links_to_remove = []
			node = nodes[0]
			(tmpnodes, tmplinks) = self.getOrderedNextLinksAndNodes(node)
			for tmpnode in tmpnodes:
				if tmpnode not in nodes:
					nodes.append(tmpnode)
			for tmplink in tmplinks:
				if tmplink not in links:
					links.append(tmplink)
			for link in links:
				if node in link[0] or node in link[1]:
					ret_links.append(link)
					links_to_remove.append(link)
			nodes.remove(node)
			for toremove in links_to_remove:
				links.remove(toremove)
		return ret_links

	# get Next Hop and links towards the next hop, and pop the node and
	# links from nodes and links before to return
	def getOrderedNextLinksAndNodes(self, node):
		ret_node = []
		ret_link = []
		for link in self.links:
			if node in link[0]:
				ret_node.append(link[1])
				ret_link.append(link)
			elif node in link[1]:
				ret_node.append(link[0])
				ret_link.append(link)
		for link in ret_link:
			self.links.remove(link)
		self.nodes.remove(node)
		return (ret_node, ret_link)

class TestbedSubnet(Subnet):

		def __init__(self, Type=None):
        		Subnet.__init__(self, Type)

		def getOrderedLinks(self):
			print self.nodes			
			links = []
			i = 0			
			for i in range(0, len(self.nodes)):
				for j in range(i+1,len(self.nodes)):
					if 'sw' not in self.nodes[i] and 'sw' not in self.nodes[j]:
						if 'euh' not in self.nodes[i] or 'euh' not in self.nodes[j]:
							links.append((self.nodes[i], self.nodes[j]))
					j = j + 1
				i = i + 1
			self.nodes = []
			self.links = []
			return links
			





