%define debug_package %{nil}
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
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}
AutoReq: no
%if 0%{?rhel} >= 8
BuildRequires: python3-devel
Requires: python3-boto3
Requires: python3-dataclasses
Requires: python3-nagiosplugin
%else
Requires: python36
Requires(post): python36
BuildRequires: python36
%endif

%description
Nagios plugin for monitoring CloudWatch-enabled AWS services

%prep
%setup -q -n %{name}-%{version}

%build

%install
export LC_ALL=en_US.UTF-8

%if 0%{?rhel} >= 8
# Install check_aws into %%python3_sitelib and require dependencies from rpm repos.
%py3_install_wheel check_aws*.whl
%{__sed} -i -e '1 s|^#!.*|#!%{__python3} -I|' %{profile_source_path}
%else
# Ship pre-built binary wheels, to be installed in %%post.
%{__install} --directory %{buildroot}%{app_install_path}/wheels
%{__install} -m 644 -t %{buildroot}%{app_install_path}/wheels dist/*.whl
%endif

%{__install} -Dp %{profile_source_path} %{buildroot}%{check_install_path}

%if 0%{?rhel} < 8
%post
cd %{app_install_path}
%{__rm} -rf dist venv
/usr/bin/python3 -m venv venv
# First install the pip version that was used in the build
venv/bin/pip --quiet install --upgrade -f wheels --no-index --no-deps pip
# Then install all the remaining packages
venv/bin/pip --quiet install --upgrade -f wheels --no-index check_aws
%endif

%preun
if [ $1 -eq 0 ]; then
	%{__rm} -rf %{app_install_path}/venv || :
fi

%postun
# Remove old installation path created by previous versions before path was
# changed to current path, as venv created in %%post is left there.
%{__rm} -rf %{dirname:%{app_install_path}}/nagios_aws || :


%files
%if 0%{?rhel} >= 8
%python3_sitelib/check_aws*
%else
%{app_install_path}
%ghost %dir %{app_install_path}/venv
%endif
%{check_install_path}
%license LICENSE
%doc README.md

%clean
rm -rf %buildroot

%changelog
* Mon May  3 2021 Aksel Sjögren <asjogren@itrsgroup.com> - v2021.5.1
- Remove dependency on op5-monitor-user.
- Disable creation of debug package.
- Build for EL8; distribute prebuilt package and rely on Python dependencies
  via OS package manager.
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
