from util import *
from json import loads
from json import dumps
import unittest
import ConfigParser
import time

tenant_name = "admin"
network = "net"
subnet_name = "snet"
subnet = "129.127.0.0/24"
instance = "host"
CONF = "config.ini"
parser = ConfigParser.SafeConfigParser()
parser.read(CONF)
gm_ip = parser.get('Default', 'GRID_VIP')

class BasicScenarioHostRecord(unittest.TestCase):
    def test_Network_added_to_NIOS(self):
        args = "network=%s" % (subnet)
        code, msg = wapi_get_request("network", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['network'], subnet)
        else:
            self.fail("Network %s is not added to NIOS" % subnet)
    
    def test_instance_host_record(self):
        args = "name=%s" % (host_name)
        code, msg = wapi_get_request("record:host", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['name'], host_name)
        else:
            self.fail("Host %s is not added to NIOS" % host_name)

    def test_instance_EA_VM_Name(self):
        args = "_return_fields=extattrs;name=%s" % (host_name)
        code, msg = wapi_get_request("record:host", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['extattrs']['VM Name']['value'], instance)
        else:
            self.fail("Host %s is not added to NIOS" % host_name)

class BasicScenarioFixedAddress(unittest.TestCase):
    def test_Network_added_to_NIOS(self):
        args = "network=%s" % (subnet)
        code, msg = wapi_get_request("network", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['network'], subnet)
        else:
            self.fail("Network %s is not added to NIOS" % subnet)

    def test_instance_A_record(self):
        args = "name=%s" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['name'], host_name)
        else:
            self.fail("A Record for %s is not added to NIOS" % host_name)

    def test_instance_PTR_record(self):
        args = "ptrdname=%s" % (host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['ptrdname'], host_name)
        else:
            self.fail("PTR Record for %s not added to NIOS" % host_name)

    def test_instance_EA_VM_Name(self):
        args = "_return_fields=extattrs;name=%s" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['extattrs']['VM Name']['value'], instance)
        else:
            self.fail("Host %s is not added to NIOS" % host_name)

s = utils(tenant_name)
params="?ipv4_address=" + gm_ip
gm_ref = wapi_request('GET', object_type="member", params=params)
ref = loads(gm_ref)[0]['_ref']
data = {"extattrs+": {"Default Host Name Pattern": {"value": "host-{ip_address}"}, "Admin Network Deletion": {"value": "True"}, "DHCP Support": {"value": "True"}, "DNS Support": {"value": "True"}, "IP Allocation Strategy": {"value": "Host Record"}, "Default Domain Name Pattern": {"value": "{subnet_id}.cloud.global.com"}}}
wapi_request('PUT', object_type=ref,fields=dumps(data))
time.sleep(20)

s.create_network(network)
time.sleep(5)
s.create_subnet(network, subnet_name, subnet)
s1 = s.launch_instance(instance, network)
ips = s.get_instance_ips(instance)
host_name = s.get_hostname_pattern_from_grid_config(ips['net'][0]['addr'],s1,network,subnet_name)

print "*" * 70
print "Starts of Basic Tests for HostRecord IP Allocation Strategy"
print "*" * 70
suite = unittest.TestLoader().loadTestsFromTestCase(BasicScenarioHostRecord)
unittest.TextTestRunner(verbosity=2).run(suite)
print "*" * 70
print "End of Basic Tests for HostRecord IP Allocation Strategy"
print "*" * 70

## Tears Down the Objects Created ###
s.terminate_instance(instance)
s.delete_subnet(subnet_name)
s.delete_network(network)



s = utils(tenant_name)
params="?ipv4_address=" + gm_ip
gm_ref = wapi_request('GET', object_type="member", params=params)
ref = loads(gm_ref)[0]['_ref']
data = {"extattrs+": {"Default Host Name Pattern": {"value": "host-{ip_address}"}, "Default Network View Scope": {"value": "Single"}, "Default Network View": {"value": "default"}, "Admin Network Deletion": {"value": "True"}, "DHCP Support": {"value": "True"}, "DNS Support": {"value": "True"}, "IP Allocation Strategy": {"value": "Fixed Address"}, "Default Domain Name Pattern": {"value": "{subnet_name}.cloud.global.com"}}}
wapi_request('PUT', object_type=ref,fields=dumps(data))
time.sleep(20)

s.create_network(network)
s.create_subnet(network, subnet_name, subnet)
time.sleep(10)
s1 = s.launch_instance(instance, network)
ips = s.get_instance_ips(instance)
host_name = s.get_hostname_pattern_from_grid_config(ips['net'][0]['addr'],s1,network,subnet_name)

print "*" * 70
print "Starts of Basic Tests for FixedAddress IP Allocation Strategy"
print "*" * 70
suite = unittest.TestLoader().loadTestsFromTestCase(BasicScenarioFixedAddress)
unittest.TextTestRunner(verbosity=2).run(suite)
print "*" * 70
print "End of Basic Tests for FixedAddress IP Allocation Strategy"
print "*" * 70

## Tears Down the Objects Created ###
s.terminate_instance(instance)
s.delete_subnet(subnet_name)
s.delete_network(network)
