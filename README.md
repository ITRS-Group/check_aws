# check_aws: Nagios-compatible plugin for monitoring AWS

[![image](https://badgen.net/travis/ITRS-Group/check_aws)](https://travis-ci.org/ITRS-Group/check_aws)
[![image](https://badgen.net/lgtm/grade/g/ITRS-Group/check_aws)](https://lgtm.com/projects/g/ITRS-Group/check_aws)
[![image](https://badgen.net/codecov/c/github/ITRS-Group/check_aws)](https://codecov.io/gh/ITRS-Group/check_aws)
[![image](https://badgen.net/badge/license/GPLv3/blue)](https://raw.githubusercontent.com/ITRS-Group/check_aws/master/LICENSE)


This plugin can be used to monitor [AWS Services That Publish CloudWatch Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html).

It uses [boto/boto3](https://github.com/boto/boto3) for interacting with AWS CloudWatch, and the [mpounsett/nagiosplugin](https://github.com/mpounsett/nagiosplugin) library for working with the Nagios plugin format.


### Table of Contents

- [Usage](#cli-usage)
- [Credentials](#credentials-and-authentication)
- [Profiles](#profiles)
- [Dimensions](#dimensions)
- [Examples](#examples)
    * [VPN Availability](#vpn-availability)
    * [Free Space](#free-space)
    * [Credit Usage](#credit-usage)
    * [CPU Utilization](#cpu-utilization)
    * [ECS Running Tasks](#ecs-running-tasks)
- [Troubleshooting](#troubleshooting)
- [Other](#other)
    * [AWS CLI](#aws-cli)
- [Credits](#credits)

## CLI Usage

```
usage: check-aws.py [-h] -r
                    {af-south-1,ap-east-1,ap-northeast-1,ap-northeast-2,ap-northeast-3,ap-south-1,ap-southeast-1,ap-southeast-2,ca-central-1,eu-central-1,eu-north-1,eu-south-1,eu-west-1,eu-west-2,eu-west-3,me-south-1,sa-east-1,us-east-1,us-east-2,us-west-1,us-west-2}
                    [-u UNIT] -m METRIC -n NAMESPACE [-d [DIMENSIONS]]
                    [-p PROFILE]
                    [-s {Average,Sum,SampleCount,Maximum,Minimum}]
                    [-w WARNING] [-c CRITICAL] [-v] [-P [PERIOD]] [-D DELTA]
                    [-l LAG] [-C [CREDENTIALS_FILE]] [-f [CREDENTIALS_FILE]]

Plugin for monitoring AWS via CloudWatch

optional arguments:
  -h, --help            show this help message and exit
  -r {af-south-1,ap-east-1,ap-northeast-1,ap-northeast-2,ap-northeast-3,ap-south-1,ap-southeast-1,ap-southeast-2,ca-central-1,eu-central-1,eu-north-1,eu-south-1,eu-west-1,eu-west-2,eu-west-3,me-south-1,sa-east-1,us-east-1,us-east-2,us-west-1,us-west-2}, --region {af-south-1,ap-east-1,ap-northeast-1,ap-northeast-2,ap-northeast-3,ap-south-1,ap-southeast-1,ap-southeast-2,ca-central-1,eu-central-1,eu-north-1,eu-south-1,eu-west-1,eu-west-2,eu-west-3,me-south-1,sa-east-1,us-east-1,us-east-2,us-west-1,us-west-2}
                        AWS Region
  -u UNIT, --unit UNIT  Expected unit in the response
  -m METRIC, --metric METRIC
                        Metric name
  -n NAMESPACE, --namespace NAMESPACE
                        Service Namespace
  -d [DIMENSIONS], --dimensions [DIMENSIONS]
                        One or more Dimensions for selecting datapoints:
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
  -v, --verbosity       Verbosity (use up to 3 times)
  -P [PERIOD], --period [PERIOD]
                        Period in seconds over which the statistic is applied
                        (default: 60)
  -D DELTA, --delta DELTA
                        Delta measurement in seconds
  -l LAG, --lag LAG     Delay in seconds to add to starting time (default: 0)
  -f [CREDENTIALS_FILE], --credentials_file [CREDENTIALS_FILE]
                        File containing AWS credentials
```

## Credentials and Authentication

The program looks for credentials in *~/.aws/credentials* by default. Use `--credentials_file` to override.

## Profiles

The [profiles](/profiles) directory contains a set of scripts for running the `check_aws` app in various
environments.

## Dimensions

Dimensions are name/value pairs that are part of the identity of a metric. One or more Dimensions can be provided
to the `check_aws` CLI to select what to monitor.

## Examples

Shows how the [profiles/check-aws.py](/profiles/check-aws.py) script can be used to monitor AWS metrics.

#### VPN availability

```
$ ./check-aws.py --metric TunnelState --namespace AWS/VPN -r eu-west-1 -w @0 -c @0 -d TunnelIpAddress=1.2.3.4
```

#### Free Space

```
$ ./check-aws.py --metric FreeStorageSpace --namespace AWS/RDS -r eu-west-1 -w @5000000000 -c @3000000000
```

#### Credit Usage

```
$ ./check-aws.py --metric CPUCreditUsage --namespace AWS/EC2 -r eu-west-1 -w 2 -c 3 -d InstanceId=i-0d7c12ec7asdf229
```

#### CPU utilization

```
$ ./check-aws.py --metric CPUUtilization --namespace AWS/EC2 -r eu-west-1 -w 50 -c 70 -d InstanceId=i-0d7c44ec7eaad229
```

#### ECS Running Tasks

```
$ ./check_aws.py -d ClusterName=my-ecs-cluster,ServiceName=my-ecs-service --metric RunningTaskCount --namespace ECS/ContainerInsights -w 1 -c 2
```

## Troubleshooting

To have the program print out stack traces and other useful information when troubleshooting, simply pass the `-v`
flag to the CLI. This argument can be stacked up to 3 times for extra verbosity.

## Other

#### AWS CLI

The AWS CLI--which expects a *Credentials File* for authentication, just like check-aws--can be used instead of the AWS
Web Console to get information about Instances and other data commonly used as plugin input.

##### Installation

```
$ pip install awscli
```

##### List instances

```
$ aws ec2 describe-instances --region eu-west-1
```

## Credits

This plugin was created by [ITRS Group: For the always-on enterprise](https://github.com/ITRS-Group).
