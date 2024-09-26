sudo route del default

sudo route del -net 192.168.31.0/24 gw 10.1.1.1
sudo route del -net 192.168.32.0/24 gw 10.1.1.2
sudo route del -net 192.168.3.0/24 gw 10.1.1.3

sudo ip rule del pref 32765
sudo ip route flush table 1
