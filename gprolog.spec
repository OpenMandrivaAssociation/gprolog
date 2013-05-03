Summary:	Summary GNU Prolog is a free implementation of Prolog
Name:		gprolog
Version:	1.3.1
Release:	3
Group:		Development/Other
License:	GPLv2
Url:		http://gnu-prolog.inria.fr/
Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
#Patch0 was sent upstream (Kharec)
Patch0:		gprolog-1.3.1-fix-str-fmt.patch
Patch2:		gprolog-1.3.0-noexecstack.patch
Patch3:		gprolog-1.3.1-reverse-order.patch
ExclusiveArch:	%{ix86} x86_64 amd64 ppc

%description
GNU Prolog is a native Prolog compiler with constraint solving over finite
domains (FD) developed by Daniel Diaz. Latest information about GNU Prolog can
be found at http://www.gnu.org/software/prolog.
A lot of work has been devoted to the ISO compatibility. GNU Prolog is very
close to the ISO standard (http://www.logic-programming.org/prolog_std.html).

%prep
%setup -q
%apply_patches
(cd src && autoconf)

%build
cd src
CFLG="$(echo %{optflags} | sed -s "s/\-O2/-O1/g" \
	| sed -e "s/\-fomit-frame-pointer//")"

# Based on a gentoo ebuild (??)
CFLG="$CFLG -funsigned-char"
%configure2_5x \
	-with-c-flags="$CFLG -fno-unit-at-a-time" \
	--with-install-dir=%{_prefix} \
	--with-doc-dir=%{_datadir}/%{name}-%{version} \
	--with-html-dir=%{_datadir}/%{name}-%{version}/html \
	--with-examples-dir=%{_datadir}/%{name}-%{version}/examples
# parallel build is not safe - AdamW 2008/12
make

%check
cd src
#
export PATH=%{buildroot}%{_bindir}:$PATH
#
make check

%install
install -d %{buildroot}%{_bindir}

(cd src ; make install-system INSTALL_DIR=%{buildroot}%{_libdir}/%{name}-%{version})

(cd %{buildroot}%{_bindir} ; ln -sf ../%{_lib}/%{name}-%{version}/bin/* .)


mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=GNU Prolog
Comment=%{Summary}
Exec=%{name}
Icon=interpreters_section
Terminal=true
Type=Application
Categories=Development;X-MandrivaLinux-MoreApplications-Development-Interpreters;
EOF

%files
%doc Examples* doc/html_node
%{_bindir}/*
%{_libdir}/%{name}*
%{_datadir}/applications/*

