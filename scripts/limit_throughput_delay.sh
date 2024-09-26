CARD='wlxbc2228c6c661'
#THROUGHPUT='100Mbit'
THROUGHPUT=$1
DELAY=$2
sudo tc qdisc del dev $CARD root
sudo tc qdisc add dev $CARD root handle 1: htb default 1
sudo tc class add dev $CARD parent 1: classid 0:1 htb rate $THROUGHPUT
sudo tc qdisc add dev $CARD parent 1:1 netem delay $DELAY
