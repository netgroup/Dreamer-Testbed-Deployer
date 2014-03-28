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
# HOST - machine and router hostname - i.e. oshi
#
# ROUTERPWD - Machine password and quagga router password - i.e. dreamer
#
# SLICEVLAN - OFELIA slice VLAN - i.e. 200
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
# tapX - tap interface details. Local tap port, remote tap port, name of variable indicating the ip address to reach and the interface to use (see endipX below)
# i.e. tapX=(1191 1194 endip1)
#
# endipX - express the ip address to connect to with a specific tap interface and the local ethernet interface to use to make the connection
# i.e. endipX=(192.168.0.1 eth1)
#
# Quagga interfaces - Define quagga virtual interfaces, used for the connection with OVS. They must be the same number of tap interfaces.
# i.e. QUAGGAINT=(vi1 vi2 vi3 vi4)
#
# viX - For each interface specify ip address/netmask, ospf cost and the helo interval
# i.e. vi1=(10.0.0.1/24 15 2)
#
# OSPFNET - List of OSPF networks to be announced (specified below) - i.e. OSPFNET=(NET1 NET2 NET3 NET4)
#
# NETX - Details of networks (named and listed above) to be anounced. Specify the network to be announced, the netmask and the OSPF area
# i.e. declare -a net1 - net1=(192.168.0.0/24 0.0.0.0)
################################################################ ISTRUCTIONS END ###############################################################
# general configuration - start
MGMTNET=10.216.0.0
# general configuration - end
# 10.216.33.175 - start
HOST=osh1
ROUTERPWD=dreamer
DPID=0000000000000001
SLICEVLAN=199
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.0.2 6633)
declare -a LOOPBACK=(172.168.0.1/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.1 255.255.0.0)
declare -a TAP=(tap1 tap2)
declare -a tap1=(1191 1191 endip1)
declare -a tap2=(1192 1191 endip2)
declare -a endip1=(192.168.1.2 eth1)
declare -a endip2=(192.168.1.3 eth1)
declare -a QUAGGAINT=(vi1 vi2)
declare -a vi1=(10.0.0.1/24 1 1)
declare -a vi2=(10.0.1.1/24 1 1)
declare -a OSPFNET=(NET1 NET2 NET3)
declare -a NET1=(172.168.0.1/32 0.0.0.0)
declare -a NET2=(10.0.0.0/24 0.0.0.0)
declare -a NET3=(10.0.1.0/24 0.0.0.0)
# 10.216.33.175 - end
# 10.216.33.178 - start
HOST=ctrl1
SLICEVLAN=199
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.2 255.255.0.0)
declare -a TAP=(tap1)
declare -a tap1=(1191 1191 10.0.0.2/24 ENDIP1)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.0.1 tap1)
declare -a ENDIP1=(192.168.1.1 eth1)
# 10.216.33.178 - end
# 10.216.33.145 - start
HOST=aos4
ROUTERPWD=dreamer
DPID=0000000000000004
SLICEVLAN=199
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.0.2 6633)
declare -a LOOPBACK=(172.168.0.2/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.3 255.255.0.0)
declare -a TAP=(tap1)
declare -a tap1=(1191 1192 endip1)
declare -a endip1=(192.168.1.1 eth1)
declare -a QUAGGAINT=(vi1)
declare -a vi1=(10.0.1.2/24 1 1)
declare -a OSPFNET=(NET1 NET2)
declare -a NET1=(172.168.0.2/32 0.0.0.0)
declare -a NET2=(10.0.1.0/24 0.0.0.0)
# 10.216.33.145 - end
