#!/bin/bash
id=$(basename $(find /sys/bus/pci/drivers/xhci_hcd/ -maxdepth 1 -type l))
echo -n "$id" > /sys/bus/pci/drivers/xhci_hcd/unbind
echo ''
sleep 3
lsusb
echo -n "$id" > /sys/bus/pci/drivers/xhci_hcd/bind
echo ''
sleep 3
lsusb
