%global debug_package %{nil}

Summary:         Openfire XMPP Server
Name:            openfire
Version:         5.0.4
Release:         1%{?dist}
BuildRequires:   ant java-devel-openjdk fdupes
Requires:        java
Source0:         https://github.com/igniterealtime/Openfire/releases/download/v%{version}/openfire-%{version}.tar.gz
License:         GPL
URL:             http://www.igniterealtime.org/
Patch0:          openfire-sysvinit.patch
#Patch1:         openfire-3.7.0-SSLConfig.patch
#Patch2:         openfire-3.7.0-IPv6-workaround.patch
%define          prefix /usr/share
%define          homedir %{prefix}/openfire

%description
Openfire is a leading Open Source, cross-platform IM server based on the
XMPP (Jabber) protocol. It has great performance, is easy to setup and use,
and delivers an innovative feature set.

%package doc
Summary:     Openfire XMPP Server Documentation
#BuildArch:  noarch

%description doc
This package contains optional documentation provided in addition to
this package's base documentation.

%prep
%setup -q -n %{name}_src
%patch0 -p1
#patch1 -p0
#%patch2 -p0

%build
# Build Tasks
cd build
# Default | openfire
ant openfire
# Specific Plugins
ant -Dplugin=search plugin
cd ..

%install
export NO_BRP_CHECK_BYTECODE_VERSION=true

# Prep the install location.
mkdir -p %{buildroot}%{prefix}

# Copy over the main install tree.
cp -R target/openfire %{buildroot}%{homedir}

# Set up the init script.
mkdir -p %{buildroot}/etc/init.d
cp %{buildroot}%{homedir}/bin/extra/redhat/openfire %{buildroot}/etc/init.d/openfire
chmod 755 %{buildroot}/etc/init.d/openfire
mkdir -p %{buildroot}%{_sbindir}
ln -s -f %{_sysconfdir}/init.d/%{name} %{buildroot}%{_sbindir}/rc%{name}

# Make the startup script executable.
chmod 755 %{buildroot}%{homedir}/bin/openfire.sh

# Set up the sysconfig file.
#mkdir -p %{buildroot}/etc/sysconfig
#cp %{buildroot}%{homedir}/bin/extra/redhat/openfire-sysconfig %{buildroot}/etc/sysconfig/openfire
mkdir -p %{buildroot}/var/adm/fillup-templates/
install -D %{buildroot}%{homedir}/bin/extra/redhat/openfire-sysconfig %{buildroot}/var/adm/fillup-templates/sysconfig.openfire
chmod -x %{buildroot}/var/adm/fillup-templates/sysconfig.openfire

# Copy over the i18n files
cp -R resources/i18n %{buildroot}%{homedir}/resources/i18n

# Make sure scripts are executable
chmod 755 %{buildroot}%{homedir}/bin/extra/openfired
chmod 755 %{buildroot}%{homedir}/bin/extra/redhat-postinstall.sh

# Move over the embedded db viewer pieces
mv %{buildroot}%{homedir}/bin/extra/embedded-db.rc %{buildroot}%{homedir}/bin
mv %{buildroot}%{homedir}/bin/extra/embedded-db-viewer.sh %{buildroot}%{homedir}/bin

# We don't really need any of these things.
rm -rf %{buildroot}%{homedir}/bin/extra
rm -f %{buildroot}%{homedir}/bin/*.bat
rm -rf %{buildroot}%{homedir}/resources/nativeAuth/osx-ppc
rm -rf %{buildroot}%{homedir}/resources/nativeAuth/solaris-sparc
rm -rf %{buildroot}%{homedir}/resources/nativeAuth/win32-x86
rm -f %{buildroot}%{homedir}/lib/*.dll
rm -rf %{buildroot}%{homedir}/resources/spank

# Dont enable fdupes (on resources/security/) as it breaks the crypto store
# See: http://www.igniterealtime.org/issues/browse/OF-30
# For now disabled completely..
#%fdupes -s %{buildroot}

%files
%attr(750, daemon, daemon) %dir %{homedir}
%dir %{homedir}/bin
%{homedir}/bin/openfire.sh
%attr(750, daemon, daemon) %{homedir}/bin/openfirectl
%config(noreplace) %{homedir}/bin/embedded-db.rc
%{homedir}/bin/embedded-db-viewer.sh
%dir %{homedir}/conf
%config(noreplace) %{homedir}/conf/*
%dir %{homedir}/lib
%{homedir}/lib/*.jar
%{homedir}/lib/log4j.xml
%dir %{homedir}/logs
%{homedir}/plugins
%dir %{homedir}/resources
%dir %{homedir}/resources/database
%{homedir}/resources/database/*.sql
%dir %{homedir}/resources/database/upgrade
%dir %{homedir}/resources/database/upgrade/*
%{homedir}/resources/database/upgrade/*/*
%dir %{homedir}/resources/i18n
%{homedir}/resources/i18n/*
%dir %{homedir}/resources/nativeAuth
%dir %{homedir}/resources/nativeAuth/linux-i386
%{homedir}/resources/nativeAuth/linux-i386/*
%dir %{homedir}/resources/security
%config(noreplace) %{homedir}/resources/security/keystore
%config(noreplace) %{homedir}/resources/security/truststore
%config(noreplace) %{homedir}/resources/security/client.truststore
#%doc %{homedir}/documentation
#%doc %{homedir}/LICENSE.html
#%doc %{homedir}/README.html
#%doc %{homedir}/changelog.html
%{_sbindir}/rc%{name}
%{_sysconfdir}/init.d/openfire
#%config(noreplace) %{_sysconfdir}/sysconfig/openfire
%config(noreplace) /var/adm/fillup-templates/sysconfig.openfire
#%{homedir}/jre

%files doc
%doc documentation/docs/* LICENSE.html README.html changelog.html

%changelog
* Fri Apr 24 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 5.0.4-1
- Update to 5.0.4
- Update Source0 to GitHub release tarball URL

* Fri Apr 24 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 4.2.3-2
- Modernize spec for AlmaLinux 10; remove Group, %clean, %defattr
- Replace $RPM_BUILD_ROOT with %%{buildroot} throughout

* Sat Jan 29 2022 CasjaysDev <rpm-dev@casjaysdev.pro> - 4.2.3
- Updated to 4.2.3 and fix source URL
* Mon Feb 20 2017 Huaren Zhong <huaren.zhong@gmail.com> 4.1.2
- Rebuild for Fedora
* Tue Jan 26 2010 nix@opensuse.org
- Dont enable fdupes (on resources/security/) as it breaks the crypto store
  See: http://www.igniterealtime.org/issues/browse/OF-30
  For now disabled completely..
* Tue Jan 19 2010 nix@opensuse.org
- Add openfire-3.6.4-self_signed_certificate.patch from to fix SSL
  cert problem: http://www.igniterealtime.org/issues/browse/OF-30
* Fri Oct 23 2009 nix@opensuse.org
- Change java dependency to "java-sun >=1.6.0" so that SLES 11 works properly
* Fri Jun 19 2009 claes.backstrom@fsfe.org
- New upstrean 3.6.4
* Wed Apr 29 2009 claes.backstrom@fsfe.org
- New upstream 3.6.3
* Wed Jan  9 2008 claes.backstrom@fsfe.org
- Initial package
