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
declare -a OSHI=(62.40.110.49 62.40.110.16 62.40.110.149 62.40.110.45 62.40.110.8 62.40.110.147)
declare -a EUH=(62.40.110.52 62.40.110.20 62.40.110.153)
declare -a CTRL=(62.40.110.51)
declare -a L2SW=()
declare -a NODE_LIST=(62.40.110.16 62.40.110.149 62.40.110.49 62.40.110.20 62.40.110.153 62.40.110.52 62.40.110.45 62.40.110.147 62.40.110.8 62.40.110.51)
