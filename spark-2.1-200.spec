# Example spec file for hadoop
Summary: Apache spark
Name: spark
Version: 2.1
Release: 200
License: GPL
Group: Applications/Server
Source: %{name}-%{version}-%{release}.tar.gz
Source1: spark-env.sh
Source2: hive-site.xml
URL: http://spark.apache.org
Packager: xbzy007
BuildRequires: /bin/cp,/bin/mkdir,/bin/rm
Requires:/bin/bash,/bin/sh,/bin/unlink
#Requires: perl-Net-SNMP xinetd,openssl-devel
Requires: jdk >=  1.8.0
Autoreq: 0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
#BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXX)
#Requires(post): chkconfig

%define __jar_repack 0
%define sparkpath  /usr/local/%{name}-%{version}-%{release}
%description
Apache Spark™ is a fast and general engine for large-scale data processing.

%prep
#%setup -q
rm -rf $RPM_BUILD_DIR/%{name}-%{version}-%{release}
zcat $RPM_SOURCE_DIR/%{name}-%{version}-%{release}.tar.gz | tar -xvf -
%build
cd %{name}-%{version}-%{release}
%install
cd %{name}-%{version}-%{release}
install -d -m 0755 ${RPM_BUILD_ROOT}%{sparkpath}
#tar zxf %{name}*.tar.gz -C ${RPM_BUILD_ROOT}%{sparkpath}
cp -a *  ${RPM_BUILD_ROOT}%{sparkpath}

install -p -D -m 0644 %{SOURCE1}  %{SOURCE2}  ${RPM_BUILD_ROOT}%{sparkpath}/conf
#cp  %{name}*.tar.gz  ${RPM_BUILD_ROOT}%{sparkpath}

%pre
%preun
#if [ $1 == 0 ];then
#fi
%post
if [ $1 == 1 ];then
#   tar zxf /usr/local/%{name}-*.tar.gz -C /usr/local/
#   rm -f /usr/local/%{name}-%{version}.tar.gz
/bin/ln -s /usr/local/%{name}-%{version}-%{release}  /usr/local/spark-current
mkdir -pm 777 /data/sparktmp
cp /etc/profile  /etc/profile_jdk_$(date +%F_%H-%M-%S)
sed -i '/SPARK_HOME/d' /etc/profile
source /etc/profile
echo 'export SPARK_HOME=/usr/local/spark-current' >>/etc/profile
echo 'export PATH=$SPARK_HOME/bin:$PATH'  >>/etc/profile
source /etc/profile
export SPARK_HOME=/usr/local/spark-current
export PATH=$SPARK_HOME/bin:$PATH
fi
%postun
if [ $1 == 0 ];then
sed -i '/SPARK_HOME/d' /etc/profile
source /etc/profile
/bin/unlink  /usr/local/spark-current
/bin/echo -e  "\e[1;32m %{name}-%{version}-%{release}  uninstall [ success ]\e[0m"
fi
%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_builddir}/%{name}-%{version}-%{release}
rm -f %{SOURCE1}  %{SOURCE2}   %{SOURCE0}
%files
%defattr(-,root,root)
/usr/local/%{name}-%{version}-%{release}
%changelog
* Thu  Mar  15   2017  xbz <xbzy007@didichuxing.com>
- Add rpm package
