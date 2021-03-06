# CloudTUI-FTS

### Authors
Andrea Lombardo<br/>
Davide Monfrecola<br/>
Giorgio Gambino

### Institute
Department of Science and Innovation Technology (DiSIT) - University of Eastern Piedmont - ITALY

### Superadvisor
Massimo Canonico

### Contact info
massimo.canonico@uniupo.it

### Description
***Cloud Text User Interface - Fault Tolerant and Scalable***<br>
CloudTUI-FTS is a text user interface able to interact
with multiple cloud platforms (such as OpenStack, HPE Helion
Eucalytus and so on)

With CloudTUI-FTS, a user can:
- start/stop/clone a VM
- monitor the VM health status
- create/manage policies in order to prevent faults (i.e.,
"if the CPU utilization is higher than XX %, then clone it")

CloudTUI-FTS is an open source project written in Python,
distributed for free under GPL v.3 license.

### Step 1: Install Requirements

First you need to install the required libraries by typing the following
commands in a terminal window:
```
sudo pip install boto
sudo pip install python-novaclient
sudo pip install python-ceilometerclient
sudo pip install http://www.antlr3.org/download/Python/antlr_python_runtime-3.1.3.tar.gz
```
### Step 2: Get the lastest CloudTUI-FTS version

Download the source code from the git repository by using one of the following
commands:
```
git clone https://github.com/mrbuzz/CloudTUI-FTS.git
wget https://github.com/mrbuzz/CloudTUI-FTS/archive/master.zip
```
### Step 3: Openstack Configuration
You'll need an up and running OpenStack installation. If you do not have enough
resources to run your own installation you can use [CloudLab](https://cloudlab.us/)
resources that are available for free.  In this case, we suggest to use the
***OpenStack*** profile for your experiment.

Open the openstack.conf file under /conf/conf_files and set those values
```
os_auth_url = http://<HOSTNAME>:<PORT>/v2.0
os_username = <USERNAME>
os_password = <PASSWORD>
os_api_key = <USERNAME>
os_tenant_name = <USERNAME>

os_ceilometer_auth = = http://<HOSTNAME>:<PORT>/v2.0
os_ceilometer_username = <USERNAME>
os_ceilometer_password = <PASSWORD>
os_ceilometer_tenant_name = <USERNAME>
```
`<HOSTNAME>`and `<PORT>` are the hostname and port of the OpenStack Nova
and Openstack Ceilometer services.
`<USERNAME>` and `<PASSWORD>` are the login credentials for your OpenStack
installation

We suggest you to add a line into your /etc/hosts file (superuser permissions
required) by adding the IP Address of the controller followed by "ctl" word. If
you do not do this you might have connection problems.

## Example
```
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1				localhost
195.84.22.xx    ctl
255.255.255.255 broadcasthost
::1							localhost
fe80::1%lo0			localhost
```

Here is a copy-paste configuration file for using the CloudLab OpenStack profile:
```
os_auth_url = http://ctl:5000/v2.0
os_username = admin
os_password = <RANDOM PASSWORD>
os_api_key = admin
os_tenant_name = admin

os_ceilometer_auth = http://ctl:5000/v2.0
os_ceilometer_username = admin
os_ceilometer_password = <RANDOM PASSWORD>
os_ceilometer_tenant_name = admin
```

Copy and paste in openstack.conf the above lines; change `<RANDOM PASSWORD>`
with the password randomly-generated by CloudLab situated in the "Profile
Instructions" section once your experiment is started.

### Step 4: Eucalyptus Configuration
You'll need an up and running Eucalyptus installation. If you do not have enough
resources to run a real environment you can use a CentOS 5+ release and the
[FastStart](https://github.com/eucalyptus/eucalyptus-cookbook/tree/master/faststart)
script.

Open the eucalyptus.conf file under /conf/conf_files and set those values:
```
ec2_access_key_id = <KEY ID>
ec2_secret_access_key = <ACCESS KEY>
ec2_host = <HOSTNAME>
ec2_port = <PORT>
ec2_path = /services/Eucalyptus

s3_host = <HOSTNAME>
s3_port = <PORT>
s3_path = /services/Walrus
```

`<HOSTNAME>`and `<PORT>` are the hostname and port of the Eucalyptus
 and Walrus services.<br>
`<KEY ID>` and `<ACCESS KEY>` are the login credentials for your Eucalyptus
installation. You can generate those values from you Eucalyptus admin dashboard

### Step 6: Policy
CloudTUI-FTS comes with an example policy - called test-top - feel free to modify
it or to create your own policy files.


### Step 6: Running
The basic setup in now completed. You can run cloudtui-fts by running "python
cloudtui-fts.py" and then following the instruction provided by our tool.


For support or any comment: massimo.canonico@uniupo.it
