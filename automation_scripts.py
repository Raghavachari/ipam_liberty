#!/bin/bash
import time
import subprocess
import os
import sys
import pexpect

def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() != None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return output
    else:
        raise ProcessException(command, exitCode, output)

try:
#    patch_path = str(sys.argv[1])
#    base=os.path.basename(patch_path)
    machineip = str(sys.argv[1])
#    test = os.path.splitext(base)[0]
#    patch_name = os.path.splitext(test)[0]
except:
   print "no patch file name given"
   exit (0)

ssh_newkey = 'Are you sure you want to continue connecting'
# my ssh command line
destpath='stack@' + machineip
p=pexpect.spawn('ssh-copy-id ' + '-i ' + '/root/.ssh/id_rsa.pub ' + destpath)

i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==0:
    p.sendline('yes')
    i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==1:
    p.sendline("stack")
    p.expect(pexpect.EOF)
    #p.sendline("/home/jenkins/./test.sh")
    print p.before
elif i==2:
    print "I either got key or connection timeout"
    pass
print p.before # print out the result

command = 'scp ' + '-r ' +  '/root/Openstack-IPAM/ipam' + ' ' + destpath  + ':/home/stack/' 
execute([command])
time.sleep(2)
command = 'scp ' + '-r ' +  '/root/Openstack-IPAM/executio*' + ' ' + destpath  + ':/home/stack/'
execute([command])
time.sleep(2)
command = 'scp ' + '-r ' +  '/root/Openstack-IPAM/tempest_execution.sh' + ' ' + destpath  + ':/home/stack/'
execute([command])
time.sleep(2)
#command = 'ssh ' +  destpath  + ' /home/stack/execution.sh'
#execute([command])
