%define plugin_root /opt/plugins
%define lib_root /opt/monitor/op5/check_aws
%define pkg_path aws
%define user monitor
%define executable_name check_aws

Summary: CloudWatch Nagios Plugin
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
Flexible Nagios plugin for monitoring CloudWatch-enabled AWS.

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
%{__mkdir} -p %{buildroot}%{lib_root}
%{__install} -Dp -m0644 dist.tar.gz %{buildroot}%{lib_root}/dist.tar.gz
# %{__install} -Dp -m0755 check_aws %{buildroot}%{plugin_root}/%{executable_name}

%post
cd %{lib_root}
%{__rm} -rf dist venv
%{__tar} xvfz dist.tar.gz
/usr/bin/python3 -m venv .venv
.venv/bin/pip install --upgrade -f dist --no-index dist/check_aws-*.whl
%{__chown} -R %{user} .

%files
%defattr(-, monitor, root)
%attr(644, monitor, root) %{lib_root}/dist.tar.gz
# %attr(755, monitor, root) %{plugin_root}/%{executable_name}
%exclude %{lib_root}/setup.pyc
%exclude %{lib_root}/setup.pyo
%license LICENSE
%doc README.md

%clean
rm -rf %buildroot

%changelog
* Fri Oct 11 2019 Robert Wikman <rwikman@op5.com> - 0.1.0
- Init
