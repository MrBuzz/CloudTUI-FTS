******** CloudTUI-FTS ******************************

Cloud Text User Interface - Fault Tolerant Scalable (CloudTUI-FTS)
is text user interface able to interact with multiple
cloud platforms (such as OpenStack, Eucalytus, ...).

With CloudTUI-FTS, a user can:
- start/stop/clone a VM
- monitor the VM health status
- create/manage policies in order to prevent faults (i.e.,
"if the CPU utilization is higher than XX %, then clone it")

CloudTUI-FTS is an open source project written in python,
free available under GPL v.3 license.

		----
Quick start:

0.) Requirements
	You need an up and running OpenStack installation. We are planning
	to provide support even for other Cloud Platform in the next future.
	If you do have enough resource to run your own OpenStack installation
	you may use CloudLab resources freely available (https://cloudlab.us/).
	In this case, we suggest to use the "ARM64OpenStack" profile for your
	experiment.

1.) Install the required libraries
	0.a) boto (the following command should work on most
			of the linux distos:
	 		"sudo pip install boto")
	0.b) python-novaclient ("sudo pip install python-novaclient")
	0.c) python-ceilometerclient ("sudo pip install python-ceilometerclient")
	0.d) antlr3 ("sudo pip install http://www.antlr3.org/download/Python/antlr_python_runtime-3.1.3.tar.gz") --> TODO: mettere un link generico


2.) Download the source code from git repository by using one of the following two methods:
	1.a) git clone https://github.com/trampfox/CloudTUI-FTS.git (recommended)
	1.b) wget https://github.com/trampfox/CloudTUI-FTS/archive/master.zip

3.) Open the file conf/openstack/login.conf and set the os_auth_url and os_ceilometer_auth parameters with the endpoint of the OpenStack controller: just
    replace <HOSTNAME> and <PORT> with the hostname and port of the OpenStack controller.

4.) The basic setup in now completed. You can run cloudtui-fts by running "python cloudtui-fts.py" and then following the instruction provided by our tool.

5.) If you have connecting problem, try to add a line into your /etc/hosts file (superuser permissio required) by adding the IP of the controller followed by "controller" word:
<Controller_IP> ctl

If you need any help, please contact: massimo.canonico@uniupo.it
