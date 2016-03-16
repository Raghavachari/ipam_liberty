#!/bin/bash
source ~/devstack/openrc admin admin
set -e
remove_default_router()
{
        routerid=`neutron router-list | grep router1 | awk '{print $2}'`
        neutron router-gateway-clear $routerid
        neutron router-interface-delete $routerid private-subnet
        neutron router-interface-delete $routerid ipv6-private-subnet

        if [ "$routerid" != "" ]; then
                neutron router-delete $routerid
        fi

}
remove_default_net()
{
        local netname=$1
        netid=`neutron net-list | grep $netname | awk '{print $2}'`
	neutron net-delete $netid
}

remove_default_router
remove_default_net private
remove_default_net public
