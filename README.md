# Configurations for MPTCP experiments

This repository includes details about the configurations used for the paper at https://doi.org/10.3390/s24186022: Navarro-Ortiz, J.; Ramos-Munoz, J.J.; Delgado-Ferro, F.; Canellas, F.; Camps-Mur, D.; Emami, A.; Falaki, H. _**Combining 5G New Radio, Wi-Fi, and LiFi for Industry 4.0: Performance Evaluation.**_ Sensors 2024, 24, 6022.

- Code to experiment using MPTCP in a virtual testbed is available at **https://github.com/jorgenavarroortiz/multitechnology_testbed_v0**. MPTCP schedulers and Linux kernels supporting MPTCP are included in this repo, and are required for real testbeds.

**If you use code from these repositories, please cite our paper. Thanks!**

## Testing WRR with 5G NR + Wi-Fi 6 + LiFi

The topology of the complete scenario is shown in the following picture:

![image](https://user-images.githubusercontent.com/17797704/232044341-13eb259c-bb90-4145-b0f6-b2df96fc8b41.png)

And the real testbed is shown in the following picture:

![image](https://github.com/jorgenavarroortiz/multitechnology_testbed_v0_NUC/assets/17797704/692f3ac6-cdfb-47d7-be90-1d2cf88dc84f)

You will need to add the required scripts to connect your 5G modem (`connect_quectel_amarisoft.sh ` in our case) and your LiFi dongle (`connect_to_lifi_ap_open.sh` in our case). In addition, you will also need to change the name of the network interfaces in the different scripts to match your setup. We include the configuration files for our Wi-Fi 6 access point (directory `wifi_aps`) and the configuration files for our Amarisoft basestation (directory `amarisoft`). For the LiFi access point we use the default configuration, so no files are needed.

Using MPTCP, we can change the weights for WRR (on both the CPE and the proxy) by executing the following commands (3 is the weight for the Wi-Fi interface, and 1 is the weight for 5G NR; you can change them to other values):
```
# For CPE (uplink)
cd ~/mptcp_ctrl
sudo python3 ./wrr_test_cpe-5gnr-wifi6-lifi.py 10 10 1

# For PROXY (downlink)
cd ~/mptcp_ctrl
sudo python3 ./wrr_test_proxy-5gnr-wifi6-lifi.py 10 10 1
```

- On _proxy 1_ (WIMUNET-NUC03):

```
sudo route del default # Remove default route (used for the management network interface)
# IMPORTANT: the if_names file has to include the Amarisoft basestation as default route (third parameter). If you use one of the Wi-Fi routers, it does not work.
cd ~/free5gc/mptcp_test/
./set_MPTCP_parameters.sh -p fullmesh -s roundrobin -c olia -f if_names.txt.nuc03.5GNR-WIFI-LIFI -C N
iperf3 -s
```

- On _CPE_ (WIMUNET-NUC02):

```
# Routing stuff
sudo route del default # Remove default route (used for the management network interface)

# Start connection to the 5G NR base station (gNB)
# You can use a different terminal (e.g. using `screen -S quectel`) to run these commands.
cd ~/quectel-linux/
./connect_quectel_amarisoft.sh 
# WAIT HERE UNTIL THE CARD IS CONNECTED AND AN IP ADDRESS IS ASSIGNED (assumed 192.168.3.2/24 in our tests and configuration files)
# Make sure that it is connected to the Amarisoft basestation (e.g. by pinging 192.168.3.1 or by checking it in the Amarisoft basestation)

# Connect to LiFi AP
cd ~/LIFI
./connect_to_lifi_ap_open.sh
# Make sure that it is connected to the LIFI AP by e.g. executing iwconfig and testing connectivity to the DHCP server (which acts as router), e.g. ping 192.168.200.1

# Run MPTCP on the CPE
cd ~/free5gc/mptcp_test/
./set_MPTCP_parameters.sh -p fullmesh -s roundrobin -c olia -f if_names.txt.nuc02.5GNR-WIFI6-LIFI -C N
iperf3 -c 10.1.1.4 -P 10 -R -t 100 & ifstat # For downlink. Remove -R for uplink.
```

Example of results (using Round-Robin without weights):

![image](https://user-images.githubusercontent.com/17797704/231997688-187b5cad-5914-4c1b-977c-a9226df926fb.png)
