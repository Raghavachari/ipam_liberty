#!/bin/bash
# Execution Starts
source /home/stack/devstack/openrc admin admin
cd /home/stack/ipam/

#./host_and_domain_name_pattern_validation.sh > automation_report.txt 2>&1
python test_clear_cloud_eas.py > test_clear_cloud_eas.txt 2>&1
sleep 60
python test_floating_ip_association.py > test_floating_ip_association.txt 2>&1
sleep 180
python test_basic_scenario.py > test_basic_scenario.txt 2>&1
sleep 180
python test_host_record.py > test_host_record.txt 2>&1
