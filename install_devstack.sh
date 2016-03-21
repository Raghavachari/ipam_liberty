#!/bin/bash
cd /home/stack/devstack/
sed -i '/NETWORKING_INFOBLOX_DC_HTTP_REQUEST_TIMEOUT/a NETWORKING_INFOBLOX_DC_WAPI_MAX_RESULTS=-10' local.conf
sed -i '/Q_PLUGIN/a Q_ML2_PLUGIN_PATH_MTU=1500' local.conf
sed -i '/RECLONE/a IP_VERSION=4' local.conf
sed -i '/IP_VERSION/a NEUTRON_CREATE_INITIAL_NETWORKS=False' local.conf
sed -i '/NETWORKING_INFOBLOX_DC_GRID_MASTER_HOST/a  NETWORKING_INFOBLOX_DC_GRID_MASTER_NAME=infoblox.localdomain' local.conf
sed -i '/NETWORKING_INFOBLOX_DC_WAPI_MAX_RESULTS/a NETWORKING_INFOBLOX_DC_PARTICIPATING_NETWORK_VIEWS=default' local.conf
#./stack.sh > install_log.txt 2>&1
./stack.sh
