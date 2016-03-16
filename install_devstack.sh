#!/bin/bash
cd /home/stack/devstack/
sed -i '/NETWORKING_INFOBLOX_DC_HTTP_REQUEST_TIMEOUT/a NETWORKING_INFOBLOX_DC_WAPI_MAX_RESULTS=-10' local.conf
#./stack.sh > install_log.txt 2>&1
./stack.sh
