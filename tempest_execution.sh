#!/bin/bash

gm_ip=$1
vm_ip=$2
gm_ref=`curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" https://$gm_ip/wapi/v2.3/member?ipv4_address=$gm_ip | grep _ref | awk '{print $2}' | cut -d '/' -f 2 | sed 's/,$//' | sed 's/"$//'`

curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" -X PUT https://$gm_ip/wapi/v2.3/member/$gm_ref -d '{"extattrs+": {"Default Network View Scope": {"value": "Subnet"},"DHCP Support": {"value": "False"}, "DNS Support": {"value": "False"}, "IP Allocation Strategy":{"value": "Fixed Address"}}}'

#source /home/stack/devstack/openrc admin admin
cat >> ~/.bashrc <<EOF
export OS_USERNAME=admin
export OS_PASSWORD=admin
export OS_TENANT_NAME=admin
export OS_AUTH_URL=http://$vm_ip:35357/v2.0
EOF

ext_net_id=`neutron --os-username admin --os-password admin --os-tenant-name admin --os-auth-url http://$vm_ip:35357/v2.0 net-create ext-net --router:external True -f value -c id | tail -1`
echo $ext_net_id
ext_snet_id=`neutron --os-username admin --os-password admin --os-tenant-name admin --os-auth-url http://$vm_ip:35357/v2.0 subnet-create ext-net 10.39.19.0/24 -f value -c id | tail -1`
echo $ext_snet_id

sed -i "s/^\(public_network_id\s*=\s*\).*$/\1$ext_net_id/" /opt/stack/tempest/etc/tempest.conf

sudo apt-get install python-pip python-dev build-essential libffi6 libffi-dev libssl-dev -y
sudo pip install virtualenv
cd /opt/stack/tempest/
rm -rf community*
sudo pip install -r test-requirements.txt
./run_tempest.sh -V tempest.api.network.test_networks > community_tempest_test_networks 2>&1
./run_tempest.sh -V tempest.api.network.test_ports > community_tempest_test_ports 2>&1
./run_tempest.sh -V tempest.api.network > community_tempest_total_network 2>&1

neutron --os-username admin --os-password admin --os-tenant-name admin --os-auth-url http://$vm_ip:35357/v2.0 net-delete $ext_net_id
