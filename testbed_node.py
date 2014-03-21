#!/usr/bin/python

"""

author: Pier Luigi Ventre (pl.ventre@gmail.com)
author: Giuseppe Siracusano (a_siracusano@tin.it)
author: Stefano Salsano (stefano.salsano@uniroma2.it)

"""
import re
from testbed_intf import Intf, EthIntf, LoIntf, TapIntf, TapIPIntf, ViIntf
from testbed_deployer_utils import EndIP
from testbed_deployer_utils import OSPFNetwork
import sys
import paramiko
from subprocess import Popen

#TODO Integration with psShell
# TODO Integrity Check, before starting the creation of the testbed.sh

class Node:
	
	ipBaseTestbed=[192,168, 1, 0]
	netbitTestbed=16
	netmaskTestbed=[255, 255, 0, 0]
	
	def __init__( self, NODInfo, user, pwd):
		self.name = NODInfo.name
		self.mgt_ip = NODInfo.mgt_ip
		self.eths = []
		self.nameToEths = {}
		self.user = user
		self.pwd = pwd
		self.chan = None
		self.conn = None
		self.process = None
		#self.connect()
		for eth in NODInfo.intfs:
			eth_intf = EthIntf(eth, self.next_testbedAddress(), self.netbitTestbed, self.netmaskTestbed)
			self.eths.append(eth_intf)
			self.nameToEths[eth] = eth_intf

	def next_testbedAddress(self):
		self.ipBaseTestbed[3] = (self.ipBaseTestbed[3] + 1) % 256
		if self.ipBaseTestbed[3] == 0:
			self.ipBaseTestbed[2] = (self.ipBaseTestbed[2] + 1) % 256
		if self.ipBaseTestbed[2] == 255 and self.ipBaseTestbed[3] == 255:
			print "Ip Testbed Address Sold Out"
			sys.exit(-2)
		return "%s.%s.%s.%s" %(self.ipBaseTestbed[0], self.ipBaseTestbed[1], self.ipBaseTestbed[2], self.ipBaseTestbed[3])

	def connect(self):
		self.conn = paramiko.SSHClient()
		self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.conn.connect(self.mgt_ip,username=self.user, password=self.pwd)
		self.chan = self.conn.invoke_shell()
		self.wait_command('', False) 

	def run(self, command, verbose=True):
		buff = ''
		self.chan.send(command+"\r")
		buff = self.wait_command(command, verbose)
		return buff

	def exe(self, command):
		buff = ''
		stdin, stdout, stderr = self.conn.exec_command(command)
		stdin.close()
		for line in stdout.read().splitlines():
			buff+= line+'\n'
		return buff    
        
	def wait_command(self,command, verbose):
		buff = ''
		i = 0
		s = re.compile('[^#]# ')
		u = re.compile('[$] ')
		if (verbose):
			sys.stdout.flush()    
		while not u.search(buff) and not s.search(buff):
			resp = self.chan.recv(9999)
			if (verbose):
				sys.stdout.write(resp)
			buff += resp
		if (verbose):
			sys.stdout.write("\n")
		return buff

	def close(self):
		self.conn.close()
		if self.process:
			self.process.terminate()

	def xterm(self):
		self.process = Popen(['xterm', '-e','sshpass','-p',self.pwd, 'ssh','-o', 'StrictHostKeyChecking=no', self.user+'@'+self.mgt_ip]) 

	def start(self):
		raise NotImplementedError("Abstract Method")

	def stop(self):
		raise NotImplementedError("Abstract Method")

	def configure(self):
		raise NotImplementedError("Abstract Method")

	def addIntf(self, param):
		raise NotImplementedError("Abstract Method")

	def ethsSerialization(self):
		return "declare -a INTERFACES=(" + " ".join("%s" % eth.name for eth in self.eths) + ")\n"

# XXX Static Route could change in future
class Host(Node):

	def __init__( self, NODInfo, vlan, user, pwd):
		Node.__init__(self, NODInfo, user, pwd)
		self.vlan = vlan
		self.endips = []
		self.nameToEndIps = {}
		self.taps = []
		self.staticroutes = []
		self.nameToTaps = {}
		
		self.endIPBase = 1
		self.tapBase = 1
		self.ethIndex = 0
		self.tapPortBase = 1190
	
	def addIntf(self, param):
		if len(param) != 7:
			print "Error Host.addIntf Invalid Parameter"
			sys.exit(-2)
		remote_ip = param[0]
		local_eth = param[1]
		local_port = param[2]
		remote_port =param[3]
		net = param[4]
		tap_ip = param[5]
		self.staticroutes.append(param[6])
		endip = self.addEndIP(remote_ip, local_eth)
		tap = self.addTapIP(local_port, remote_port, endip.name, tap_ip, net.netbitOSPF)
		return (None, tap, None)

	def addEndIP(self, remoteIP, localIntf):
		name = self.newEndIPName().upper()
		endip = EndIP(name, remoteIP, localIntf)
		self.endips.append(endip)
		self.nameToEndIps[name] = endip
		return endip
		
	def newEndIPName(self):
		ret = self.endIPBase
		self.endIPBase = self.endIPBase + 1
		return "endip%s" % ret

	def newTapName(self):
		ret = self.tapBase
		self.tapBase = self.tapBase + 1
		return "tap%s" % ret
	
	def newTapPort(self):
		self.tapPortBase = self.tapPortBase + 1
		return self.tapPortBase
	
	def addTapIP(self, localport, remoteport, endipname, ip, netbit):
		name = self.newTapName()
		tap = TapIPIntf(name, localport, remoteport, endipname, ip, netbit)
		self.taps.append(tap)
		self.nameToTaps[name] = tap
		return tap
	
	def next_eth(self):
		ret = (self.eths[self.ethIndex].name, self.eths[self.ethIndex].ip)
		self.ethIndex = (self.ethIndex + 1) % len(self.eths) 		
		return ret
	
	def tapsSerialization(self):
		return "declare -a TAP=(" + " ".join("%s" % tap.name for tap in self.taps) + ")\n"
	
	def configure(self, ipbase):
		testbed = open('testbed.sh','a')
		testbed.write("# %s - start\n" % self.mgt_ip)
		testbed.write("HOST=%s\n" % self.name)
		testbed.write("SLICEVLAN=%s\n" % self.vlan)
		testbed.write(self.ethsSerialization())
		for eth in self.eths:
			testbed.write(eth.serialize())
		testbed.write(self.tapsSerialization())
		for tap in self.taps:
			testbed.write(tap.serialize())
		ip_and_mask = ipbase.split("/")
		testbed.write("declare -a STATICROUTE=(%s %s %s %s)\n" %(ip_and_mask[0], ip_and_mask[1], self.staticroutes[0], self.taps[0].name))
		for endip in self.endips:
			testbed.write(endip.serialize())
		testbed.write("# %s - end\n" % self.mgt_ip)
		testbed.close()

class Controller(Host):

	def __init__( self, NODInfo, vlan, port, user, pwd):
		Host.__init__(self, NODInfo, vlan, user, pwd)
		self.port = port
		self.ips = []

	def addIP(self, ip):
		if ip not in self.ips:
			self.ips.append(ip)

	def addIntf(self, param):
		ip = param[5]
		self.addIP(ip)
		return Host.addIntf(self, param)

class Oshi(Host):

	loopbackBaseTestbed = [172, 168, 0, 0]
	dpidLen = 16

	def __init__( self, NODInfo, vlan, user, pwd):
		Host.__init__(self, NODInfo, vlan, user, pwd)
		self.dpid = self.defaultDpid()
		self.loopback = LoIntf(ip=self.next_loopbackAddress())
		self.vis = []
		self.nameToVis = {}
		self.ctrls = []
		self.ospfnets = []
		self.nameToNets = {}
		
		self.viBase = 1
		
		self.ospfNetBase = 1
		loopbacknet = OSPFNetwork("fake", "%s/32" % self.loopback.ip )
		self.addOSPFNet(loopbacknet)


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
	
	def setControllers(self, ips, ports):
		for i in range (0, len(ips)):
			key = ips[i] + " " + str(ports[i])
			if key in self.ctrls:
				continue
			self.ctrls.append(key)
	
	def addTap(self, localport, remoteport, endipname):
		name = self.newTapName()
		tap = TapIntf(name, localport, remoteport, endipname)
		self.taps.append(tap)
		self.nameToTaps[name] = tap
		return tap

	def addIntf(self, param):
		if len(param) != 7:
			print "Error Oshi.addIntf Invalid Parameter"
			sys.exit(-2)
		remote_ip = param[0]
		local_eth = param[1]
		local_port = param[2]
		remote_port =param[3]
		ospf_net = param[4]
		vi_ip = param[5]
		endip = self.addEndIP(remote_ip, local_eth)
		tap = self.addTap(local_port, remote_port, endip.name)
		ospf_net = self.addOSPFNet(ospf_net)
		vi = self.addVi(vi_ip, ospf_net.netbitOSPF, ospf_net.hello_int, ospf_net.cost)
		return (vi, tap, ospf_net)

	def addEndIP(self, remoteIP, localIntf):
		name = self.newEndIPName()
		endip = EndIP(name, remoteIP, localIntf)
		self.endips.append(endip)
		self.nameToEndIps[name] = endip
		return endip
	
	def newOSPFNetName(self):
		ret = self.ospfNetBase
		self.ospfNetBase = self.ospfNetBase + 1
		return "NET%s" % ret		
		
	def addOSPFNet(self, net):
		name = self.newOSPFNetName()
		net.name = name
		self.ospfnets.append(net)
		self.nameToNets[name] = net
		return net
	
	def newViName(self):
		ret = self.viBase
		self.viBase = self.viBase + 1
		return "vi%s" % ret
	
	def addVi(self, ip, netbit, hello_int, cost):
		name = self.newViName()
		vi = ViIntf(name, ip, netbit, hello_int, cost)
		self.vis.append(vi)
		self.nameToVis[name] = vi
		return vi 		
	
	def next_loopbackAddress(self):
		self.loopbackBaseTestbed[3] = (self.loopbackBaseTestbed[3] + 1) % 256
		if self.loopbackBaseTestbed[3] == 0:
			self.loopbackBaseTestbed[2] = (self.loopbackBaseTestbed[2] + 1) % 256
		if self.loopbackBaseTestbed[2] == 255 and self.loopbackBaseTestbed[3] == 255:
			print "Loopback Address Sold Out"
			sys.exit(-2)
		return "%s.%s.%s.%s" %(self.loopbackBaseTestbed[0], self.loopbackBaseTestbed[1], self.loopbackBaseTestbed[2], self.loopbackBaseTestbed[3])

	def controllersSerialization(self):
		i = 1
		names = []
		serialized_line = ""
		for ctrl in self.ctrls:
			name = "CTRL" + str(i)
			names.append(name)
			serialized_line = serialized_line + ("declare -a %s=(%s)\n" %(name, ctrl))			
			i = i + 1			
		ret = "declare -a CTRL=(" + " ".join(names) + ")\n" + serialized_line
		return ret

	def visSerialization(self):
		return "declare -a QUAGGAINT=(" + " ".join("%s" % vi.name for vi in self.vis) + ")\n"

	def ospfnetsSerialization(self):
		return "declare -a OSPFNET=(" + " ".join("%s" % net.name for net in self.ospfnets) + ")\n"

	def configure(self, ipbase):
		testbed = open('testbed.sh','a')
		testbed.write("# %s - start\n" % self.mgt_ip)
		testbed.write("HOST=%s\n" % self.name)
		testbed.write("ROUTERPWD=dreamer\n")
		testbed.write("DPID=%s\n" % self.dpid)
		testbed.write("SLICEVLAN=%s\n" % self.vlan)
		testbed.write("BRIDGENAME=br-dreamer\n")
		testbed.write(self.controllersSerialization())
		testbed.write(self.loopback.serialize())
		testbed.write(self.ethsSerialization())
		for eth in self.eths:
			testbed.write(eth.serialize())
		testbed.write(self.tapsSerialization())
		for tap in self.taps:
			testbed.write(tap.serialize())
		for endip in self.endips:
			testbed.write(endip.serialize())
		testbed.write(self.visSerialization())
		for vi in self.vis:
			testbed.write(vi.serialize())
		testbed.write(self.ospfnetsSerialization())
		for net in self.ospfnets:
			testbed.write(net.serialize())
		testbed.write("# %s - end\n" % self.mgt_ip)
		testbed.close()

	# XXX Specific Dreamer Function
	# TODO Check Output In Order To Return False
	# When We Have An Error
	# def start():
	#	self.run("su", False)
        #	self.run("./config.sh")
        #	return True

	# XXX Specific Dreamer Function
	# TODO Check Output In Order To Return False
	# When We Have An Error
	# def stop():
	#	self.run("su", False)
        #	self.run("./clean.sh")
        #	return True

	
	


