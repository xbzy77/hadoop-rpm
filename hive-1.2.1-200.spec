# Example spec file for hadoop
Summary: Apache Hive
Name: hive
Version: 1.2.1
Release: 200%{?dist}
License: GPL
Group: Applications/Server
Source: %{name}-%{version}.tar.gz
Source1: hive-env.sh
Source2: hive-log4j.properties
Source3: hive-site.xml
Source4: ivysettings.xml
URL: http://hive.apache.org
Packager: xbzy007
BuildRequires: /bin/cp,/bin/mkdir,/bin/rm
Requires:/bin/bash,/bin/sh,/bin/unlink
#Requires: perl-Net-SNMP xinetd,openssl-devel
Requires: jdk >=  1.8.0
Autoreq: 0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
#BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXX)
#Requires(post): chkconfig

%define sversion 300
%define __jar_repack 0
%define hivepath  /usr/local/%{name}-%{version}-%{sversion}
%description
Apache Spark™ is a fast and general engine for large-scale data processing.

%prep
%setup -q
#rm -rf $RPM_BUILD_DIR/%{name}-%{version}
#zcat $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz | tar -xvf -
%build
#cd %{name}-%{version}
%install
install -d -m 0755 ${RPM_BUILD_ROOT}%{hivepath}
#tar zxf %{name}*.tar.gz -C ${RPM_BUILD_ROOT}%{hivepath}
cp -a *  ${RPM_BUILD_ROOT}%{hivepath}
#cp  %{name}*.tar.gz  ${RPM_BUILD_ROOT}%{hivepath}
install -p -D -m 0644 %{SOURCE1}  %{SOURCE2} %{SOURCE3}  ${RPM_BUILD_ROOT}%{hivepath}/conf


%pre
%preun
#if [ $1 == 0 ];then
#fi
%post
if [ $1 == 1 ];then
#   tar zxf /usr/local/%{name}-*.tar.gz -C /usr/local/
#   rm -f /usr/local/%{name}-%{version}.tar.gz
/bin/ln -snf %{hivepath}  /usr/local/hive-current
/bin/mkdir -pm 1777 /data/hive
cp /etc/profile  /etc/profile_hive_$(date +%F_%H-%M-%S)
sed -i '/HIVE_HOME/d' /etc/profile
source /etc/profile
echo 'export HIVE_HOME=/usr/local/hive-current' >>/etc/profile
echo 'export PATH=$HIVE_HOME/bin:$PATH'  >>/etc/profile
export HIVE_HOME=/usr/local/hive-current
export PATH=${HIVE_HOME}/bin:$PATH
fi
%postun
if [ $1 == 0 ];then
sed -i '/HIVE_HOME/d' /etc/profile
/bin/unlink  /usr/local/hive-current
/bin/rm -rf /data/hive
/bin/echo -e  "\e[1;32m %{name}-%{version} uninstall [ success ]\e[0m"
fi
%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_builddir}/%{name}-%{version}
rm -f %{SOURCE1}  %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE0}
%files
%defattr(-,root,root)
%{hivepath}
%changelog
* Thu  Mar  15   2017  xbz <xbzy007@007.com>
- Add rpm package
