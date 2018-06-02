I have set the default gateway of H1(192.168.101.128/24) as R1(192.168.101.1) and H2(192.168.106.128/24) as R4(192.168.106.1). This I did in topo.py file itself.

I configured Quagga ripd daemon to set R1, R2, R3 and R4 as RIP router.

Step 1:
I enable zebra and ripd in the file /etc/quagga/daemons 
zebra=yes
ripd=yes

Step 2:
Next I created two blank files - zebra.conf and ripd.conf in the config directory of all the routers - /config/XX, where XX is R1, R2, R3, R4
To set password for zebra I updated the zebra.conf file for every router and included the following line:
password a

Step 3:
Then I copied /etc/quagga/debian.conf to all the routers as above

Step 4:
Then I restart the quagga service: 
$ /etc/init.d/quagga restart

Step 5:
Lastly I configured every router with Quagga ripd daemons
a. Run start.py
  $ python start.py
b. Login to any router/host
  mininet> xterm R1
c. Launch mx on any host/router 
  $ cd /home/mininet/miniNExT/util
  $ ./mx R1
d. Find the port of running ripd
  $ netstat -na
e. Remote access for localhost/ripd process
  $ telnet localhost zebra
  User Access Verification
  Password:                               -> login with password
  ripd> enable
  ripd# config term                       -> to configure the ripd terminal
  ripd(config)# router rip                -> Enables RIP as a routing protocol
  ripd(config-router)# network X.X.X.X/24 -> configure the subnet where the router is connected to
  ripd(config-router)# exit               -> come out of the terminal
  ripd(config)# write                     -> save the config
                                             Configuration saved to /configs/R1/ripd.conf
Finally all ripd configuration are saved in /configs/XX/ripd.conf, where XX is R1, R2, R3, R4

Once done I run the start.py file again to check. All screenshots are after this step.

