%define plugin_root /opt/plugins
%define exec_path check_ec2cw.py
%define pkg_path ec2cw

Summary: EC2 CloudWatch Nagios Plugin
Name: monitor-plugin-check_ec2cw
Version: %{op5version}
Release: %{op5release}%{?dist}
Vendor: OP5 AB
License: GPL-3.0
Group: op5/system-addons
URL: http://www.op5.com/support
Prefix: /opt/plugins
%if 0%{?rhel} <= 6
Requires: python34
BuildRequires: python34
%else
Requires: python36
BuildRequires: python36
%endif
BuildRequires: curl
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArch: noarch

%description
Flexible Nagios plugin for monitoring CloudWatch-enabled EC2 instances.

%prep
%setup -q -n %{name}-%{version}

%build
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest

%{__install} -D -p %{exec_path} %{buildroot}/%{plugin_root}/%{exec_path}
cp --archive %{pkg_path} %{buildroot}/%{plugin_root}/

%files
%defattr(-, monitor, root)
%attr(755, monitor, root) %{plugin_root}/%{exec_path}
%attr(755, monitor, root) %{plugin_root}/%{pkg_path}/*
%license LICENSE
%doc README.md

%clean
rm -rf %buildroot

%changelog
* Fri Oct 10 2019 Robert Wikman <rwikman@op5.com> - 0.1.0
- Init
