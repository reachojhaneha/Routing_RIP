(a) To bring a link down I am using the command:
$ link R1 R2 down

(b) Time for connectivity to be establised: 10s (approx).
First I log into H1 (xterm H1) and start pinging to H2. Then I break down the link from R1 and R2. This results in the ping to fail, since the route between H1 and H2 is broken. After 10 consecutive destination host unreachable H1 connects to H2 again. Since ping waits for 1 sec by default before sending another packet, we can assume that it took 10 secs to establish connection.

(c) Provide the Traceroute Output
mininext> h1 traceroute h2
traceroute to 192.168.6.128 (192.168.6.128), 30 hops max, 60 byte packets
 1  192.168.1.1 (192.168.1.1)  0.029 ms  0.006 ms  0.005 ms
 2  192.168.3.1 (192.168.3.1)  0.015 ms  0.009 ms  0.008 ms
 3  192.168.5.2 (192.168.5.2)  0.016 ms  0.009 ms  0.009 ms
 4  192.168.6.128 (192.168.6.128)  0.017 ms  0.012 ms  0.009 ms
mininext>
