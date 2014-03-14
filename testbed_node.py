#!/usr/bin/python

"""
Based On Mininet API
thanks to: Bob Lantz (rlantz@cs.stanford.edu), Brandon Heller (brandonh@stanford.edu)
thanks to all Dreamer Team, especially to Luca Prete (preteluca@gmail.com) for the bash scripts;

author: Pier Luigi Ventre (pl.ventre@gmail.com)
author: Giuseppe Siracusano (a_siracusano@tin.it)
author: Stefano Salsano (stefano.salsano@uniroma2.it)

"""

from testbed_intf import EthIntf

#TODO Integration with psShell
# TODO Integrity Check, before starting the creation of the testbed.sh
class Oshi:

	loopbackBaseTestbed = [172, 168, 0, 0]
	ipBaseTestbed=[192,168, 0, 0]
	netbitTestbed=16
	netmaskTestbed=[255, 255, 0, 0]

	def __init__( self, NODInfo, vlan):
		self.name = NODInfo.name
		self.dpid = self.defaultDpid()
		self.mgt_ip = NODInfo.mgt_ip
		self.loopback = LoIntf(ip=self.next_loopbackAddress())
		self.eths = []
		self.nameToEths = {}
		self.vlan = vlan
		self.endips = []
		self.nameToEndIps = {}
		self.taps = []
		self.nameToTaps = {}
		self.vis = []
		self.nameToVis = {}
		self.ctrls = []
		
		self.endIPBase = 1
		self.tapBase = 1
		self.viBase = 1
		self.ethIndex = 0
		self.tapPortBase = 1190

		for eth in NODInfo.intfs:
			eth_intf = EthIntf(eth, self.next_testbedAddress(), self.netbitTestbed, self.netmaskTestbed)
			self.eths.append(eth_intf)
			self.nameToEths[eth] = eth_intf

	def defaultDpid( self ):
		"Derive dpid from switch name, s1 -> 1"
		try:
			dpid = int( re.findall( r'\d+', self.name )[ 0 ] )
			dpid = hex( dpid )[ 2: ]
			dpid = '0' * ( self.dpidLen - len( dpid ) ) + dpid
			return dpid
		except IndexError:
			raise Exception( 'Unable to derive default datapath ID - '
							 'please either specify a dpid or use a '
							 'canonical switch name such as s23.' )	
	
	def setControllers(self, controllers):
		for controller in controllers:
			(ip,port) = controller.split(":")
			key = ip + " " + port
			if key in self.ctrls:
				continue
			self.ctrls.append(key)

	def newViName(self):
		ret = self.viBase
		self.viBase = self.viBase + 1
		return ret
	
	def addVi(self, ip, netbit, hello_int, cost):
		name = self.newViName()
		vi = ViIntf(name, ip, netbit, hello_int. cost)
		self.vis.append(vi)
		self.nameToVis[name] = vi
		return vi 		
	
	def newTapName(self):
		ret = self.tapBase
		self.tapBase = self.tapBase + 1
		return ret
	
	def newTapPort(self):
		self.tapPortBase = self.tapPortBase + 1
		return self.tapPortBase
	
	def addTap(self, localport, remoteport, endipname):
		name = self.newTapName()
		tap = TapIntf(name, localport, remoteport, endipname)
		self.taps.append(tap)
		self.nameToTaps[name] = tap
		return tap
 
	def next_eth(self):
		ret = (self.eths[eth_Index].name, self.eths[eth_Index].ip)
		eth_Index = (eth_Index + 1) % len(self.eths) 		
		return ret

	def addEndIP(self, remoteIP, localIntf):
		name = self.newEndIPName()
		endip = EndIP(name, remoteIP, localIntf)
		self.endips.append(endip)
		self.nameToEndIps[name] = endip
		return endip
		
	def newEndIPName(self):
		ret = self.endIPBase
		self.endIPBase = self.endIPBase + 1
		return ret
		
	def next_testbedAddress(self):
		self.ipBaseTestbed[3] = (self.ipBaseTestbed[3] + 1) % 256
		if self.ipBaseTestbed[3] == 0:
			self.ipBaseTestbed[2] = (self.ipBaseTestbed[2] + 1) % 256
		if self.ipBaseTestbed[2] == 255 and self.ipBaseTestbed[3] == 255:
			print "Ip Testbed Address Sold Out"
			sys.exit(-2)
		return "%s.%s.%s.%s" %(self.ipBaseTestbed[0], self.ipBaseTestbed[1], self.ipBaseTestbed[2], self.ipBaseTestbed[3])

	def next_loopbackAddress(self):
		self.loopbackBaseTestbed[3] = (self.loopbackBaseTestbed[3] + 1) % 256
		if self.loopbackBaseTestbed[3] == 0:
			self.loopbackBaseTestbed[2] = (self.loopbackBaseTestbed[2] + 1) % 256
		if self.loopbackBaseTestbed[2] == 255 and self.loopbackBaseTestbed[3] == 255:
			print "Loopback Address Sold Out"
			sys.exit(-2)
		return "%s.%s.%s.%s" %(self.loopbackBaseTestbed[0], self.loopbackBaseTestbed[1], self.loopbackBaseTestbed[2], self.loopbackBaseTestbed[3])

	# XXX Probably we have to change keys
	def controllersSerialization(self):
		i = 1
		names = []
		serialized_line = ""
		for ctrl in self.ctrls:
			name = "ctrl" + str(i)
			names.append(name)
			serialized_line = serialized_line + ("declare -a %s=(%s)\n" %(name, ctrl))			
			i = i + 1			
		ret = "declare -a CTRL=(" + " ".join(names) + ")\n" + serialized_line
		return ret
	
	def ethsSerialization(self):
		return "declare -a INTERFACES=(" + " ".join(self.eths) + ")\n"

	def configure(self):
		testbed = open('testbed.sh','wa')
		testbed.write("# %s - start\n" % self.mgt_ip)
		testbed.write("HOST=%s\n" % self.name)
		testbed.write("ROUTERPWD=dreamer\n")
		testbed.write("DPID=%s\n" % self.dpid)
		testbed.write("SLICEVLAN=%s\n" % self.vlan)
		testbed.write("BRIDGENAME=br-dreamer\n")
		testbed.write(self.controllersSerialization())
		testbed.write(self.loopback.serialize())
		testbed.write("# %s - end\n" % self.mgt_ip)
		testbed.close()

	#def start():

	#def stop():

	#def cmd():
	"""	
		# 10.216.33.133 - start
		HOST=oshi
		ROUTERPWD=dreamer
		SLICEVLAN=200
		BRIDGENAME=br-dreamer
		declare -a CTRL=(10.0.50.25 6633)
		declare -a LOOPBACK=(10.0.100.1/32 15 2)
		declare -a INTERFACES=(eth1 eth2 eth3 eth4)
		declare -a eth1=(192.168.1.11 255.255.0.0)
		declare -a eth2=(192.168.1.12 255.255.0.0)
		declare -a eth3=(192.168.1.13 255.255.0.0)
		declare -a eth4=(192.168.1.14 255.255.0.0)
		declare -a TAP=(tap1 tap2 tap3 tap4)
		declare -a tap1=(1191 1191 endip1)
		declare -a tap2=(1192 1192 endip1)
		declare -a tap3=(1193 1193 endip1)
		declare -a tap4=(1194 1194 endip2)
		declare -a endip1=(192.168.1.21 eth1)
		declare -a endip2=(192.168.1.22 eth2)
		declare -a QUAGGAINT=(vi1 vi2 vi3 vi4)
		declare -a vi1=(10.0.1.1/24 15 2)
		declare -a vi2=(10.0.2.1/24 15 2)
		declare -a vi3=(10.0.3.1/24 15 2)
		declare -a vi4=(10.0.4.1/24 15 2)
		declare -a OSPFNET=(NET1 NET2 NET3 NET4 NET5)
		declare -a NET1=(10.0.1.0/24 0.0.0.0)
		declare -a NET2=(10.0.2.0/24 0.0.0.0)
		declare -a NET3=(10.0.3.0/24 0.0.0.0)
		declare -a NET4=(10.0.4.0/24 0.0.0.0)
		declare -a NET5=(10.0.100.1/32 0.0.0.0)
		# 10.216.33.133 - end
	"""	
	


