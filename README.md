check_ec2cw: EC2 CloudWatch Nagios Plugin
===

Flexible Nagios plugin for monitoring CloudWatch-enabled EC2 instances.

It makes use of [boto/boto](https://github.com/boto/boto) for interacting with AWS,
and [flyingcircus/nagiosplugin](https://bitbucket.org/flyingcircus/nagiosplugin/src/default) to convert the results
to a Nagios-interpretable format.


Usage
---

```
usage: check_cloudwatch.py [-h] -r
                           {ap-south-1,us-east-2,us-east-1,us-west-1,us-west-2,ca-central-1,eu-central-1,cn-north-1,ap-southeast-1,eu-west-2,ap-southeast-2,ap-northeast-2,us-gov-west-1,sa-east-1,ap-northeast-1,eu-west-1}
                           -m METRIC -n NAMESPACE [-d DIMENSIONS] [-p PROFILE]
                           [-s {Average,Sum,SampleCount,Maximum,Minimum}]
                           [-w WARNING] [-c CRITICAL] [-v] [-P PERIOD]
                           [-D DELTA] [-l LAG]

Plugin for monitoring CloudWatch-enabled AWS instances

optional arguments:
  -h, --help            show this help message and exit
  -r {ap-south-1,us-east-2,us-east-1,us-west-1,us-west-2,ca-central-1,eu-central-1,cn-north-1,ap-southeast-1,eu-west-2,ap-southeast-2,ap-northeast-2,us-gov-west-1,sa-east-1,ap-northeast-1,eu-west-1}, --region {ap-south-1,us-east-2,us-east-1,us-west-1,us-west-2,ca-central-1,eu-central-1,cn-north-1,ap-southeast-1,eu-west-2,ap-southeast-2,ap-northeast-2,us-gov-west-1,sa-east-1,ap-northeast-1,eu-west-1}
                        CloudWatch metric name
  -m METRIC, --metric METRIC
                        CloudWatch metric name
  -n NAMESPACE, --namespace NAMESPACE
                        CloudWatch metric namespace
  -d DIMENSIONS, --dimensions DIMENSIONS
                        Dimensions of one or more metrics:
                        dimension=value[,dimension=value...]
  -p PROFILE, --profile PROFILE
                        Profile name from ~/.aws/credentials (default:
                        default)
  -s {Average,Sum,SampleCount,Maximum,Minimum}, --statistic {Average,Sum,SampleCount,Maximum,Minimum}
                        Statistic for evaluating metrics (default: Average)
  -w WARNING, --warning WARNING
                        Warning if threshold is outside range (default: 0)
  -c CRITICAL, --critical CRITICAL
                        Critical if threshold is outside range (default: 0)
  -v, --verbosity       Set verbosity (use up to 3 times)
  -P PERIOD, --period PERIOD
                        Period in seconds over which the statistic is applied
                        (default: 60)
  -D DELTA, --delta DELTA
                        Delta measurement in seconds
  -l LAG, --lag LAG     Delay in seconds to add to starting time for gathering
                        metric.useful for ec2 basic monitoring which
                        aggregates over 5min periods (default: 0)
```


Credentials and authentication
---

This plugin *currently* only supports authentication using credentials stored in ~/.aws/credentials.

Usage examples
---

**AWS/VPN tunnel**

Checks the state of an AWS VPN tunnel, with *Dimensions* to specify an interface.

Input:

```
$ python check_cloudwatch.py --metric TunnelState --namespace AWS/VPN -r eu-west-1 -w @0 -c @0 -d TunnelIpAddress=1.2.3.4
```

Output:

```
EC2CW CRITICAL - Metric AWS/VPN:TunnelState (TunnelIpAddress=1.2.3.4) | TunnelState=0.0;@0;@0
```
