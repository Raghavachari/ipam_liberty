#!/bin/bash
# Installing Dependencies for execution
sudo apt-get install python-neutronclient -y
sudo apt-get install python-novaclient -y

# Execution Starts
source /home/stack/devstack/openrc admin admin
cd /home/stack/ipam

./host_and_domain_name_pattern_validation.sh > automation_report.txt 2>&1
python test_clear_cloud_eas.py >> automation_report.txt 2>&1
