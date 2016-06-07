%if 0%{?fedora}
%global with_devel 1
%global with_unit_test 1
%else
%global with_devel 0
%global with_unit_test 0
%endif

%global with_unit_test 1
# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global __os_install_post %{_rpmconfigdir}/brp-compress

#debuginfo not supported with Go
%global debug_package %{nil}
%global provider_tld com
%global provider github
%global project docker
%global repo %{project}

%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}

# docker
%global git0 https://github.com/projectatomic/docker
%global commit0 47792252c76d4f10ae06795e91a982874ee02e8d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# docker-selinux
%global git1 https://github.com/projectatomic/docker-selinux
%global commit1 032bcda7b1eb6d9d75d3c0ce64d9d35cdb9c7b85
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

# d-s-s
%global git2 https://github.com/projectatomic/docker-storage-setup
%global commit2 194eca25fd0d180b62f3ecf1b7b408992fd6a083
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global dss_libdir %{_exec_prefix}/lib/%{name}-storage-setup

# forward-journald
%global git3 https://github.com/projectatomic/forward-journald
%global commit3  77e02a9774a6ca054e41c27f6f319d701f1cbaea
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})

# docker-novolume-plugin
%global git4 https://github.com/projectatomic/%{repo}-novolume-plugin
%global commit4 7715854b5f3ccfdbf005c9e95d6e9afcaae9376a
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})

# rhel-push-plugin
%global git5 https://github.com/projectatomic/rhel-push-plugin
%global commit5 904c0ca2a285e5e7c514c2eb90f5919bc59b6f86
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})

# docker-lvm-plugin
%global git6 https://github.com/projectatomic/%{repo}-lvm-plugin
%global commit6 3253f53a791f61397fa77478904c87460a9258ca
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})

# v1.10-migrator
%global git7 https://github.com/%{repo}/v1.10-migrator
%global commit7 c417a6a022c5023c111662e8280f885f6ac259be
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})

# oci-register-machine
%global git16 https://github.com/projectatomic/oci-register-machine
%global commit16 7d4ce654a2eaf282d16fd43f20130b3cf69b70c2
%global shortcommit16 %(c=%{commit16}; echo ${c:0:7})

# oci-systemd-hook
%global git17 https://github.com/projectatomic/oci-systemd-hook
%global commit17 41491a3c73193527487fb502026d41d3f0aad1aa
%global shortcommit17 %(c=%{commit17}; echo ${c:0:7})

# %%{name}-selinux stuff (prefix with ds_ for version/release etc.)
# Some bits borrowed from the openstack-selinux package
%global selinuxtype targeted
%global moduletype services
%global modulenames %{name}

# Usage: _format var format
# Expand 'modulenames' into various formats as needed
# Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;

# Relabel files
%global relabel_files() %{_sbindir}/restorecon -R %{_bindir}/%{name} %{_localstatedir}/run/%{name}.sock %{_localstatedir}/run/%{name}.pid %{_sysconfdir}/%{name} %{_localstatedir}/log/%{name} %{_localstatedir}/log/lxc %{_localstatedir}/lock/lxc %{_unitdir}/%{name}.service %{_sysconfdir}/%{name} &> /dev/null || :

# Version of SELinux we were using
%if 0%{?fedora} >= 22
%global selinux_policyver 3.13.1-119
%else
%global selinux_policyver 3.13.1-23
%endif

Name: %{repo}
Version: 1.10.3
Release: 33%{?dist}
Summary: Automates deployment of containerized applications
License: ASL 2.0
URL: https://%{import_path}
# only x86_64 for now: https://%%{provider}.%%{provider_tld}/%%{name}/%%{name}/issues/136
ExclusiveArch: x86_64
# Branch used available at
# https://%%{provider}.%%{provider_tld}/projectatomic/%%{name}/commits/rhel7-1.10.3
Source0: %{git0}/archive/%{commit0}.tar.gz
Source1: %{git1}/archive/%{commit1}/%{name}-selinux-%{shortcommit1}.tar.gz
Source2: %{git2}/archive/%{commit2}/%{name}-storage-setup-%{shortcommit2}.tar.gz
Source3: %{git3}/archive/%{commit3}/forward-journald-%{shortcommit3}.tar.gz
Source4: %{git4}/archive/%{commit4}/%{name}-novolume-plugin-%{shortcommit4}.tar.gz
Source5: %{git5}/archive/%{commit5}/rhel-push-plugin-%{shortcommit5}.tar.gz
Source6: %{git6}/archive/%{commit6}/%{name}-lvm-plugin-%{shortcommit6}.tar.gz
Source7: %{git7}/archive/%{commit7}/v1.10-migrator-%{shortcommit7}.tar.gz
Source8: %{name}.service
Source9: %{name}.sysconfig
Source10: %{name}-storage.sysconfig
Source11: %{name}-network.sysconfig
Source12: %{name}-logrotate.sh
Source13: README.%{name}-logrotate
Source14: %{name}-common.sh
Source15: README-%{name}-common
Source16: %{git16}/archive/%{commit16}/oci-register-machine-%{shortcommit16}.tar.gz
Source17: %{git17}/archive/%{commit17}/oci-systemd-hook-%{shortcommit17}.tar.gz
Source18: v1.10-migrator-helper
Patch0: use-RWMutex-to-access-container-store.patch
BuildRequires: git
BuildRequires: glibc-static
BuildRequires: golang >= 1.4.2
BuildRequires: device-mapper-devel
BuildRequires: pkgconfig(audit)
BuildRequires: btrfs-progs-devel
BuildRequires: sqlite-devel
BuildRequires: go-md2man >= 1.0.4
BuildRequires: pkgconfig(systemd)
BuildRequires: libseccomp-devel
Requires: %{name}-common = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# need xz to work with ubuntu images
Requires: xz
Requires: device-mapper-libs >= 7:1.02.97
Requires: subscription-manager
Requires: %{name}-rhel-push-plugin = %{version}-%{release}
Provides: lxc-%{name} = %{version}-%{release}
Provides: %{name}-io = %{version}-%{release}

# RE: rhbz#1195804 - ensure min NVR for selinux-policy
Requires: selinux-policy >= 3.13.1-23
Requires(pre): %{name}-selinux >= %{version}-%{release}
# rhbz#1300076
Requires: %{name}-forward-journald = %{version}-%{release}
Requires: %{name}-v1.10-migrator = %{version}-%{release}

# rhbz#1214070 - update deps for d-s-s
Requires: lvm2 >= 2.02.112
Requires: xfsprogs

# rhbz#1282898 - obsolete docker-storage-setup
Obsoletes: %{name}-storage-setup <= 0.0.4-2


%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%if 0%{?with_unit_test}
%package unit-test
Summary: %{summary} - for running unit tests

%description unit-test
%{summary} - for running unit tests
%endif

%package logrotate
Summary: cron job to run logrotate on Docker containers
Requires: %{name} = %{version}-%{release}
Provides: %{name}-io-logrotate = %{version}-%{release}

%description logrotate
This package installs %{summary}. logrotate is assumed to be installed on
containers for this to work, failures are silently ignored.

%package selinux
Summary: SELinux policies for Docker
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): selinux-policy-targeted >= %{selinux_policyver}
Requires(post): policycoreutils
Requires(post): policycoreutils-python
Requires(post): libselinux-utils
Provides: %{name}-io-selinux = %{version}-%{release}

%description selinux
SELinux policy modules for use with Docker.

%package forward-journald
Summary: Forward stdin to journald
License: ASL 2.0

%description forward-journald
Forward stdin to journald

The main driver for this program is < go 1.6rc2 has a issue where 10
SIGPIPE's on stdout or stderr cause go to generate a non-trappable SIGPIPE
killing the process. This happens when journald is restarted while docker is
running under systemd.

%package common
Summary: Common files for docker and docker-latest

%description common
This package contains the common files %{_bindir}/%{name} which will point to
%{_bindir}/%{name}-current or %{_bindir}/%{name}-latest configurable via
%{_sysconfdir}/sysconfig/%{repo}

%package novolume-plugin
URL: %{git4}
License: MIT
Summary: Block container starts with local volumes defined
Requires: %{name} = %{version}-%{release}

%description novolume-plugin
When a volume in provisioned via the `VOLUME` instruction in a Dockerfile or
via `docker run -v volumename`, host's storage space is used. This could lead to
an unexpected out of space issue which could bring down everything.
There are situations where this is not an accepted behavior. PAAS, for
instance, can't allow their users to run their own images without the risk of
filling the entire storage space on a server. One solution to this is to deny users
from running images with volumes. This way the only storage a user gets can be limited
and PAAS can assign quota to it.

This plugin solves this issue by disallowing starting a container with
local volumes defined. In particular, the plugin will block `docker run` with:

- `--volumes-from`
- images that have `VOLUME`(s) defined
- volumes early provisioned with `docker volume` command

The only thing allowed will be just bind mounts.

%package rhel-push-plugin
License: GPLv2
Summary: Avoids pushing a RHEL-based image to docker.io registry

%description rhel-push-plugin
In order to use this plugin you must be running at least Docker 1.10 which
has support for authorization plugins.

This plugin avoids any RHEL based image to be pushed to the default docker.io
registry preventing users to violate the RH subscription agreement.

%package lvm-plugin
License: LGPLv3
Summary: Docker volume driver for lvm volumes
Requires: %{name} = %{version}-%{release}

%description lvm-plugin
Docker Volume Driver for lvm volumes.

This plugin can be used to create lvm volumes of specified size, which can 
then be bind mounted into the container using `docker run` command.

%package v1.10-migrator
License: ASL 2.0 and CC-BY-SA
Summary: Calculates SHA256 checksums for docker layer content
Requires: %{name} = %{version}-%{release}

%description v1.10-migrator
Starting from v1.10 docker uses content addressable IDs for the images and
layers instead of using generated ones. This tool calculates SHA256 checksums
for docker layer content, so that they don't need to be recalculated when the
daemon starts for the first time.

The migration usually runs on daemon startup but it can be quite slow(usually
100-200MB/s) and daemon will not be able to accept requests during
that time. You can run this tool instead while the old daemon is still
running and skip checksum calculation on startup.

%package -n oci-register-machine
License: ASL 2.0
Summary: Golang binary to register OCI containers with systemd-machined

%description -n oci-register-machine
%{summary}

%package -n oci-systemd-hook
License: GPLv3+
Summary: OCI systemd hook for docker
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: pkgconfig(yajl)
BuildRequires: pkgconfig(libselinux)
BuildRequires: pkgconfig(mount)
BuildRequires: go-md2man

%description -n oci-systemd-hook
OCI systemd hooks enable running systemd in an OCI runc/docker container.

%prep
%autosetup -Sgit -n %{name}-%{commit0}

# unpack %%{name}-selinux
tar zxf %{SOURCE1}

# untar d-s-s
tar zxf %{SOURCE2}

# untar forward-journald
tar zxf %{SOURCE3}

# untar novolume-plugin
tar zxf %{SOURCE4}

# untar rhel-push-plugin
tar zxf %{SOURCE5}

# untar lvm-plugin
tar zxf %{SOURCE6}
pushd %{repo}-lvm-plugin-%{commit6}/vendor
mkdir src
mv g* src/
popd

# untar v1.10-migrator
tar zxf %{SOURCE7}

# systemd file
cp %{SOURCE8} .

# sysconfig file
cp %{SOURCE9} .

# storage sysconfig file
cp %{SOURCE10} .

# network sysconfig file 
cp %{SOURCE11} .

# logrotate script
cp %{SOURCE12} .

# logrotate README
cp %{SOURCE13} .

# common exec script
cp %{SOURCE14} .

# common exec README
cp %{SOURCE15} .

# untar oci-register-machine
tar zxf %{SOURCE16}

# untar oci-systemd-hook
tar zxf %{SOURCE17}

%build
mkdir _build

pushd _build
  mkdir -p src/%{provider}.%{provider_tld}/{%{name},projectatomic}
  ln -s $(dirs +1 -l) src/%{import_path}
  ln -s $(dirs +1 -l)/forward-journald-%{commit3} src/%{provider}.%{provider_tld}/projectatomic/forward-journald
  ln -s $(dirs +1 -l)/%{repo}-novolume-plugin-%{commit4} src/%{provider}.%{provider_tld}/projectatomic/%{repo}-novolume-plugin
  ln -s $(dirs +1 -l)/rhel-push-plugin-%{commit5} src/%{provider}.%{provider_tld}/projectatomic/rhel-push-plugin
  ln -s $(dirs +1 -l)/%{repo}-lvm-plugin-%{commit6} src/%{provider}.%{provider_tld}/projectatomic/%{repo}-lvm-plugin
  ln -s $(dirs +1 -l)/oci-register-machine-%{commit16} src/%{provider}.%{provider_tld}/projectatomic/oci-register-machine
  ln -s $(dirs +1 -l)/oci-systemd-hook-%{commit17} src/%{provider}.%{provider_tld}/projectatomic/oci-systemd-hook
popd

export DOCKER_GITCOMMIT="%{shortcommit0}/%{version}"
export DOCKER_BUILDTAGS='selinux seccomp'
export GOPATH=$(pwd)/_build:$(pwd)/vendor:%{gopath}
export GOPATH=$GOPATH:$(pwd)/_build:$(pwd)/forward-journald-%{commit3}/vendor
export GOPATH=$GOPATH:$(pwd)/%{repo}-novolume-plugin-%{commit4}/Godeps/_workspace
export GOPATH=$GOPATH:$(pwd)/rhel-push-plugin-%{commit5}/Godeps/_workspace
export GOPATH=$GOPATH:$(pwd)/%{repo}-lvm-plugin-%{commit6}/vendor

# build %%{name} manpages
man/md2man-all.sh
go-md2man -in %{repo}-novolume-plugin-%{commit4}/man/%{repo}-novolume-plugin.8.md -out %{repo}-novolume-plugin.8
go-md2man -in rhel-push-plugin-%{commit5}/man/rhel-push-plugin.8.md -out rhel-push-plugin.8
go-md2man -in %{repo}-lvm-plugin-%{commit6}/man/%{repo}-lvm-plugin.8.md -out %{repo}-lvm-plugin.8

# build %%{name} binary
sed -i '/LDFLAGS_STATIC/d' hack/make/.dockerinit
IAMSTATIC=false DOCKER_DEBUG=1 hack/make.sh dynbinary
cp contrib/syntax/vim/LICENSE LICENSE-vim-syntax
cp contrib/syntax/vim/README.md README-vim-syntax.md

# build %%{name}-selinux
pushd %{name}-selinux-%{commit1}
make SHARE="%{_datadir}" TARGETS="%{modulenames}"
popd

pushd $(pwd)/_build/src
go build -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" %{provider}.%{provider_tld}/projectatomic/forward-journald
go build -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" %{provider}.%{provider_tld}/projectatomic/%{repo}-novolume-plugin
go build -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" %{provider}.%{provider_tld}/projectatomic/rhel-push-plugin
go build -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" %{provider}.%{provider_tld}/projectatomic/%{repo}-lvm-plugin
popd

# build v1.10-migrator
pushd v1.10-migrator-%{commit7}
export GOPATH=$GOPATH:$(pwd)/Godeps/_workspace
sed -i 's/godep //g' Makefile
make v1.10-migrator-local
popd

# build oci-register-machine
pushd oci-register-machine-%{commit16}
export GOPATH=$GOPATH:$(pwd)/Godeps/_workspace
make %{?_smp_mflags}
popd

# build oci-systemd-hook
pushd oci-systemd-hook-%{commit17}
aclocal
autoreconf -i
%configure --libexecdir=%{_libexecdir}/oci/hooks.d/
make %{?_smp_mflags}
popd

%install
# install binary
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libexecdir}/%{name}

for x in bundles/latest; do
    if ! test -d $x/dynbinary; then
        continue
    fi
    install -p -m 755 $x/dynbinary/%{name}-%{version} %{buildroot}%{_bindir}/%{name}-current
    break
done

# install manpages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 man/man1/* %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5
install -p -m 644 man/man5/* %{buildroot}%{_mandir}/man5
install -d %{buildroot}%{_mandir}/man8
install -p -m 644 man/man8/%{repo}*.8 %{buildroot}%{_mandir}/man8

# install bash completion
install -d %{buildroot}%{_datadir}/bash-completion/completions/
install -p -m 644 contrib/completion/bash/%{name} %{buildroot}%{_datadir}/bash-completion/completions/

# install fish completion
# create, install and own %%{_datadir}/fish/vendor_completions.d until
# upstream fish provides it
install -dp %{buildroot}%{_datadir}/fish/vendor_completions.d
install -p -m 644 contrib/completion/fish/%{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d

# install container logrotate cron script
install -dp %{buildroot}%{_sysconfdir}/cron.daily/
install -p -m 755 %{SOURCE12} %{buildroot}%{_sysconfdir}/cron.daily/%{name}-logrotate

# install vim syntax highlighting
install -d %{buildroot}%{_datadir}/vim/vimfiles/{doc,ftdetect,syntax}
install -p -m 644 contrib/syntax/vim/doc/%{name}file.txt %{buildroot}%{_datadir}/vim/vimfiles/doc
install -p -m 644 contrib/syntax/vim/ftdetect/%{name}file.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -p -m 644 contrib/syntax/vim/syntax/%{name}file.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax

# install zsh completion
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 contrib/completion/zsh/_%{name} %{buildroot}%{_datadir}/zsh/site-functions

# install udev rules
install -d %{buildroot}%{_udevrulesdir}
install -p -m 755 contrib/udev/80-%{name}.rules %{buildroot}%{_udevrulesdir}

# install storage dir
install -d -m 700 %{buildroot}%{_sharedstatedir}/%{name}

# install systemd/init scripts
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE8} %{buildroot}%{_unitdir}

# for additional args
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -p -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-storage
install -p -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-network

# install SELinux interfaces
%_format INTERFACES $x.if
install -d %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 %{name}-selinux-%{commit1}/$INTERFACES %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}

# install policy modules
%_format MODULES $x.pp.bz2
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 0644 %{name}-selinux-%{commit1}/$MODULES %{buildroot}%{_datadir}/selinux/packages

%if 0%{?with_unit_test}
install -d -m 0755 %{buildroot}%{_sharedstatedir}/%{name}-unit-test/
cp -pav VERSION Dockerfile %{buildroot}%{_sharedstatedir}/%{name}-unit-test/.
for d in */ ; do
  cp -a $d %{buildroot}%{_sharedstatedir}/%{name}-unit-test/
done
# remove %%{name}.initd as it requires /sbin/runtime no packages in Fedora
rm -rf %{buildroot}%{_sharedstatedir}/%{name}-unit-test/contrib/init/openrc/%{name}.initd
%endif

# remove %%{name}-selinux rpm spec file
rm -rf %{name}-selinux-%{commit1}/%{name}-selinux.spec

# install secrets dir
install -d -p -m 750 %{buildroot}/%{_datadir}/rhel/secrets
# rhbz#1110876 - update symlinks for subscription management
ln -s %{_sysconfdir}/pki/entitlement %{buildroot}%{_datadir}/rhel/secrets/etc-pki-entitlement
ln -s %{_sysconfdir}/rhsm %{buildroot}%{_datadir}/rhel/secrets/rhsm
ln -s %{_sysconfdir}/yum.repos.d/redhat.repo %{buildroot}%{_datadir}/rhel/secrets/rhel7.repo

mkdir -p %{buildroot}/etc/%{name}/certs.d/redhat.{com,io}
ln -s %{_sysconfdir}/rhsm/ca/redhat-uep.pem %{buildroot}/%{_sysconfdir}/%{name}/certs.d/redhat.com/redhat-ca.crt
ln -s %{_sysconfdir}/rhsm/ca/redhat-uep.pem %{buildroot}/%{_sysconfdir}/%{name}/certs.d/redhat.io/redhat-ca.crt

# install %%{name} config directory
install -dp %{buildroot}%{_sysconfdir}/%{name}/

# install %%{name}-storage-setup
pushd %{name}-storage-setup-%{commit2}
install -d %{buildroot}%{_bindir}
install -p -m 755 %{name}-storage-setup.sh %{buildroot}%{_bindir}/%{name}-storage-setup
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{name}-storage-setup.service %{buildroot}%{_unitdir}
install -d %{buildroot}%{dss_libdir}
install -p -m 644 %{name}-storage-setup.conf %{buildroot}%{dss_libdir}/%{name}-storage-setup
install -p -m 755 libdss.sh %{buildroot}%{dss_libdir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 %{name}-storage-setup-override.conf %{buildroot}%{_sysconfdir}/sysconfig/%{name}-storage-setup
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 %{name}-storage-setup.1 %{buildroot}%{_mandir}/man1
popd

# install forward-journald
install -d %{buildroot}%{_bindir}
install -p -m 700 _build/src/forward-journald %{buildroot}%{_bindir}

# install %%{_bindir}/%{name}
install -d %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE14} %{buildroot}%{_bindir}/%{name}

# install novolume-plugin executable, unitfile, socket and man
install -d %{buildroot}/%{_libexecdir}/%{repo}
install -p -m 755 _build/src/%{repo}-novolume-plugin %{buildroot}/%{_libexecdir}/%{repo}/%{repo}-novolume-plugin
install -p -m 644 %{repo}-novolume-plugin-%{commit4}/systemd/%{repo}-novolume-plugin.s* %{buildroot}%{_unitdir}
install -d %{buildroot}%{_mandir}/man8
install -p -m 644 %{repo}-novolume-plugin.8 %{buildroot}%{_mandir}/man8

# install rhel-push-plugin executable, unitfile, socket and man
install -d %{buildroot}%{_libexecdir}/%{repo}
install -p -m 755 _build/src/rhel-push-plugin %{buildroot}%{_libexecdir}/%{repo}/rhel-push-plugin
install -p -m 644 rhel-push-plugin-%{commit5}/systemd/rhel-push-plugin.service %{buildroot}%{_unitdir}/rhel-push-plugin.service
install -p -m 644 rhel-push-plugin-%{commit5}/systemd/rhel-push-plugin.socket %{buildroot}%{_unitdir}/rhel-push-plugin.socket
install -d %{buildroot}%{_mandir}/man8
install -p -m 644 rhel-push-plugin.8 %{buildroot}%{_mandir}/man8

# install %%{repo}-lvm-plugin executable, unitfile, socket and man
install -d %{buildroot}/%{_libexecdir}/%{repo}
install -p -m 755 _build/src/%{repo}-lvm-plugin %{buildroot}/%{_libexecdir}/%{repo}/%{repo}-lvm-plugin
install -p -m 644 %{repo}-lvm-plugin-%{commit6}/systemd/%{repo}-lvm-plugin.s* %{buildroot}%{_unitdir}
install -d %{buildroot}%{_mandir}/man8
install -p -m 644 %{repo}-lvm-plugin.8 %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_sysconfdir}/%{repo}
install -p -m 644 %{repo}-lvm-plugin-%{commit6}%{_sysconfdir}/%{repo}/%{repo}-lvm-plugin %{buildroot}%{_sysconfdir}/%{repo}/%{repo}-lvm-plugin

# install v1.10-migrator
install -d %{buildroot}%{_bindir}
install -p -m 700 v1.10-migrator-%{commit7}/v1.10-migrator-local %{buildroot}%{_bindir}

# install v1.10-migrator-helper
install -p -m 700 %{SOURCE18} %{buildroot}%{_bindir}

# install oci-register-machine
pushd oci-register-machine-%{commit16}
install -d -p %{buildroot}%{_bindir}
make DESTDIR=%{buildroot} install
popd

# install oci-systemd-hook
pushd oci-systemd-hook-%{commit17}
%make_install

%check
[ ! -w /run/%{name}.sock ] || {
    mkdir test_dir
    pushd test_dir
    git clone https://github.com/projectatomic/docker.git -b %{branch}
    pushd %{name}
    make test
    popd
    popd
}

%pre
getent passwd %{name}root > /dev/null || %{_sbindir}/useradd -r -d %{_sharedstatedir}/%{name} -s /sbin/nologin -c "Docker User" %{name}root
exit 0

%post
%systemd_post %{name}.service

%post selinux
# Install all modules in a single transaction
%_format MODULES %{_datadir}/selinux/packages/$x.pp.bz2
%{_sbindir}/semodule -n -s %{selinuxtype} -i $MODULES
if %{_sbindir}/selinuxenabled ; then
    %{_sbindir}/load_policy
    %relabel_files
    if [ $1 -eq 1 ]; then
    restorecon -R %{_sharedstatedir}/%{name} &> /dev/null || :
    fi
fi

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%postun selinux
if [ $1 -eq 0 ]; then
%{_sbindir}/semodule -n -r %{modulenames} &> /dev/null || :
if %{_sbindir}/selinuxenabled ; then
%{_sbindir}/load_policy
%relabel_files
fi
fi

%triggerin -n %{name}-v1.10-migrator -- %{repo} < %{version}
%{_bindir}/v1.10-migrator-local 2>/dev/null
exit 0

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE*
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md MAINTAINERS NOTICE README*.md
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-*
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/*
%{_mandir}/man1/%{name}*.1.gz
%{_mandir}/man5/*.5.gz
%{_mandir}/man8/%{name}-daemon.8.gz
%{_bindir}/%{name}-*
%dir %{_datadir}/rhel
%{_datadir}/rhel/*
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-storage-setup.service
%{_datadir}/bash-completion/completions/%{name}
%dir %{_sharedstatedir}/%{name}
%{_udevrulesdir}/80-%{name}.rules
%dir %{_datadir}/fish/vendor_completions.d/
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%dir %{_datadir}/vim/vimfiles/doc
%{_datadir}/vim/vimfiles/doc/%{name}file.txt
%dir %{_datadir}/vim/vimfiles/ftdetect
%{_datadir}/vim/vimfiles/ftdetect/%{name}file.vim
%dir %{_datadir}/vim/vimfiles/syntax
%{_datadir}/vim/vimfiles/syntax/%{name}file.vim
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}
%dir %{dss_libdir}
%{dss_libdir}/*

%if 0%{?with_unit_test}
%files unit-test
%{_sharedstatedir}/%{name}-unit-test/
%endif

%files logrotate
%doc README.%{name}-logrotate
%{_sysconfdir}/cron.daily/%{name}-logrotate

%files selinux
%doc %{name}-selinux-%{commit1}/README.md
%{_datadir}/selinux/*

%files forward-journald
%license forward-journald-%{commit3}/LICENSE
%doc forward-journald-%{commit3}/README.md
%{_bindir}/forward-journald

%files common
%doc README-%{name}-common
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%files novolume-plugin
%license %{repo}-novolume-plugin-%{commit4}/LICENSE
%doc %{repo}-novolume-plugin-%{commit4}/README.md
%{_mandir}/man8/%{repo}-novolume-plugin.8.gz
%{_libexecdir}/%{repo}/%{repo}-novolume-plugin
%{_unitdir}/%{repo}-novolume-plugin.*

%files rhel-push-plugin
%license rhel-push-plugin-%{commit5}/LICENSE
%doc rhel-push-plugin-%{commit5}/README.md
%{_mandir}/man8/rhel-push-plugin.8.gz
%{_libexecdir}/%{repo}/rhel-push-plugin
%{_unitdir}/rhel-push-plugin.*

%files lvm-plugin
%license %{repo}-lvm-plugin-%{commit6}/LICENSE
%doc %{repo}-lvm-plugin-%{commit6}/README.md
%config(noreplace) %{_sysconfdir}/%{repo}/%{repo}-lvm-plugin
%{_mandir}/man8/%{repo}-lvm-plugin.8.gz
%{_libexecdir}/%{repo}/%{repo}-lvm-plugin
%{_unitdir}/%{repo}-lvm-plugin.*

%files v1.10-migrator
%license v1.10-migrator-%{commit7}/LICENSE.{code,docs}
%doc v1.10-migrator-%{commit7}/{CONTRIBUTING,README}.md
%{_bindir}/v1.10-migrator-*

%files -n oci-register-machine
%license oci-register-machine-%{commit16}/LICENSE
%doc oci-register-machine-%{commit16}/oci-register-machine.1.md
%doc oci-register-machine-%{commit16}/README.md
%dir %{_libexecdir}/oci
%dir %{_libexecdir}/oci/hooks.d
%{_libexecdir}/oci/hooks.d/oci-register-machine
%{_mandir}/man1/oci-register-machine.1*

%files -n oci-systemd-hook
%license oci-systemd-hook-%{commit17}/LICENSE
%doc oci-systemd-hook-%{commit17}/README.md
%{_libexecdir}/oci/hooks.d/oci-systemd-hook
%{_mandir}/man1/oci-systemd-hook.1*
%dir %{_libexecdir}/oci
%dir %{_libexecdir}/oci/hooks.d

%changelog
* Tue Jun 07 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-33
- Patch0 used in previous build updated

* Mon Jun 06 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-32
- Resolves: #1341906 - use RWMutex to acces container store

* Thu Jun 02 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-31
- Resolves: #1342274 - update file listings to avoid file ownerships by
multiple subpackages
- update docker.sysconfig to include --log-driver=journald in OPTIONS

* Thu Jun 02 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-30
- Resolves: #1342149 - v1.10-migrator shipped separately in both docker and
docker-latest
- The v1.10-migrator subpackage in docker-latest has executables prepended 
with 'docker-latest-', while there's no change in the ones shipped with 
docker (RE: #1342149)

* Thu Jun 02 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-29
- Resolves: #1342149 - docker-v1.10-migrator obsoletes
docker-latest-v1.10-migrator

* Wed Jun 01 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-28
- Resolves: #1341789 - update unitfile to use systemd for cgroups

* Wed Jun 01 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-27
- Resolves: #1341328 - include v1.10-migrator-helper script in the migrator
subpackage
- Resolves: #1335635 - solve log spam issues
- built docker projectatomic/rhel7-1.10.3 commit 4779225
- built dss commit 194eca2

* Sat May 14 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-26
- Resolves: #1341171 - add oci-register-machine and oci-systemd-hook subpackages
- built oci-register-machine commit 7d4ce65
- built oci-systemd-hook commit 41491a3

* Sat May 14 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-25
- docker requires docker-rhel-push-plugin

* Sat May 14 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-24
- docker unitfile updates to include rhel-push-plugin

* Tue May 03 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-23
- bump release tag to obsolete packages in docker-latest

* Tue May 03 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.10.3-1
- Resolves: #1335597 - rebase to v1.10.3 + rh patches
- add subpackages for novolume-plugin, lvm-plugin, rhel-push-plugin, v1.10-migrator
- BR: libseccomp-devel
- built docker @projectatomic/rhel7-1.10.3 commit 86bbf84
- built docker-selinux @origin/rhel7-1.10 commit 032bcda
- built d-s-s commit df2af94
- built forward-journald commit 77e02a9
- built novolume-plugin commit 7715854
- built rhel-push-plugin commit 904c0ca
- built lvm-plugin commit 3253f53
- built v1.10-migrator commit c417a6a

* Tue May 03 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-40
- Resolves: #1332592 - requires docker-common = version-release
- From: Ed Santiago <santiago@redhat.com>

* Tue May 03 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-39
- Resolves: #1332016, #1329743
- built docker projectatomic/rhel7-1.9 commit ab77bde
- built docker-selinux origin/rhel-1.10 commit 032bcda

* Wed Apr 27 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-38
- Resolves: #1331007 - fix selinux labels for new docker execs names
- built docker-selinux commit#501ea4c

* Tue Apr 26 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-37
- Resolves: #1330622 - /usr/bin/docker handles docker/docker-latest
conditions
- Resolves: #1330290 - d-s-s: do not pass devices which have 'creation of
device node' in progress
- built d-s-s commit#df2af94

* Tue Apr 26 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-36
- Resolves: #1330622 - don't allow $DOCKERBINARY==/usr/bin/docker

* Tue Apr 26 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-35
- #1330595 fix From: Ed Santiago <santiago@redhat.com>

* Tue Apr 26 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-34
- Resolves: #1330595
- use correct exec path for docker-current in unitfile

* Mon Apr 25 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-33
- Resolves: #1328219 - include docker-common subpackage
- docker-common is a runtime requirement for both docker and docker-latest

* Thu Apr 21 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-32
- update upstream URL
- Resolves: #1329423 - skip /dev setup in container when it's bind mounted in
- Resolves: #1329452 - CVE-2016-3697
- built docker @projectatomic/rhel7-1.9 commit#639e055
- built docker-selinux commit#39c092c
- built d-s-s commit#04a3847
- built forward-journald commit#77e02a9

* Thu Apr 21 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-31
- test-fix for https://github.com/openshift/openshift-ansible/issues/1779

* Mon Apr 18 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-30
- Bump release - previous git log had 2 docker commit values
- built docker @projectatomic/rhel7-1.9 commit#a1c9058
- built docker-selinux commit#39c092c
- built d-s-s commit#04a3847
- built forward-journald commit#77e02a9

* Mon Apr 18 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-29
- Resolves: #1283718, #1277982, #1126555 #1134424, #1186066,
    #1228777, #1255060, #1256832, #1261565, #1264562, #1266307,
    #1266525 #1266902 #1268059 #1272143 #1277982 #1283718 #1300033,
    #1303110 #1309739 #1316651 #1319783
- remove conflicts with atomic-openshift and origin
- built docker @projectatomic/rhel7-1.9 commit#a1c9058
- built docker-selinux commit#39c092c
- built d-s-s commit#04a3847
- built forward-journald commit#77e02a9
- do not even build dockerinit

* Sun Apr 10 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-28
- built docker @projectatomic/rhel7-1.9 commit#b795b73
- built docker-selinux commit#39c092c
- built d-s-s commit#ac50cee
- built docker-utils commit#b851c03
- built v1.10-migrator commit#c417a6a
- built forward-journald commit#77e02a9

* Sun Apr 10 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-27
- split docker-utils into a subpackage so docker-latest can reuse it.
- docker requires docker-utils at runtime
- do not ship dockerinit
- spec cleanups

* Mon Apr 04 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-26
- Resolves: rhbz#1323819 - allow images with VOLUME(s) when binds destination
override volume definition
- built docker @projectatomic/rhel7-1.9 commit#b795b73
- built docker-selinux commit#e72d8d7
- built d-s-s commit#346018e
- built docker-utils commit#b851c03
- built forward-journald commit#77e02a9

* Wed Mar 23 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-25
- Resolves: rhbz#1320302 - Backport fix for --cgroup-parent in docker
- same commits as release -24, only added bug number

* Wed Mar 23 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-24
- built docker @projectatomic/rhel7-1.9 commit#78ee77d
- built docker-selinux commit#8718b62
- built d-s-s commit#c6f0553
- built docker-utils commit#b851c03
- built forward-journald commit#77e02a9

* Thu Mar 17 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-23
- Resolves: rhbz#1318360 - delete bounds checking rules
- built docker @projectatomic/rhel7-1.9 commit#f97fb16
- built docker-selinux commit#8718b62
- built d-s-s commit#c6f0553
- built docker-utils commit#b851c03
- built forward-journald commit#77e02a9

* Tue Mar 15 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-22
- Resolves: rhbz#1317991 - Set Delegate=yes for cgroup transient units
- built docker @projectatomic/rhel7-1.9 commit#f97fb16
- built docker-selinux commit#69be4dc
- built d-s-s commit#03dfc7b
- built docker-utils commit#b851c03
- built forward-journald commit#77e02a9

* Mon Mar 14 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-21
- Resolves: rhbz#1317662 - include manpage for docker daemon (corrected)

* Mon Mar 14 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-20
- Resolves: rhbz#1317662 - include manpage for docker run
- Resolves: rhbz#1317627 - ensure that we join all the cgroups
- built docker @projectatomic/rhel7-1.9 commit#0275914
- built docker-selinux commit#69be4dc
- built d-s-s commit#03dfc7b
- built docker-utils commit#b851c03
- built forward-journald commit#77e02a9

* Wed Mar 09 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-19
- Resolves: rhbz#1316190 - set NotifyAccess=all in unitfile

* Tue Mar 08 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-18
- Resolves: rhbz#1286765 - set TimeoutStartSec=0 in unitfile
- Resolves: rhbz#1298363, rhbz#1300076, rhbz#1304038, rhbz#1302418
- built forward-journald commit#77e02a9 - other subpackage commits same as
previous build

* Tue Mar 08 2016 Lokesh Mandvekar <lsm5@redhat.com> - 1.9.1-17
- built docker @projectatomic/rhel7-1.9 commit#185277d
- built docker-selinux commit#e2e1f22
- built d-s-s commit#03dfc7b
- built docker-utils commit#b851c03
- built forward-journald commit#48b9599

* Tue Feb 02 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-16
- Resolves: rhbz#1304038 - conflict with openshift 3.1
- allow golang >= 1.4.2

* Thu Jan 28 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-15
- Resolves: rhbz#1302411
- built docker @projectatomic/rhel7-1.9 commit#50e78a0
- built docker-selinux commit#e2e1f22
- built d-s-s commit#1c2b95b
- built docker-utils commit#dab51ac

* Tue Jan 26 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-14
- built docker @projectatomic/rhel7-1.9 commit#fe0b590
- built docker-selinux commit#e2e1f22
- built d-s-s commit#1c2b95b
- built docker-utils commit#dab51ac

* Mon Jan 25 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-13
- Resolves: rhbz#1301199 - do not append distro tag to docker version

* Wed Jan 20 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-12
- built docker @projectatomic/rhel7-1.9 commit#2dbcc37
- built docker-selinux commit#e2e1f22
- built d-s-s commit#1c2b95b
- built docker-utils commit#dab51ac

* Fri Jan 15 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-11
- built docker @projectatomic/rhel7-1.9 commit#2dbcc37
- built docker-selinux commit#e2e1f22
- built d-s-s commit#1c2b95b
- built docker-utils commit#dab51ac

* Mon Jan 11 2016 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-10
- built docker @projectatomic/rhel7-1.9 commit#26797f7
- built docker-selinux commit#e2e1f22
- built d-s-s commit#1c2b95b
- built docker-utils commit#dab51ac

* Sat Dec 12 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-9
- built docker @projectatomic/rhel7-1.9 commit#401dfee
- built docker-selinux commit#e2e1f22
- built d-s-s commit#91d6cfd
- built docker-utils commit#dab51ac

* Fri Dec 04 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-8
- built docker @projectatomic/rhel7-1.9 commit#32fb322
- built docker-selinux commit#441f312
- built d-s-s commit#e38b94d
- built docker-utils commit#dab51ac

* Wed Dec 02 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-7
- built docker @projectatomic/rhel7-1.9 commit#32fb322
- built docker-selinux commit#441f312
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Wed Dec 02 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-6
- built docker @projectatomic/rhel7-1.9 commit#32fb322
- built docker-selinux commit#441f312
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Mon Nov 30 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-5
- built docker @projectatomic/rhel7-1.9 commit#32fb322
- built docker-selinux commit#dbfad05
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Wed Nov 25 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-4
- Resolves: rhbz#1275399
- built docker @projectatomic/rhel7-1.9 commit#390a466
- built docker-selinux commit#dbfad05
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Tue Nov 24 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-3
- built docker @projectatomic/rhel7-1.9 commit#698d463
- built docker-selinux commit#dbfad05
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Tue Nov 24 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-2
- Resolves: rhbz#1263394 - set unitfile to 5 mins

* Tue Nov 24 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-1
- use correct version number, no other change since last build

* Tue Nov 24 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-11
- built docker @projectatomic/rhel7-1.9 commit#f1cda67
- built docker-selinux commit#dbfad05
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Mon Nov 23 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-10
- Resolves: rhbz#1283718
- built docker @projectatomic/rhel7-1.9 commit#0ba2491
- built docker-selinux commit#dbfad05
- built d-s-s commit#0814c26
- built docker-utils commit#dab51ac

* Thu Nov 19 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-9
- built docker @projectatomic/rhel7-1.9 commit#eb84909
- built docker-selinux commit#dbfad05
- built d-s-s commit#c638a60
- built docker-utils commit#dab51ac

* Wed Nov 11 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-10
- Resolves: rhbz#1281805, rhbz#1271229, rhbz#1276346
- Resolves: rhbz#1275376, rhbz#1282898

* Wed Nov 11 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-9
- Resolves: rhbz#1280068 - Build docker with DWARF
- Move back to 1.8.2
- built docker @rhatdan/rhel7-1.8 commit#a01dc02
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Mon Nov 02 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-8
- Resolves: rhbz#1225093 (partially)
- built docker @projectatomic/rhel7-1.9 commit#cdd3941
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Wed Oct 28 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-7
- Resolves: rhbz#1275554
- built docker @projectatomic/rhel7-1.9 commit#61fd965
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Wed Oct 28 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-6
- built docker @projectatomic/rhel7-1.9 commit#166d43b
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Mon Oct 26 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-5
- built docker @projectatomic/rhel7-1.9 commit#6897d78
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Fri Oct 23 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-4
- built docker @projectatomic/rhel7-1.9 commit#0bb2bf4
- built docker-selinux commit#dbfad05
- built d-s-s commit#e9722cc
- built docker-utils commit#dab51ac

* Thu Oct 22 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-3
- built docker @projectatomic/rhel7-1.9 commit#1ea7f30
- built docker-selinux commit#dbfad05
- built d-s-s commit#01df512
- built docker-utils commit#dab51ac

* Thu Oct 22 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-2
- built docker @projectatomic/rhel7-1.9 commit#1ea7f30
- built docker-selinux commit#fe61432
- built d-s-s commit#01df512
- built docker-utils commit#dab51ac

* Wed Oct 14 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-8
- built docker @rhatdan/rhel7-1.8 commit#a01dc02
- built docker-selinux master commit#e2a5226
- built d-s-s master commit#6898d43
- built docker-utils master commit#dab51ac

* Fri Oct 09 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-7
- https://github.com/rhatdan/docker/pull/127 (changes for libcontainer/user)
- https://github.com/rhatdan/docker/pull/128 (/dev mount from host)

* Wed Oct 07 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-6
- built docker @rhatdan/rhel7-1.8 commit#bb472f0
- built docker-selinux master commit#44abd21
- built d-s-s master commit#6898d43
- built docker-utils master commit#dab51ac

* Wed Sep 30 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-5
- Resolves: rhbz#1267743
- https://github.com/docker/docker/pull/16639
- https://github.com/opencontainers/runc/commit/c9d58506297ed6c86c9d8a91d861e4de3772e699

* Wed Sep 30 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-4
- built docker @rhatdan/rhel7-1.8 commit#23f26d9
- built docker-selinux master commit#2ed73eb
- built d-s-s master commit#6898d43
- built docker-utils master commit#dab51ac

* Wed Sep 30 2015 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.8.2-3
- Resolves: rhbz#1264557 (extras-rhel-7.1.6) - rebase to 1.8.2
- Resolves: rhbz#1265810 (extras-rhel-7.2) - rebase to 1.8.2
- built docker @rhatdan/rhel7-1.8 commit#23f26d9
- built docker-selinux master commit#d6560f8
- built d-s-s master commit#6898d43
- built docker-utils master commit#dab51ac
- use golang == 1.4.2

* Mon Sep 21 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.8.2-2
- built docker-selinux master commit#d6560f8

* Fri Sep 18 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.8.2-1
- package only provides docker, docker-selinux and docker-logrotate
- Resolves: rhbz#1261329, rhbz#1263394, rhbz#1264090
- built docker @rhatdan/rhel7-1.8 commit#23f26d9
- built d-s-s master commit#6898d43
- built docker-selinux master commit#b5281b7
- built docker-utils master commit#dab51ac

* Thu Aug 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-115
- Resolves: rhbz#1252421
- built docker @rhatdan/rhel7-1.7 commit#446ad9b
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#d3b9ba7
- built atomic master commit#011a826
- built docker-selinux master commit#6267b83
- built docker-utils master commit#dab51ac

* Mon Aug 24 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-114
- Resolves: rhbz#1255874 - (#1255488 is for 7.2)

* Fri Aug 21 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-113
- Resolves: rhbz#1255488
- built docker @rhatdan/rhel7-1.7 commit#4136d06
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#d3b9ba7
- built atomic master commit#995a223
- built docker-selinux master commit#39a894e
- built docker-utils master commit#dab51ac

* Thu Aug 20 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-112
- Resolves: rhbz#1255051
- built docker @rhatdan/rhel7-1.7 commit#4136d06
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#ac1b30e
- built atomic master commit#53169d5
- built docker-selinux master commit#39a894e
- built docker-utils master commit#dab51ac

* Tue Aug 18 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-111
- built docker @rhatdan/rhel7-1.7 commit#9fe211a
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#ac1b30e
- built atomic master commit#53169d5
- built docker-selinux master commit#39a894e
- built docker-utils master commit#dab51ac

* Mon Aug 17 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-110
- built docker @rhatdan/rhel7-1.7 commit#ba2de95
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#ac1b30e
- built atomic master commit#53169d5
- built docker-selinux master commit#39a894e
- built docker-utils master commit#dab51ac

* Mon Aug 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-109
- Resolves: rhbz#1249651 - unpin python-requests requirement
- update python-websocket-client to 0.32.0

* Tue Jul 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-108
- built docker @rhatdan/rhel7-1.7 commit#3043001
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#b152398
- built atomic master commit#a4442c4
- built docker-selinux master commit#bebf349
- built docker-utils master commit#dab51ac

* Fri Jul 24 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-107
- built docker @rhatdan/rhel7-1.7 commit#3043001
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#b152398
- built atomic master commit#52d695c
- built docker-selinux master commit#bebf349

* Thu Jul 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-106
- built docker @rhatdan/rhel7-1.7 commit#3043001
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#b152398
- built atomic master commit#52d695c
- built docker-selinux master commit#bebf349

* Thu Jul 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-105
- Resolves: rhbz#1245325
- built docker @rhatdan/rhel7-1.7 commit#ac162a3
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#b152398
- built atomic master commit#ac162a3
- built docker-selinux master commit#ac162a3
- disable dockerfetch and dockertarsum

* Wed Jul 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-104
- use a common release tag for all subpackages, much easier to update via
rpmdev-bumpspec

* Wed Jul 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.1-1
- built docker @rhatdan/rhel7-1.7 commit#d2fbc0b
- built docker-py @rhatdan/master commit#54a154d
- built d-s-s master commit#b152398
- built atomic master commit#d2fbc0b
- built docker-selinux master commit#d2fbc0b

* Fri Jul 17 2015 Jonathan Lebon <jlebon@redhat.com> - 1.7.0-5
- Add patch for atomic.sysconfig
- Related: https://github.com/projectatomic/atomic/pull/94

* Wed Jul 15 2015 Jan Chaloupka <jchaloup@redhat.com> - 1.7.0-3.1
- Add unit-test subpackage

* Thu Jul 09 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.0-3
- built docker @rhatdan/rhel7-1.7 commit#4740812

* Wed Jul 08 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.0-2
- increment all release tags to make koji happy

* Wed Jul 08 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.7.0-1
- Resolves: rhbz#1241186 - rebase to v1.7.0 + rh patches
- built docker @rhatdan/rhel7-1.7 commit#0f235fc
- built docker-selinux master commit#bebf349
- built d-s-s master commit#e9c3a4c
- built atomic master commit#f133684
- rebase python-docker-py to upstream v1.2.3
- disable docker-fetch for now, doesn't build

* Mon Jun 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-14
- Resolves: rhbz#1218639, rhbz#1225556 (unresolved in -11)
- build docker @lsm5/rhel7-1.6 commit#ba1f6c3

* Mon Jun 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-13
- Resolves: rhbz#1222453

* Mon Jun 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-12
- build docker-selinux master commit#9c089c6

* Mon Jun 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-11
- Resolves: rhbz#1231936 (clone of fedora rhbz#1231134), rhbz#1225556, rhbz#1215819
- build docker @rhatdan/rhel7-1.6 commit#7b32c6c

* Wed Jun 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-10
- correct typo

* Wed Jun 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-9
- Resolves: rhbz#1214070 - update d-s-s related deps
- Resolves: rhbz#1229374 - use prior existing metadata volume if any
- Resolves: rhbz#1230192 (include d-s-s master commit#eefbef7)
- build docker @rhatdan/rhel7-1.6 commit#b79465d

* Mon Jun 08 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-8
- Resolves: rhbz#1229319 - do not claim /run/secrets
- Resolves: rhbz#1228167
- build docker rhatdan/rhel7-1.6 commit#ac7d43f
- build atomic master commit#f863afd

* Thu Jun 04 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-7
- Resolves: rhbz#1228397 - install manpage for d-s-s
- Resolves: rhbz#1228459 - solve 'Permission denied' error for d-s-s
- Resolves: rhbz#1228685 - don't append dist tag to docker version
(revert change in 1.6.2-4)

* Tue Jun 02 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-6
- build docker rhatdan/rhel7-1.6 commit#f1561f6

* Tue Jun 02 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-5
- build docker-selinux master commit#99c4c77
- build atomic master commit#2f1398c
- include docker-storage-setup in docker itself, no subpackage created
- docker.service Wants=docker-storage-setup.service

* Mon Jun 01 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-4
- include dist tag in 'docker version' to tell a distro build from a docker
upstream rpm

* Mon Jun 01 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-3
- Resolves: rhbz#1226989 - correct install path for docker-stroage-setup
config file
- Resolves: rhbz#1227040 - docker requires docker-storage-setup at runtime
- built docker @rhatdan/rhel7-1.6 commit#a615a49
- built atomic master commit#2f1398c
- built d-s-s master commit#0f2b772

* Thu May 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-2
- build docker @rhatdan/rhel7-1.6 commit#175dd9c

* Thu May 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.2-1
- Resolves: rhbz#1225965 - rebase to 1.6.2
- Resolves: rhbz#1226320, rhbz#1225549, rhbz#1225556
- Resolves: rhbz#1219705 - CVE-2015-3627
- Resolves: rhbz#1219701 - CVE-2015-3629
- Resolves: rhbz#1219709 - CVE-2015-3630
- Resolves: rhbz#1219713 - CVE-2015-3631
- build docker @rhatdan/rhel7-1.6 commit#d8675b5
- build atomic master commit#ec592be
- build docker-selinux master commit#e86b2bc

* Tue May 26 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-15
- d-s-s br: pkgconfig(systemd)
- Resolves: rhbz#1214070 enforce min NVR for lvm2

* Tue May 26 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-14
- build atomic master commit#cc9aed4
- build docker-utils master commit#562e2c0
- build docker-selinux master commit#ba1ff3c
- include docker-storage-setup subpackage, use master commit#e075395
- Resolves: rhbz#1216095

* Mon May 25 2015 Michal Minar <miminar@redhat.com> - 1.6.0-13
- Remove all repositories when removing image by ID.
- Resolves: #1222784

* Thu Apr 30 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-11
- build docker @rhatdan/rhel7-1.6 commit#8aae715
- build atomic @projectatomic/master commit#5b2fa8d (fixes a typo)
- Resolves: rhbz#1207839
- Resolves: rhbz#1211765
- Resolves: rhbz#1209545 (fixed in 1.6.0-10)
- Resolves: rhbz#1151167 (fixed in 1.6.0-6)

* Tue Apr 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-10
- Resolves: rhbz#1215768
- Resolves: rhbz#1212579
- build docker @rhatdan/rhel7-1.6 commit#0852937

* Fri Apr 24 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-9
- build docker @rhatdan/rhel7-1.6 commit#6a57386
- fix registry unit test

* Wed Apr 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-8
- build docker @rhatdan/rhel7-1.6 commit#7bd2216

* Tue Apr 21 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-7
- build docker @rhatdan/rhel7-1.6 commit#c3721ce
- build atomic master commit#7b136161
- Resolves: rhbz#1213636

* Fri Apr 17 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-6
- Rebuilt with golang 1.4.2
- Resolves: rhbz#1212813

* Fri Apr 17 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-5
- build docker @rhatdan/rhel7-1.6 commit#9c42d44
- build docker-selinux master commit#d59539b
- Resolves: rhbz#1211750

* Thu Apr 16 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-4
- build docker @rhatdan/rhel7-1.6 commit#c1a573c
- includes 1.6.0 release + redhat patches
- include docker-selinux @fedora-cloud/master commit#d74079c

* Thu Apr 16 2015 Michal Minar <miminar@redhat.com> - 1.6.0-3
- Fixed login command
- Resolves: rhbz#1212188

* Wed Apr 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-2
- Resolves: rhbz#1211292 - move GOTRACEBACK=crash to unitfile
- build docker @rhatdan/rhel7-1.6 commit#fed6da1
- build atomic master commit#e5734c4

* Tue Apr 14 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.6.0-1
- use docker @rhatdan/rhel7-1.6 commit#a8ccea4

* Fri Apr 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-30
- use docker @rhatdan/1.6 commit#24bc1b9

* Fri Mar 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-29
- use docker @rhatdan/1.6 commit#2d06cf9

* Fri Mar 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-28
- Resolves: rhbz#1206443 - CVE-2015-1843

* Wed Mar 25 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-27
- revert rhatdan/docker commit 72a9000fcfa2ec5a2c4a29fb62a17c34e6dd186f
- Resolves: rhbz#1205276

* Tue Mar 24 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-26
- revert rhatdan/docker commit 74310f16deb3d66444bb461c29a09966170367db

* Mon Mar 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-25
- don't delete autogen in hack/make.sh
- re-enable docker-fetch

* Mon Mar 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-24
- bump release tags for all

* Mon Mar 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-23
- Resolves: rhbz#1204260 - do not delete linkgraph.db before starting service

* Mon Mar 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-22
- increment release tag (no other changes)

* Sun Mar 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-21
- install cert for redhat.io authentication

* Mon Mar 16 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-20
- Resolves: rhbz#1202517 - fd leak
- build docker rhatdan/1.5.0 commit#ad5a92a
- build atomic master commit#4ff7dbd

* Tue Mar 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-19
- Resolves: rhbz#1200394 - don't mount /run as tmpfs if mounted as a volume
- Resolves: rhbz#1187603 - 'atomic run' no longer ignores new image if
container still exists
- build docker rhatdan/1.5.0 commit#5992901
- no rpm change, ensure release tags in changelogs are consistent

* Tue Mar 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-18
- handle updates smoothly from a unified docker-python to split out
docker-python and atomic

* Tue Mar 10 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-17
- build docker @rhatdan/1.5.0 commit#d7dfe82
- Resolves: rhbz#1198599 - use homedir from /etc/passwd if $HOME isn't set
- atomic provided in a separate subpackage

* Mon Mar 09 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-16
- build docker @rhatdan/1.5.0 commit#867ff5e
- build atomic master commit#
- Resolves: rhbz#1194445 - patch docker-python to make it work with older
python-requests
- Resolves: rhbz#1200104 - dns resolution works with selinux enforced

* Mon Mar 09 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-15
- Resolves: rhbz#1199433 - correct install path for 80-docker.rules

* Mon Mar 09 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-14
- build docker, @rhatdan/1.5.0 commit#365cf68
- build atomic, master commit#f175fb6

* Fri Mar 06 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-13
- build docker, @rhatdan/1.5.0 commit#e0fdceb
- build atomic, master commit#ef2b661

* Thu Mar 05 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-12
- Resolves: rhbz#1198630
- build docker, @rhatdan/1.5.0 commit#233dc3e
- build atomic, master commit#c6390c7

* Tue Mar 03 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-11
- build docker rhatdan/1.5.0 commit#3a4d0f1
- build atomic master commit#d68d76b
- Resolves: rhbz#1188252 - rm /var/lib/docker/linkgraph.db in unit file
before starting docker daemon

* Mon Mar 02 2015 Michal Minar <miminar@redhat.com> - 1.5.0-10
- Fixed and speeded up repository searching

* Fri Feb 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-9
- increment all release tags

* Fri Feb 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-9
- increment docker release tag

* Thu Feb 26 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-7
- Resolves: rhbz#1196709 - fix docker build's authentication issue
- Resolves: rhbz#1197158 - fix ADD_REGISTRY and BLOCK_REGISTRY in unitfile
- Build docker-utils commit#dcb4518
- update docker-python to 1.0.0
- disable docker-fetch (not compiling currently)

* Tue Feb 24 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-6
- build docker rhatdan/1.5.0 commit#e5d3e08
- docker registers machine with systemd
- create journal directory so that journal on host can see journal content in
container
- build atomic commit#a7ff4cb

* Mon Feb 16 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-5
- use docker rhatdan/1.5.0 commit#1a4e592
- Complete fix for rhbz#1192171 - patch included in docker tarball
- use docker-python 0.7.2
- Resolves: rhbz#1192312 - solve version-release requirements for
subpackages

* Mon Feb 16 2015 Michal Minar <miminar@redhat.com> - 1.5.0-4
- Readded --(add|block)-registry flags.

* Fri Feb 13 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-2
- Resolves: rhbz#1192312 - custom release numbers for 
python-websocket-client and docker-py
- Resolves: rhbz#1192171 - changed options and env vars for
adding/replacing registries

* Thu Feb 12 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.5.0-1
- build docker rhatdan/1.5 a06d357
- build atomic projectaomic/master d8c35ce

* Thu Feb 05 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-39
- Resolves: rhbz#1187993 - allow core dump with no size limit
- build atomic commit#98c21fd

* Mon Feb 02 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-38
- Resolves: rhbz#1188318
- atom commit#ea7ab31

* Fri Jan 30 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-37
- add extra options to /etc/sysconfig/docker to add/block registries
- build atom commit#3d4fd20

* Fri Jan 30 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-36
- remove dependency on python-backports

* Fri Jan 30 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-35
- build atomic rhatdan/master commit#973142b
- build docker rhatdan/1.4.1-beta2 commit#d26b358

* Fri Jan 30 2015 Michal Minar <miminar@redhat.com> - 1.4.1-34
- added patch fixed tagging issue

* Fri Jan 30 2015 Michal Minar <miminar@redhat.com> - 1.4.1-33
- build docker rhatdan/1.4.1-beta2 commit#b024f0f
- --registry-(replace|preprend) replaced with --(add|block)-registry

* Thu Jan 29 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-32
- build atom commit#567c2c8

* Thu Jan 29 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-31
- build atom commit#b9e02ad

* Wed Jan 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-30
- Require python-backports >= 1.0-8 for docker-python

* Wed Jan 28 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-29
- build docker rhatdan/1.4.1-beta2 commit#0af307b
- --registry-replace|prepend flags via Michal Minar <miminar@redhat.com>
- build atomic rhatdan/master commit#37f9be0

* Tue Jan 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-27
- patch to avoid crash in atomic host

* Tue Jan 27 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-26
- build docker rhatdan/1.4.1-beta2 commit#0b4cade
- build atomic rhatdan/master commit#b8c7b9d
- build docker-utils vbatts/master commit#fb94a28

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-25
- build atomic commit#fcbc57b with fix for install/upgrade/status
- build docker rhatdan/1.4.1-beta2 commit#f476836

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-24
- install dockertarsum from github.com/vbatts/docker-utils

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-23
- build rhatdan/atom commit#ef16d40
- try urlparse from six, else from argparse

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-22
- use python-argparse to provide urlparse

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-21
- move atomic bits into -python subpackage

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-20
- update atom commit#10fc4c8

* Fri Jan 23 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-19
- build rhatdan/1.4.1-beta2 commit#35a8dc5
- --registry-prepend instead of --registry-append

* Thu Jan 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-18
- don't install nsinit

* Thu Jan 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-17
- install atomic and manpages
- don't provide -devel subpackage

* Thu Jan 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-16
- install python-websocket-client and python-docker as subpackages

* Thu Jan 22 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-15
- build rhatdan/1.4.1-beta2 commit#06670da
- install subscription manager

* Tue Jan 20 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-14
- increment release number to avoid conflict with 7.0

* Tue Jan 20 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-13
- build rhatdan/1.4.1-beta2 commit#2de8e5d
- Resolves: rhbz#1180718 - MountFlags=slave in unitfile

* Mon Jan 19 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-12
- build rhatdan/1.4.1-beta2 commit#218805f

* Mon Jan 19 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-11
- build rhatdan/1.4.1-beta2 commit#4b7addf

* Fri Jan 16 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-10
- build rhatdan/1.4.1-beta2 commit #a0c7884
- socket activation not used
- include docker_transition_unconfined boolean info and disable socket
activation in /etc/sysconfig/docker
- docker group not created

* Fri Jan 16 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-9
- run all tests and not just unit tests
- replace codegansta.tgz with codegangsta-cli.patch

* Thu Jan 15 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-8
- build rhatdan/1.4.1-beta2 commit #6ee2421

* Wed Jan 14 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-7
- build rhatdan/1.4.1-beta2 01a64e011da131869b42be8b2f11f540fd4b8f33
- run tests inside a docker repo during check phase

* Mon Jan 12 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-6
- build rhatdan/1.4.1-beta2 01a64e011da131869b42be8b2f11f540fd4b8f33

* Wed Jan 07 2015 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-5
- own /etc/docker
- include check for unit tests

* Fri Dec 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-4
- Install vim and shell completion files in main package itself

* Thu Dec 18 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-3
- rename cron script
- change enable/disable to true/false

* Thu Dec 18 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-2
- Enable the logrotate cron job by default, disable via sysconfig variable
- Install docker-network and docker-container-logrotate sysconfig files

* Thu Dec 18 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.1-1
- Resolves: rhbz#1174351 - update to 1.4.1
- Provide subpackages for fish and zsh completion and vim syntax highlighting
- Provide subpackage to run logrotate on running containers as a daily cron
job

* Mon Dec 15 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.4.0-1
- Resolves: rhbz#1174266 - update to 1.4.0
- Fixes: CVE-2014-9357, CVE-2014-9358
- uses /etc/docker as cert path
- create dockerroot user
- skip btrfs version check

* Fri Dec 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.2-4
- update libcontainer paths
- update docker.sysconfig to include DOCKER_TMPDIR
- update docker.service unitfile
- package provides docker-io-devel

* Mon Dec 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.2-3
- revert docker.service change, -H fd:// in sysconfig file

* Mon Dec 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.2-2
- update systemd files

* Tue Nov 25 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.2-1
- Resolves: rhbz#1167870 - update to v1.3.2
- Fixes CVE-2014-6407, CVE-2014-6408

* Fri Nov 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.1-2
- remove unused buildrequires

* Thu Nov 13 2014 Lokesh Mandvekar <lsm5@redhat.com> - 1.3.1-1
- bump to upstream v1.3.1
- patch to vendor in go-md2man and deps for manpage generation

* Thu Oct 30 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-1.8
- Remove docker-rhel entitlment patch. This was buggy and is no longer needed

* Mon Oct 20 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-1.7
- Add 404 patch to allow docker to continue to try to download updates with 
- different certs, even if the registry returns 404 error

* Tue Oct 7 2014 Eric Paris <eparis@redhat.com> - 1.2.0-1.6
- make docker.socket start/restart when docker starts/restarts

* Tue Sep 30 2014 Eric Paris <eparis@redhat.com> - 1.2.0-1.5
- put docker.socket back the right way

* Sat Sep 27 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-1.4
- Remove docker.socket

* Mon Sep 22 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-1.2
- Fix docker.service file to use /etc/sysconfig/docker-storage.service

* Mon Sep 22 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-1.1
- Bump release to 1.2.0
- Add support for /etc/sysconfig/docker-storage
- Add Provides:golang(github.com/docker/libcontainer)
- Add provides docker-io to get through compatibility issues
- Update man pages
- Add missing pieces of libcontainer
- Devel now obsoletes golang-github-docker-libcontainer-devel
- Remove runtime dependency on golang
- Fix secrets patch
- Add -devel -pkg-devel subpackages
- Move libcontainer from -lib to -devel subpackage
- Allow docker to use /etc/pki/entitlement for certs
- New sources that satisfy nsinit deps
- Change docker client certs links
- Add nsinit

* Tue Sep 2 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-10
- Add  docker client entitlement certs

* Fri Aug 8 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-9
- Add Matt Heon patch to allow containers to work if machine is not entitled

* Thu Aug 7 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-8
- Fix handing of rhel repos

* Mon Aug 4 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-6
- Update man pages

* Mon Jul 28 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-5
- Fix environment patch
- Add /etc/machine-id patch

* Fri Jul 25 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-4
- Add Secrets Patch back in

* Fri Jul 25 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-3
- Pull in latest docker-1.1.2 code

* Fri Jul 25 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-2
- Update to the latest from upstream
- Add comment and envoroment patches to allow setting of comments and 
- enviroment variables from docker import

* Wed Jul 23 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.1-3
- Install docker bash completions in proper location
- Add audit_write as a default capability

* Tue Jul 22 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.1-2
- Update man pages
- Fix docker pull registry/repo

* Fri Jul 18 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.1-1
- Update to latest from upstream

* Mon Jul 14 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-10
- Pass otions from /etc/sysconfig/docker into docker.service unit file

* Thu Jul 10 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-9
- Fix docker-registry patch to handle search

* Thu Jul 10 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-8
- Re-add %%{_datadir}/rhel/secrets/rhel7.repo

* Wed Jul 9 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-7
- Patch: Save "COMMENT" field in Dockerfile into image content.
- Patch: Update documentation noting that SIGCHLD is not proxied.
- Patch: Escape control and nonprintable characters in docker ps
- Patch: machine-id: add container id access
- Patch: Report child error better (and later)
- Patch: Fix invalid fd race
- Patch: Super minimal host based secrets
- Patch: libcontainer: Mount cgroups in the container
- Patch: pkg/cgroups Add GetMounts() and GetAllSubsystems()
- Patch: New implementation of /run support
- Patch: Error if Docker daemon starts with BTRFS graph driver and SELinux enabled
- Patch: Updated CLI documentation for docker pull with notes on specifying URL
- Patch: Updated docker pull manpage to reflect ability to specify URL of registry.
- Patch: Docker should use /var/tmp for large temporary files.
- Patch: Add --registry-append and --registry-replace qualifier to docker daemon
- Patch: Increase size of buffer for signals
- Patch: Update documentation noting that SIGCHLD is not proxied.
- Patch: Escape control and nonprintable characters in docker ps

* Tue Jun 24 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-4
- Documentation update for --sig-proxy
- increase size of buffer for signals
- escape control and nonprintable characters in docker ps

* Tue Jun 24 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-3
- Resolves: rhbz#1111769 - CVE-2014-3499

* Thu Jun 19 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-2
- Resolves: rhbz#1109938 - upgrade to upstream version 1.0.0 + patches
  use repo: https://github.com/lsm5/docker/commits/htb2
- Resolves: rhbz#1109858 - fix race condition with secrets
- add machine-id patch:
https://github.com/vbatts/docker/commit/4f51757a50349bbbd2282953aaa3fc0e9a989741

* Wed Jun 18 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-1
- Resolves: rhbz#1109938 - upgrade to upstream version 1.0.0 + patches
  use repo: https://github.com/lsm5/docker/commits/2014-06-18-htb2
- Resolves: rhbz#1110876 - secrets changes required for subscription
management
- btrfs now available (remove old comment)

* Fri Jun 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-19
- build with golang-github-kr-pty-0-0.19.git98c7b80.el7

* Fri Jun 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-18
- update manpages
- use branch: https://github.com/lsm5/docker/commits/2014-06-06-2

* Thu Jun 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-17
- use branch: https://github.com/lsm5/docker/commits/2014-06-05-final2

* Thu Jun 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-16
- latest repo: https://github.com/lsm5/docker/commits/2014-06-05-5
- update secrets symlinks

* Mon Jun 02 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-15
- correct the rhel7.repo symlink

* Mon Jun 02 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-14
- only symlink the repo itself, not the dir

* Sun Jun 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-13
- use the repo dir itself and not repo for second symlink

* Sat May 31 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-12
- create symlinks at install time and not in scriptlets
- own symlinks in /etc/docker/secrets

* Sat May 31 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-11
- add symlinks for sharing host entitlements

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-10
- /etc/docker/secrets has permissions 750

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-9
- create and own /etc/docker/secrets

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-8
- don't use docker.sysconfig meant for sysvinit (just to avoid confusion)

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-7
- install /etc/sysconfig/docker for additional args
- use branch 2014-05-29 with modified secrets dir path

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-6
- secret store patch

* Thu May 22 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-5
- native driver: add required capabilities (dotcloud issue #5928)

* Thu May 22 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-4
- branch 2014-05-22
- rename rhel-dockerfiles dir to dockerfiles

* Wed May 21 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-3
- mount /run with correct selinux label

* Mon May 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-2
- add btrfs

* Mon May 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-1
- use latest master
- branch: https://github.com/lsm5/docker/commits/2014-05-09-2

* Mon May 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-13
- add registry search list patch

* Wed May 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-12
- include dockerfiles for postgres, systemd/{httpd,mariadb}

* Mon May 12 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-11
- add apache, mariadb and mongodb dockerfiles
- branch 2014-05-12

* Fri May 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-10
- add rhel-dockerfile/mongodb

* Fri May 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-9
- use branch: https://github.com/lsm5/docker/commits/2014-05-09
- install rhel-dockerfile for apache
- cleanup: get rid of conditionals
- libcontainer: create dirs/files as needed for bind mounts

* Thu May 08 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-8
- fix docker top

* Tue May 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-7
- set container pid for process in native driver

* Tue May 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-6
- ensure upstream PR #5529 is included

* Mon May 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-5
- block push to docker index

* Thu May 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-4
- enable selinux in unitfile

* Thu May 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-3
- branch https://github.com/lsm5/docker/commits/2014-05-01-2

* Thu May 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-2
- branch https://github.com/lsm5/docker/tree/2014-05-01

* Fri Apr 25 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-1
- renamed (docker-io -> docker)
- rebased on 0.10.0
- branch used: https://github.com/lsm5/docker/tree/2014-04-25
- manpages packaged separately (pandoc not available on RHEL-7)

* Tue Apr 08 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-4.collider
- manpages merged, some more patches from alex

* Thu Apr 03 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-3.collider
- fix --volumes-from mount failure, include docker-images/info/tag manpages

* Tue Apr 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-2.collider
- solve deadlock issue

* Mon Mar 31 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-1.collider
- branch 2014-03-28, include additional docker manpages from whenry

* Thu Mar 27 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-7.collider
- env file support (vbatts)

* Mon Mar 17 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-6.collider
- dwalsh's selinux patch rewritten
- point to my docker repo as source0 (contains all patches already)
- don't require tar and libcgroup

* Fri Mar 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-5.collider
- add kraman's container-pid.patch

* Fri Mar 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-4.collider
- require docker.socket in unitfile

* Thu Mar 13 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-3.collider
- use systemd socket activation

* Wed Mar 12 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-2.collider
- add collider tag to release field

* Tue Mar 11 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-1
- upstream version bump to 0.9.0

* Mon Mar 10 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.1-3
- add alexl's patches upto af9bb2e3d37fcddd5e041d6ae45055f649e2fbd4
- add guelfey/go.dbus to BR

* Sun Mar 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.1-2
- use upstream commit 3ace9512bdf5c935a716ee1851d3e636e7962fac
- add dwalsh's patches for selinux, emacs-gitignore, listen_pid and
remount /var/lib/docker as --private

* Wed Feb 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.1-1
- Bug 1066841 - upstream version bump to v0.8.1
- use sysvinit files from upstream contrib
- BR golang >= 1.2-7

* Thu Feb 13 2014 Adam Miller <maxamillion@fedoraproject.org> - 0.8.0-3
- Remove unneeded sysctl settings in initscript
  https://github.com/dotcloud/docker/pull/4125

* Sat Feb 08 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.0-2
- ignore btrfs for rhel7 and clones for now
- include vim syntax highlighting from contrib/syntax/vim

* Wed Feb 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.0-1
- upstream version bump
- don't use btrfs for rhel6 and clones (yet)

* Mon Jan 20 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.6-2
- bridge-utils only for rhel < 7
- discard freespace when image is removed

* Thu Jan 16 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.6-1
- upstream version bump v0.7.6
- built with golang >= 1.2

* Thu Jan 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.5-1
- upstream version bump to 0.7.5

* Thu Jan 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.4-1
- upstream version bump to 0.7.4 (BZ #1049793)
- udev rules file from upstream contrib
- unit file firewalld not used, description changes

* Mon Jan 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-3
- udev rules typo fixed (BZ 1048775)

* Sat Jan 04 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-2
- missed commit value in release 1, updated now
- upstream release monitoring (BZ 1048441)

* Sat Jan 04 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-1
- upstream release bump to v0.7.3

* Thu Dec 19 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.2-2
- require xz to work with ubuntu images (BZ #1045220)

* Wed Dec 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.2-1
- upstream release bump to v0.7.2

* Fri Dec 06 2013 Vincent Batts <vbatts@redhat.com> - 0.7.1-1
- upstream release of v0.7.1

* Mon Dec 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-14
- sysvinit patch corrected (epel only)
- 80-docker.rules unified for udisks1 and udisks2

* Mon Dec 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-13
- removed firewall-cmd --add-masquerade

* Sat Nov 30 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-12
- systemd for fedora >= 18
- firewalld in unit file changed from Requires to Wants
- firewall-cmd --add-masquerade after docker daemon start in unit file
  (Michal Fojtik <mfojtik@redhat.com>), continue if not present (Michael Young
  <m.a.young@durham.ac.uk>)
- 80-docker.rules included for epel too, ENV variables need to be changed for
  udisks1

* Fri Nov 29 2013 Marek Goldmann <mgoldman@redhat.com> - 0.7.0-11
- Redirect docker log to /var/log/docker (epel only)
- Removed the '-b none' parameter from sysconfig, it's unnecessary since
  we create the bridge now automatically (epel only)
- Make sure we have the cgconfig service started before we start docker,
    RHBZ#1034919 (epel only)

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-10
- udev rules added for fedora >= 19 BZ 1034095
- epel testing pending

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-9
- requires and started after firewalld

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-8
- iptables-fix patch corrected

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-7
- use upstream tarball and patch with mgoldman's commit

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-6
- using mgoldman's shortcommit value 0ff9bc1 for package (BZ #1033606)
- https://github.com/dotcloud/docker/pull/2907

* Wed Nov 27 2013 Adam Miller <maxamillion@fedoraproject.org> - 0.7.0-5
- Fix up EL6 preun/postun to not fail on postun scripts

* Wed Nov 27 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-4
- brctl patch for rhel <= 7

* Wed Nov 27 2013 Vincent Batts <vbatts@redhat.com> - 0.7.0-3
- Patch how the bridge network is set up on RHEL (BZ #1035436)

* Wed Nov 27 2013 Vincent Batts <vbatts@redhat.com> - 0.7.0-2
- add libcgroup require (BZ #1034919)

* Tue Nov 26 2013 Marek Goldmann <mgoldman@redhat.com> - 0.7.0-1
- Upstream release 0.7.0
- Using upstream script to build the binary

* Mon Nov 25 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.20.rc7
- correct the build time defines (bz#1026545). Thanks dan-fedora.

* Fri Nov 22 2013 Adam Miller <maxamillion@fedoraproject.org> - 0.7-0.19.rc7
- Remove xinetd entry, added sysvinit

* Fri Nov 22 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.18.rc7
- rc version bump

* Wed Nov 20 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.17.rc6
- removed ExecStartPost lines from docker.service (BZ #1026045)
- dockerinit listed in files

* Wed Nov 20 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.16.rc6
- adding back the none bridge patch

* Wed Nov 20 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.15.rc6
- update docker source to crosbymichael/0.7.0-rc6
- bridge-patch is not needed on this branch

* Tue Nov 19 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.14.rc5
- update docker source to crosbymichael/0.7-rc5
- update docker source to 457375ea370a2da0df301d35b1aaa8f5964dabfe
- static magic
- place dockerinit in a libexec
- add sqlite dependency

* Sat Nov 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.13.dm
- docker.service file sets iptables rules to allow container networking, this
    is a stopgap approach, relevant pull request here:
    https://github.com/dotcloud/docker/pull/2527

* Sat Oct 26 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.12.dm
- dm branch
- dockerinit -> docker-init

* Tue Oct 22 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.11.rc4
- passing version information for docker build BZ #1017186

* Sat Oct 19 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.10.rc4
- rc version bump
- docker-init -> dockerinit
- zsh completion script installed to /usr/share/zsh/site-functions

* Fri Oct 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.9.rc3
- lxc-docker version matches package version

* Fri Oct 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.8.rc3
- double quotes removed from buildrequires as per existing golang rules

* Fri Oct 11 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.7.rc3
- xinetd file renamed to docker.xinetd for clarity

* Thu Oct 10 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.6.rc3
- patched for el6 to use sphinx-1.0-build

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.5.rc3
- rc3 version bump
- exclusivearch x86_64

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.4.rc2
- debuginfo not Go-ready yet, skipped

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.3.rc2
- debuginfo package generated
- buildrequires listed with versions where needed
- conditionals changed to reflect systemd or not
- docker commit value not needed
- versioned provides lxc-docker

* Mon Oct 07 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-2.rc2
- rc branch includes devmapper
- el6 BZ #1015865 fix included

* Sun Oct 06 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-1
- version bump, includes devicemapper
- epel conditionals included
- buildrequires sqlite-devel

* Fri Oct 04 2013 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.6.3-4.devicemapper
- docker-io service enables IPv4 and IPv6 forwarding
- docker user not needed
- golang not supported on ppc64, docker-io excluded too

* Thu Oct 03 2013 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.6.3-3.devicemapper
- Docker rebuilt with latest kr/pty, first run issue solved

* Fri Sep 27 2013 Marek Goldmann <mgoldman@redhat.com> - 0.6.3-2.devicemapper
- Remove setfcap from lxc.cap.drop to make setxattr() calls working in the
  containers, RHBZ#1012952

* Thu Sep 26 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.3-1.devicemapper
- version bump
- new version solves docker push issues

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-14.devicemapper
- package requires lxc

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-13.devicemapper
- package requires tar

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-12.devicemapper
- /var/lib/docker installed
- package also provides lxc-docker

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-11.devicemapper
- better looking url

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-10.devicemapper
- release tag changed to denote devicemapper patch

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-9
- device-mapper-devel is a buildrequires for alex's code
- docker.service listed as a separate source file

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-8
- install bash completion
- use -v for go build to show progress

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-7
- build and install separate docker-init

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-4
- update to use new source-only golang lib packages

* Sat Sep 21 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-3
- man page generation from docs/.
- systemd service file created
- dotcloud/tar no longer required

* Fri Sep 20 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-2
- patched with alex larsson's devmapper code

* Wed Sep 18 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-1
- Version bump

* Tue Sep 10 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.1-2
- buildrequires updated
- package renamed to docker-io
 
* Fri Aug 30 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.1-1
- Version bump
- Package name change from lxc-docker to docker
- Makefile patched from 0.5.3

* Wed Aug 28 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-5
- File permissions settings included

* Wed Aug 28 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-4
- Credits in changelog modified as per reference's request

* Tue Aug 27 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-3
- Dependencies listed as rpm packages instead of tars
- Install section added

* Mon Aug 26 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-2
- Github packaging
- Deps not downloaded at build time courtesy Elan Ruusamäe
- Manpage and other docs installed

* Fri Aug 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-1
- Initial fedora package
- Some credit to Elan Ruusamäe (glen@pld-linux.org)
