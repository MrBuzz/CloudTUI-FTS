__author__ = 'Giorgio Gambino'

import boto
import datetime
import time
import boto.ec2.cloudwatch
#from monitor import Monitor

#class EucalyptusMonitor(Monitor):
class EucalyptusMonitor:
    """Eucalyptus monitor class"""
    def __init__(self,resources,conf,region):
        try:
            self.conf = conf
            self.resources = resources
            self.meters = ['CPUUtilization'] #modify
            self.loop = True
            self.clwconn = boto.ec2.cloudwatch.CloudWatchConnection(aws_access_key_id=self.conf.ec2_access_key_id,
                                                                    aws_secret_access_key=self.conf.ec2_secret_access_key,
                                                                    region=region,
                                                                    validate_certs=False,
                                                                    is_secure=False,
                                                                    port=int(self.conf.ec2_port),
                                                                    path="/services/CloudWatch")
        except Exception as e:
            print("An error occurred: {0}".format(e.message))

    def stop(self):
        self.loop = False

    def get_samples_v2(self, resource_id):
        samples = []
        for meter in self.meters:
            metrics = self.clwconn.list_metrics(metric_name=meter, dimensions={'InstanceId':[resource_id]})

            for metric in metrics:
                end = datetime.datetime.utcnow()
                start = end - datetime.timedelta(minutes=2)
                datapoints = metric.query(start, end, 'Average', 'Percent', 60)

                for datapoint in datapoints:
                    samples.append(
                        {"resource_id": resource_id,
                        "meter": meter,
                        "timestamp": datapoint['Timestamp'],
                        "value": datapoint['Average']
                        })
        return samples

    def get_samples(self, resource_id):
        samples = []
        for meter in self.meters:
            end = datetime.datetime.utcnow()
            start = end - datetime.timedelta(minutes=2)
            datapoints = self.clwconn.get_metric_statistics(60,
                                                            start,
                                                            end,
                                                            meter,
                                                            'AWS/EC2',
                                                            'Average',
                                                            dimensions={'InstanceId':[resource_id]})
            for datapoint in datapoints:
                samples.append(
                    {"resource_id": resource_id,
                    "meter": meter,
                    "timestamp": datapoint['Timestamp'],
                    "value": datapoint['Average']
                    })

        return samples

    def run(self,meters_queue):
        while self.loop:
            for resource in self.resources:
                samples = self.get_samples_v2(resource["id"])

                for sample in samples:
                    meters_queue.put(sample)

            time.sleep(120)
