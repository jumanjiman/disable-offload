Name:		disable-offload
Version:	0.2
Release:	1%{?dist}
Summary:	Disables NIC offload settings at boot-time

Group:		System Environment/Base
License:	GPLv3+
URL:		https://github.com/jumanjiman/disable-offload
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

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
%doc README
%doc COPYING.GPLv3
%{_sbindir}/disable-offload
%{_sysconfdir}/rc.d/init.d/disable-offload


%preun
if [ $1 -eq 0 ]; then
  service disable-offload stop || :
  chkconfig --del disable-offload || :
fi

%post
if [ $1 -gt 0 ]; then
  /sbin/chkconfig disable-offload --add || :
  /sbin/chkconfig disable-offload --resetpriorities || :
  /sbin/chkconfig disable-offload on || :
  grep 'ks=' /proc/cmdline &> /dev/null
  if [ $? -eq 0 ]; then
    # kickstarting
    :
  else
    # not kickstarting
    /sbin/service disable-offload start || :
  fi
fi


%changelog
* Wed Dec 19 2012 Paul Morgan <jumanjiman@gmail.com> 0.2-1
- wait until network is active to disable offload

* Thu Mar 24 2011 Paul Morgan <jumanjiman@gmail.com> 0.1-2
- enable init-script for boot-time (jumanjiman@gmail.com)

* Thu Jan 27 2011 Paul Morgan <jumanjiman@gmail.com> 0.1-1
- initial package


