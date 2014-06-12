#!/bin/bash
############################################################
##        DREAMER IP/SDN Hyibrid Management Config        ##
##                                                        ##
##   Parameters to be set by the user for the management  ##
##	 process through Distributed Shell (DSH)			  ##
##                                                        ##
############################################################
# HowTO
#
# PLEASE, DO NOT USE WHITE SPACES
#
# DSH_GROUPS are the active groups in the topology, for example OSHI, EUH, etc.
#
# OSHI are the management IPs of the active machine in the OSHI group
#
# EUH are the the management IPs of the active machine in the EUH group
#
# CTRL are the management IPs of the active machine in the CTRL group
#
# L2SW are the management IPs of the active machine in the L2SW group
#
# ROUTER are the management IPs of the active machine in the ROUTER group
#
# NODE_LIST are the management IPs of the all active machine 
################################################################ ISTRUCTIONS END ###############################################################
declare -a DSH_GROUPS=(OSHI EUH CTRL L2SW)
declare -a OSHI=(10.216.33.175 10.216.33.176 10.216.33.145 10.216.33.147 10.216.33.182)
declare -a EUH=(10.216.33.179 10.216.33.180 10.216.33.181)
declare -a CTRL=(10.216.33.178)
declare -a L2SW=()
declare -a NODE_LIST=(10.216.33.175 10.216.33.180 10.216.33.181 10.216.33.176 10.216.33.179 10.216.33.145 10.216.33.147 10.216.33.182 10.216.33.178)
