%if !( 0%{?rhel} > 0 && 0%{?rhel} <= 7)
# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%endif


Name:           liblouis
Version:        2.5.2
Release:        11%{?dist}
Summary:        Braille translation and back-translation library

Group:          System Environment/Libraries
License:        LGPLv3+
URL:            http://www.abilitiessoft.com/
Source0:        http://liblouis.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         security-fixes.patch

BuildRequires:  help2man
BuildRequires:  texinfo-tex
BuildRequires:  python2-devel

%if !( 0%{?rhel} > 0 && 0%{?rhel} <= 7)
BuildRequires:  python3-devel
%endif

Requires(post): info
Requires(preun): info

# gnulib is a copylib that has been granted an exception from the no-bundled-libraries policy
# http://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Copylibs
Provides: bundled(gnulib) = 20091111

%description
Liblouis is an open-source braille translator and back-translator. It features
support for computer and literary braille, supports contracted and uncontracted
translation for many, many languages and has support for hyphenation. 
New languages can easily be added through tables that support a rule- or 
dictionary based approach. Liblouis also supports math braille 
(Nemeth and Marburg).

Liblouis is based on the translation routines in the BRLTTY screenreader for 
Linux. It has, however, gone far beyond these routines. 
The library is named in honor of Louis Braille.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        utils
Summary:        Command-line utilities to test %{name}
Group:          Applications/Text
Requires:       %{name}%{?_isa} = %{version}-%{release}
License:        GPLv3+

%description    utils
Five test programs are provided as part of the liblouis package. They
are intended for testing liblouis and for debugging tables. None of
them is suitable for braille transcription.

%package python
Summary:        Python 2 language bindings for %{name}
Group:          Development/Languages
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description python
This package provides Python 2 language bindings for %{name}.


%if !( 0%{?rhel} > 0 && 0%{?rhel} <= 7)
%package python3
Summary:        Python 3 language bindings for %{name}
Group:          Development/Languages
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description python3
This package provides Python 3 language bindings for %{name}.
%endif


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
This package provides the documentation for liblouis.


%prep
%setup -q
%patch0 -p1


%build
%configure --disable-static --enable-ucs4
make %{?_smp_mflags}
make -C doc %{name}.pdf

# Don't run the tests as they haven't been adapted to the current release yet.
#%check
#make check


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_infodir}/dir
rm -f %{buildroot}/%{_libdir}/%{name}.la
rm -rf %{buildroot}/%{_defaultdocdir}/%{name}/
cd python/louis

install -d %{buildroot}%{python_sitelib}/louis
install -pm 0644 __init__.py %{buildroot}%{python_sitelib}/louis/

%if !( 0%{?rhel} > 0 && 0%{?rhel} <= 7)
%py_byte_compile %{__python} %{buildroot}%{python_sitelib}/louis/

install -d %{buildroot}%{python3_sitelib}/louis
install -pm 0644 __init__.py %{buildroot}%{python3_sitelib}/louis/
%py_byte_compile %{__python3} %{buildroot}%{python3_sitelib}/louis/
%endif

sed -i '1s|^#!/usr/bin/env python|#!%{__python}|' $RPM_BUILD_ROOT%{_bindir}/lou_harnessGenerator


%clean
rm -rf %{buildroot}


%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :


%postun -p /sbin/ldconfig


%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi


%files
%defattr(-,root,root,-)
%doc README COPYING.LIB AUTHORS NEWS ChangeLog TODO
%{_libdir}/%{name}.so.*
%{_datadir}/%{name}/
%{_infodir}/%{name}.info*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

%files utils
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/lou_*
%{_mandir}/man1/lou_*.1*

%files python
%defattr(-,root,root,-)
%doc python/README
%{python_sitelib}/louis/

%if !( 0%{?rhel} > 0 && 0%{?rhel} <= 7)
%files python3
%defattr(-,root,root,-)
%{python3_sitelib}/louis/
%endif

%files doc
%doc doc/%{name}.{html,txt,pdf}


%changelog
* Fri Sep 15 2017 Rui Matos <rmatos@redhat.com> - 2.5.2-11
- Resolves: CVE-2017-13738, CVE-2017-13740, CVE-2017-13741,
  CVE-2017-13742, CVE-2017-13743, CVE-2017-13744, CVE-2014-8184

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.5.2-10
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.5.2-9
- Mass rebuild 2013-12-27

* Wed Nov  6 2013 Rui Matos <rmatos@redhat.com> - 2.5.2-8
- Resolves: rhbz#987026 - liblouis - shebang with /usr/bin/env

* Thu Jul 18 2013 Matthias Clasen <mclasen@redhat.com> - 2.5.2-7
- Tighten dependencies between subpackages (pointed out by rpmdiff)

* Tue Apr 16 2013 Martin Gieseking <martin.gieseking@uos.de> 2.5.2-6
- Restrict exclusion of Python 3 packages to RHEL <= 7.

* Mon Apr 15 2013 Martin Gieseking <martin.gieseking@uos.de> 2.5.2-5
- Restrict exclusion of Python 3 packages to RHEL < 7.

* Mon Apr 15 2013 Rui Matos <rmatos@redhat.com> - 2.5.2-4
- Don't depend on python3 in RHEL.

* Tue Feb 26 2013 Martin Gieseking <martin.gieseking@uos.de> 2.5.2-3
- Added Python 3 language bindings.

* Fri Feb 22 2013 Martin Gieseking <martin.gieseking@uos.de> 2.5.2-2
- Moved documentation to doc subpackage.

* Wed Feb 06 2013 Martin Gieseking <martin.gieseking@uos.de> 2.5.2-1
- Updated to new upstream release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Martin Gieseking <martin.gieseking@uos.de> 2.4.1-1
- Updated to upstream release 2.4.1.
- Made the devel package's dependency on the base package arch specific.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Martin Gieseking <martin.gieseking@uos.de> 2.4.0-1
- Updated to upstream release 2.4.0.

* Fri May 20 2011 Martin Gieseking <martin.gieseking@uos.de> 2.3.0-1
- Updated to upstream release 2.3.0.

* Mon Feb 28 2011 Martin Gieseking <martin.gieseking@uos.de> - 2.2.0-2
- Added release date of bundled gnulib to Provides.
- Use %%{name} macro consistently.

* Tue Feb 15 2011 Martin Gieseking <martin.gieseking@uos.de> - 2.2.0-1
- Updated to upstream release 2.2.0.
- Added Python bindings.

* Mon Jul 5 2010 Lars Bjørndal <lars.bjorndal@broadpark.no> - 1.9.0-2
- In advice from Martin Gieseking: Removed some garbage from the file section, and added a PDF version of the liblouis documentation. See <https://bugzilla.redhat.com/show_bug.cgi?id=597597>.

* Wed Jun 30 2010 Lars Bjørndal <lars.bjorndal@broadpark.no> - 1.9.0-1
- A new version was up to day. At the same time, fixed a minor spec issue according to a comment from Martin Gieseking, see <https://bugzilla.redhat.com/show_bug.cgi?id=597597>.

* Sun Jun 20 2010 Lars Bjørndal <lars.bjorndal@broadpark.no> - 1.8.0-3
- Fixed some small problems, among them wrong destination directory for documentation. See <https://bugzilla.redhat.com/show_bug.cgi?id=597597> for further details.

* Thu Jun 17 2010 Lars Bjørndal <lars.bjorndal@broadpark.no> 1.8.0-2
- Created the tools sub package and did a lot of clean ups, see <https://bugzilla.redhat.com/show_bug.cgi?id=597597>.

* Sat May 29 2010 Lars Bjørndal <lars.bjorndal@broadpark.no> 1.8.0-1
- Create the RPM for Fedora.
