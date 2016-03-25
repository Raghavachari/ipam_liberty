#!/bin/bash

gm_ip=10.39.19.140

gm_ref=`curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" https://$gm_ip/wapi/v2.3/member?ipv4_address=$gm_ip | grep _ref | awk '{print $2}' | cut -d '/' -f 2 | sed 's/,$//' | sed 's/"$//'`

curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" -X PUT https://$gm_ip/wapi/v2.3/member/$gm_ref -d '{"extattrs+": {"Grid Sync Maximum Wait Time": {"value": 20},"Grid Sync Minimum Wait Time": {"value": 10}}}'

curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" -X PUT https://$gm_ip/wapi/v2.3/member/$gm_ref -d '{"extattrs+": {"Default Host Name Pattern": {"value": "host-{ip_address}"},"Default Domain Name Pattern": {"value": "{subnet_id}.cloud.global.com"}}}'

sleep 60

echo "Instance Name Pattern = ip_address"
python scenario1.py

set +e
curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" -X PUT https://$gm_ip/wapi/v2.3/member/$gm_ref -d '{"extattrs+": {"Default Host Name Pattern": {"value": "host-{instance_name}"},"Default Domain Name Pattern": {"value": "{network_name}.cloud.global.com"}}}'
sleep 60
echo "Instance Name Pattern = instance_name"
python scenario1.py

set+e
curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" -X PUT https://$gm_ip/wapi/v2.3/member/$gm_ref -d '{"extattrs+": {"Default Host Name Pattern": {"value": "host-{subnet_id}"},"Default Domain Name Pattern": {"value": "{subnet_name}.cloud.global.com"}}}'
sleep 60
echo "Instance Name Pattern = subnet_id"
python scenario1.py

set +e
curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" -X PUT https://$gm_ip/wapi/v2.3/member/$gm_ref -d '{"extattrs+": {"Default Host Name Pattern": {"value": "host-{subnet_name}"},"Default Domain Name Pattern": {"value": "{network_id}.cloud.global.com"}}}'
sleep 60
echo "Instance Name Pattern = subnet_name"
python scenario1.py

set +e
curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" -X PUT https://$gm_ip/wapi/v2.3/member/$gm_ref -d '{"extattrs+": {"Default Host Name Pattern": {"value": "host-{network_name}"},"Default Domain Name Pattern": {"value": "{tenant_id}.cloud.global.com"}}}'
sleep 60
echo "Instance Name Pattern = network_name"
python scenario1.py

set +e
curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" -X PUT https://$gm_ip/wapi/v2.3/member/$gm_ref -d '{"extattrs+": {"Default Host Name Pattern": {"value": "host-{network_id}"},"Default Domain Name Pattern": {"value": "cloud.global.com"}}}'
sleep 60
echo "Instance Name Pattern = network_id"
python scenario1.py

set +e
curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" -X PUT https://$gm_ip/wapi/v2.3/member/$gm_ref -d '{"extattrs+": {"Default Host Name Pattern": {"value": "host-{tenant_id}"}}}'
sleep 60
echo "Instance Name Pattern = tenant_id"
python scenario1.py

#curl -k1 -u admin:infoblox -H "content-type:application/json" -w "\nThe Response Code:%{http_code}\n" -X PUT https://$gm_ip/wapi/v2.3/member/$gm_ref -d '{"extattrs+": {"Default Host Name Pattern": {"value": "host-{tenant_name}"}}}'
#sleep 60
#echo "Instance Name Pattern = tenant_name"
#python scenario1.py
