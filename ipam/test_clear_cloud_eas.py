from util import *
from json import loads
import unittest

tenant_name = "admin"
network = "net"
subnet_name = "snet"
subnet = "69.69.0.0/24"

class beforeDelete(unittest.TestCase):
    def test_Network_added_to_NIOS(self):
        args = "network=%s" % (subnet)
        code, msg = wapi_get_request("network", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['network'], subnet)
        else:
            self.fail("Network %s is not added to NIOS" % subnet)
    
    def test_CMPType_EA(self):
        args = "_return_fields=extattrs;network=%s" % (subnet)
        code, msg = wapi_get_request("network", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['extattrs']['CMP Type']['value'], "OpenStack")
        else:
            self.fail("CMP Type EA Notset")

    def test_CloudAPIOwned_EA(self):
        args = "_return_fields=extattrs;network=%s" % (subnet)
        code, msg = wapi_get_request("network", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['extattrs']['Cloud API Owned']['value'], "False")
        else:
            self.fail("Cloud API Owned Not set")

    def test_TenantID_EA(self):
        args = "_return_fields=extattrs;network=%s" % (subnet)
        code, msg = wapi_get_request("network", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['extattrs']['Tenant ID']['value'], tenant_id)
        else:
            self.fail("Tenant ID EA Not set")

class afterDelete(unittest.TestCase):
    def test_Network_still_exist(self):
        args = "network=%s" % (subnet)
        code, msg = wapi_get_request("network", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['network'], subnet)
        else:
            self.fail("Network %s is not added to NIOS" % subnet)

    def test_CMPType_EA(self):
        args = "_return_fields=extattrs;network=%s" % (subnet)
        code, msg = wapi_get_request("network", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['extattrs']['CMP Type']['value'], "N/A")
        else:
            self.fail("CMP Type EA Notset")

    def test_CloudAPIOwned_EA(self):
        args = "_return_fields=extattrs;network=%s" % (subnet)
        code, msg = wapi_get_request("network", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['extattrs']['Cloud API Owned']['value'], "False")
        else:
            self.fail("Cloud API Owned Not set")

    def test_TenantID_EA(self):
        args = "_return_fields=extattrs;network=%s" % (subnet)
        code, msg = wapi_get_request("network", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['extattrs']['Tenant ID']['value'], "N/A")
        else:
            self.fail("Tenant ID EA Not set")

s = utils(tenant_name)
s.create_network(network,external=True)
s.create_subnet(network, subnet_name, subnet)
tenant_id=s.get_tenant_id()

print "*" * 70
print "Starts Tests"
print "*" * 70
suite = unittest.TestLoader().loadTestsFromTestCase(beforeDelete)
unittest.TextTestRunner(verbosity=2).run(suite)
print "*" * 70
print "End of Tests"
print "*" * 70

## Tears Down the Objects Created ###
s.delete_subnet(subnet_name)
s.delete_network(network)

print "*" * 70
print "Starts Tests"
print "*" * 70
suite = unittest.TestLoader().loadTestsFromTestCase(afterDelete)
unittest.TextTestRunner(verbosity=2).run(suite)
print "*" * 70
print "End of Tests"
print "*" * 70
