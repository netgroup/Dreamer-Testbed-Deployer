#!/usr/bin/python

##############################################################################################
# Copyright (C) 2014 Pier Luigi Ventre - (Consortium GARR and University of Rome "Tor Vergata")
# Copyright (C) 2014 Giuseppe Siracusano, Stefano Salsano - (CNIT and University of Rome "Tor Vergata")
# www.garr.it - www.uniroma2.it/netgroup - www.cnit.it
#
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Testbed Deployer CLI.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
# XXX Depends On Dreamer-Setup-Script

import cmd
from testbed_node import Node

class TestbedCLI(cmd.Cmd):
    """ TestbedCLI, run a command on moltiple  hosts """

    prompt = 'testbed > '

    def __init__(self, Testbed):
		cmd.Cmd.__init__(self)
		self.hosts = {}
		for key, value in Testbed.nameToNode.iteritems():
			self.hosts[key] = value 
		self.cmdloop()      

    def do_add_host(self, args):
        """add_host 
        Add the host to the host list"""
        if args:
            self.hosts.update({args.split(',')[3]:Node(args.split(',')[0],args.split(',')[1],args.split(',')[2])})
        else:
            print "usage: host "

    def do_exe(self, command):
        """exe 
        Execute this command on all hosts in the list"""
        if command:
            for node in self.hosts.itervalues():
                print '%s:\n%s' % (node.mgt_ip, node.exe(command))
        else:
            print "usage: exe "

    def do_run(self, command):
        """run 
        Execute/interact this command on all hosts in the list """
        for node in self.hosts.itervalues():
            node.run(command) 
            
    def do_close(self,args):
        for node in self.hosts.itervalues():
            node.close()

    def do_list(self, args):
        """list 
        print the name of all hosts in the list """
        for node,obj in self.hosts.iteritems():
            print node,obj.mgt_ip 

    def do_EOF(self, line):
        for node in self.hosts.itervalues():
            node.close()
        print 
        return True

    def do_xterm(self,args):
        """xterm  
        in all hosts in the list """
        if args.split(" ")[0] == 'all':
            for node in self.hosts.itervalues():
                node.xterm()
        else:       
            for arg in args.split(" "):
                if arg in self.hosts:
                    self.hosts[arg].xterm()
                
    def do_on(self,args):
        """on  
        run/exe command on a set of nodes 
        usage : on [node0,node1] run ls
        """
        arg = args.split(" ")
        if '[' and ']'in arg[0]:
            nodes = arg[0].replace('[','').replace(']','').split(',')
        else:
            print "usage: on"
            return 
        
        for node in nodes:
            if node in self.hosts:
                if arg[1] == 'run':
                    self.hosts[node].run(args.replace(arg[0]+' run ',''))
                elif arg[1] == 'exe':
                    print self.hosts[node].exe(args.replace(arg[0]+' exe ',''))

    def do_oshi_start(self,args):
        """oshi_start 
        Execute config.sh in all hosts in the list """
	raise NotImplementedError("For Now Not Implemented")
        # for node in self.hosts.itervalues():
        #    node.start()


    def do_oshi_stop(self,args):
        """oshi_stop 
        Stop... in all hosts in the list """
	raise NotImplementedError("For Now Not Implemented")
        # for node in self.hosts.itervalues():
        #    node.stop()
