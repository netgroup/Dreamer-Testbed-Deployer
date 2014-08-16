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
# Configuration options, each line is a configuration option used by config script
################################################################ ISTRUCTIONS END ###############################################################
# general configuration - start
TESTBED=OFELIA
TUNNELING=OpenVPN
declare -a MGMTNET=(10.216.0.0 255.255.0.0 10.216.32.1 eth0)
# general configuration - end
# 10.216.33.175 - start
HOST=rou1
ROUTERPWD=dreamer
SLICEVLAN=199
declare -a LOOPBACK=(172.16.0.1/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.1 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3)
declare -a tap1=(1191 1191 10.0.0.2/24 1 1 endip1)
declare -a tap2=(1192 1191 10.0.1.2/24 1 1 endip2)
declare -a tap3=(1193 1191 10.0.3.2/24 1 1 endip3)
declare -a endip1=(192.168.1.2 eth1)
declare -a endip2=(192.168.1.3 eth1)
declare -a endip3=(192.168.1.4 eth1)
declare -a OSPFNET=(NET1 NET2 NET3 NET4)
declare -a NET1=(172.16.0.1/32 0.0.0.0)
declare -a NET2=(10.0.0.0/24 0.0.0.0)
declare -a NET3=(10.0.1.0/24 0.0.0.0)
declare -a NET4=(10.0.3.0/24 0.0.0.0)
# 10.216.33.175 - end
# 10.216.33.176 - start
HOST=rou2
ROUTERPWD=dreamer
SLICEVLAN=199
declare -a LOOPBACK=(172.16.0.2/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.2 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3)
declare -a tap1=(1191 1191 10.0.0.1/24 1 1 endip1)
declare -a tap2=(1192 1192 10.0.2.2/24 1 1 endip2)
declare -a tap3=(1193 1191 10.0.4.2/24 1 1 endip3)
declare -a endip1=(192.168.1.1 eth1)
declare -a endip2=(192.168.1.3 eth1)
declare -a endip3=(192.168.1.5 eth1)
declare -a OSPFNET=(NET1 NET2 NET3 NET4)
declare -a NET1=(172.16.0.2/32 0.0.0.0)
declare -a NET2=(10.0.0.0/24 0.0.0.0)
declare -a NET3=(10.0.2.0/24 0.0.0.0)
declare -a NET4=(10.0.4.0/24 0.0.0.0)
# 10.216.33.176 - end
# 10.216.33.177 - start
HOST=rou3
ROUTERPWD=dreamer
SLICEVLAN=199
declare -a LOOPBACK=(172.16.0.3/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.3 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3)
declare -a tap1=(1191 1192 10.0.1.1/24 1 1 endip1)
declare -a tap2=(1192 1192 10.0.2.1/24 1 1 endip2)
declare -a tap3=(1193 1191 10.0.5.2/24 1 1 endip3)
declare -a endip1=(192.168.1.1 eth1)
declare -a endip2=(192.168.1.2 eth1)
declare -a endip3=(192.168.1.6 eth1)
declare -a OSPFNET=(NET1 NET2 NET3 NET4)
declare -a NET1=(172.16.0.3/32 0.0.0.0)
declare -a NET2=(10.0.1.0/24 0.0.0.0)
declare -a NET3=(10.0.2.0/24 0.0.0.0)
declare -a NET4=(10.0.5.0/24 0.0.0.0)
# 10.216.33.177 - end
# 10.216.33.179 - start
HOST=euh4
SLICEVLAN=199
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.4 255.255.0.0)
declare -a TAP=(tap1)
declare -a tap1=(1191 1193 10.0.3.1/24 ENDIP1)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.3.2 tap1)
declare -a ENDIP1=(192.168.1.1 eth1)
# 10.216.33.179 - end
# 10.216.33.180 - start
HOST=euh5
SLICEVLAN=199
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.5 255.255.0.0)
declare -a TAP=(tap1)
declare -a tap1=(1191 1193 10.0.4.1/24 ENDIP1)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.4.2 tap1)
declare -a ENDIP1=(192.168.1.2 eth1)
# 10.216.33.180 - end
# 10.216.33.181 - start
HOST=euh6
SLICEVLAN=199
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.6 255.255.0.0)
declare -a TAP=(tap1)
declare -a tap1=(1191 1193 10.0.5.1/24 ENDIP1)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.5.2 tap1)
declare -a ENDIP1=(192.168.1.3 eth1)
# 10.216.33.181 - end
