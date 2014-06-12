#!/bin/bash
############################################################
##            DREAMER IP/SDN Hyibrid LME rules            ##
##                                                        ##
##      Parameters to be set by the user for the LME      ##
##	    bootstrap configuration process  				  ##
##                                                        ##
############################################################
# HowTO
#
# PLEASE, DO NOT USE WHITE SPACES
#
# Insert here your bootstrap rules, that you want to be pushed by LME
#
# Each line is an Open vSwitch rule 
################################################################ ISTRUCTIONS END ###############################################################
# 10.216.33.175 - start
# COEXA - start
ovs-ofctl add-flow br-dreamer "table=0,hard_timeout=0,priority=300,dl_vlan=1,actions=resubmit(,1)"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap1,action=output:vi1"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,action=output:tap1"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap2,action=output:vi2"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi2,action=output:tap2"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap3,action=output:vi3"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,action=output:tap3"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap4,action=output:vi4"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi4,action=output:tap4"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap5,action=output:vi5"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi5,action=output:tap5"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x88cc,action=controller"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x8942,action=controller"
# COEXA - end
# 10.216.33.175 - end
# 10.216.33.176 - start
# COEXA - start
ovs-ofctl add-flow br-dreamer "table=0,hard_timeout=0,priority=300,dl_vlan=1,actions=resubmit(,1)"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap1,action=output:vi1"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,action=output:tap1"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap2,action=output:vi2"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi2,action=output:tap2"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap3,action=output:vi3"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,action=output:tap3"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap4,action=output:vi4"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi4,action=output:tap4"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap5,action=output:vi5"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi5,action=output:tap5"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap6,action=output:vi6"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi6,action=output:tap6"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x88cc,action=controller"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x8942,action=controller"
# COEXA - end
# INGRB - start
ovs-ofctl add-flow br-dreamer "table=0,hard_timeout=0,priority=300,in_port=tap1,actions=mod_vlan_vid:1,resubmit(,1)"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,actions=strip_vlan,output:tap1"
# INGRB - end
# 10.216.33.176 - end
# 10.216.33.145 - start
# COEXA - start
ovs-ofctl add-flow br-dreamer "table=0,hard_timeout=0,priority=300,dl_vlan=1,actions=resubmit(,1)"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap1,action=output:vi1"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,action=output:tap1"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap2,action=output:vi2"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi2,action=output:tap2"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap3,action=output:vi3"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,action=output:tap3"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap4,action=output:vi4"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi4,action=output:tap4"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap5,action=output:vi5"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi5,action=output:tap5"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x88cc,action=controller"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x8942,action=controller"
# COEXA - end
# INGRB - start
ovs-ofctl add-flow br-dreamer "table=0,hard_timeout=0,priority=300,in_port=tap3,actions=mod_vlan_vid:1,resubmit(,1)"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,actions=strip_vlan,output:tap3"
# INGRB - end
# 10.216.33.145 - end
# 10.216.33.147 - start
# COEXA - start
ovs-ofctl add-flow br-dreamer "table=0,hard_timeout=0,priority=300,dl_vlan=1,actions=resubmit(,1)"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap1,action=output:vi1"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,action=output:tap1"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap2,action=output:vi2"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi2,action=output:tap2"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap3,action=output:vi3"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,action=output:tap3"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap4,action=output:vi4"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi4,action=output:tap4"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap5,action=output:vi5"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi5,action=output:tap5"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x88cc,action=controller"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x8942,action=controller"
# COEXA - end
# INGRB - start
ovs-ofctl add-flow br-dreamer "table=0,hard_timeout=0,priority=300,in_port=tap3,actions=mod_vlan_vid:1,resubmit(,1)"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,actions=strip_vlan,output:tap3"
# INGRB - end
# 10.216.33.147 - end
# 10.216.33.182 - start
# COEXA - start
ovs-ofctl add-flow br-dreamer "table=0,hard_timeout=0,priority=300,dl_vlan=1,actions=resubmit(,1)"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap1,action=output:vi1"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,action=output:tap1"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap2,action=output:vi2"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi2,action=output:tap2"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap3,action=output:vi3"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,action=output:tap3"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap4,action=output:vi4"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi4,action=output:tap4"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap5,action=output:vi5"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi5,action=output:tap5"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x88cc,action=controller"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x8942,action=controller"
# COEXA - end
# INGRB - start
ovs-ofctl add-flow br-dreamer "table=0,hard_timeout=0,priority=300,in_port=tap1,actions=mod_vlan_vid:1,resubmit(,1)"
ovs-ofctl add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,actions=strip_vlan,output:tap1"
# INGRB - end
# 10.216.33.182 - end
