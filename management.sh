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
declare -a DSH_GROUPS=(OSHI CER CTRL)
declare -a OSHI=(62.40.110.49 62.40.110.16 62.40.110.149 62.40.110.45 62.40.110.8 62.40.110.147)
declare -a CER=(62.40.110.52 62.40.110.20 62.40.110.153)
declare -a CTRL=(62.40.110.51 62.40.110.18)
declare -a NODE_LIST=(62.40.110.8 62.40.110.147 62.40.110.45 62.40.110.149 62.40.110.16 62.40.110.49 62.40.110.20 62.40.110.153 62.40.110.52 62.40.110.18 62.40.110.51)
