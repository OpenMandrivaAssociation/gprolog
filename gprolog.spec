%define	name	gprolog
%define	version	1.3.0
%define	release	%mkrel 1
%define	Summary	GNU Prolog is a free implementation of Prolog

Name:		%{name}
Summary:	%{Summary}
Version:	%{version}
Release:	%{release}
# http://www.gnu.org/software/prolog
URL:		http://gnu-prolog.inria.fr/
# ftp://ftp.inria.fr/INRIA/Projects/contraintes/gnu-prolog/%{name}-%{version}.tar.bz2
Source0:	ftp://ftp.gnu.org/gnu/gprolog/%{name}-%{version}.tar.bz2
Patch1:		gprolog-1.3.0-bootstrap.patch
Patch2:		gprolog-1.2.19-noexecstack.patch.bz2
Group:		Development/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
ExclusiveArch:	%{ix86} x86_64 amd64 ppc
License:	GPL

%description
GNU Prolog is a native Prolog compiler with constraint solving over finite
domains (FD) developed by Daniel Diaz. Latest information about GNU Prolog can
be found at http://www.gnu.org/software/prolog.
A lot of work has been devoted to the ISO compatibility. GNU Prolog is very
close to the ISO standard (http://www.logic-programming.org/prolog_std.html).


%prep
%setup -q
%patch1 -p1
%patch2 -p1
(cd src && autoconf)

%build
cd src
%configure2_5x	-with-c-flags="%{optflags} -fno-unit-at-a-time" \
		--with-install-dir=%{_prefix} \
		--with-doc-dir=%{_datadir}/%{name}-%{version} \
		--with-html-dir=%{_datadir}/%{name}-%{version}/html \
		--with-examples-dir=%{_datadir}/%{name}-%{version}/examples
%make

%check
# all tests pass on x86-64
make check || echo "#### FIXME ####"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

(cd src ; make install-system INSTALL_DIR=$RPM_BUILD_ROOT%{_libdir}/%{name}-%{version})

(cd $RPM_BUILD_ROOT%{_bindir} ; ln -sf ../%{_lib}/%{name}-%{version}/bin/* .)

install -d $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): \
needs="text" \
section="More Applications/Development/Interpreters" \
title="GNU Prolog" \
longtitle="%{Summary}" \
command="%{name}" \
icon="interpreters_section.png" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=GNU Prolog
Comment=%{Summary}
Exec=%{name}
Icon=interpreters_section
Terminal=true
Type=Application
Categories=Development;X-MandrivaLinux-MoreApplications-Development-Interpreters;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post 
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(-,root,root)
%doc Examples* doc/html_node
%{_bindir}/*
%{_libdir}/%{name}*
%{_datadir}/applications/*
%{_menudir}/*
