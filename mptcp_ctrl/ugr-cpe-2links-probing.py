#!/usr/bin/env python3
import mptcp_wrr_controller as wrr 
import sys
import os
import random
import math
import subprocess
import json
import time

DEBUG=False

# Change meeeee!!!!!!!!!!!!!!
interfaces=["wlo1","wwp0s20f0u3i4"]
ips=["192.168.32.2", "192.168.3.2"]
#TARGET_IP="localhost"
TARGET_IP="10.1.1.4"
interprobing_time=10
probing_time=5


# Estimated ips...
#bws=[[115000,95000,85000],
#    [8000,6000,5000]]

def read_info_json():
    process = subprocess.Popen(["ip", "-j", "-s","link","show"], stdout=subprocess.PIPE)
    jj=process.communicate()[0]
    dictionary = json.loads(jj)

    stats={}
    for i in dictionary:
        if DEBUG:
            print("[DEBUG] " + i["ifname"]+" "+str(i["stats64"]["tx"]["bytes"]))
        stats[i["ifname"]]=i["stats64"]["tx"]["bytes"]

    return stats

def read_info():
    stats={}
    # Using readlines()
    file = open('/proc/net/dev', 'r')
    lines = file.readlines()

    i=0
    for line in lines:
        if i>=2:
            params=line.split()
            stats[params[0].strip()]=int(params[1])
        i=i+1

    file.close()
    return stats

def read_stats_json():
    start = time.time() * 1000
    stats_from=read_info_json()
    stats_from["timestamp"]=start

    return stats_from

# ms
def read_stats():
    start = time.time() * 1000
    stats_from=read_info()
    stats_from["timestamp"]=start

    return stats_from

# ms
def update_stats():
    stop= time.time() * 1000
    stats_to=read_info()
    stats_to["timestamp"]=stop

    return stats_to

def probe(remoteIp, protocol, probe_time, ran):

    current=(wrr.get_mptcp_current_scheduler()).strip()
    current_=(current.split(" = "))
    current=current_[1].strip()

    wrr.set_mptcp_scheduler("redundant")

    # stats_from=read_stats_json()
    stats_from=read_stats_json()

    if protocol=="tcp":
        if DEBUG:
            os.system("iperf3 -p 5202 -c "+remoteIp+" -t "+str(probe_time)+" ")
        else:
            os.system("iperf3 -p 5202 -c "+remoteIp+" -t "+str(probe_time)+" ")
#            os.system("iperf3 -p 5202 -c "+remoteIp+" -t "+str(probe_time)+" 2>&1 > /dev/null")
    else:
        for interface in ips:
            os.system("iperf3 -c "+ips[interface]+" -t "+str(probe_time)+" -B "+interface+" -u -b "+str(maxbw)+"&") # -P 2
        os.system("sleep "+str(probe_time))

    stats_to=read_stats_json()

    elapsed=(stats_to["timestamp"]-stats_from["timestamp"])/1000.0
    if DEBUG:
        print("[DEBUG] " + elapsed)
    bw={}

    values=""
    for value in stats_to:
        bw[value]=round(8*(stats_to[value]-stats_from[value])/elapsed,0)
        print("[INFO] Througphput estimation of interface " + str(value) + ": " + str(bw[value]) + " bps")

    wrr.set_mptcp_scheduler(current)

    # time.sleep(inter_time)
    return bw



def gcd(a,b):
    if a==0:
        return b
    return gcd(b%a,a)



def weight_gcd(bw_):
    bww=[]

    gcd_=bw_[0]
    for i in range(1,len(bw_)):
        gcd_=gcd(gcd_,bw_[i])

    # to review!!!!!!
    if gcd_==0:
    	gcd_=1

    for i in range(len(bw_)):
        bww.append(bw_[i]/gcd_)

    return bww


def weight_floor(bw_):
    bww=[]

    floor_=1
    minbw = bw_[len(bw_)-1]

    for bw__ in bw_:
        bww.append(int(math.floor(bw__/minbw)))
    return bww

def weight_ceil(bw_):
    bww=[]

    floor_=1
    minbw = bw_[len(bw_)-1]

    for bw__ in bw_:
        bww.append(int(math.ceil(bw__/minbw)))
    return bww

def weight_round(bw_):
    bww=[]

    floor_=1
    minbw = bw_[len(bw_)-1]

    for bw__ in bw_:
        bww.append(int(round(bw__/minbw)))
    return bww

# def weight_floor(bw_):
#     bww=[]


#     gcd_=gcd(bw_)
#     for i in range(len(bw_)):
#         bww[i]=bw_[i]/gcd_

#     return bww

def str_bw(bw_):
    bww=str(bw_[0])

    for i in range(1,len(bw_)):
        bww=bww+"-"+str(bw_[i])

    return bww


# mptcp@mptcp-vmwarevirtualplatform:~$ ifstat -b -T -w -n | tee /tmp/fich.txt
def main():
    bw=[0]*len(interfaces)

    #current=wrr.get_mptcp_current_scheduler()
    wrr.set_mptcp_scheduler("roundrobin")

    ran=random.randrange(20000)

    for i in range(100):
            ran=random.randrange(20000)

            bw__=probe(TARGET_IP, "tcp", probing_time,ran )
            print("[INFO] " + str(bw__))

            for j in range(len(interfaces)):
            	bw[j]=bw__[interfaces[j]]

            w=weight_gcd(bw)
            alg="gcd"

#            rules = [{"dst_ip":ips[0], "weight":int(w[0])},{"dst_ip":ips[1], "weight":int(w[1])},{"dst_ip":ips[2], "weight":int(w[2])}]
##            rules = [{"src_ip":ips[0], "weight":int(w[0])},{"src_ip":ips[1], "weight":int(w[1])}]
            if w[0] > w[1]:
                rules = [{"src_ip":ips[0], "weight":int(w[0]/w[1])},{"src_ip":ips[1], "weight":int(1)}]
            else:
                rules = [{"src_ip":ips[0], "weight":int(1)},{"src_ip":ips[1], "weight":int(w[1]/w[0])}]
            print("[INFO] Assigning "+str(rules))

            # period: 1s, 50 times...
            if DEBUG:
                os.system("(ifstat -b -T -w -n 1 55 | tee ifstat-"+str_bw(bw)+"-"+str(ran)+"-"+alg+".txt) &")

            ##wrr.set_local_interfaces_rules(rules)
            wrr.set_local_interfaces_rules(rules)

#            if DEBUG:
#                os.system("iperf3 -c "+TARGET_IP+" -t 60")
#            else:
#                os.system("iperf3 -c "+TARGET_IP+" -t 60 2>&1 > /dev/null")

            time.sleep(interprobing_time)
if __name__ == '__main__':
    main()
