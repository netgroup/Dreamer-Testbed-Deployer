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
# 10.216.33.176 - start
HOST=osh2
ROUTERPWD=dreamer
DPID=0000000000000002
SLICEVLAN=199
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.0.2 6633)
declare -a LOOPBACK=(172.168.0.2/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.2 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3 tap4 tap5)
declare -a tap1=(1191 1191 endip1)
declare -a tap2=(1192 1193 endip2)
declare -a tap3=(1193 1192 endip3)
declare -a tap4=(1194 1192 endip4)
declare -a tap5=(1195 1192 endip5)
declare -a endip1=(192.168.1.6 eth1)
declare -a endip2=(192.168.1.1 eth1)
declare -a endip3=(192.168.1.3 eth1)
declare -a endip4=(192.168.1.4 eth1)
declare -a endip5=(192.168.1.5 eth1)
declare -a QUAGGAINT=(vi1 vi2 vi3 vi4 vi5)
declare -a vi1=(10.0.0.1/24 1 1)
declare -a vi2=(10.0.3.2/24 1 1)
declare -a vi3=(10.0.4.1/24 1 1)
declare -a vi4=(10.0.5.2/24 1 1)
declare -a vi5=(10.0.7.2/24 1 1)
declare -a OSPFNET=(NET1 NET2 NET3 NET4 NET5 NET6)
declare -a NET1=(172.168.0.2/32 0.0.0.0)
declare -a NET2=(10.0.0.0/24 0.0.0.0)
declare -a NET3=(10.0.3.0/24 0.0.0.0)
declare -a NET4=(10.0.4.0/24 0.0.0.0)
declare -a NET5=(10.0.5.0/24 0.0.0.0)
declare -a NET6=(10.0.7.0/24 0.0.0.0)
# 10.216.33.176 - end
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
declare -a TAP=(tap1 tap2 tap3 tap4)
declare -a tap1=(1191 1191 endip1)
declare -a tap2=(1192 1191 endip2)
declare -a tap3=(1193 1192 endip3)
declare -a tap4=(1194 1191 endip4)
declare -a endip1=(192.168.1.3 eth1)
declare -a endip2=(192.168.1.4 eth1)
declare -a endip3=(192.168.1.2 eth1)
declare -a endip4=(192.168.1.5 eth1)
declare -a QUAGGAINT=(vi1 vi2 vi3 vi4)
declare -a vi1=(10.0.1.2/24 1 1)
declare -a vi2=(10.0.2.1/24 1 1)
declare -a vi3=(10.0.3.1/24 1 1)
declare -a vi4=(10.0.6.2/24 1 1)
declare -a OSPFNET=(NET1 NET2 NET3 NET4 NET5)
declare -a NET1=(172.168.0.1/32 0.0.0.0)
declare -a NET2=(10.0.1.0/24 0.0.0.0)
declare -a NET3=(10.0.2.0/24 0.0.0.0)
declare -a NET4=(10.0.3.0/24 0.0.0.0)
declare -a NET5=(10.0.6.0/24 0.0.0.0)
# 10.216.33.175 - end
# 10.216.33.180 - start
HOST=euh2
SLICEVLAN=199
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.8 255.255.0.0)
declare -a TAP=(tap1 tap2)
declare -a tap1=(1191 1193 10.0.9.2/24 ENDIP1)
declare -a tap2=(1192 1194 10.0.11.1/24 ENDIP2)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.9.1 tap1)
declare -a ENDIP1=(192.168.1.4 eth1)
declare -a ENDIP2=(192.168.1.4 eth1)
# 10.216.33.180 - end
# 10.216.33.181 - start
HOST=euh3
SLICEVLAN=199
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.9 255.255.0.0)
declare -a TAP=(tap1 tap2)
declare -a tap1=(1191 1193 10.0.8.1/24 ENDIP1)
declare -a tap2=(1192 1194 10.0.12.1/24 ENDIP2)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.8.2 tap1)
declare -a ENDIP1=(192.168.1.3 eth1)
declare -a ENDIP2=(192.168.1.3 eth1)
# 10.216.33.181 - end
# 10.216.33.179 - start
HOST=euh1
SLICEVLAN=199
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.7 255.255.0.0)
declare -a TAP=(tap1)
declare -a tap1=(1191 1193 10.0.10.2/24 ENDIP1)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.10.1 tap1)
declare -a ENDIP1=(192.168.1.5 eth1)
# 10.216.33.179 - end
# 10.216.33.145 - start
HOST=aos3
ROUTERPWD=dreamer
DPID=0000000000000003
SLICEVLAN=199
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.0.2 6633)
declare -a LOOPBACK=(172.168.0.3/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.3 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3 tap4)
declare -a tap1=(1191 1191 endip1)
declare -a tap2=(1192 1193 endip2)
declare -a tap3=(1193 1191 endip3)
declare -a tap4=(1194 1192 endip4)
declare -a endip1=(192.168.1.1 eth1)
declare -a endip2=(192.168.1.2 eth1)
declare -a endip3=(192.168.1.9 eth1)
declare -a endip4=(192.168.1.9 eth1)
declare -a QUAGGAINT=(vi1 vi2 vi3 vi4)
declare -a vi1=(10.0.1.1/24 1 1)
declare -a vi2=(10.0.4.2/24 1 1)
declare -a vi3=(10.0.8.2/24 1 1)
declare -a vi4=(10.0.12.2/24 1 1)
declare -a OSPFNET=(NET1 NET2 NET3 NET4 NET5)
declare -a NET1=(172.168.0.3/32 0.0.0.0)
declare -a NET2=(10.0.1.0/24 0.0.0.0)
declare -a NET3=(10.0.4.0/24 0.0.0.0)
declare -a NET4=(10.0.8.0/24 0.0.0.0)
declare -a NET5=(10.0.12.0/24 0.0.0.0)
# 10.216.33.145 - end
# 10.216.33.182 - start
HOST=aos5
ROUTERPWD=dreamer
DPID=0000000000000005
SLICEVLAN=199
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.0.2 6633)
declare -a LOOPBACK=(172.168.0.5/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.5 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3)
declare -a tap1=(1191 1194 endip1)
declare -a tap2=(1192 1195 endip2)
declare -a tap3=(1193 1191 endip3)
declare -a endip1=(192.168.1.1 eth1)
declare -a endip2=(192.168.1.2 eth1)
declare -a endip3=(192.168.1.7 eth1)
declare -a QUAGGAINT=(vi1 vi2 vi3)
declare -a vi1=(10.0.6.1/24 1 1)
declare -a vi2=(10.0.7.1/24 1 1)
declare -a vi3=(10.0.10.1/24 1 1)
declare -a OSPFNET=(NET1 NET2 NET3 NET4)
declare -a NET1=(172.168.0.5/32 0.0.0.0)
declare -a NET2=(10.0.6.0/24 0.0.0.0)
declare -a NET3=(10.0.7.0/24 0.0.0.0)
declare -a NET4=(10.0.10.0/24 0.0.0.0)
# 10.216.33.182 - end
# 10.216.33.147 - start
HOST=aos4
ROUTERPWD=dreamer
DPID=0000000000000004
SLICEVLAN=199
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.0.2 6633)
declare -a LOOPBACK=(172.168.0.4/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.4 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3 tap4)
declare -a tap1=(1191 1192 endip1)
declare -a tap2=(1192 1194 endip2)
declare -a tap3=(1193 1191 endip3)
declare -a tap4=(1194 1192 endip4)
declare -a endip1=(192.168.1.1 eth1)
declare -a endip2=(192.168.1.2 eth1)
declare -a endip3=(192.168.1.8 eth1)
declare -a endip4=(192.168.1.8 eth1)
declare -a QUAGGAINT=(vi1 vi2 vi3 vi4)
declare -a vi1=(10.0.2.2/24 1 1)
declare -a vi2=(10.0.5.1/24 1 1)
declare -a vi3=(10.0.9.1/24 1 1)
declare -a vi4=(10.0.11.2/24 1 1)
declare -a OSPFNET=(NET1 NET2 NET3 NET4 NET5)
declare -a NET1=(172.168.0.4/32 0.0.0.0)
declare -a NET2=(10.0.2.0/24 0.0.0.0)
declare -a NET3=(10.0.5.0/24 0.0.0.0)
declare -a NET4=(10.0.9.0/24 0.0.0.0)
declare -a NET5=(10.0.11.0/24 0.0.0.0)
# 10.216.33.147 - end
# 10.216.33.178 - start
HOST=ctrl1
SLICEVLAN=199
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.6 255.255.0.0)
declare -a TAP=(tap1)
declare -a tap1=(1191 1191 10.0.0.2/24 ENDIP1)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.0.1 tap1)
declare -a ENDIP1=(192.168.1.2 eth1)
# 10.216.33.178 - end
