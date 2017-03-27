# Example spec file for hadoop
Summary: Apache hadoop
Name: hadoop
Version: 2.7.2
Release: 300%{?dist}
License: GPL
Group: Applications/Server
Source: %{name}-%{version}.tar.gz
Source1: core-site.xml
Source2: hdfs-site.xml
Source3: mapred-site.xml
Source4: yarn-site.xml
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

%define sversion 300
%define __jar_repack 0
%define hadooppath  /usr/local/%{name}-%{version}-%{sversion}
%description

The Apache™ Hadoop® project develops open-source software for reliable, scalable, distributed computing.

%prep
%setup -q
#rm -rf $RPM_BUILD_DIR/%{name}-%{version}-%{release}
#zcat $RPM_SOURCE_DIR/%{name}-%{version}-%{release}.tar.gz | tar -xvf -
%build
#cd %{name}-%{version}-%{release}
%install
#cd %{name}-%{version}-%{release}
install -d -m 0755 ${RPM_BUILD_ROOT}%{hadooppath}
#install -d -m 0755 ${RPM_BUILD_ROOT}%{hadooppath}/etc/hadoop
#tar zxf %{name}*.tar.gz -C ${RPM_BUILD_ROOT}%{hadooppath}
cp -a *  ${RPM_BUILD_ROOT}%{hadooppath}

install -p -D -m 0644 %{SOURCE4}  %{SOURCE1} %{SOURCE2} %{SOURCE3}   ${RPM_BUILD_ROOT}%{hadooppath}/etc/hadoop/

#cp  %{name}*.tar.gz  ${RPM_BUILD_ROOT}%{hadooppath}

%pre
%preun
#if [ $1 == 0 ];then
#fi
%post
if [ $1 == 1 ];then
/bin/ln -snf %{hadooppath}  /usr/local/hadoop-current
#/bin/ln -sf /usr/local/%{name}-%{version}  /usr/local/hadoop-%{version}
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
/bin/echo -e  "\e[1;32m %{name}-%{version}-%{release} uninstall [ success ]\e[0m"
fi
%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_builddir}/%{name}-%{version}-%{release}
rm -f %{SOURCE4}  %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE0}
%files
%defattr(-,root,root)
%{hadooppath}
%changelog
* Thu  Mar  15   2017  xbz <xbzy007@007.com>
- Add rpm package
