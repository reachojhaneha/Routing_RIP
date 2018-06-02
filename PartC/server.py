#!/usr/bin/python
import sys
import timeit
import json
import time
import socket
import os.path
from thread import *
import itertools

nodes = {}
nodes['H1'] = '192.168.101.128'
nodes['R1'] = '192.168.101.1' 
nodes['R2'] = '192.168.102.1' 
nodes['R3'] = '192.168.103.1' 
nodes['R4'] = '192.168.106.1' 
nodes['H2'] = '192.168.106.128'
hosts = ['H1', 'H2', 'R1', 'R2', 'R3', 'R4']

class BellFordAlgo:
    def __init__(self, nodeId):
        mtime = os.path.getmtime('weight.csv')
        self.prev_time = time.ctime(mtime)
        self.next_nodes = {}
        self.node_weights = {}
        self.neighbor_weights = {}
        self.neighbors = {}
        self.nodeID = nodeId
        mtime = os.path.getmtime('weight.csv')
        self.mod_time = time.ctime(mtime)
        self.init_distance_table()
        start_new_thread(self.send_distance_table, (1,))
        print 'Starting on ' + nodeId
        self.start_time = timeit.default_timer()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create an AF_INET, STREAM socket (TCP)
        except:
            sys.exit('Creating socket failed')

        try:
            HOST = ''            # Symbolic name meaning all available interfaces
            s.bind((HOST, 8886)) # Arbitrary non-privileged port
        except:
            sys.exit('Bind Failed')

        print 'Socket bind complete for ' + nodeId 
        s.listen(10)

        for dummy in itertools.count():
            connection, addr = s.accept()
            start_new_thread(self.recv_distance_table, (connection,))
        s.close() 

    def init_distance_table(self):
        weight = open('weight.csv', 'r')
        for node in hosts:
            self.next_nodes[node] = None
            self.node_weights[node] = float('inf')
        self.next_nodes[self.nodeID] = self.nodeID
        self.node_weights[self.nodeID] = 0
        for line in weight:
            l = line.strip().split(',')
            node1 = l[0]
            node2 = l[1]
            nbr_wt = l[2]

            if self.nodeID == node1:
                self.neighbor_weights[node2] = 0 if nbr_wt < 0 else float(nbr_wt)
                self.neighbors[node2] = nodes[node2]
            elif node2 == self.nodeID:
                self.neighbor_weights[node1] = 0 if nbr_wt < 0 else float(nbr_wt)
                self.neighbors[node1] = nodes[node1]
        for neighbor in self.neighbors:
            self.next_nodes[neighbor] = neighbor
            self.node_weights[neighbor] = self.neighbor_weights[neighbor]

    def update_neighbor_weight(self):
        mtime = os.path.getmtime('weight.csv')
        self.mod_time = time.ctime(mtime)
        if self.prev_time != self.mod_time:
            self.init_distance_table()
            weight = open('weight.csv', 'r')
            self.start_time = timeit.default_timer()
            for line in weight:
                l = line.strip().split('\t')
                node1 = l[0]
                node2 = l[1]
                nbr_wt = l[2]
                if node1 == self.nodeID:
                    self.neighbor_weights[node2] = 0 if nbr_wt < 0 else float(nbr_wt)
                elif node2 == self.nodeID:
                    self.neighbor_weights[node1] = 0 if nbr_wt < 0 else float(nbr_wt)
            for neighbor in self.neighbor_weights:
                self.node_weights[neighbor] = self.neighbor_weights[neighbor]
            self.prev_time = self.mod_time

    def send_distance_table(self, p):
        for dummy in itertools.count():
            for neighbor in self.neighbors:
                try:
                    self.update_neighbor_weight()
                    HOST = self.neighbors[neighbor]
                    nid = self.nodeID
                    wt = self.node_weights
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((HOST, 8886))
                    s.sendall(nid+"##"+json.dumps(wt))
                    s.close()
                except:
                    pass
            time.sleep(10)

    def recv_distance_table(self, conn):
        for dummy in itertools.count():
            packet = conn.recv(2048)
            length = len(packet)
            if 0 < length:
                change = False
                d = packet.split("##")
                packet = json.loads(d[1])
                p = d[0]
                for node in hosts:
                    x = float(packet[node]) + float(self.node_weights[p])
                    if p == self.next_nodes[node]:
                        self.node_weights[node] = x
                    elif (float(self.node_weights[node]) > x):
                        self.node_weights[node] = x
                        change=True
                        self.next_nodes[node] = p
                if change:
                    self.elapsed = timeit.default_timer() - self.start_time
                    print
                    print self.nodeID + ' Routing Table; Convergence Time - ', self.elapsed
                    print 'Destination', 
                    print 'via',
                    print 'Weight'
                    for node in hosts:
                        if self.next_nodes[node] <> None:
                            string = node + "    " 
                            string = string + self.next_nodes[node] + "    "
                            print string, self.node_weights[node] 

if len(sys.argv) < 2:
    print 'Please provide node id'
    sys.exit()
BellFordAlgo(sys.argv[1])
