#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from time import sleep

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='172.28.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
    rs1 = net.addSwitch('rs1', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add routers\n')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r1 = net.addHost('r1', cls=Node)
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    sah1 = net.addHost('sah1', cls=Host, ip='172.28.0.22/24', defaultRoute='via 172.28.0.17')
    sah2 = net.addHost('sah2', cls=Host, ip='172.28.0.25/24', defaultRoute='via 172.28.0.17')
    sah3 = net.addHost('sah3', cls=Host, ip='172.28.0.30/24', defaultRoute='via 172.28.0.17')
    
    sbh1 = net.addHost('sbh1', cls=Host, ip='172.28.5.38/24', defaultRoute='via 172.28.5.35')
    sbh2 = net.addHost('sbh2', cls=Host, ip='172.28.5.39/24', defaultRoute='via 172.28.5.35')
    sbh3 = net.addHost('sbh3', cls=Host, ip='172.28.5.40/24', defaultRoute='via 172.28.5.35')

    sch1 = net.addHost('sch1', cls=Host, ip='172.28.10.36/24', defaultRoute='via 172.28.10.34')
    sch2 = net.addHost('sch2', cls=Host, ip='172.28.10.124/24', defaultRoute='via 172.28.10.34')
    sch3 = net.addHost('sch3', cls=Host, ip='172.28.10.126/24', defaultRoute='via 172.28.10.34')

    info( '*** Add links\n')
    net.addLink(r1, rs1, intfName1='r1-reth1')
    net.addLink(r2, rs1, intfName1='r2-reth1')
    net.addLink(r3, rs1, intfName1='r3-reth1')

    
    net.addLink(r1, s1, intfName1='r1-reth0',intfName2='s1-reth1')

    net.addLink(r2, s2, intfName1='r2-reth0',intfName2='s2-reth2')
    net.addLink(r3, s3, intfName1='r3-reth0',intfName2='s3-reth3')
    net.addLink(s1, r1)
    net.addLink(s2, r2)
    net.addLink(s3, r3)
    net.addLink(s1, sah1)
    net.addLink(s1, sah2)
    net.addLink(s1, sah3)

    net.addLink(s2, sbh1)
    net.addLink(s2, sbh2)
    net.addLink(s2, sbh3)

    net.addLink(s3, sch1)
    net.addLink(s3, sch2)
    net.addLink(s3, sch3)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info ('*** configuring routers *****\n')
    r1.cmd('ip route flush table main')
    r1.cmd('ip a add dev r1-reth0 172.28.0.17/24')
    r1.cmd('ip a add dev r1-reth1 10.28.0.17/24')
    r1.cmd( 'ip route add 172.28.5.0/24 via 10.28.0.35')
    r1.cmd('ip route add 172.28.10.0/24 via 10.28.0.34')

    r2.cmd('ip route flush table main')
    r2.cmd('ip a add dev r2-reth0 172.28.5.35/24')
    r2.cmd('ip a add dev r2-reth1 10.28.0.35/24')
    r2.cmd('ip route add 172.28.10.0/24 via 10.28.0.34')
    r2.cmd('ip route add 172.28.0.0/24 via 10.28.0.17')

    r3.cmd('ip route flush table main')
    r3.cmd('ip a add dev r3-reth0 172.28.10.34/24')
    r3.cmd('ip a add dev r3-reth1 10.28.0.34/24')
    r3.cmd('ip route add 172.28.0.0/24 via 10.28.0.17')
    r3.cmd('ip route add 172.28.5.0/24 via 10.28.0.35')


    info( '*** Starting switches\n')
    net.get('s1').start([])
    net.get('s2').start([])
    net.get('s3').start([])
    net.get('rs1').start([])

    info( '*** Post configure switches and hosts\n')
    net.start()
    sleep(1) 
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

