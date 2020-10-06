#global commit 13a0dd86874b5d7558a0e131f3deaa42cd7d9d23
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}
%{?commit:%global commitdate 20200828}
%{?commit:%global scmsnap %{commitdate}git%{shortcommit}}

%global enable_dm_mpath_support 1

##############################################################################
# SID
##############################################################################

Name: sid
Version: 0.0.3
Release: 1%{?scmsnap:.%{scmsnap}}%{?dist}
Summary: Storage Instantiation Daemon (SID)

License: GPLv2+
URL: http://sid-project.github.io
%if %{defined commit}
Source0: https://github.com/sid-project/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0: https://github.com/sid-project/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: systemd-rpm-macros
BuildRequires: systemd-devel >= 221
BuildRequires: libudev-devel >= 174
BuildRequires: libuuid-devel
BuildRequires: libblkid-devel
%if %{enable_dm_mpath_support}
BuildRequires: device-mapper-multipath-devel >= 0.8.4-7
%endif

Requires: %{name}-base-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-log-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-resource-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-tools = %{version}-%{release}

%description
Storage Instantiation Daemon (SID) aims to help with Linux storage
device state tracking that encompasses device layers, groups and whole
stacks by monitoring progression of events. Based on monitored states
and further recorded information, it is able to trigger associated
actions for well-defined triggers, including activation and deactivation
of devices and their layers in the stack.

%prep
%if %{defined commit}
%autosetup -p1 -n sid-%{commit}
%else
%autosetup -p1 -n sid-%{version}
%endif

%if ! %{enable_dm_mpath_support}
%global configure_dm_mpath --disable-mod-dm_mpath
%endif

%build
./autogen.sh
%configure %{?configure_dm_mpath}
%make_build

%install
make DESTDIR=%{buildroot} install
rm -f $RPM_BUILD_ROOT%{_libdir}/sid/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/sid/modules/ucmd/block/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/sid/modules/ucmd/type/*.{a,la}

%files
%license COPYING
%{_sbindir}/sid
%config(noreplace) %{_sysconfdir}/sysconfig/sid.sysconfig
%{_udevrulesdir}/00-sid.rules
%{_unitdir}/sid.socket
%{_unitdir}/sid.service
%doc README.md

%post
%systemd_post sid.socket sid.service

%preun
%systemd_preun sid.service sid.socket


##############################################################################
# SID-BASE-LIBS
##############################################################################

%package base-libs
Summary: Libraries for Storage Instantiation Daemon (SID) base
License: GPLv2+
%description base-libs
This package contains shared libraries with low-level functionality needed for
Storage Instantiation Daemon (SID), its modules and related tools. Currently,
it contains basic support for bitmaps, buffering, IPC, hashing, lists, memory
handling and other helper functions.

%files base-libs
%{_libdir}/sid/libsidbase.so.*
%doc README.md


##############################################################################
# SID-BASE-LIBS-DEVEL
##############################################################################

%package base-libs-devel
Summary: Development files for Storage Instantiation Daemon (SID) base
License: GPLv2+
Requires: %{name}-base-libs%{?_isa} = %{version}-%{release}
%description base-libs-devel
This package contains development files for Storage Instantiation Daemon (SID)
base libraries.

%files base-libs-devel
%{_libdir}/sid/libsidbase.so
%{_includedir}/sid/config.h
%{_includedir}/sid/base/bitmap.h
%{_includedir}/sid/base/buffer-common.h
%{_includedir}/sid/base/buffer.h
%{_includedir}/sid/base/common.h
%{_includedir}/sid/base/comms.h
%{_includedir}/sid/base/list.h
%{_includedir}/sid/base/mem.h
%{_includedir}/sid/base/util.h
%doc README.md


##############################################################################
# SID-LOG-LIBS
##############################################################################

%package log-libs
Summary: Libraries for Storage Instantiation Daemon (SID) logging
License: GPLv2+
%description log-libs
This package contains shared libraries with logging support needed for Storage
Instantiation daemon (SID), its modules and related tools.

%files log-libs
%{_libdir}/sid/libsidlog.so.*
%doc README.md


##############################################################################
# SID-LOG-LIBS-DEVEL
##############################################################################

%package log-libs-devel
Summary: Development files for Storage Instantiation Daemon (SID) logging
License: GPLv2+
Requires: %{name}-log-libs%{?_isa} = %{version}-%{release}
%description log-libs-devel
This package contains development files for Storage Instantiation Daemon (SID)
logging libraries.

%files log-libs-devel
%{_libdir}/sid/libsidlog.so
%{_includedir}/sid/log/log.h
%doc README.md


##############################################################################
# SID-IFACE-LIBS
##############################################################################

%package iface-libs
Summary: Libraries for Storage Instantiation Daemon (SID) interfaces
License: GPLv2+
Requires: %{name}-base-libs%{?_isa} = %{version}-%{release}
%description iface-libs
This package contains shared libraries to support interfaces used in Storage
Instatiation Daemon (SID), its modules and related tools.

%files iface-libs
%{_libdir}/sid/libsidiface_servicelink.so.*
%{_libdir}/sid/libsidiface_usid.so.*
%doc README.md


##############################################################################
# SID-IFACE-LIBS-DEVEL
##############################################################################

%package iface-libs-devel
Summary: Development files for Storage Instantiation Daemon (SID) interfaces
License: GPLv2+
Requires: %{name}-iface-libs%{?_isa} = %{version}-%{release}
%description iface-libs-devel
This package contains development files for Storage Instantiation Daemon (SID)
interface libraries.

%files iface-libs-devel
%{_libdir}/sid/libsidiface_servicelink.so
%{_libdir}/sid/libsidiface_usid.so
%{_includedir}/sid/iface/service-link.h
%{_includedir}/sid/iface/usid.h
%doc README.md


##############################################################################
# SID-RESOURCE-LIBS
##############################################################################

%package resource-libs
Summary: Libraries for Storage Instantiation Daemon (SID) resources
License: GPLv2+
Requires: %{name}-base-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-log-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-iface-libs%{?_isa} = %{version}-%{release}
# Systemd supports event loop since v221
Requires: systemd-libs >= 221
%description resource-libs
This package contains shared libraries to support high-level resources that
represent hierarchical units of reusable code used in Storage Instantiation
Daemon (SID), its modules and related tools. Currently, it contains support
for aggregation, key-value store, module loading and registry, worker process
control, bridging SID core and udev and creating an instance of SID as a whole.

%files resource-libs
%{_libdir}/sid/libsidresource.so.*
%doc README.md


##############################################################################
# SID-RESOURCE-LIBS-DEVEL
##############################################################################

%package resource-libs-devel
Summary: Development files for Storage Instantiation Daemon (SID) resources
License: GPLv2+
Requires: %{name}-resource-libs%{?_isa} = %{version}-%{release}
%description resource-libs-devel
This package contains development files for Storage Instantiation Daemon (SID)
resource libraries.

%files resource-libs-devel
%{_libdir}/sid/libsidresource.so
%{_includedir}/sid/resource/kv-store.h
%{_includedir}/sid/resource/module-registry.h
%{_includedir}/sid/resource/module.h
%{_includedir}/sid/resource/resource-type-regs.h
%{_includedir}/sid/resource/resource.h
%{_includedir}/sid/resource/ucmd-module.h
%{_includedir}/sid/resource/worker-control.h
%doc README.md


##############################################################################
# SID-TOOLS
##############################################################################

%package tools
Summary: Storage Instantiation Daemon (SID) supporting tools
Requires: %{name}-base-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-log-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-iface-libs%{?_isa} = %{version}-%{release}
%description tools
This package contains tools to support Storage Instantiation Daemon (SID).

%files tools
%{_udevrulesdir}/../usid
%doc README.md


##############################################################################
# SID-MOD-DUMMIES
##############################################################################
%package mod-dummies
Summary: Dummy block and type module for Storage Instantiation Daemon (SID)
Requires: %{name}-log-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-resource-libs%{?_isa} = %{version}-%{release}
%description mod-dummies
This package contains dummy block and type modules for Storage Instantiation
Daemon (SID). Their only purpose is to test SID module functionality and hook
execution.

%files mod-dummies
%{_libdir}/sid/modules/ucmd/block/dummy_block.so
%{_libdir}/sid/modules/ucmd/type/dummy_type.so
%doc README.md


##############################################################################
# SID-MOD-BLOCK-BLKID
##############################################################################

%package mod-block-blkid
Summary: Blkid block module for Storage Instantiation Daemon (SID)
Requires: %{name}-log-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-resource-libs%{?_isa} = %{version}-%{release}
%description mod-block-blkid
This package contains blkid block module for Storage Instantiation Daemon (SID).

%files mod-block-blkid
%{_libdir}/sid/modules/ucmd/block/blkid.so
%doc README.md


##############################################################################
# SID-MOD-BLOCK-DM_MPATH
##############################################################################

%if %{enable_dm_mpath_support}

%package mod-block-dm-mpath
Summary: Device-mapper multipath block module for Storage Instantiation Daemon (SID)
Requires: %{name}-log-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-resource-libs%{?_isa} = %{version}-%{release}
Requires: device-mapper-multipath-libs >= 0.8.4-7
%description mod-block-dm-mpath
This package contains device-mapper multipath block module for Storage
Instantiation Daemon (SID).

%files mod-block-dm-mpath
%{_libdir}/sid/modules/ucmd/block/dm_mpath.so
%doc README.md

%endif


%changelog
* Tue Oct 06 2020 Peter Rajnoha <prajnoha@redhat.com> - 0.0.4-1
- Initial release.
