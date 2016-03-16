from util import *
from json import loads
import unittest

tenant_name = "admin"
network = "net"
subnet_name = "snet"
subnet = "69.69.0.0/24"
instance = "host"

class scenario1(unittest.TestCase):
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

s = utils(tenant_name)
s.create_network(network)
s.create_subnet(network, subnet_name, subnet)
s1 = s.launch_instance(instance, network)
#get host name
host_name = s.get_hostname_pattern_from_grid_config(s1,network,subnet_name)
#print host_name

print "*" * 70
print "Starts Tests"
print "*" * 70
suite = unittest.TestLoader().loadTestsFromTestCase(scenario1)
unittest.TextTestRunner(verbosity=2).run(suite)
print "*" * 70
print "End of Tests"
print "*" * 70

## Tears Down the Objects Created ###
s.terminate_instance(instance)
s.delete_subnet(subnet_name)
s.delete_network(network)
