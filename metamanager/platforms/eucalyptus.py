__author__ = 'Davide Monfrecola'
__author__ = 'Giorgio Gambino'

import boto
import datetime
import boto.ec2.cloudwatch
import logging

from threading import Thread
from Queue import Queue

from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import SubdomainCallingFormat
from boto.s3.connection import S3Connection
from boto.ec2.regioninfo import RegionInfo
#

from conf.confmanager.eucalyptusconfmanager import EucalyptusConfManager
from monitors.eucalyptusmonitor import EucalyptusMonitor
from rules.ruleengine import RuleEngine
from metaagent.actionbinder import bind_action
from metaagent.metaagent import MetaAgent


class Eucalyptus():

    def __init__(self):
        self.conf = EucalyptusConfManager()
        self.conf.read()
        self.images = None
        self.instances = None
        self.instance_types = None
        self.security_groups = None
        self.key_pairs = None
        #self.snapshots = None
        self.volumes = None
        self.monitor = None
        self.rule_engine = None
        self.agent = None
        #self.instance_monitored = []

    def connect(self):
        """Connection to the endpoint specified in the configuration file"""
        try:
            self.region = RegionInfo(name="eucalyptus", endpoint=self.conf.ec2_host)
            # trying connection to endpoint
            self.ec2conn = boto.connect_euca(host=self.conf.ec2_host,
                                             aws_access_key_id=self.conf.ec2_access_key_id,
                                             aws_secret_access_key=self.conf.ec2_secret_access_key,
                                             is_secure=False,
                                             port=int(self.conf.ec2_port),
                                             path=self.conf.ec2_path)

            #cf = OrdinaryCallingFormat()
            cf = SubdomainCallingFormat()

            self.s3conn = S3Connection(self.conf.ec2_access_key_id,
                                       self.conf.ec2_secret_access_key,
                                       host=self.conf.s3_host,
                                       port=int(self.conf.s3_port),
                                       path=self.conf.s3_path,
                                       is_secure=False,
                                       calling_format=cf)

            print("Connection successfully established")
            print("Connection successfully established (s3conn): " + self.s3conn.host)
        except Exception as e:
            print("Connection error({0})".format(e.message))

    def print_all_images(self):
        """ print all available images """
        print("--- Images available ---")
        print("%-10s %-25s %-25s %-25s %-25s" % ("ID", "Image ID", "Kernel ID", "Type", "State"))
        i = 1
        if self.images is None:
            self.images = self.ec2conn.get_all_images()
        for image in self.images:
            print("%-10s %-25s %-25s %-25s %-25s" % (i, image.id, image.kernel_id, image.type, image.state))
            i = i + 1

    def print_all_instance_types(self):
        """ print all instance types """
        print("--- Instance types available ---")
        print("%-10s %-25s %-15s %-15s %-15s" % ("ID", "Instance name", "Memory (MB)", "Disk (GB)", "Cores"))
        i = 1
        if self.instance_types is None:
            self.instance_types = self.ec2conn.get_all_instance_types()
        for instance_type in self.instance_types:
            print("%-10s %-25s %-15s %-15s %-15s"%(i, instance_type.name, instance_type.memory,instance_type.disk, instance_type.cores))
            i = i + 1

    def print_all_security_groups(self):
        """ print all security groups """
        print("--- Security groups available ---")
        print("%-10s %-25s %-35s" % ("ID", "SG name", "SG description"))
        i = 1
        if self.security_groups is None:
            self.security_groups = self.ec2conn.get_all_security_groups()
        for security_group in self.security_groups:
            print("%-10s %-25s %-35s" % (i, security_group.name, security_group.description))
            i = i + 1

    def print_all_key_pairs(self):
        """ print all key pairs """
        print("--- Key pairs available ---")
        i = 1
        print("%-10s %-25s %-35s" % ("ID", "Key name", "Key fingerprint"))
        if self.key_pairs is None:
            self.key_pairs = self.ec2conn.get_all_key_pairs()
        for key_pair in self.key_pairs:
            print("%-10s %-25s %-35s" % (i, key_pair.name, key_pair.fingerprint))
            i = i + 1

    def create_new_instance(self):
        #image types
        self.print_all_images()
        if len(self.images) > 0:
            image_index = input("Select image: ")
            self.image_id = self.images[image_index - 1].id
        else:
            print("There are no images available!")
            return False
        #instance type
        self.print_all_instance_types()
        if len(self.instance_types) > 0:
            instance_index = input("Select image: ")
            self.instance_type = self.instance_types[instance_index - 1].name
        else:
            print("There are no instance types available!")
            return False
        # security group
        self.print_all_security_groups()
        if len(self.security_groups) > 0:
            security_group_index = input("Select security group: ")
            self.security_group = [self.security_groups[security_group_index - 1].name]
        else:
            #self.security_group = None
            print("There are no security groups available!")
            return False
        # key name
        self.print_all_key_pairs()
        if len(self.key_pairs) > 0:
            key_pair_index = input("Select key pair: ")
            self.key_name = self.key_pairs[key_pair_index - 1].name
        else:
            #self.key_name = None
            print("There are no keys available!")
            return False

        # monitoring
        monitoring = raw_input("Do you want to enable monitoring? (y/n): ")
        if monitoring == "y":
            monitoring_enabled = True
        else:
            monitoring_enabled = False

        print("\n--- Creating new instance with the following properties:")
        print("- %-20s %-30s" % ("Image ID", str(self.image_id)))
        print("- %-20s %-30s" % ("Security group", str(self.security_group)))
        print("- %-20s %-30s" % ("Key pair", str(self.key_name)))
        print("\nDo you want to continue? (y/n)")
        print("- %-20s %-30s" % ("Monitoring", str(monitoring_enabled)))

        try:
            reservation = self.ec2conn.run_instances(image_id=self.image_id,
                                                     key_name=self.key_name,
                                                     instance_type=self.instance_type,
                                                     security_groups=self.security_group,
                                                     monitoring_enabled=monitoring_enabled,
                                                     min_count=1,
                                                     max_count=1)
            print("\n--- Reservation created")
            print("- %-20s %-30s" % ("ID", reservation.id))
            for instance in reservation.instances:
                print("- %-20s %-30s" % ("Instance ID", instance.id))
                print("- %-20s %-30s" % ("Instance status", instance.state))
                print("- %-20s %-30s" % ("Instance placement", instance.placement))
        except Exception as e:
            print("An error occured: {0}".format(e.message))

    def print_all_instances(self):
        """Print instance id, image id, IP address and state for each active instance"""
        print("Retrieving all instances...")
        self.instances = self.ec2conn.get_only_instances()
        #self.reservations = self.ec2conn.get_all_reservations()
        #instances_objects = [vm for instance in self.reservations for vm in instance.instances]
        if not self.instances:
            print("There are no running or pending instances")
        else:
            i = 1
            for instance in self.instances:
                print("{0} - Instance: {1} | IP address: {2} | Status: {3} | Monitoring: {4}".format(i, instance.id + " / " + instance.image_id, instance.ip_address, instance.state, instance.monitored))
                i += 1

    def print_all_volumes(self):
        """Print volumes and some informations"""
        print("--- Volumes available ---")
        #print("%-10s %-25s %-15s %-25s" % ("ID", "Volume ID", "Size (GB)", "Status"))
        print("Retrieving all volumes...")
        self.volumes = self.ec2conn.get_all_volumes()

        if not self.volumes:
            print("There are no volumes")
        else:
            i = 1
            for volume in self.volumes:
                print("{0} - Volume ID: {1} | Creation {2} | Size: {3} | Attached To: {4} | Status: {5}".format(i, volume.id , volume.create_time, volume.size,volume.attach_data.instance_id ,volume.status))
                i += 1

    def instance_action(self, action):
        try:
            self.print_all_instances()
            if not self.instances:
                print("There are no running or pending instances")
            else:
                instance_index = input("Please select the instance: ")

            if action == "reboot":
                self.ec2conn.reboot_instances(self.instances[instance_index - 1].id)
                print("Instance rebooted")
            elif action == "terminate":
                self.ec2conn.terminate_instances(self.instances[instance_index - 1].id)
                print("Instance terminated")
            else:
                raise Exception("Action not supported")
        except Exception as e:
           print("An error occurred: {0}".format(e.message))

    def get_instance_info(self):
        info = []
        for instance in self.ec2conn.get_only_instances():
            info.append({"id": instance.id, "name": instance.image_id})
        return info

    @bind_action('Eucalyptus','clone')
    def clone_instance(self, instance_id):
        pass

    @bind_action('Eucalyptus','alarm')
    def alarm(self,resource_id):
        logging.debug("Alarm on resource: {0}".format(resource_id))


    def start_monitor(self):
        meters_queue = Queue()
        cmd_queue = Queue()

        resources = self.get_instance_info()
        self.monitor = EucalyptusMonitor(resources=resources, conf=self.conf, region=self.region)
        monitor_thread = Thread(target=self.monitor.run, args=(meters_queue,))
        monitor_thread.setDaemon(True)
        monitor_thread.start()
        logging.info("Eucalyptus Monitor Thread Started")

        self.rule_engine = RuleEngine(resources=resources, cmd_queue=cmd_queue)
        rule_engine_thread = Thread(target=self.rule_engine.run, args=(meters_queue,))
        rule_engine_thread.setDaemon(True)
        rule_engine_thread.start()
        logging.info("Rule Engine Thread Started")


        #self.agent = EucalyptusAgent(manager=self)
        self.agent = MetaAgent(manager=self)
        agent_thread = Thread(target=self.agent.run, args=(cmd_queue,))
        agent_thread.setDaemon(True)
        agent_thread.start()
        logging.info("Eucalyptus Agent Thread Started")



    def stop_monitor(self):
        if self.monitor is not None:
            self.monitor.stop()

    def show_menu(self):
        menu_text = """\nWhat would you like to do?
        --------------------------
        1) Create new instance
        2) Show running instances
        3) Reboot instance
        4) Terminate instance
        5) Start monitor
        6) Stop monitor
        7) Create new volume
        8) Show available volumes
        9) Show key pairs
        10) Show connection information
        11) Exit\n"""
        print(menu_text)
        try:
            # user input
            print("Please make a choice: ")
            choice = input()
            if choice == 1:
                self.create_new_instance()
            elif choice == 2:
                self.print_all_instances()
            elif choice == 3:
                self.instance_action("reboot")
            elif choice == 4:
                self.instance_action("terminate")
            elif choice == 5:
                self.start_monitor()
            elif choice == 6:
                self.stop_monitor()
            elif choice == 8:
                self.print_all_volumes()
            elif choice == 11:
                exit(0)
            else:
                raise Exception("Unavailable choice!")
        except Exception as e:
            print(e.message)
