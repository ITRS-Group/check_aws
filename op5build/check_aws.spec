%define profile_source_path profiles/op5_monitor.py
%define app_install_path /opt/monitor/op5/nagios_aws
%define check_install_path /opt/plugins/check_aws.py
%define user monitor

Summary: AWS Nagios plugin
Name: monitor-plugin-check_aws
Version: %{op5version}
Release: %{op5release}%{?dist}
Vendor: OP5 AB
License: GPL-3.0-or-later
Group: op5/system-addons
URL: http://www.op5.com/support
Prefix: /opt/plugins
Requires: python36
BuildRequires: python36
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArch: noarch

%description
Nagios plugin for monitoring CloudWatch-enabled AWS services

%prep
%setup -q -n %{name}-%{version}

%build
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest

%install
export LC_ALL=en_US.UTF-8
/usr/bin/python3 -m venv .venv
.venv/bin/pip install poetry
.venv/bin/python -m poetry build
.venv/bin/pip download -r requirements.txt -d dist
%{__tar} cvfz dist.tar.gz dist

%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{app_install_path}
%{__install} -Dp -m0644 dist.tar.gz %{buildroot}%{app_install_path}/dist.tar.gz
# %{__install} -Dp -m0755 %{profile_source_path} %{buildroot}%{check_install_path}

%post
cd %{app_install_path}
%{__rm} -rf dist .venv
%{__tar} xvfz dist.tar.gz
/usr/bin/python3 -m venv .venv
.venv/bin/pip install --upgrade -f dist --no-index dist/nagios_aws-*.whl
%{__chown} -R %{user} .

%files
%defattr(-, monitor, root)
%attr(644, monitor, root) %{app_install_path}/dist.tar.gz
# %attr(755, monitor, root) %{check_install_path}
%exclude %{app_install_path}/setup.pyc
%exclude %{app_install_path}/setup.pyo
%license LICENSE
%doc README.md

%clean
rm -rf %buildroot

%changelog
* Fri Oct 11 2019 Robert Wikman <rwikman@op5.com> - 0.1.0
- Init
