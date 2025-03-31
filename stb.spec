%define major   0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%define commit f0569113c93ad095470c54bf34a17b36646bbbb5
%define date 20250314
%define rel 1

Name:           stb
Version:        0
Release:        0.%{date}.0
Group:          System/Libraries
Summary:        stb single-file public domain libraries for C/C++
License:        MIT or Public Domain
URL:            https://github.com/nothings/stb
Source0:        https://github.com/nothings/stb/archive/%{commit}.tar.gz
Patch0:         stb-add-missing-include.patch
# Debian patches (P1->P10)
Patch1:         0001-Makefile-refactor.patch
Patch2:         0002-Mask-out-rectangle-packing-replacement-in-stb_truety.patch
Patch3:         0003-stb.h-fix-pointer-detection.patch
Patch4:         0004-stb_c_lexer.h-exit-on-error.patch
Patch5:         0005-stb_sprintf.h-fix-pointer-detection.patch
# Out of bounds heap buffer write (GHSL-2023-171/CVE-2023-45681)
# https://github.com/nothings/stb/pull/1559
# Fixes CVE-2023-45681 and duplicate CVE-2023-47212
# https://bugzilla.redhat.com/show_bug.cgi?id=2278402
Patch10:          %{url}/pull/1559.patch

%description
stb single-file public domain libraries for C/C++.

%package -n %{libname}
Summary:        stb single-file public domain libraries for C/C++
Group:          System/Libraries

%description -n %{libname}
stb single-file public domain libraries for C/C++.

%package -n %{devname}
Summary:        Development package for %{name}
Group:          Development/Libraries
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{devname}
Header files for development with %{name}.

%prep
%autosetup -p1 -n %{name}-%{commit}

%build
%set_build_flags
%global optflags %{optflags} -Wno-incompatible-pointer-types
%make_build LIBDIR=%{_lib}

%install
%make_install LIBDIR=%{_lib}

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}{,.*}

%files -n %{devname}
%doc README.md docs
%{_includedir}/stb/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/stb.pc
