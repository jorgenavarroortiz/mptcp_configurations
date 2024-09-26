#!/bin/bash
IFNAME="wlx00ad244648c1"

sudo iptables -t nat -A PREROUTING -p tcp --dport 8031 -i $IFNAME -j DNAT --to 192.168.31.1:80
sudo iptables -t nat -A PREROUTING -p tcp --dport 8032 -i $IFNAME -j DNAT --to 192.168.32.1:80

