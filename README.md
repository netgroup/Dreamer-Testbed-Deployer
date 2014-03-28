![Alt text](repo_data/dreamer-logo.png "Optional title")

Dreamer-Testbed-Deployer
========================

Testbed Deployer For Dreamer Project (GÉANT Open Call)

Using this tool you can "literally" program your Testbed
configuration file. Moreover you can connect in remote to the VM
leveraging the internal CLI or execute remote command on single VM
or on a group of VMs. 

License
=======

This sofware is licensed under the Apache License, Version 2.0.

Information can be found here:
 [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

Tips
==============

Set Environment Variable At The Beginning Of testbed_deployer.py
(vll_path)

When you choose the build of Topology from json file, the topology
must be saved in topo folder

When you use networkx the topo's png is saved in topo.png

In testbed_deployer.py there are usage example of the Testbed Deployer

Testbed Deployer Dependencies
=============================

0) Luca Prete's script

1) networkx + its dependencies

2) pygraphviz

3) matplotlib

Usage
=====

./testbed_deployer.py [-h] [--topology TOPOINFO]

Mininet Deployer

optional arguments:

  -h, --help           show this help message and exit

  --topology TOPOINFO  Topology Info topo:param

		1) topo1:x Deploy A Core Mesh Network

		2) topo2:x Deploy A Core Mesh Network And Simple Access

		3) topo3:file Deploy A Network Taking The Data From JSON File

		4) topo4:file Deploy A Network And Services(TODO) Taking The Data From JSON File 

		5) e_r:x,y Deploy A Network And Preconfigured Services(TODO) Using Random Generation Of Networkx

Todo
=====

1) Deploy Classification Services

2) Deploy VLL Services


