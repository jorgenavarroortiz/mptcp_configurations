# Check with "ifconfig" that interface enx00e04cbe42d2 has IP 10.1.1.4/24. If not, execute "sudo ifconfig enx00e04cbe42d2 10.1.1.4/24".
sudo ifconfig enx00e04cbe42d2 10.1.1.4/24
# Routing staff
sudo route del default
sudo route add -net 192.168.31.0/24 gw 10.1.1.1
sudo route add -net 192.168.32.0/24 gw 10.1.1.2
