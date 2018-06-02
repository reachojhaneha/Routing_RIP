"""
Example topology of Quagga routers
"""

import inspect
import os
from mininext.topo import Topo
from mininext.services.quagga import QuaggaService

from collections import namedtuple

QuaggaHost = namedtuple("QuaggaHost", "name ip")
net = None

class QuaggaTopo(Topo):

    "Creates a topology of Quagga routers"

    def __init__(self):
        """Initialize a Quagga topology with 5 routers, configure their IP
           addresses, loop back interfaces, and paths to their private
           configuration directories."""
        Topo.__init__(self)

        # Directory where this file / script is located"
        selfPath = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))  # script directory

        # Initialize a service helper for Quagga with default options
        quaggaSvc = QuaggaService(autoStop=False)

        # Path configurations for mounts
        quaggaBaseConfigPath = selfPath + '/configs/'

        # List of Quagga host configs
        quaggaHosts = []
        quaggaHosts.append(QuaggaHost(name='H1', ip='192.168.101.128/24'))
        quaggaHosts.append(QuaggaHost(name='H2', ip='192.168.106.128/24'))
        quaggaHosts.append(QuaggaHost(name='R1', ip='192.168.101.1/24'))
        quaggaHosts.append(QuaggaHost(name='R2', ip='192.168.102.1/24'))
        quaggaHosts.append(QuaggaHost(name='R3', ip='192.168.103.1/24'))
        quaggaHosts.append(QuaggaHost(name='R4', ip='192.168.106.1/24'))

        # Setup each Quagga router, add a link between it and the IXP fabric
        quaggaContainer = {}
        for host in quaggaHosts:
            # Create an instance of a host, called a quaggaContainer
            quaggaContainer[host.name] = self.addHost(name=host.name,
                                           ip=host.ip,
                                           hostname=host.name,
                                           privateLogDir=True,
                                           privateRunDir=True,
                                           inMountNamespace=True,
                                           inPIDNamespace=True,
                                           inUTSNamespace=True)

            # Configure and setup the Quagga service for this node
            quaggaSvcConfig = \
                {'quaggaConfigPath': quaggaBaseConfigPath + host.name}
            self.addNodeService(node=host.name, service=quaggaSvc,
                                nodeConfig=quaggaSvcConfig)

        # Attach the quaggaContainer to the IXP Fabric Switch
        self.addLink(quaggaContainer['R1'], quaggaContainer['H1'])
        self.addLink(quaggaContainer['R1'], quaggaContainer['R2'])
        self.addLink(quaggaContainer['R1'], quaggaContainer['R3'])
        self.addLink(quaggaContainer['R4'], quaggaContainer['H2'])
        self.addLink(quaggaContainer['R4'], quaggaContainer['R2'])
        self.addLink(quaggaContainer['R4'], quaggaContainer['R3'])

