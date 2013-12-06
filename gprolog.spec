%define	name	gprolog
%define	version	1.4.0
%define release	5
%define	Summary	GNU Prolog is a free implementation of Prolog

Name:		%{name}
Summary:	%{Summary}
Version:	%{version}
Release:	%{release}
URL:		http://www.gprolog.org/
Source0:	http://www.gprolog.org/%{name}-%{version}.tar.gz
Patch1:		gprolog-1.4.0-test.patch
Group:		Development/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
ExclusiveArch:	%{ix86} x86_64 amd64 ppc
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
cd src
CFLG="$(echo %{optflags} | sed -s "s/\-O2/-O1/g" \
     		    | sed -e "s/\-fomit-frame-pointer//")"

# Based on a gentoo ebuild (??)
CFLG="$CFLG -funsigned-char"
%configure2_5x	-with-c-flags="$CFLG -fno-unit-at-a-time" \
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
rm -rf $RPM_BUILD_ROOT
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

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post 
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files
%defattr(-,root,root)
%doc ChangeLog NEWS PROBLEMS README doc/html_node
%{_bindir}/*
%{_libdir}/%{name}*
%{_datadir}/applications/*


%changelog
* Mon Oct 31 2011 Sergey Zhemoitel <serg@mandriva.org> 1.4.0-1mdv2012.0
+ Revision: 707993
- new version 1.4.0
- add russian comment

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-2mdv2011.0
+ Revision: 605497
- rebuild

  + Sandro Cazzaniga <kharec@mandriva.org>
    - patch send upstream, not release.

* Fri Mar 05 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.3.1-1mdv2010.1
+ Revision: 514797
- fix Source to use tar.gz
- drop old patches (applied upstream)
- add a patch for fix str fmt in 1.3.1
- update to 1.3.1
- fix license

* Mon Oct 05 2009 Funda Wang <fwang@mandriva.org> 1.3.0-4mdv2010.0
+ Revision: 453832
- fix test
- fix stf fmt
- rediff noexecstack patch
- bunzip2 patches

* Tue Dec 09 2008 Adam Williamson <awilliamson@mandriva.org> 1.3.0-3mdv2009.1
+ Revision: 312144
- rebuild
- disable parallel build (it breaks)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sat Jan 12 2008 Thierry Vignaud <tv@mandriva.org> 1.3.0-2mdv2008.1
+ Revision: 150233
- rebuild
- drop old menu
- kill re-definition of %%buildroot on Pixel's request
- kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri May 18 2007 Pixel <pixel@mandriva.com> 1.3.0-1mdv2008.0
+ Revision: 27816
- new release, 1.3.0
- drop patch0 (gcc4) hopefully not needed anymore
- drop patch3 (test) applied upstream
- Import gprolog



* Thu Aug 24 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1.2.19-4mdv2007.0
- fix usage of summary macro in menu item
- move check to new %%check stage
- fix macro-in-%%changelog
- cosmetics

* Fri Jul  7 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.2.19-3mdv2007.0
- make check in build
- build with optimisations

* Fri Jul  7 2006 Pixel <pixel@mandriva.com> 1.2.19-2mdv2007.0
- switch to XDG menu

* Mon May 29 2006 Pascal Terjan <pterjan@mandriva.org> 1.2.19-1mdv2007.0
- use unstable version 1.2.19
- mkrel
- add gentoo patches (P1,2,3,4)
- drop patch0
- disable gcc4 optims until I find the breaking ones
- install into the right places

* Wed Aug  6 2003 Pixel <pixel@mandrakesoft.com> 1.2.16-5mdk
- fix url, description (thanks to John Keller)

* Tue Aug  5 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.16-4mdk
- Handle amd64 as arch

* Tue Dec 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.16-3mdk
- Enable build on PPC, it should work there too.
- Update Patch0 (x86-64) to what Daniel Diaz committed upstream. Simply
  reformatting tweeks but make sure latest code still works.

* Mon Dec 16 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.16-2mdk
- Update Patch0 (x86-64) to preserve callee-saved register %%rbx

* Mon Dec  9 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.16-1mdk
- 1.2.16
- Update Patch0 (x86_64): handle 64-bit integers though I don't think
  this could occur, define M_MMAP_HIGH_ADR, define global registers

* Sat Dec  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.13-2mdk
- Patch0: Add initial support for x86-64. There may be some clean-ups,
  optimizations and fixlets to do though.

* Thu Jun 27 2002 Pixel <pixel@mandrakesoft.com> 1.2.13-1mdk
- new release

* Wed Jan 09 2002 David BAUDENS <baudens@mandrakesoft.com> 1.2.8-2mdk
- Use standard interpreters_section.png icon

* Mon Oct 22 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.2.8-1mdk
- 1.2.8

* Wed Aug 29 2001 David BAUDENS <baudens@mandrakesoft.com> 1.2.1-8mdk
- Use new icon

* Thu Jul 26 2001 Pixel <pixel@mandrakesoft.com> 1.2.1-7mdk
- rebuild

* Tue Dec 26 2000 Pixel <pixel@mandrakesoft.com> 1.2.1-6mdk
- removed ppc from exclusivearch 

* Mon Dec  4 2000 Pixel <pixel@mandrakesoft.com> 1.2.1-5mdk
- ensure optflags are used

* Tue Nov  7 2000 Pixel <pixel@mandrakesoft.com> 1.2.1-4mdk
- change menu title
- icons the way I want :p

* Mon Oct 09 2000 Daouda Lo <daouda@mandrakesoft.com> 1.2.1-3mdk
- icons
- embedded menu
 
* Wed Aug 23 2000 Pixel <pixel@mandrakesoft.com> 1.2.1-2mdk
- add packager field

* Mon Jul 31 2000 Pixel <pixel@mandrakesoft.com> 1.2.1-1mdk
- new version

* Sun Jul 30 2000 Pixel <pixel@mandrakesoft.com> 1.2-1mdk
- new version

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 1.1.2-4mdk
- macroization
- BM

* Tue May 16 2000 Pixel <pixel@mandrakesoft.com> 1.1.2-3mdk
- add exclusivearch

* Fri Mar 31 2000 Pixel <pixel@mandrakesoft.com> 1.1.2-2mdk
- cleanup, add menu, new group

* Wed Dec 01 1999 Lenny Cartier <lenny@mandrakesoft.com>
- initial specfile
- added %%doc
- added symlinks in /usr/bin
- enable mdk CFLAGS
- ...things to satisfy Mr Pixel
