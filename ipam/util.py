from novaclient.client import Client
from json import loads
import httplib, base64
from neutronclient.v2_0 import client
import os, re, time, shlex, subprocess
import ConfigParser, logging, sys
import pdb

GRID_VIP = "10.39.19.140"
USERNAME = "cloud"
PASSWORD = "cloud"
#NEUTRON_CONF = "/etc/neutron/infoblox_conditional.conf"
log_level = logging.INFO
if os.environ.has_key("DEBUG") and os.environ['DEBUG'] == "1":
    log_level = logging.DEBUG
logging.basicConfig(level=log_level,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

def wapi_get_request(object_type, args):
    auth = base64.encodestring("%s:%s" % (USERNAME, PASSWORD))
    auth_header = {}
    auth_header['content-type'] = "application/json"
    auth_header['Authorization'] = "Basic %s" % (auth)
    conn = httplib.HTTPSConnection(GRID_VIP)
    req = "/wapi/v2.3/" + object_type + "?" + args
    conn.request("GET", req, headers=auth_header)
    response = conn.getresponse()
    return response.status, response.read()

class utils:
    def __init__(self, tenant_name):
        self.tenant_name = tenant_name
        credentials = {}
        credentials['username'] = os.environ['OS_USERNAME']
        credentials['auth_url'] = os.environ['OS_AUTH_URL']
        nova_credentials = credentials
        nova_credentials['api_key'] = os.environ['OS_PASSWORD']
        nova_credentials['project_id'] = self.tenant_name
        nova_credentials['version'] = '2'
        self.nova_client = Client(**nova_credentials)
        neutron_credentials = credentials
        neutron_credentials['tenant_name'] = self.tenant_name
        neutron_credentials['password'] = os.environ['OS_PASSWORD']
        self.neutron_client = client.Client(**neutron_credentials)
    
    def get_domain_suffix_pattern_from_grid_config(self,netname,subname):
	'''
	Gets Zone name from 'Default Domain Name Pattern' in grid configuration
	'''
        extattrs = self.get_grid_configuration()
	domainsuffixpat = extattrs['Default Domain Name Pattern']['value']
	if re.search("{tenant_id}", domainsuffixpat):
	    tenantid = self.get_tenant_id()
	    domainsuffixpat = re.sub("{tenant_id}",tenantid,domainsuffixpat)
	if re.search("{subnet_id}", domainsuffixpat):
	    subnetid = self.get_subnet_id(subname)
	    domainsuffixpat = re.sub("{subnet_id}",subnetid,domainsuffixpat)
	if re.search("{subnet_name}", domainsuffixpat):
	    domainsuffixpat = re.sub("{subnet_name}",subname,domainsuffixpat)
	if re.search("{network_name}", domainsuffixpat):
	    domainsuffixpat = re.sub("{network_name}",netname,domainsuffixpat)
	if re.search("{network_id}", domainsuffixpat):
	    netid = self.get_net_id(netname)
	    domainsuffixpat = re.sub("{network_id}",netid,domainsuffixpat)
	
	return domainsuffixpat
	    
    def get_hostname_pattern_from_grid_config(self,instanceobj,network,subnet):
	'''
	Gets Host name from 'Default Host Name Pattern' in grid configuration
	'''
        extattrs = self.get_grid_configuration()
	fqdn = self.get_domain_suffix_pattern_from_grid_config(network,subnet)
	hostpat = extattrs['Default Host Name Pattern']['value']
	ipadd = instanceobj.addresses[network][0]['addr'] 
	ipsplit = ipadd.split(".")
	ipadd = ipadd.replace(".","-")
	if re.search("{tenant_id}", hostpat):
	    tenantid = self.get_tenant_id()
	    hostpat = re.sub("{tenant_id}",tenantid,hostpat)
	    
	if re.search("{subnet_id}", hostpat):
	    subnetid = self.get_subnet_id(subnet)
	    hostpat = re.sub("{subnet_id}",subnetid,hostpat)
	    
	if re.search("{subnet_name}", hostpat):
	    hostpat = re.sub("{subnet_name}",subnet,hostpat)
	    
	if re.search("{network_name}", hostpat):
	    hostpat = re.sub("{network_name}",network,hostpat)
	    
	if re.search("{network_id}", hostpat):
	    netid = self.get_net_id(network)
	    hostpat = re.sub("{network_id}",netid,hostpat)

        if re.search("{instance_name}", hostpat):
            inst_name = instanceobj.name
            hostpat = re.sub("{instance_name}",inst_name,hostpat)
	    
	if re.search("{ip_address}", hostpat):
	    hostpat = re.sub("{ip_address}",ipadd,hostpat)
	    
	if re.search("{ip_address_octet1}", hostpat):
	    hostpat = re.sub("{ip_address_octet1}",ipsplit[0],hostpat)
	    
	if re.search("{ip_address_octet2}", hostpat):
	    hostpat = re.sub("{ip_address_octet2}",ipsplit[1],hostpat)
	    
	if re.search("{ip_address_octet3}", hostpat):
	    hostpat = re.sub("{ip_address_octet3}",ipsplit[2],hostpat)
	    
	if re.search("{ip_address_octet4\}", hostpat):
	    hostpat = re.sub("{ip_address_octet4}",ipsplit[3],hostpat)
	    
	return hostpat + "." + fqdn
    	
    def create_network(self, network_name, external=False):
        """
        Creates a Network
        
        It takes Network Name as argument.
        """
        nw = {'network': {'name': network_name, 'admin_state_up': True, 'router:external' : external}}
        netw = self.neutron_client.create_network(body=nw)
        net_dict = netw['network']
        network_id = net_dict['id']
        logger.info("Created Network '%s'", network_name)
        logger.debug("Network ID of '%s' : %s", network_name, network_id)

    def get_networks(self):
        """
        Return List of Networks
        """
        netw = self.neutron_client.list_networks()
        return netw['networks']

    def get_net_id(self, nw_name):
        """
        Return Network ID for the given Network name
        """
        nw = self.get_networks()
        for n in nw:
            if n['name'] == nw_name:
                return n['id'], n['tenant_id']
        return None

    def create_subnet(self, network_name, subnet_name, subnet):
        """
        Creates a Subnet
        It takes Network Name, Subnet Name and Subnet as arguments.
        For Example:-
        project.create_subnet("Network1", "Subnet-1-1", "45.0.0.0/24")
        """
        net_id, tenant_id = self.get_net_id(network_name)
        body_create_subnet = {'subnets': [{'name': subnet_name, 'cidr': subnet, 'ip_version': 4, 'tenant_id': tenant_id, 'network_id': net_id}]}
        try:
            subnet = self.neutron_client.create_subnet(body=body_create_subnet)
            logger.info("Created Subnet '%s' under the Network '%s'", subnet_name, network_name)
        except:
            print("Failed to create Subnet : ", sys.exc_info()[0])

    def launch_instance(self, name, nw_name):
        """
        Return Server Object if the instance is launched successfully
        
        It takes Instance Name and the Network Name it should be associated with as arguments.
        """
        image = self.nova_client.images.find(name="cirros-0.3.3-x86_64-disk")
        flavor = self.nova_client.flavors.find(name="m1.tiny")
        net_id, tenant_id = self.get_net_id(nw_name)
        nic_d = [{'net-id': net_id}]
        instance = self.nova_client.servers.create(name=name, image=image,
                                                   flavor=flavor, nics=nic_d)
        logger.info("Launched Instance '%s', waiting for it to boot", name)
        time.sleep(60)
        return instance

    def get_servers_list(self):
        """
        Return List of Servers
        """
        return self.nova_client.servers.list()
    
    def get_server(self, name):
        """
        Return Server Object for a given instance name
        """
        servers_list = self.get_servers_list()
        server_exists = False
        for s in servers_list:
            if s.name == name:
                logger.debug("Instance '%s' exists", name)
                server_exists = True
                break
        if not server_exists:
            return None
        else:
            return s
  
    def terminate_instance(self, name):
        """
        Terminates an instance
        It takes Instance Name as argument.
        """
        server = self.get_server(name)
        if server:
            self.nova_client.servers.delete(server)
            time.sleep(60)
            logger.info("Terminated Instance '%s'", name)
        else:
            logger.error("Instance '%s' does not exist", name)

    def delete_subnet(self, subnet_name):
        """
        Deletes a Subnet
        It takes Subnet Name as argument.
        """
        subnets = self.neutron_client.list_subnets()
        logger.debug("Subnets details before deleting '%s' : %s", subnet_name, subnets)
        for s in subnets['subnets']:
            if s['name'] == subnet_name:
                self.neutron_client.delete_subnet(s['id'])
                logger.info("Deleted Subnet '%s'", subnet_name)
        subnets = self.neutron_client.list_subnets()
        logger.debug("Subnets details after deleting '%s' : %s", subnet_name, subnets)

    def delete_network(self, network_name):
        """
        Deletes a Network
        It takes Network Name as argument.
        """
        net_id, tenant_id = self.get_net_id(network_name)
        if net_id:
            netw = self.neutron_client.delete_network(net_id)
            logger.debug("Network ID of '%s' : %s", network_name, net_id)
            logger.info("Deleted Network '%s'", network_name)
        else:
            logger.error("Network '%s' does not exist", network_name)

    def get_grid_configuration(self):
        args = "_return_fields=extattrs;ipv4_address=%s" % (GRID_VIP)
        data = wapi_get_request("member", args)
	extattrs = loads(data[1])[0]['extattrs']
	return extattrs

    def get_tenant_id(self):
        """
        Return Tenant ID
        """
        cmd = "keystone tenant-get %s" % (self.tenant_name)
        args = shlex.split(cmd)
        p = subprocess.Popen(args, stdout = subprocess.PIPE, stderr= subprocess.STDOUT)
        output, error = p.communicate()
        if p.returncode == 0:
            match = re.search("\s*id\s*\|\s*(\w*)\s*", output)
            if match:
                return match.group(1)
            else:
                return None
        else:
            return None
	
    def get_subnets(self):
	"""
        Return List of Subnets
        """
        netw = self.neutron_client.list_subnets()
        return netw['subnets']
	
    def get_subnet_id(self, sn_name):
        """
        Return Subnet ID for the given subnet name
        """
        nw = self.get_subnets()
        for n in nw:
            if n['name'] == sn_name:
                return n['id']
        return None
