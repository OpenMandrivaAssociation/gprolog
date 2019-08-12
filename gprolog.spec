%define	Summary	GNU Prolog is a free implementation of Prolog
%define _disable_lto 1
%define _disable_rebuild_configure 1

Name:		gprolog
Summary:	%{Summary}

Version:	1.4.5
Release:	1
URL:		http://www.gprolog.org/
Source0:	http://gprolog.univ-paris1.fr/%{name}-%{version}.tar.gz
Source100:	%{name}.rpmlintrc
Patch1:		gprolog-1.4.4-test.patch
Group:		Development/Other
ExclusiveArch:	%{ix86} %{x86_64} amd64 ppc
License:	GPLv2

%description
GNU Prolog is a native Prolog compiler with constraint solving over finite
domains (FD) developed by Daniel Diaz. Latest information about GNU Prolog can
be found at http://www.gnu.org/software/prolog.
A lot of work has been devoted to the ISO compatibility. GNU Prolog is very
close to the ISO standard (http://www.logic-programming.org/prolog_std.html).


%prep
%setup -q
%patch1 -p1 -b .tst

%build

# fails with clang
export CC=gcc
export CXX=g++

cd src
CFLG="$(echo %{optflags} | sed -s "s/\-O2/-O1/g" \
     		    | sed -e "s/\-fomit-frame-pointer//")"

# Based on a gentoo ebuild (??)
CFLG="$CFLG -funsigned-char"
%configure	-with-c-flags="$CFLG -fno-unit-at-a-time" \
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
Name[ru]=Язык логического программирования Пролог
Comment=%{Summary}
Comment[ru]=Компилятор языка программирования Пролог
Exec=%{name}
Icon=interpreters_section
Terminal=true
Type=Application
Categories=Development;X-MandrivaLinux-MoreApplications-Development-Interpreters;
EOF


%files
%doc ChangeLog NEWS PROBLEMS README doc/html_node
%{_bindir}/*
%{_libdir}/%{name}*
%{_datadir}/applications/*
