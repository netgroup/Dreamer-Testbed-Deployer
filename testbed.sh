#!/bin/bash
############################################################
##            DREAMER IP/SDN Hyibrid node param           ##
##                                                        ##
##   Parameters to be set by the user for config process  ##
##                                                        ##
############################################################
# HowTO
#
# PLEASE, DO NOT USE WHITE SPACES
#
# General Configuration Section
#
# TESTEBED - type of testbed - i.e. OFELIA or GOFF
#
# TUNNELING - type of tunneling mechanism - i.e. OpenVPN or VXLAN
#
# COEX - parameters of coexistence mechanism - NECESSARY FOR OSHI
# First parameter -> Type - i.e COEXA or COEXB
# Second parameter -> Data - i.e VLAN tag for IP in the case of COEXA, 0 for COEXB
# i.e COEX=(COEXA 15) or COEX=(COEXB 0)
#
# declare -a MGMTNET=(10.216.0.0 255.255.0.0 10.216.32.1 eth0)
# MGMTNET - Parameters of the management network - NECESSARY ONLY FOR OFELIA TESTBED
# First parameter -> Network
# Second parameter -> Mask
# Third parameter -> Testbed default via
# Fourth parameter -> Management interface
#
####################################################################################################################################
#
# Node Specific Section
#
# HOST - machine and router hostname - i.e. oshi
#
# ROUTERPWD - Machine password and quagga router password - i.e. dreamer
#
# DPID - OVS Datapath id - i.e 00000000AC100001
#
# SLICEVLAN - OCF slice VLAN - i.e. 200
#
# BRIDGENAME - OVS bridge name - i.e. br-dreamer
#
# CTRL - Parameters to reach the OpenFlow controller
# First parameter -> OpenFlow controller IP address
# Second parameter -> OpenFlow controller TCP port
# i.e. CTRL=(192.168.0.100 6633)
#
# LOOPBACK - Loopback interface address and subnet, ospf cost, ospf helo interval - i.e. LOOPBACK=(192.168.100.1/32 15 2)
#
# INTERFACES - List of physical interface to be used by the oshi node - Do not specify eth0 (the mngmt interface)
# i.e. INTERFACES=(eth1 eth2 eth3 eth4)
#
# ethX - IP address and netmask to be assigned to each interface specified above into INTERFACES
# i.e. eth1=(192.168.1.1/24)
#
# TAP - List of tap interfaces used to create point-to-point tunnels between end-hosts
# i.e. TAP=(tap1 tap2 tap3 tap4)
#
# tapX - tap interface details. Local tap port, remote tap port, name of variable indicating the ip address to reach and the interface to use (see endipX below) - OpenVPN SCENARIO
# i.e. tapX=(1191 1194 endip1)
#
# tapX - tap interface details. VNI (globally unique), name of variable indicating the ip address to reach and the interface to use (see endipX below)
# i.e. tapX=(1 endip1) - VXLAN SCENARIO
#
# endipX - express the ip address to connect to with a specific tap interface and the local ethernet interface to use to make the connection
# i.e. endipX=(192.168.0.1 eth1)
#
# VI - Define IP virtual interfaces, used for the connection with OVS. They must be the same number of tap interfaces.
# i.e. QUAGGAINT=(vi1 vi2 vi3 vi4)
#
# viX - For each interface specify ip address/netmask, ospf cost and the helo interval
# i.e. vi1=(10.0.0.1/24 15 2)
# 
# vitapX - For each interface specify ip address/netmask - EUH or CTRL nodes
# i.e. vitap1=(10.0.0.1/24)
#
# OSPFNET - List of OSPF networks to be announced (specified below) - i.e. OSPFNET=(NET1 NET2 NET3 NET4)
#
# declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.9.2 vitap1)
#
# STATICROUTE - Default via for the IP network - EUH or CTRL nodes
# First parameter -> Network
# Second parameter -> Mask
# Third parameter -> Gateway
# Fourth parameter -> IP interface
#
# NETX - Details of networks (named and listed above) to be anounced. Specify the network to be announced, the netmask and the OSPF area
# i.e. declare -a net1 - net1=(192.168.0.0/24 0.0.0.0)
################################################################ ISTRUCTIONS END ###############################################################
# general configuration - start
TESTBED=GOFF
TUNNELING=OpenVPN
declare -a COEX=(COEXB 0)
# general configuration - end
# 62.40.110.49 - start
HOST=osh1
ROUTERPWD=dreamer
DPID=00000000AC100001
SLICEVLAN=700
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.3.2 6633)
declare -a LOOPBACK=(172.16.0.1/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.1 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3)
declare -a tap1=(1191 1191 endip1)
declare -a tap2=(1192 1191 endip2)
declare -a tap3=(1193 1191 endip3)
declare -a endip1=(192.168.1.2 eth1)
declare -a endip2=(192.168.1.3 eth1)
declare -a endip3=(192.168.1.5 eth1)
declare -a VI=(vi1 vi2 vi3)
declare -a vi1=(10.0.0.2/24 1 1)
declare -a vi2=(10.0.1.2/24 1 1)
declare -a vi3=(10.0.4.2/24 1 1)
declare -a OSPFNET=(NET1 NET2 NET3 NET4)
declare -a NET1=(172.16.0.1/32 0.0.0.0)
declare -a NET2=(10.0.0.0/24 0.0.0.0)
declare -a NET3=(10.0.1.0/24 0.0.0.0)
declare -a NET4=(10.0.4.0/24 0.0.0.0)
# 62.40.110.49 - end
# 62.40.110.16 - start
HOST=osh2
ROUTERPWD=dreamer
DPID=00000000AC100002
SLICEVLAN=700
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.3.2 6633)
declare -a LOOPBACK=(172.16.0.2/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.2 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3)
declare -a tap1=(1191 1191 endip1)
declare -a tap2=(1192 1192 endip2)
declare -a tap3=(1193 1191 endip3)
declare -a endip1=(192.168.1.1 eth1)
declare -a endip2=(192.168.1.3 eth1)
declare -a endip3=(192.168.1.6 eth1)
declare -a VI=(vi1 vi2 vi3)
declare -a vi1=(10.0.0.1/24 1 1)
declare -a vi2=(10.0.2.2/24 1 1)
declare -a vi3=(10.0.5.2/24 1 1)
declare -a OSPFNET=(NET1 NET2 NET3 NET4)
declare -a NET1=(172.16.0.2/32 0.0.0.0)
declare -a NET2=(10.0.0.0/24 0.0.0.0)
declare -a NET3=(10.0.2.0/24 0.0.0.0)
declare -a NET4=(10.0.5.0/24 0.0.0.0)
# 62.40.110.16 - end
# 62.40.110.149 - start
HOST=osh3
ROUTERPWD=dreamer
DPID=00000000AC100003
SLICEVLAN=700
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.3.2 6633)
declare -a LOOPBACK=(172.16.0.3/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.3 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3 tap4)
declare -a tap1=(1191 1192 endip1)
declare -a tap2=(1192 1192 endip2)
declare -a tap3=(1193 1191 endip3)
declare -a tap4=(1194 1191 endip4)
declare -a endip1=(192.168.1.1 eth1)
declare -a endip2=(192.168.1.2 eth1)
declare -a endip3=(192.168.1.4 eth1)
declare -a endip4=(192.168.1.7 eth1)
declare -a VI=(vi1 vi2 vi3 vi4)
declare -a vi1=(10.0.1.1/24 1 1)
declare -a vi2=(10.0.2.1/24 1 1)
declare -a vi3=(10.0.3.1/24 1 1)
declare -a vi4=(10.0.6.2/24 1 1)
declare -a OSPFNET=(NET1 NET2 NET3 NET4 NET5)
declare -a NET1=(172.16.0.3/32 0.0.0.0)
declare -a NET2=(10.0.1.0/24 0.0.0.0)
declare -a NET3=(10.0.2.0/24 0.0.0.0)
declare -a NET4=(10.0.3.0/24 0.0.0.0)
declare -a NET5=(10.0.6.0/24 0.0.0.0)
# 62.40.110.149 - end
# 62.40.110.45 - start
HOST=aos1
ROUTERPWD=dreamer
DPID=00000000AC100004
SLICEVLAN=700
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.3.2 6633)
declare -a LOOPBACK=(172.16.0.4/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.5 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3)
declare -a tap1=(1191 1193 endip1)
declare -a tap2=(1192 1191 endip2)
declare -a tap3=(1193 1192 endip3)
declare -a endip1=(192.168.1.1 eth1)
declare -a endip2=(192.168.1.8 eth1)
declare -a endip3=(192.168.1.8 eth1)
declare -a VI=(vi1 vi2 vi3)
declare -a vi1=(10.0.4.1/24 1 1)
declare -a vi2=(10.0.7.2/24 1 1)
declare -a vi3=(0.0.0.0/32 1 60)
declare -a OSPFNET=(NET1 NET2 NET3)
declare -a NET1=(172.16.0.4/32 0.0.0.0)
declare -a NET2=(10.0.4.0/24 0.0.0.0)
declare -a NET3=(10.0.7.0/24 0.0.0.0)
# 62.40.110.45 - end
# 62.40.110.8 - start
HOST=aos2
ROUTERPWD=dreamer
DPID=00000000AC100005
SLICEVLAN=700
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.3.2 6633)
declare -a LOOPBACK=(172.16.0.5/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.6 255.255.0.0)
declare -a TAP=(tap1 tap2)
declare -a tap1=(1191 1193 endip1)
declare -a tap2=(1192 1191 endip2)
declare -a endip1=(192.168.1.2 eth1)
declare -a endip2=(192.168.1.9 eth1)
declare -a VI=(vi1 vi2)
declare -a vi1=(10.0.5.1/24 1 1)
declare -a vi2=(10.0.8.2/24 1 1)
declare -a OSPFNET=(NET1 NET2 NET3)
declare -a NET1=(172.16.0.5/32 0.0.0.0)
declare -a NET2=(10.0.5.0/24 0.0.0.0)
declare -a NET3=(10.0.8.0/24 0.0.0.0)
# 62.40.110.8 - end
# 62.40.110.147 - start
HOST=aos3
ROUTERPWD=dreamer
DPID=00000000AC100006
SLICEVLAN=700
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.3.2 6633)
declare -a LOOPBACK=(172.16.0.6/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.7 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3)
declare -a tap1=(1191 1194 endip1)
declare -a tap2=(1192 1191 endip2)
declare -a tap3=(1193 1192 endip3)
declare -a endip1=(192.168.1.3 eth1)
declare -a endip2=(192.168.1.10 eth1)
declare -a endip3=(192.168.1.10 eth1)
declare -a VI=(vi1 vi2 vi3)
declare -a vi1=(10.0.6.1/24 1 1)
declare -a vi2=(10.0.9.2/24 1 1)
declare -a vi3=(0.0.0.0/32 1 60)
declare -a OSPFNET=(NET1 NET2 NET3)
declare -a NET1=(172.16.0.6/32 0.0.0.0)
declare -a NET2=(10.0.6.0/24 0.0.0.0)
declare -a NET3=(10.0.9.0/24 0.0.0.0)
# 62.40.110.147 - end
# 62.40.110.52 - start
HOST=euh1
SLICEVLAN=700
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.8 255.255.0.0)
declare -a TAP=(tap1 tap2)
declare -a tap1=(1191 1192 10.0.7.1/24 ENDIP1)
declare -a tap2=(1192 1193 10.0.10.1/24 ENDIP2)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.7.2 tap1)
declare -a ENDIP1=(192.168.1.5 eth1)
declare -a ENDIP2=(192.168.1.5 eth1)
# 62.40.110.52 - end
# 62.40.110.20 - start
HOST=euh2
SLICEVLAN=700
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.9 255.255.0.0)
declare -a TAP=(tap1)
declare -a tap1=(1191 1192 10.0.8.1/24 ENDIP1)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.8.2 tap1)
declare -a ENDIP1=(192.168.1.6 eth1)
# 62.40.110.20 - end
# 62.40.110.153 - start
HOST=euh3
SLICEVLAN=700
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.10 255.255.0.0)
declare -a TAP=(tap1 tap2)
declare -a tap1=(1191 1192 10.0.9.1/24 ENDIP1)
declare -a tap2=(1192 1193 10.0.10.2/24 ENDIP2)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.9.2 tap1)
declare -a ENDIP1=(192.168.1.7 eth1)
declare -a ENDIP2=(192.168.1.7 eth1)
# 62.40.110.153 - end
# 62.40.110.51 - start
HOST=ctrl1
SLICEVLAN=700
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.4 255.255.0.0)
declare -a TAP=(tap1)
declare -a tap1=(1191 1193 10.0.3.2/24 ENDIP1)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.3.1 tap1)
declare -a ENDIP1=(192.168.1.3 eth1)
# 62.40.110.51 - end
