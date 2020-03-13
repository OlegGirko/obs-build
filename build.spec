#
# spec file for package build
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%define _binaries_in_noarch_packages_terminate_build 0

Name:           build
Summary:        A Script to Build SUSE Linux RPMs
License:        GPL-2.0+ and GPL-2.0
Group:          Development/Tools/Building
Version:        20200313
Release:        1
#!BuildIgnore:  build-mkbaselibs
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
# Manual requires to avoid hard require to bash-static
AutoReqProv:    off
# Keep the following dependencies in sync with obs-worker package
Requires:       bash
Requires:       binutils
Requires:       perl
Requires:       tar
Requires:       bsdtar
%if 0%{?fedora}
Requires:       perl-MD5
Requires:       perl-TimeDate
%endif
Conflicts:      bsdtar < 2.5.5
Provides:       obs-build = %{version}-%{release}
Provides:       perl(Build)
Provides:       perl(Build::Arch)
Provides:       perl(Build::Archrepo)
Provides:       perl(Build::Collax)
Provides:       perl(Build::Deb)
Provides:       perl(Build::Debrepo)
Provides:       perl(Build::Kiwi)
Provides:       perl(Build::LiveBuild)
Provides:       perl(Build::Mdkrepo)
Provides:       perl(Build::Repo)
Provides:       perl(Build::Rpm)
Provides:       perl(Build::Rpmmd)
Provides:       perl(Build::SimpleXML)
Provides:       perl(Build::Susetags)
Provides:       perl(Build::Zypp)
%if 0%{?suse_version} > 1000
# None of them are actually required for core features.
# Perl helper scripts use them.
Recommends:     perl(Date::Language)
Recommends:     perl(Date::Parse)
Recommends:     perl(LWP::UserAgent)
Recommends:     perl(Pod::Usage)
Recommends:     perl(Time::Zone)
Recommends:     perl(URI)
Recommends:     perl(XML::Parser)
Recommends:     bsdtar
Recommends:     qemu-linux-user
%endif

%if 0%{?suse_version} > 1120 || ! 0%{?suse_version}
Requires:       build-mkbaselibs
%endif

%if 0%{?suse_version} > 1120 || 0%{?mdkversion}
Recommends:     build-mkdrpms
%endif

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
Requires:       build

%description mkdrpms
This package contains the parts which may be installed in the inner build system
for generating delta rpm packages.

%endif

%define initvm_arch %{_host_cpu}
%if %{_host_cpu} == "i686"
%define initvm_arch i586
%endif
%package initvm-%{initvm_arch}
Summary:        Virtualization initializer for emulated cross architecture builds
Group:          Development/Tools/Building
Requires:       build
BuildRequires:  gcc
BuildRequires:  glibc-devel
Provides:       build-initvm
Obsoletes:      build-initvm
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

# Explicitly specify Python version
sed -e '1s/^\(#!.*python\)$/\12/' -i openstack-console

%build
make CFLAGS="$RPM_BUILD_FLAGS" initvm-all

%install
# initvm
make DESTDIR=$RPM_BUILD_ROOT initvm-install
strip $RPM_BUILD_ROOT/usr/lib/build/initvm.*
export NO_BRP_STRIP_DEBUG="true"
chmod 0644 $RPM_BUILD_ROOT/usr/lib/build/initvm.*

# main
make DESTDIR=$RPM_BUILD_ROOT install
cd $RPM_BUILD_ROOT/usr/lib/build/configs/
%if 0%{?suse_version}
%if 0%{?sles_version}
 ln -s sles%{sles_version}.conf default.conf
%else
 V=%suse_version
 ln -s sl${V:0:2}.${V:2:1}.conf default.conf
%endif
test -e default.conf
%endif

%files
%defattr(-,root,root)
%doc README
/usr/bin/build
/usr/bin/buildvc
/usr/bin/unrpm
/usr/lib/build
%config(noreplace) /usr/lib/build/emulator/emulator.sh
%{_mandir}/man1/*.1*
%exclude /usr/lib/build/initvm.*

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

%files initvm-%{initvm_arch}
%defattr(-,root,root)
/usr/lib/build/initvm.*

%changelog
