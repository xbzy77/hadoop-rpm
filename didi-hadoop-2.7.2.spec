# Example spec file for hadoop
Summary: Apache hadoop
Name: didi-hadoop
Version: 2.7.2
Release: 1%{?dist}
License: GPL
Group: Applications/Server
Source: %{name}-%{version}.tar.gz
URL: http://hadoop.apache.org
Packager: xbzy007
BuildRequires: /bin/cp,/bin/mkdir,/bin/rm
Requires:/bin/bash,/bin/sh
#Requires: perl-Net-SNMP xinetd,openssl-devel
Requires: jdk >=  1.8.0
Autoreq: 0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
#BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXX)
#Requires(post): chkconfig

%define __jar_repack 0
%define hadooppath  /usr/local/%{name}-%{version}
%description

The Apache™ Hadoop® project develops open-source software for reliable, scalable, distributed computing.

%prep
%setup -q
#rm -rf $RPM_BUILD_DIR/%{name}-%{version}
#zcat $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz | tar -xvf -
%build
#cd %{name}-%{version}
%install
install -d -m 0755 ${RPM_BUILD_ROOT}%{hadooppath}
#tar zxf %{name}*.tar.gz -C ${RPM_BUILD_ROOT}%{hadooppath}
cp -a *  ${RPM_BUILD_ROOT}%{hadooppath}

#cp  %{name}*.tar.gz  ${RPM_BUILD_ROOT}%{hadooppath}

%pre
%preun
#if [ $1 == 0 ];then
#fi
%post
if [ $1 == 1 ];then
/bin/ln -sf /usr/local/%{name}-%{version}  /usr/local/hadoop-current
/bin/ln -sf /usr/local/%{name}-%{version}  /usr/local/hadoop-%{version}
cp /etc/profile  /etc/profile_jdk_$(date +%F_%H-%M-%S)
sed -i '/HADOOP_HOME/d' /etc/profile
source /etc/profile
echo 'export HADOOP_HOME=/usr/local/hadoop-current' >>/etc/profile
echo 'export PATH=$HADOOP_HOME/bin:$PATH'  >>/etc/profile
export HADOOP_HOME=/usr/local/hadoop-current
export PATH=$HADOOP_HOME/bin:$PATH
fi
%postun
if [ $1 == 0 ];then
sed -i '/HADOOP_HOME/d' /etc/profile
unlink /usr/local/hadoop-current
unlink /usr/local/hadoop-%{version}
/bin/echo -e  "\e[1;32m %{name}-%{version} uninstall [ success ]\e[0m"
fi
%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_builddir}/%{name}-%{version}
%files
%defattr(-,root,root)
/usr/local/%{name}-%{version}
%changelog
* Thu  Mar  15   2017  xbz <xuebaiji@didichuxing.com>
- Add rpm package
