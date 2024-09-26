# Routing staff (source-based routing)
CARD1="wlxbc2228c6c661"
CARD2="wlo1"
sudo route del default
sudo route add -net 172.20.38.0/23 gw 192.168.100.100 # Access to eduroam, so "external" users may see the Grafana dashboard
sudo ip rule add from 192.168.31.2 table 1
sudo ip route add 192.168.31.0/24 dev $CARD1 scope link table 1
sudo ip route add default via 192.168.31.1 dev $CARD1 table 1
sudo ip rule add from 192.168.32.2 table 2
sudo ip route add 192.168.32.0/24 dev $CARD2 scope link table 2
sudo ip route add default via 192.168.32.1 dev $CARD2 table 2
sudo ip route flush cache
