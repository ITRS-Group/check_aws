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
BuildRequires: python39-devel
BuildRequires: python39-pip
Requires: python39
Requires(post): python39
%else
Requires: python36
Requires(post): python36
BuildRequires: python36
%endif
# This package has changed from noarch to arch specific. Therefor obsolete
# everything before the last released noarch package (v2021.5.1), to avoid yum
# "Error: Protected multilib versions".
Obsoletes: %{name} <= 2021.5.1-op5.2

%description
Nagios plugin for monitoring CloudWatch-enabled AWS services

%package test
Summary: Test tools for check_aws
Requires: monitor-plugin-check_aws == %{version}-%{release}

%description test
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build

%install
export LC_ALL=en_US.UTF-8

# Upgrade to pip version used for building the wheels in pre-build step
%{__python3} -m pip install --user --no-index -f dist/ --upgrade pip

# Ship pre-built binary wheels, to be installed in %%post.
%{__install} --directory %{buildroot}%{app_install_path}/wheels
%{__install} -m 644 -t %{buildroot}%{app_install_path}/wheels dist/*.whl

%{__install} -Dp %{profile_source_path} %{buildroot}%{check_install_path}

# Install all wheels in /test dir, for -test subpackage.
%{__python3} -m pip install -I --no-index --no-warn-script-location --no-deps \
	--prefix %{app_install_path}/test --root %{buildroot} dist/*.whl

%{__python3} -m pip install -I --no-index --no-warn-script-location --no-deps \
	--prefix %{app_install_path}/test --root %{buildroot} test-wheels/*.whl

# Metadata
%{__mkdir} -p -m 0755 %buildroot%prefix/metadata
%{__install} -m 0644 op5build/check_aws.metadata %buildroot%prefix/metadata/

%post
cd %{app_install_path}
%{__rm} -rf dist venv
%{__python3} -m venv venv
# First install the pip version that was used in the build
venv/bin/pip --quiet install --upgrade -f wheels --no-index --no-deps pip
# Then install all the remaining packages
venv/bin/pip --quiet install --upgrade -f wheels --no-index check_aws

%preun
if [ $1 -eq 0 ]; then
	%{__rm} -rf %{app_install_path}/venv || :
fi

%postun
# Remove old installation path created by previous versions before path was
# changed to current path, as venv created in %%post is left there.
%{__rm} -rf %{dirname:%{app_install_path}}/nagios_aws || :


%files
%{app_install_path}
%exclude %{app_install_path}/test
%ghost %dir %{app_install_path}/venv
%{check_install_path}
%license LICENSE
%doc README.md
%dir %attr(0755,-,-) %prefix/metadata/
%prefix/metadata/check_aws.metadata

%files test
%{app_install_path}/test

%clean
rm -rf %buildroot

%changelog
* Tue Mar  7 2023 Jerson Dumalaon <jdumalaon@itrsgroup.com>
- Update to use Python3.9
* Mon Jan 17 2022 Erik Sjöström <esjostrom@itrsgroup.com>
- Package metadata.
* Thu Jan  6 2022 Aksel Sjögren <asjogren@itrsgroup.com>
- Add test subpackage with Python packages for post install tests.
* Mon May 31 2021 Aksel Sjögren <asjogren@itrsgroup.com>
- Obsolete previous noarch releases of the package.
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
