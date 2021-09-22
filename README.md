# Mininet labs for the network training

## Three subnets
run sudo ./three-subnets.py
The scrip will create the folowing hosts 
- subnet A 172.28.0.0/24
  - sah1 
  - sah2 
  - sah3 
- subnet B 172.28.5.0/24
  - sbh1 
  - sbh2
  - sbh3
- subnet C 172.28.19.0/24
  - sch1 
  - sch2 
  - sch3
and routers :
- r1 172.28.0.17 10.28.0.17/24
- r2 172.28.5.35 10.28.0.35/24
- r3 172.28.1.34 10.28.10.34/24


### Task 
- Please run on each router r1 r2 r3 the folowing commands 
``` ip route show```
``` ip address show```
- Please run on the hosts sah1 sbh1 sbh1 the folowing commands 
``` ip route show```
``` ip address show```
- Please repeet activities sone on the slack chanel using ping command example on Subnet A H1 
``` sah1 ping -c 2 172.28.10.34``` 
