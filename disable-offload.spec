Name:		disable-offload
Version:	0.1
Release:	1%{?dist}
Summary:	Disables NIC offload settings at boot-time

Group:		System Environment/Base
License:	GPLv3+
URL:		
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	ethtool

%description
Disables offload settings at boot-time for ethernet adapters.
Behavior is controlled via SysV-style init script.

%prep
%setup -q


%build
# nothing to build


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_sbindir}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -pm755 src/scripts/disable-offload %{buildroot}%{_sbindir}
%{__install} -pm755 src/init.d/disable-offload %{buildroot}%{_sysconfdir}/rc.d/init.d


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sbindir}/disable-offload
%{_sysconfdir}/rc.d/init.d/disable-offload


%preun
if [ $1 -eq 0 ]; then
  service disable-offload stop || :
  chkconfig --del disable-offload || :
fi


%changelog
