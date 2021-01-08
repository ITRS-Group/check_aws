# nagios_aws: AWS monitoring plugin

Nagios/Naemon-compatible plugin for monitoring CloudWatch-enabled AWS instances.

To get started, visit the [AWS Web Console](https://console.aws.amazon.com/cloudwatch) to determine what to monitor, and
check out
the [AWSEC2 UserGuide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html) to see
how things maps to **nagios_aws** input.

### Table of Contents

- [CLI Usage](#cli-usage)
- [Credentials and Authentication](#credentials-and-authentication)
- [Examples](#examples)
    * [VPN Availability](#vpn-availability)
    * [Free Space](#free-space)
    * [Credit Usage](#credit-usage)
    * [CPU Utilization](#cpu-utilization)
- [Troubleshooting](#troubleshooting)
- [Other](#other)
    * [AWS CLI](#aws-cli)
- [Credits](#credits)

## CLI Usage

```
usage: nagios_aws [-h] -r
                    {ap-southeast-2,us-east-1,ca-central-1,us-gov-west-1,eu-west-1,eu-west-2,us-west-2,eu-central-1,cn-north-1,us-west-1,ap-northeast-1,ap-southeast-1,sa-east-1,us-east-2,ap-northeast-2,ap-south-1}
                    [-u UNIT] -m METRIC -n NAMESPACE [-d [DIMENSIONS]]
                    [-p PROFILE]
                    [-s {Average,Sum,SampleCount,Maximum,Minimum}]
                    [-w WARNING] [-c CRITICAL] [-v] [-P [PERIOD]] [-D DELTA]
                    [-l LAG] [-C [CREDENTIALS_FILE]]

Plugin for monitoring CloudWatch-enabled AWS instances

optional arguments:
  -h, --help            show this help message and exit
  -r {ap-southeast-2,us-east-1,ca-central-1,us-gov-west-1,eu-west-1,eu-west-2,us-west-2,eu-central-1,cn-north-1,us-west-1,ap-northeast-1,ap-southeast-1,sa-east-1,us-east-2,ap-northeast-2,ap-south-1}, --region {ap-southeast-2,us-east-1,ca-central-1,us-gov-west-1,eu-west-1,eu-west-2,us-west-2,eu-central-1,cn-north-1,us-west-1,ap-northeast-1,ap-southeast-1,sa-east-1,us-east-2,ap-northeast-2,ap-south-1}
                        AWS region name
  -u UNIT, --unit UNIT  Metric Unit
  -m METRIC, --metric METRIC
                        CloudWatch metric name
  -n NAMESPACE, --namespace NAMESPACE
                        CloudWatch metric namespace
  -d [DIMENSIONS], --dimensions [DIMENSIONS]
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
  -P [PERIOD], --period [PERIOD]
                        Period in seconds over which the statistic is applied
                        (default: 60)
  -D DELTA, --delta DELTA
                        Delta measurement in seconds
  -l LAG, --lag LAG     Delay in seconds to add to starting time for gathering
                        metric.useful for ec2 basic monitoring which
                        aggregates over 5min periods (default: 0)
  -C [CREDENTIALS_FILE], --credentials [CREDENTIALS_FILE]
                        File containing AWS credentials
```

## Credentials and Authentication

The program looks for credentials in *~/.aws/credentials* by default. This can be overridden by passing a custom path as
argument to the `--credentials` CLI option.

## Examples

These examples can be invoked with `$ python -m nagios_aws <example>`.

#### VPN availability

```
--metric TunnelState --namespace AWS/VPN -r eu-west-1 -w @0 -c @0 -d TunnelIpAddress=1.2.3.4 --unit Count
```

#### Free Space

```
--metric FreeStorageSpace --namespace AWS/RDS -r eu-west-1 -w @5000000000 -c @3000000000 --unit Bytes
```

#### Credit Usage

```
--metric CPUCreditUsage --namespace AWS/EC2 -r eu-west-1 -w 2 -c 3 --period 18000 -d InstanceId=i-0d7c12ec7asdf229 --unit Count
```

#### CPU utilization

```
--metric CPUUtilization --namespace AWS/EC2 -r eu-west-1 -w 50 -c 70 -d InstanceId=i-0d7c44ec7eaad229 --period 1800 --unit Count
```

## Troubleshooting

To have the program print out stack traces and other useful information when troubleshooting, simply pass the `-v`
argument to the CLI. The argument can be stacked up to 3 times, with each stack adding an extra level of detail.

## Other

#### AWS CLI

The AWS CLI--which expects a *Credentials File* for authentication, just like nagios_aws--can be used instead of the AWS
Web Console to get information about Instances and other data commonly used as plugin input.

##### Install

```
$ pip install awscli
```

##### List instances

```
$ aws ec2 describe-instances --region eu-west-1
```

## Credits

The plugin was created by [ITRS Group: For the always-on enterprise](https://github.com/ITRS-Group). It makes use
of [boto/boto3](https://github.com/boto/boto3) for interacting with AWS CloudWatch,
and [mpounsett/nagiosplugin](https://github.com/mpounsett/nagiosplugin) for marshalling with Nagios.
