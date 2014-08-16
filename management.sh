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
# DSH groups of machine, each line is a group of machines
################################################################ ISTRUCTIONS END ###############################################################
declare -a DSH_GROUPS=(ROUTER EUH L2SW)
declare -a ROUTER=(10.216.33.175 10.216.33.176 10.216.33.177)
declare -a EUH=(10.216.33.179 10.216.33.180 10.216.33.181)
declare -a L2SW=()
declare -a NODE_LIST=(10.216.33.181 10.216.33.179 10.216.33.180 10.216.33.176 10.216.33.177 10.216.33.175)
