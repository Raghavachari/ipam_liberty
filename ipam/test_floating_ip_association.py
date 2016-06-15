from util import *
from json import loads
import unittest
from json import dumps
import ConfigParser
import time
import os

tenant_name = "admin"
network = "net"
subnet_name = "snet"
ext_net_name = "public"
ext_snet_name = "public_snet"
ext_snet = "10.39.12.0/24"
subnet = "70.70.0.0/24"
instance = "host"

CONF = "config.ini"
parser = ConfigParser.SafeConfigParser()
parser.read(CONF)
gm_ip = parser.get('Default', 'GRID_VIP')


class scenario1(unittest.TestCase):
    def test_Network_added_to_NIOS(self):
        args = "network=%s" % (subnet)
        code, msg = wapi_get_request("network", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['network'], subnet)
        else:
            self.fail("Network %s is not added to NIOS" % subnet)

    def test_A_record_added_to_NIOS(self):
        args = "name=%s" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['name'], host_name)
        else:
            self.fail("Record:A %s is not added to NIOS" % host_name)

    def test_ptr_record_added_to_NIOS(self):
        args = "ptrdname=%s" % (host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(loads(msg)[0]['ptrdname'], host_name)
        else:
            self.fail("Record:PTR %s is not added to NIOS" % host_name)

# EA Test For Instance Object

    def test_EA_VM_ID(self):
        args = "name=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for instance ID %s does not match with NIOS" %
                s1.id)

    def test_EA_VM_Name(self):
        args = "name=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM Name']['value'],
                s1.name)
        else:
            self.fail(
                "EA for instance name %s does not match with NIOS" %
                s1.name)

    def test_EA_IP_Type(self):
        args = "name=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['IP Type']['value'],
                "Fixed")
        else:
            self.fail(
                "EA IP Type for %s does not match " % s1.id)

    def test_EA_Port_Attached_Device_ID_for_instance(self):
        args = "name=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for Port Attached Device - Device ID % does not match with NIOS" %
                s1.id)

    def test_EA_Port_Attached_Device_Owner_for_instance(self):
        args = "name=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device Owner']['value'],
                'compute:None')
        else:
            self.fail(
                "EA for Port Attached Device - Device Owner % does not match with NIOS" %
                'compute:None')

    def test_EA_Tenant_ID(self):
        args = "name=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Tenant ID']['value'],
                s1.tenant_id)
        else:
            self.fail(
                "EA for tenant ID %s does not match with NIOS" %
                s1.tenant_id)

    def test_EA_Account(self):
        args = "name=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Account']['value'],
                s1.user_id)
        else:
            self.fail(
                "EA for user ID % does not match with NIOS" %
                s1.user_id)

    def test_EA_Port_ID(self):
        args = "name=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port ID']['value'],
                port_id)
        else:
            self.fail(
                "EA for PORT ID % does not match with NIOS" % port_id)

    def test_EA_CMP_Type(self):
        args = "name=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['CMP Type']['value'],
                'OpenStack')
        else:
            self.fail("EA for cmp_type is not OpenStack")

# Validating PTR Record EA's

    def test_EA_VM_ID_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for instance ID %s does not match with NIOS" %
                s1.id)

    def test_EA_VM_Name_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM Name']['value'],
                s1.name)
        else:
            self.fail(
                "EA for instance name %s does not match with NIOS" %
                s1.name)

    def test_EA_IP_Type_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['IP Type']['value'],
                "Fixed")
        else:
            self.fail(
                "EA IP Type for %s does not match " % s1.id)

    def test_EA_Port_Attached_Device_ID_for_instance_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for Port Attached Device - Device ID % does not match with NIOS" %
                s1.id)

    def test_EA_Port_Attached_Device_Owner_for_instance_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device Owner']['value'],
                'compute:None')
        else:
            self.fail(
                "EA for Port Attached Device - Device Owner % does not match with NIOS" %
                'compute:None')

    def test_EA_Tenant_ID_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Tenant ID']['value'],
                s1.tenant_id)
        else:
            self.fail(
                "EA for tenant ID %s does not match with NIOS" %
                s1.tenant_id)

    def test_EA_Account_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Account']['value'],
                s1.user_id)
        else:
            self.fail(
                "EA for user ID % does not match with NIOS" %
                s1.user_id)

    def test_EA_Port_ID_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port ID']['value'],
                port_id)
        else:
            self.fail(
                "EA for PORT ID % does not match with NIOS" % port_id)

    def test_EA_CMP_Type_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['CMP Type']['value'],
                'OpenStack')
        else:
            self.fail("EA for cmp_type is not OpenStack")

# Validating EA's For Fixedaddress

    def test_EA_VM_ID_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][0]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for instance ID %s does not match with NIOS" %
                s1.id)

    def test_EA_VM_Name_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][0]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM Name']['value'],
                s1.name)
        else:
            self.fail(
                "EA for instance name %s does not match with NIOS" %
                s1.name)

    def test_EA_IP_Type_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][0]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['IP Type']['value'],
                "Fixed")
        else:
            self.fail(
                "EA IP Type for %s does not match " % s1.id)

    def test_EA_Port_Attached_Device_ID_for_instance_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][0]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for Port Attached Device - Device ID % does not match with NIOS" %
                s1.id)

    def test_EA_Port_Attached_Device_Owner_for_instance_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][0]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device Owner']['value'],
                'compute:None')
        else:
            self.fail(
                "EA for Port Attached Device - Device Owner % does not match with NIOS" %
                'compute:None')

    def test_EA_Tenant_ID_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][0]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Tenant ID']['value'],
                s1.tenant_id)
        else:
            self.fail(
                "EA for tenant ID %s does not match with NIOS" %
                s1.tenant_id)

    def test_EA_Account_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][0]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Account']['value'],
                s1.user_id)
        else:
            self.fail(
                "EA for user ID % does not match with NIOS" %
                s1.user_id)

    def test_EA_Port_ID_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][0]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port ID']['value'],
                port_id)
        else:
            self.fail(
                "EA for PORT ID % does not match with NIOS" % port_id)

    def test_EA_CMP_Type_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][0]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['CMP Type']['value'],
                'OpenStack')
        else:
            self.fail("EA for cmp_type is not OpenStack")

# Validating EA's for floating ip 'A' Record

    def test_FIP_EA_VM_ID(self):
        args = "name=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for instance ID %s does not match with NIOS" %
                s1.id)

    def test_FIP_EA_VM_Name(self):
        args = "name=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM Name']['value'],
                s1.name)
        else:
            self.fail(
                "EA for instance name %s does not match with NIOS" %
                s1.name)

    def test_FIP_EA_IP_Type(self):
        args = "name=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['IP Type']['value'],
                "Floating")
        else:
            self.fail(
                "EA IP Type for %s does not match " % s1.id)

    def test_FIP_EA_Port_Attached_Device_ID_for_instance(self):
        args = "name=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for Port Attached Device - Device ID % does not match with NIOS" %
                s1.id)

    def test_FIP_EA_Port_Attached_Device_Owner_for_instance(self):
        args = "name=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device Owner']['value'],
                'compute:None')
        else:
            self.fail(
                "EA for Port Attached Device - Device Owner % does not match with NIOS" %
                'compute:None')

    def test_FIP_EA_Tenant_ID(self):
        args = "name=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Tenant ID']['value'],
                s1.tenant_id)
        else:
            self.fail(
                "EA for tenant ID %s does not match with NIOS" %
                s1.tenant_id)

    def test_FIP_EA_Account(self):
        args = "name=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Account']['value'],
                s1.user_id)
        else:
            self.fail(
                "EA for user ID % does not match with NIOS" %
                s1.user_id)

    def test_FIP_EA_Port_ID(self):
        args = "name=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port ID']['value'],
                port_id)
        else:
            self.fail(
                "EA for PORT ID % does not match with NIOS" % port_id)

    def test_FIP_EA_CMP_Type(self):
        args = "name=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:a", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['CMP Type']['value'],
                'OpenStack')
        else:
            self.fail("EA for cmp_type is not OpenStack")

# Validating EA's for floating ip PTR record

    def test_FIP_EA_VM_ID_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for instance ID %s does not match with NIOS" %
                s1.id)

    def test_FIP_EA_VM_Name_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM Name']['value'],
                s1.name)
        else:
            self.fail(
                "EA for instance name %s does not match with NIOS" %
                s1.name)

    def test_FIP_EA_IP_Type_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['IP Type']['value'],
                "Floating")
        else:
            self.fail(
                "EA IP Type for %s does not match " % s1.id)

    def test_FIP_EA_Port_Attached_Device_ID_for_instance_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for Port Attached Device - Device ID % does not match with NIOS" %
                s1.id)

    def test_FIP_EA_Port_Attached_Device_Owner_for_instance_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device Owner']['value'],
                'compute:None')
        else:
            self.fail(
                "EA for Port Attached Device - Device Owner % does not match with NIOS" %
                'compute:None')

    def test_FIP_EA_Tenant_ID_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Tenant ID']['value'],
                s1.tenant_id)
        else:
            self.fail(
                "EA for tenant ID %s does not match with NIOS" %
                s1.tenant_id)

    def test_FIP_EA_Account_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Account']['value'],
                s1.user_id)
        else:
            self.fail(
                "EA for user ID % does not match with NIOS" %
                s1.user_id)

    def test_FIP_EA_Port_ID_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port ID']['value'],
                port_id)
        else:
            self.fail(
                "EA for PORT ID % does not match with NIOS" % port_id)

    def test_FIP_EA_CMP_Type_PTR(self):
        args = "ptrdname=%s&_return_fields=extattrs" % (fip_host_name)
        code, msg = wapi_get_request("record:ptr", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['CMP Type']['value'],
                'OpenStack')
        else:
            self.fail("EA for cmp_type is not OpenStack")

# Validating EA's for Floating IP Fixedaddress

    def test_FIP_EA_VM_ID_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][1]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for instance ID %s does not match with NIOS" %
                s1.id)

    def test_FIP_EA_VM_Name_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][1]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['VM Name']['value'],
                s1.name)
        else:
            self.fail(
                "EA for instance name %s does not match with NIOS" %
                s1.name)

    def test_FIP_EA_IP_Type_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][1]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['IP Type']['value'],
                "Floating")
        else:
            self.fail(
                "EA IP Type for %s does not match " % s1.id)

    def test_FIP_EA_Port_Attached_Device_ID_for_instance_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][1]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device ID']['value'],
                s1.id)
        else:
            self.fail(
                "EA for Port Attached Device - Device ID % does not match with NIOS" %
                s1.id)

    def test_FIP_EA_Port_Attached_Device_Owner_for_instance_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][1]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port Attached Device - Device Owner']['value'],
                'compute:None')
        else:
            self.fail(
                "EA for Port Attached Device - Device Owner % does not match with NIOS" %
                'compute:None')

    def test_FIP_EA_Tenant_ID_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][1]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Tenant ID']['value'],
                s1.tenant_id)
        else:
            self.fail(
                "EA for tenant ID %s does not match with NIOS" %
                s1.tenant_id)

    def test_FIP_EA_Account_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][1]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Account']['value'],
                s1.user_id)
        else:
            self.fail(
                "EA for user ID % does not match with NIOS" %
                s1.user_id)

    def test_FIP_EA_Port_ID_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][1]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['Port ID']['value'],
                port_id)
        else:
            self.fail(
                "EA for PORT ID % does not match with NIOS" % port_id)

    def test_FIP_EA_CMP_Type_FA(self):
        args = "ipv4addr=%s&_return_fields=extattrs" % (ips['net'][1]['addr'])
        code, msg = wapi_get_request("fixedaddress", args)
        if code == 200 and len(loads(msg)) > 0:
            self.assertEqual(
                loads(msg)[0]['extattrs']['CMP Type']['value'],
                'OpenStack')
        else:
            self.fail("EA for cmp_type is not OpenStack")

params="?host_name=infoblox.localdomain"
gm_ref = wapi_request('GET', object_type="member", params=params)
ref = loads(gm_ref)[0]['_ref']
data = {"extattrs+": {"Default Host Name Pattern": {"value": "host-{ip_address}"}, "Default Network View Scope": {"value": "Single"}, "Default Network View": {"value": "default"}, "Admin Network Deletion": {"value": "True"}, "DHCP Support": {"value": "True"}, "DNS Support": {"value": "True"}, "IP Allocation Strategy": {"value": "Fixed Address"}, "Default Domain Name Pattern": {"value": "{subnet_id}.cloud.global.com"},"External Host Name Pattern": {"value": "host-{ip_address}"},"External Domain Name Pattern": {"value": "{subnet_name}.external.global.com"}}}
wapi_request('PUT', object_type=ref,fields=dumps(data))
time.sleep(20)
print "Restarting Devstack Screens"
os.system("sudo -H -u stack screen -X -S stack quit")
time.sleep(5)
os.system("sudo -H -u stack screen -d -m -c /home/stack/devstack/stack-screenrc")
time.sleep(20)

s = utils(tenant_name)
s.create_network(network)
s.create_subnet(network, subnet_name, subnet)
s.create_network(ext_net_name,external=True)
s.create_subnet(ext_net_name, ext_snet_name, ext_snet)
s.create_router("router", ext_net_name)
s.create_port('internal_iface',network)
s.add_router_interface('internal_iface', "router")
s1 = s.launch_instance(instance, network)
port_id = s.get_instance_port_id(s1.networks['net'][0])
s.add_floating_ip(instance)
ips = s.get_instance_ips(instance)
host_name = s.get_hostname_pattern_from_grid_config(ips['net'][0]['addr'],s1,network,subnet_name)
fip_host_name = s.get_hostname_pattern_from_grid_config(ips['net'][1]['addr'],s1,ext_net_name,ext_snet_name,rec_type="public")

print "*" * 70
print "Starts Tests"
print "*" * 70
suite = unittest.TestLoader().loadTestsFromTestCase(scenario1)
unittest.TextTestRunner(verbosity=2).run(suite)
print "*" * 70
print "End of Tests"
print "*" * 70

## Tears Down the Objects Created ###
s.delete_floating_ip(instance)
s.terminate_instance(instance)
s.remove_router_interface('internal_iface', "router")
s.delete_router('router')
s.delete_subnet(ext_snet_name)
s.delete_network(ext_net_name)
s.delete_subnet(subnet_name)
s.delete_network(network)
