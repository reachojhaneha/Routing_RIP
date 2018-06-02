#!/usr/bin/python

"""
Example network of Quagga routers
(QuaggaTopo + QuaggaService)
"""

import sys
import atexit

# patch isShellBuiltin
import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

from mininet.util import dumpNodeConnections
from mininet.node import OVSController
from mininet.log import setLogLevel, info

from mininext.cli import CLI
from mininext.net import MiniNExT

from topo import QuaggaTopo

net = None


def startNetwork():
    "instantiates a topo, then starts the network and prints debug information"

    info('** Creating Quagga network topology\n')
    topo = QuaggaTopo()

    info('** Starting the network\n')
    global net
    net = MiniNExT(topo, controller=OVSController)
    net.start()

    info('** Dumping host connections\n')
    dumpNodeConnections(net.hosts)

    for host in net.hosts:
        if host.name == 'R1':
            host.setIP('192.168.102.2/24', intf='R1-eth1')
            host.setIP('192.168.103.2/24', intf='R1-eth2')
        if host.name == 'R2':
            host.setIP('192.168.104.1/24', intf='R2-eth1')
        if host.name == 'R3':
            host.setIP('192.168.105.1/24', intf='R3-eth1')
        if host.name == 'R4':
            host.setIP('192.168.104.2/24', intf='R4-eth1')
            host.setIP('192.168.105.2/24', intf='R4-eth2')

    info('** Testing network connectivity\n')
    net.ping(net.hosts)
    
    info('** Running CLI\n')
    CLI(net)


def stopNetwork():
    "stops a network (only called on a forced cleanup)"

    if net is not None:
        info('** Tearing down Quagga network\n')
        net.stop()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
