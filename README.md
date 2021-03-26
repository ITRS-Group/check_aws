# check_aws: AWS monitoring plugin

[![image](https://badgen.net/travis/ITRS-Group/check_aws)](https://travis-ci.org/ITRS-Group/check_aws)
[![image](https://badgen.net/lgtm/grade/g/ITRS-Group/check_aws)](https://lgtm.com/projects/g/ITRS-Group/check_aws)
[![image](https://badgen.net/codecov/c/github/ITRS-Group/check_aws)](https://codecov.io/gh/ITRS-Group/check_aws)
[![image](https://badgen.net/badge/license/GPLv3/blue)](https://raw.githubusercontent.com/ITRS-Group/check_aws/master/LICENSE)

Nagios/Naemon-compatible plugin for monitoring CloudWatch-enabled AWS instances.

To get started, visit the [AWS Web Console](https://console.aws.amazon.com/cloudwatch) to determine what to monitor, and
check out
the [AWSEC2 UserGuide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html) to see
how things maps to **check_aws** input.

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
usage: check_aws [-h] -r REGION -m METRIC -n NAMESPACE
                 [-u UNIT] [-d [DIMENSIONS]] [-p PROFILE]
                 [-s {Average,Sum,SampleCount,Maximum,Minimum}]
                 [-w WARNING] [-c CRITICAL] [-v] [-P [PERIOD]] [-D DELTA]
                 [-l LAG] [-C [CREDENTIALS_FILE]]

Plugin for monitoring CloudWatch-enabled AWS instances

  -r, --region {af-south-1,ap-east-1,ap-northeast-1,ap-northeast-2,ap-northeast-3,ap-south-1,ap-southeast-1,ap-southeast-2,ca-central-1,eu-central-1,eu-north-1,eu-south-1,eu-west-1,eu-west-2,eu-west-3,me-south-1,sa-east-1,us-east-1,us-east-2,us-west-1,us-west-2}
                        AWS region name
  -u, --unit UNIT  Response unit
  -m, --metric          METRIC
                        Metric name
  -n, --namespace NAMESPACE
                        Metric namespace
  -d, --dimensions [DIMENSIONS]
                        Dimensions of one or more metrics:
                        dimension=value[,dimension=value...]
  -p, --profile PROFILE
                        Profile name from ~/.aws/credentials (default:
                        default)
  -s, --statistic {Average,Sum,SampleCount,Maximum,Minimum}
                        Statistic for evaluating metrics (default: Average)
  -w, --warning WARNING
                        Warning if threshold is outside range (default: 0)
  -c, --critical CRITICAL
                        Critical if threshold is outside range (default: 0)
  -v, --verbosity       Verbosity (use up to 3 times)
  -P, --period [PERIOD]
                        Period in seconds over which the statistic is applied
                        (default: 60)
  -D, --delta DELTA
                        Delta measurement in seconds
  -l, --lag LAG         Delay in seconds to add to starting time for gathering
                        metric.useful for ec2 basic monitoring which
                        aggregates over 5min periods (default: 0)
  -f, --credentials_file [CREDENTIALS_FILE]
                        File containing AWS credentials
```

## Credentials and Authentication

The program looks for credentials in *~/.aws/credentials* by default. Use `--credentials_file` to override.

## Examples

#### VPN availability

```
$ ./check_aws.py --metric TunnelState --namespace AWS/VPN -r eu-west-1 -w @0 -c @0 -d TunnelIpAddress=1.2.3.4
```

#### Free Space

```
$ ./check_aws.py --metric FreeStorageSpace --namespace AWS/RDS -r eu-west-1 -w @5000000000 -c @3000000000
```

#### Credit Usage

```
$ ./check_aws.py --metric CPUCreditUsage --namespace AWS/EC2 -r eu-west-1 -w 2 -c 3 --period 18000 -d InstanceId=i-0d7c12ec7asdf229
```

#### CPU utilization

```
$ ./check_aws.py --metric CPUUtilization --namespace AWS/EC2 -r eu-west-1 -w 50 -c 70 -d InstanceId=i-0d7c44ec7eaad229 --period 1800
```

## Troubleshooting

To have the program print out stack traces and other useful information when troubleshooting, simply pass the `-v`
flag to the CLI. This argument can be stacked up to 3 times for extra verbosity.

## Other

#### AWS CLI

The AWS CLI--which expects a *Credentials File* for authentication, just like check_aws--can be used instead of the AWS
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

This plugin was created by [ITRS Group: For the always-on enterprise](https://github.com/ITRS-Group). It makes use
of [boto/boto3](https://github.com/boto/boto3) for interacting with AWS CloudWatch,
and [mpounsett/nagiosplugin](https://github.com/mpounsett/nagiosplugin) for marshalling with Nagios.
