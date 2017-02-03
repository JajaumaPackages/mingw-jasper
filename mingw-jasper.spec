%?mingw_package_header

%global mingw_build_win32 1
%global mingw_build_win64 1

Name:           mingw-jasper
Version:        1.900.28
Release:        2%{?dist}
Summary:        MinGW Windows Jasper library

License:        JasPer
Group:          Development/Libraries

URL:            http://www.ece.uvic.ca/~frodo/jasper/
Source0:        http://www.ece.uvic.ca/~frodo/jasper/software/jasper-%{version}.tar.gz

# Patches from Fedora native package.
# OpenBSD hardening patches addressing couple of possible integer overflows
# during the memory allocations
# https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2008-3520
Patch5: jasper-1.900.1-CVE-2008-3520.patch

# MinGW-specific patches.
# This patch adds '-no-undefined' flag to libtool line:
Patch1000:      jasper-1.900.1-mingw32.patch
# This patch is a bit of a hack, but it's just there to fix a demo program:
Patch1001:      jasper-1.900.1-sleep.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw64-binutils
BuildRequires:  mingw32-libjpeg
BuildRequires:  mingw64-libjpeg

BuildRequires:  autoconf automake libtool


%description
MinGW Windows Jasper library.


%package -n mingw32-jasper
Summary:        MinGW Windows Jasper library

%description -n mingw32-jasper
MinGW Windows Jasper library.


%package -n mingw32-jasper-static
Summary:        Static version of the MinGW Windows Jasper library
Requires:       mingw32-jasper = %{version}-%{release}
Group:          Development/Libraries

%description -n mingw32-jasper-static
Static version of the MinGW Windows Jasper library.


%package -n mingw64-jasper
Summary:        MinGW Windows Jasper library

%description -n mingw64-jasper
MinGW Windows Jasper library.


%package -n mingw64-jasper-static
Summary:        Static version of the MinGW Windows Jasper library
Requires:       mingw64-jasper = %{version}-%{release}
Group:          Development/Libraries

%description -n mingw64-jasper-static
Static version of the MinGW Windows Jasper library.


%?mingw_debug_package


%prep
%setup -q -n jasper-%{version}
%patch5 -p1 -b .CVE-2008-3520

# The libtool bundled with this package is too old for win64 support
autoreconf -i --force

%patch1000 -p1 -b .mingw32
%patch1001 -p1 -b .sleep


%build
# comment from Red Hat Security Response Team:
# gcc inlines jas_iccattrtab_resize into jas_iccattrtab_add. Additionally, it
# essentially removes the "assert(maxents >= tab->numattrs);" assertion in
# jas_iccattrtab_resize, because it assumes that "maxents >= tab->numattrs" will
# always be true due to jas_iccattrtab_resize(attrtab, attrtab->numattrs + 32),
# especially the + 32. This assumption can only be true if it completely ignores
# the problem of signed integer overflows. I don't think it's a smart idea to
# accept that.
# -fno-strict-overflow forces gcc into keeping the assertion there.
CFLAGS="%{optflags} -fno-strict-overflow" \
%mingw_configure \
  --disable-opengl --enable-libjpeg --enable-static --enable-shared
%mingw_make %{?_smp_mflags}


%install
%mingw_make DESTDIR=$RPM_BUILD_ROOT install mandir=%{mingw32_mandir}

# Remove .la files
rm $RPM_BUILD_ROOT%{mingw32_libdir}/*.la
rm $RPM_BUILD_ROOT%{mingw64_libdir}/*.la

# Remove the manual pages - don't duplicate documentation which
# is in the native Fedora package.
rm $RPM_BUILD_ROOT%{mingw32_mandir}/man1/*


%files -n mingw32-jasper
%doc COPYRIGHT LICENSE NEWS README
%{mingw32_bindir}/imgcmp.exe
%{mingw32_bindir}/imginfo.exe
%{mingw32_bindir}/jasper.exe
%{mingw32_bindir}/tmrdemo.exe
%{mingw32_bindir}/libjasper-4.dll
%{mingw32_libdir}/libjasper.dll.a
%{mingw32_libdir}/pkgconfig/jasper.pc
%{mingw32_includedir}/jasper/

%files -n mingw32-jasper-static
%{mingw32_libdir}/libjasper.a

%files -n mingw64-jasper
%doc COPYRIGHT LICENSE NEWS README
%{mingw64_bindir}/imgcmp.exe
%{mingw64_bindir}/imginfo.exe
%{mingw64_bindir}/jasper.exe
%{mingw64_bindir}/tmrdemo.exe
%{mingw64_bindir}/libjasper-4.dll
%{mingw64_libdir}/libjasper.dll.a
%{mingw64_libdir}/pkgconfig/jasper.pc
%{mingw64_includedir}/jasper/

%files -n mingw64-jasper-static
%{mingw64_libdir}/libjasper.a


%changelog
* Fri Feb 03 2017 Jajauma's Packages <jajauma@yandex.ru> - 1.900.28-2
- Rebuild with GCC 5.4.0

* Wed Nov 23 2016 Michael Cronenworth <mike@cchtml.com> - 1.900.28-1
- Upstream release.
- Many security fixes:
     CVE-2016-9395, CVE-2016-9262, CVE-2016-8690, CVE-2016-8691,
     CVE-2016-8693, CVE-2016-2089, CVE-2015-5203, CVE-2015-5221, CVE-2016-8692,
     CVE-2016-1867, CVE-2016-1577, CVE-2016-2116

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.900.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 Michael Cronenworth <mike@cchtml.com> - 1.900.1-26
- Fixes for CVE-2014-8157 and CVE-2014-8158

* Thu Dec 18 2014 Michael Cronenworth <mike@cchtml.com> - 1.900.1-25
- Fixes for CVE-2014-8137 and CVE-2014-8138

* Sat Dec 13 2014 Michael Cronenworth <mike@cchtml.com> - 1.900.1-24
- Apply all native patches for CVEs

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.900.1-19
- Eliminated the libtool hack

* Wed Mar 14 2012 Kalev Lember <kalevlember@gmail.com> - 1.900.1-18
- Build 64 bit Windows binaries

* Fri Mar 09 2012 Kalev Lember <kalevlember@gmail.com> - 1.900.1-17
- Remove .la files

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.900.1-16
- Renamed the source package to mingw-jasper (#800426)
- Spec clean up
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.900.1-15
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 03 2011 Kalev Lember <kalev@smartlink.ee> - 1.900.1-13
- Rebuilt with mingw32-libjpeg-turbo

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 18 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.900.1-11
- Rebuild because of broken mingw32-gcc/mingw32-binutils

* Thu Aug 27 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.900.1-10
- Rebuild for mingw32-libjpeg 7
- Automatically generate debuginfo subpackage
- Added -static subpackage
- Use %%global instead of %%define

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  9 2009 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-8
- Fix defattr line.
- Remove the enable-shared patch, and just use --enable-shared on
  the configure line.
- Disable the GL patch since OpenGL is disabled.
- Document what the patches are for in the spec file.
- Only patch Makefile.in so we don't have to rerun autotools, and
  remove autotools dependency.

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-7
- Rebuild for mingw32-gcc 4.4

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-6
- Use _smp_mflags.
- Disable static libraries.
- Include documentation.
- Use the same patches as Fedora native package.
- Just run autoconf instead of autoreconf so we don't upgrade libtool.
- +BR mingw32-dlfcn.
- Don't need the manual pages.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-5
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.900.1-4
- Add overflow patch from rawhide

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.900.1-3
- Run autoreconf after changing configure.ac script and add BRs for autotools

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-2
- Enable DLLs.
- Remove static libraries.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.900.1-1
- Initial RPM release
