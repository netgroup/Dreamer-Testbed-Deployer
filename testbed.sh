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
TESTBED=GOFF
TUNNELING=VXLAN
declare -a COEX=(COEXH 0)
# general configuration - end
# 62.40.110.149 - start
HOST=cro4
ROUTERPWD=dreamer
DPID=00000000AC100001
SLICEVLAN=700
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.6.1 6633)
declare -a LOOPBACK=(172.16.0.1/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.1 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3)
declare -a tap1=(5 endip1)
declare -a tap2=(8 endip2)
declare -a tap3=(9 endip3)
declare -a endip1=(192.168.1.5 eth1)
declare -a endip2=(192.168.1.2 eth1)
declare -a endip3=(192.168.1.4 eth1)
declare -a VI=(vi1 vi2 vi3)
declare -a vi1=(10.0.4.2/24 1 5)
declare -a vi2=(10.0.7.1/24 1 5)
declare -a vi3=(10.0.8.1/24 1 5)
declare -a OSPFNET=(NET1 NET2 NET3 NET4)
declare -a NET1=(172.16.0.1/32 0.0.0.0)
declare -a NET2=(10.0.4.0/24 0.0.0.0)
declare -a NET3=(10.0.7.0/24 0.0.0.0)
declare -a NET4=(10.0.8.0/24 0.0.0.0)
# 62.40.110.149 - end
# 62.40.110.16 - start
HOST=cro2
ROUTERPWD=dreamer
DPID=00000000AC100002
SLICEVLAN=700
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.6.1 6633)
declare -a LOOPBACK=(172.16.0.2/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.2 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3 tap4 tap5)
declare -a tap1=(2 endip1)
declare -a tap2=(4 endip2)
declare -a tap3=(6 endip3)
declare -a tap4=(7 endip4)
declare -a tap5=(8 endip5)
declare -a endip1=(192.168.1.5 eth1)
declare -a endip2=(192.168.1.4 eth1)
declare -a endip3=(192.168.1.3 eth1)
declare -a endip4=(192.168.1.6 eth1)
declare -a endip5=(192.168.1.1 eth1)
declare -a VI=(vi1 vi2 vi3 vi4 vi5)
declare -a vi1=(10.0.1.2/24 1 5)
declare -a vi2=(10.0.3.1/24 1 5)
declare -a vi3=(10.0.5.2/24 1 5)
declare -a vi4=(10.0.6.2/24 1 5)
declare -a vi5=(10.0.7.2/24 1 5)
declare -a OSPFNET=(NET1 NET2 NET3 NET4 NET5 NET6)
declare -a NET1=(172.16.0.2/32 0.0.0.0)
declare -a NET2=(10.0.1.0/24 0.0.0.0)
declare -a NET3=(10.0.3.0/24 0.0.0.0)
declare -a NET4=(10.0.5.0/24 0.0.0.0)
declare -a NET5=(10.0.6.0/24 0.0.0.0)
declare -a NET6=(10.0.7.0/24 0.0.0.0)
# 62.40.110.16 - end
# 62.40.110.49 - start
HOST=cro1
ROUTERPWD=dreamer
DPID=00000000AC100003
SLICEVLAN=700
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.6.1 6633)
declare -a LOOPBACK=(172.16.0.3/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.3 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3)
declare -a tap1=(1 endip1)
declare -a tap2=(3 endip2)
declare -a tap3=(6 endip3)
declare -a endip1=(192.168.1.4 eth1)
declare -a endip2=(192.168.1.5 eth1)
declare -a endip3=(192.168.1.2 eth1)
declare -a VI=(vi1 vi2 vi3)
declare -a vi1=(10.0.0.1/24 1 5)
declare -a vi2=(10.0.2.2/24 1 5)
declare -a vi3=(10.0.5.1/24 1 5)
declare -a OSPFNET=(NET1 NET2 NET3 NET4)
declare -a NET1=(172.16.0.3/32 0.0.0.0)
declare -a NET2=(10.0.0.0/24 0.0.0.0)
declare -a NET3=(10.0.2.0/24 0.0.0.0)
declare -a NET4=(10.0.5.0/24 0.0.0.0)
# 62.40.110.49 - end
# 62.40.110.8 - start
HOST=peo5
ROUTERPWD=dreamer
DPID=00000000AC100004
SLICEVLAN=700
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.6.1 6633)
declare -a LOOPBACK=(172.16.0.4/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.4 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3 tap4 tap5 tap6)
declare -a tap1=(1 endip1)
declare -a tap2=(4 endip2)
declare -a tap3=(9 endip3)
declare -a tap4=(12 endip4)
declare -a tap5=(14 endip5)
declare -a tap6=(16 endip6)
declare -a PWTAP=(pwtap1 pwtap2)
declare -a pwtap1=(20 endip7)
declare -a pwtap2=(22 endip8)
declare -a endip1=(192.168.1.3 eth1)
declare -a endip2=(192.168.1.2 eth1)
declare -a endip3=(192.168.1.1 eth1)
declare -a endip4=(192.168.1.7 eth1)
declare -a endip5=(192.168.1.7 eth1)
declare -a endip6=(192.168.1.7 eth1)
declare -a endip7=(192.168.1.7 eth1)
declare -a endip8=(192.168.1.7 eth1)
declare -a VI=(vi1 vi2 vi3 vi4 vi5 vi6)
declare -a vi1=(10.0.0.2/24 1 5)
declare -a vi2=(10.0.3.2/24 1 5)
declare -a vi3=(10.0.8.2/24 1 5)
declare -a vi4=(10.0.11.2/24 1 5)
declare -a vi5=(0.0.0.0/32 1 60)
declare -a vi6=(0.0.0.0/32 1 60)
declare -a OSPFNET=(NET1 NET2 NET3 NET4 NET5)
declare -a NET1=(172.16.0.4/32 0.0.0.0)
declare -a NET2=(10.0.0.0/24 0.0.0.0)
declare -a NET3=(10.0.3.0/24 0.0.0.0)
declare -a NET4=(10.0.8.0/24 0.0.0.0)
declare -a NET5=(10.0.11.0/24 0.0.0.0)
# 62.40.110.8 - end
# 62.40.110.47 - start
HOST=peo3
ROUTERPWD=dreamer
DPID=00000000AC100005
SLICEVLAN=700
BRIDGENAME=br-dreamer
declare -a CTRL=(CTRL1)
declare -a CTRL1=(10.0.6.1 6633)
declare -a LOOPBACK=(172.16.0.5/32 1 1)
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.5 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3 tap4 tap5 tap6 tap7 tap8 tap9)
declare -a tap1=(2 endip1)
declare -a tap2=(3 endip2)
declare -a tap3=(5 endip3)
declare -a tap4=(10 endip4)
declare -a tap5=(11 endip5)
declare -a tap6=(13 endip6)
declare -a tap7=(15 endip7)
declare -a tap8=(17 endip8)
declare -a tap9=(18 endip9)
declare -a PWTAP=(pwtap1 pwtap2 pwtap3 pwtap4)
declare -a pwtap1=(19 endip10)
declare -a pwtap2=(21 endip11)
declare -a pwtap3=(23 endip12)
declare -a pwtap4=(24 endip13)
declare -a endip1=(192.168.1.2 eth1)
declare -a endip2=(192.168.1.3 eth1)
declare -a endip3=(192.168.1.1 eth1)
declare -a endip4=(192.168.1.8 eth1)
declare -a endip5=(192.168.1.9 eth1)
declare -a endip6=(192.168.1.8 eth1)
declare -a endip7=(192.168.1.8 eth1)
declare -a endip8=(192.168.1.9 eth1)
declare -a endip9=(192.168.1.8 eth1)
declare -a endip10=(192.168.1.8 eth1)
declare -a endip11=(192.168.1.8 eth1)
declare -a endip12=(192.168.1.9 eth1)
declare -a endip13=(192.168.1.8 eth1)
declare -a VI=(vi1 vi2 vi3 vi4 vi5 vi6 vi7 vi8 vi9)
declare -a vi1=(10.0.1.1/24 1 5)
declare -a vi2=(10.0.2.1/24 1 5)
declare -a vi3=(10.0.4.1/24 1 5)
declare -a vi4=(10.0.9.2/24 1 5)
declare -a vi5=(10.0.10.2/24 1 5)
declare -a vi6=(0.0.0.0/32 1 60)
declare -a vi7=(0.0.0.0/32 1 60)
declare -a vi8=(0.0.0.0/32 1 60)
declare -a vi9=(0.0.0.0/32 1 60)
declare -a OSPFNET=(NET1 NET2 NET3 NET4 NET5 NET6)
declare -a NET1=(172.16.0.5/32 0.0.0.0)
declare -a NET2=(10.0.1.0/24 0.0.0.0)
declare -a NET3=(10.0.2.0/24 0.0.0.0)
declare -a NET4=(10.0.4.0/24 0.0.0.0)
declare -a NET5=(10.0.9.0/24 0.0.0.0)
declare -a NET6=(10.0.10.0/24 0.0.0.0)
# 62.40.110.47 - end
# 62.40.110.52 - start
HOST=cer6
SLICEVLAN=700
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.7 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3 tap4 tap5)
declare -a tap1=(12 ENDIP1)
declare -a tap2=(14 ENDIP2)
declare -a tap3=(16 ENDIP3)
declare -a tap4=(20 ENDIP4)
declare -a tap5=(22 ENDIP5)
declare -a VI=(vitap1 vitap2 vitap3 vitap4 vitap5)
declare -a vitap1=(10.0.11.1/24)
declare -a vitap2=(10.0.12.2/24)
declare -a vitap3=(10.0.13.2/24)
declare -a vitap4=(10.0.15.2/24)
declare -a vitap5=(10.0.16.2/24)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.11.2 vitap1)
declare -a ENDIP1=(192.168.1.4 eth1)
declare -a ENDIP2=(192.168.1.4 eth1)
declare -a ENDIP3=(192.168.1.4 eth1)
declare -a ENDIP4=(192.168.1.4 eth1)
declare -a ENDIP5=(192.168.1.4 eth1)
# 62.40.110.52 - end
# 62.40.110.20 - start
HOST=cer7
SLICEVLAN=700
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.8 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3 tap4 tap5 tap6 tap7)
declare -a tap1=(10 ENDIP1)
declare -a tap2=(13 ENDIP2)
declare -a tap3=(15 ENDIP3)
declare -a tap4=(18 ENDIP4)
declare -a tap5=(19 ENDIP5)
declare -a tap6=(21 ENDIP6)
declare -a tap7=(24 ENDIP7)
declare -a VI=(vitap1 vitap2 vitap3 vitap4 vitap5 vitap6 vitap7)
declare -a vitap1=(10.0.9.1/24)
declare -a vitap2=(10.0.12.1/24)
declare -a vitap3=(10.0.13.1/24)
declare -a vitap4=(10.0.14.2/24)
declare -a vitap5=(10.0.15.1/24)
declare -a vitap6=(10.0.16.1/24)
declare -a vitap7=(10.0.17.2/24)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.9.2 vitap1)
declare -a ENDIP1=(192.168.1.5 eth1)
declare -a ENDIP2=(192.168.1.5 eth1)
declare -a ENDIP3=(192.168.1.5 eth1)
declare -a ENDIP4=(192.168.1.5 eth1)
declare -a ENDIP5=(192.168.1.5 eth1)
declare -a ENDIP6=(192.168.1.5 eth1)
declare -a ENDIP7=(192.168.1.5 eth1)
# 62.40.110.20 - end
# 62.40.110.153 - start
HOST=cer9
SLICEVLAN=700
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.9 255.255.0.0)
declare -a TAP=(tap1 tap2 tap3)
declare -a tap1=(11 ENDIP1)
declare -a tap2=(17 ENDIP2)
declare -a tap3=(23 ENDIP3)
declare -a VI=(vitap1 vitap2 vitap3)
declare -a vitap1=(10.0.10.1/24)
declare -a vitap2=(10.0.14.1/24)
declare -a vitap3=(10.0.17.1/24)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.10.2 vitap1)
declare -a ENDIP1=(192.168.1.5 eth1)
declare -a ENDIP2=(192.168.1.5 eth1)
declare -a ENDIP3=(192.168.1.5 eth1)
# 62.40.110.153 - end
# 62.40.110.51 - start
HOST=ctr8
SLICEVLAN=700
declare -a INTERFACES=(eth1)
declare -a eth1=(192.168.1.6 255.255.0.0)
declare -a TAP=(tap1)
declare -a tap1=(7 ENDIP1)
declare -a VI=(vitap1)
declare -a vitap1=(10.0.6.1/24)
declare -a STATICROUTE=(10.0.0.0 255.0.0.0 10.0.6.2 vitap1)
declare -a ENDIP1=(192.168.1.2 eth1)
# 62.40.110.51 - end
