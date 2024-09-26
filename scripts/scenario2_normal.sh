echo "wlxbc2228c6c661 connected to AP01, wlo1 connected to AP02"
sudo cp 50-nuc02.yaml.SCENARIO2 /etc/netplan/50-nuc02.yaml
sudo ifconfig wlo1 192.168.32.2/24
sudo ifconfig wlxbc2228c6c661 192.168.31.2/24

