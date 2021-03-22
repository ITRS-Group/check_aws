%define profile_source_path profiles/op5_monitor.py
%define app_install_path /opt/monitor/op5/check_aws
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
Requires: op5-monitor-user
BuildRequires: python36
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArch: noarch
AutoReq: no

%description
Nagios plugin for monitoring CloudWatch-enabled AWS services

%prep
%setup -q -n %{name}-%{version}

%build
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest

%install
export LC_ALL=en_US.UTF-8
/usr/bin/python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install poetry
venv/bin/python -m poetry build
venv/bin/pip download -r requirements.txt -d dist
%{__tar} cvfz dist.tar.gz dist

%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{app_install_path}
%{__install} -Dp dist.tar.gz %{buildroot}%{app_install_path}/dist.tar.gz
%{__install} -Dp %{profile_source_path} %{buildroot}%{check_install_path}

%post
cd %{app_install_path}
%{__rm} -rf dist venv
%{__tar} xvfz dist.tar.gz
/usr/bin/python3 -m venv venv
venv/bin/pip install --upgrade -f dist --no-index dist/check_aws-*.whl
%{__chown} -R %{user} .

# Remove build artifacts
%{__rm} --recursive --force %{app_install_path}/dist %{app_install_path}/dist.tar.gz

%files
%defattr(-, monitor, root)
%attr(644, monitor, root) %{app_install_path}/dist.tar.gz
%attr(755, monitor, root) %{check_install_path}
%exclude %{app_install_path}/setup.pyc
%exclude %{app_install_path}/setup.pyo
%exclude /opt/plugins/check_aws.pyo
%exclude /opt/plugins/check_aws.pyc
%license LICENSE
%doc README.md

%clean
rm -rf %buildroot

%changelog
* Mon Mar 15 2021 Robert Wikman <rwikman@op5.com> - 0.3.1
- Add CLI input validation
* Wed Jan 06 2021 Robert Wikman <rwikman@op5.com> - 0.3.0
- Switch to Boto3 for interacting with AWS
* Wed Oct 28 2020 Erik Sjöström <esjostrom@itrsgroup.com>
- Remove build artifacts and make the venv visible to the user
* Thu May 28 2020 Jacob Hansen <jhansen@op5.com> - 0.2.0
- Require op5-monitor-user
* Fri Oct 11 2019 Robert Wikman <rwikman@op5.com> - 0.1.0
- Init