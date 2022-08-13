#
# spec file for package build
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
# needsrootforbuild
# needsbinariesforbuild

%define _binaries_in_noarch_packages_terminate_build 0
%define __brp_mangle_shebangs %{nil}

%define __pkg_name build

%if 0%{?suse_version} || 0%{?fedora}
%bcond_without initvm
%else
%bcond_with initvm
%endif

Name:           %{__pkg_name}
Summary:        A Script to Build SUSE Linux RPMs
License:        GPL-2.0-only OR GPL-3.0-only
Group:          Development/Tools/Building
Version:        20220620
Release:        0
Source:         obs-build-%{version}.tar.bz2
Patch1:         0001-Add-support-for-using-Scratchbox2-together-with-OBS-.patch
Patch2:         0002-Make-enter_target-shell-quote-safe.patch
Patch3:         0003-Workaround-quoting-problem-with-Harmattan.patch
Patch4:         0004-Support-Xen-on-MeeGo-OBS.patch
Patch5:         0005-SPEC_REL-can-be-in-prjconf-and-must-be-substituted-a.patch
Patch6:         0006-initial-support-for-chroot-only.patch
Patch7:         0007-chroot-only-fixup.patch
Patch8:         0008-Add-skip-prep-to-ask-a-suitable-rpm-to-skip-the-prep.patch
Patch9:         0009-Only-run-the-xen-remount-in-xen-guests.patch
Patch10:        0010-Pass-the-ABUILD_UID-GID-to-the-sb2-init.patch
Patch11:        0011-Workaround-for-bug-https-bugs.merproject.org-show_bu.patch
Patch12:        0012-Move-the-rsync-overlay-actions-prior-to-any-2nd-stag.patch
Patch13:        0013-Pass-the-RSYNCDONE-flag-to-the-2nd-stage.patch
Patch14:        0014-Pass-the-SKIP_PREP-flag-to-the-2nd-stage.patch
Patch15:        0015-We-rsync-to-the-BUILD_ROOT-not-the-BUILD_TARGET.patch
Patch16:        0016-Add-support-for-a-build.script-for-spec-rpm-builds-t.patch
Patch17:        0017-Pass-additional-variables-to-sb2-build-even-if-VM_TY.patch
Patch18:        0018-Fix-permissions-of-dev-files-in-buildsystem-with-chm.patch
Patch19:        0019-Fix-filtering-out-sb2install-packages-from-package-l.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
#!BuildIgnore:  build-mkbaselibs build-mkbaselibs-sle
# Keep the following dependencies in sync with obs-worker package
Requires:       bash
Requires:       binutils
Requires:       findutils
Requires:       perl
Requires:       tar
# needed for fuser
Requires:       psmisc
# just to verify existence of packages
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  perl
BuildRequires:  psmisc
BuildRequires:  tar
# For testcases
BuildRequires:  perl(Date::Parse)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
%if 0%{?fedora}
Requires:       perl-MD5
Requires:       perl-TimeDate
BuildRequires:  perl-TimeDate
%endif
Conflicts:      bsdtar < 2.5.5
%if 0%{?suse_version}
Conflicts:      qemu < 2.5.0
%endif
BuildRequires:  perl(Date::Parse)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(YAML::LibYAML)
Provides:       obs-build = %{version}-%{release}
%if 0%{?suse_version} > 1000 || 0%{?centos_version} >= 800 || 0%{?rhel_version} >= 800 || 0%{?fedora} >= 21
# None of them are actually required for core features.
# Perl helper scripts use them.
Recommends:     perl(Date::Language)
Recommends:     perl(Date::Parse)
Recommends:     perl(LWP::UserAgent)
Recommends:     perl(Pod::Usage)
Recommends:     perl(Time::Zone)
Recommends:     perl(URI)
Recommends:     perl(XML::Parser)
Recommends:     perl(Net::SSL)
Recommends:     perl(YAML::LibYAML)
Recommends:     bsdtar
Recommends:     qemu-linux-user
Recommends:     zstd
Recommends:     /usr/bin/qemu-kvm
Recommends:     /sbin/mkfs.ext3
%endif

%if 0%{?suse_version} > 1120 || ! 0%{?suse_version}
Requires:       %{__pkg_name}-mkbaselibs
%endif

%if 0%{?suse_version} > 1120 || 0%{?mdkversion}
Recommends:     %{__pkg_name}-mkdrpms
%endif

# With fedora 33 the POSIX module was split out of the perl
# package
BuildRequires: perl(POSIX)
Requires: perl(POSIX)


%description
This package provides a script for building RPMs for SUSE Linux in a
chroot environment.


%if 0%{?suse_version} > 1120 || ! 0%{?suse_version}

%package mkbaselibs
Summary:        Tools to generate base lib packages
Group:          Development/Tools/Building
# NOTE: this package must not have dependencies which may break boot strapping (eg. perl modules)

%description mkbaselibs
This package contains the parts which may be installed in the inner build system
for generating base lib packages.

%package mkdrpms
Summary:        Tools to generate delta rpms
Group:          Development/Tools/Building
Requires:       deltarpm
# XXX: we wanted to avoid that but mkdrpms needs Build::Rpm::rpmq
Requires:       %{__pkg_name}

%description mkdrpms
This package contains the parts which may be installed in the inner build system
for generating delta rpm packages.

%endif

%define initvm_arch %{_host_cpu}
%if "%{_host_cpu}" == "i686"
%define initvm_arch i586
%endif
%package initvm-%{initvm_arch}
Summary:        Virtualization initializer for emulated cross architecture builds
Group:          Development/Tools/Building
Requires:       %{__pkg_name}
BuildRequires:  gcc
BuildRequires:  glibc-devel
Provides:       %{__pkg_name}-initvm
Obsoletes:      %{__pkg_name}-initvm
%if 0%{?suse_version} > 1200
BuildRequires:  glibc-devel-static
%endif
%if 0%{?fedora}
BuildRequires:  glibc-static
%endif

%description initvm-%{initvm_arch}
This package provides a script for building RPMs for SUSE Linux in a
chroot or a secure virtualized

%prep
%setup -q -n src
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1

%build
%if %{with initvm}
# initvm
make CFLAGS="$RPM_BUILD_FLAGS" initvm-all
%endif

%install
# initvm
%if %{with initvm}
make DESTDIR=%{buildroot} initvm-install
strip %{buildroot}/usr/lib/build/initvm.*
export NO_BRP_STRIP_DEBUG="true"
chmod 0644 %{buildroot}/usr/lib/build/initvm.*
%endif

# main
make DESTDIR=%{buildroot} install

# tweak default config on suse
%if 0%{?suse_version}
cd %{buildroot}/usr/lib/build/configs/
SUSE_V=%{?suse_version}
SLE_V=%{?sle_version}
%if 0%{?sle_version} && 0%{?is_opensuse} && %suse_version == 1315
# this is SUSE Leap 42.X
ln -s sl42.${SLE_V:3:1}.conf default.conf
%endif
%if 0%{?sle_version} && 0%{?is_opensuse} && %suse_version > 1315
# this is SUSE Leap 15 and higher
ln -s sl${SLE_V:0:2}.${SLE_V:3:1}.conf default.conf
%endif
%if !0%{?sle_version} && ( 0%{?suse_version} <= 1310 || 0%{?suse_version} == 1320 || 0%{?suse_version} == 1330 )
# this is old openSUSE releases and Factory
ln -s sl${SUSE_V:0:2}.${SUSE_V:2:1}.conf default.conf
%endif
%if !0%{?sle_version} && ( 0%{?suse_version} == 1599 )
ln -s tumbleweed.conf default.conf
%endif
%if 0%{?sle_version} && !0%{?is_opensuse}
# this is SUSE SLE 12 and higher
ln -s sle${SLE_V:0:2}.${SLE_V:3:1}.conf default.conf
%endif
%if 0%{?sles_version} == 1110
# this is SUSE SLE 11
ln -s sles11sp2.conf default.conf
%endif
# make sure that we have a config
test -e default.conf || exit 1
%endif

# tweak baselibs config on suse
%if 0%{?suse_version}
cd %{buildroot}/usr/lib/build
%if %suse_version == 1500
# SLE 15 / Leap 15
ln -sf baselibs_configs/baselibs_global-sle15.conf baselibs_global.conf
%endif
%if %suse_version == 1315
# SLE 12 / Leap 42
ln -sf baselibs_configs/baselibs_global-sle12.conf baselibs_global.conf
%endif
%if %suse_version <= 1110
# SLE 11
ln -sf baselibs_configs/baselibs_global-sle11.conf baselibs_global.conf
%endif
test -e baselibs_global.conf || exit 1
%endif

%check
for i in build build-* ; do bash -n $i || exit 1 ; done

# run perl module unit tests
LANG=C make test || exit 1

if [ `whoami` != "root" ]; then
  echo "WARNING: Not building as root, build test did not run!"
  exit 0
fi
if [ ! -f "%{buildroot}/usr/lib/build/configs/default.conf" ]; then
  echo "WARNING: No default config, build test did not run!"
  exit 0
fi
# get back the default.conf link
cp -av %{buildroot}/usr/lib/build/configs/default.conf configs/
# do not get confused when building this already with build:
export BUILD_IGNORE_2ND_STAGE=1
# use our own build code
export BUILD_DIR=$PWD

# simple chroot build test
cd test
# target is autodetected
%if 0%{?sles_version}
echo "SLES config differs currently on purpose between OBS and build script."
echo "Skipping test case"
exit 0
%endif
%if 0%{?qemu_user_space_build}
echo "test suite is not prepared to run using qemu linux user"
echo "Skipping test case"
exit 0
%endif
# we need to patch the not packaged configs, due to the buildignore
sed -i 's,build-mkbaselibs,,' ../configs/*.conf
if [ ! -e /.build.packages/rpmlint-Factory.rpm ]; then
  sed -i 's,rpmlint-Factory,,' ../configs/*.conf
fi
./testbuild.sh /.build.binaries/

%files
%defattr(-,root,root)
%doc README.md docs
/usr/bin/build
/usr/bin/pbuild
/usr/bin/buildvc
/usr/bin/unrpm
/usr/lib/build
%config(noreplace) /usr/lib/build/emulator/emulator.sh
%{_mandir}/man1/build.1*
%{_mandir}/man1/unrpm.1*
%{_mandir}/man1/buildvc.1*
%{_mandir}/man1/pbuild.1*
%if %{with initvm}
%exclude /usr/lib/build/initvm.*
%endif

%if 0%{?suse_version} > 1120 || ! 0%{?suse_version}
%exclude /usr/lib/build/mkbaselibs
%exclude /usr/lib/build/baselibs*
%exclude /usr/lib/build/mkdrpms

%files mkbaselibs
%defattr(-,root,root)
%dir /usr/lib/build
/usr/lib/build/mkbaselibs
/usr/lib/build/baselibs*

%files mkdrpms
%defattr(-,root,root)
%dir /usr/lib/build
/usr/lib/build/mkdrpms
%endif

%if %{with initvm}
%files initvm-%{initvm_arch}
%defattr(-,root,root)
/usr/lib/build/initvm.*
%endif

%changelog
