%define profile_source_path profiles/op5_monitor.py
%define app_install_path /opt/monitor/op5/check_aws
%define check_install_path /opt/plugins/check_aws.py

Summary: AWS Nagios plugin
Name: monitor-plugin-check_aws
Version: %{op5version}
Release: %{op5release}%{?dist}
Vendor: OP5 AB
License: GPLv3+
Group: op5/system-addons
URL: https://www.itrsgroup.com
Prefix: /opt/plugins
Requires: python36
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

%{__install} -Dp -m 644 dist.tar.gz %{buildroot}%{app_install_path}/dist.tar.gz
%{__install} -Dp %{profile_source_path} %{buildroot}%{check_install_path}

%post
cd %{app_install_path}
%{__rm} -rf dist venv
%{__tar} xfz dist.tar.gz
/usr/bin/python3 -m venv venv
venv/bin/pip --quiet install --upgrade -f dist --no-index dist/check_aws-*.whl

# Remove build artifacts
%{__rm} --recursive --force %{app_install_path}/dist

%preun
if [ $1 -eq 0 ]; then
	%{__rm} -rf %{app_install_path}/venv || :
fi

%postun
# Remove old installation path created by previous versions before path was
# changed to current path, as venv created in %post is left there.
%{__rm} -rf %{dirname:%{app_install_path}}/nagios_aws || :


%files
%{app_install_path}
%ghost %dir %{app_install_path}/venv
%{check_install_path}
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
