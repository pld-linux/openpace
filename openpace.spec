#
# Conditional build:
%bcond_without	static_libs	# static library
# bindings
%bcond_with	golang		# Go binding [only gccgo build is supported]
%bcond_without	java		# Java binding
%bcond_without	python		# Python binding
%bcond_without	ruby		# Ruby binding
#
Summary:	Cryptographic library for EAC version 2
Summary(pl.UTF-8):	Biblioteka kryptograficzna do EAC v2
Name:		openpace
Version:	1.1.2
Release:	2
License:	GPL v3+
Group:		Libraries
#Source0Download: https://github.com/frankmorgner/openpace/releases
Source0:	https://github.com/frankmorgner/openpace/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	55f22686b89026fd40f60358cc2247d0
Patch0:		%{name}-optflags.patch
Patch1:		%{name}-ruby.patch
Patch2:		build.patch
URL:		https://frankmorgner.github.io/openpace/
BuildRequires:	autoconf >= 2.67
BuildRequires:	automake
BuildRequires:	doxygen
%{?with_golang:BuildRequires:	gcc-go}
BuildRequires:	gengetopt
BuildRequires:	help2man
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 1.0.2
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python-devel >= 2}
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	sphinx-pdg
BuildRequires:	swig
%{?with_python:BuildRequires:	swig-python}
%{?with_ruby:BuildRequires:	swig-ruby}
Requires:	openssl >= 1.0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cryptographic library for EAC version 2.

%description -l pl.UTF-8
Biblioteka kryptograficzna do EAC v2.

%package devel
Summary:	Header files for OpenPACE library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenPACE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel >= 1.0.2

%description devel
Header files for OpenPACE library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenPACE.

%package static
Summary:	Static OpenPACE library
Summary(pl.UTF-8):	Statyczna biblioteka OpenPACE
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenPACE library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenPACE.

%package apidocs
Summary:	API documentation for OpenPACE library
Summary(pl.UTF-8):	Dokumentacja API biblioteki OpenPACE
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for OpenPACE library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki OpenPACE.

%package -n golang-openpace
Summary:	Go language binding for OpenPACE library
Summary(pl.UTF-8):	Wiązania języka Go do biblioteki OpenPACE
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n golang-openpace
Go language binding for OpenPACE library.

%description -n golang-openpace -l pl.UTF-8
Wiązania języka Go do biblioteki OpenPACE.

%package -n java-openpace
Summary:	Java binding for OpenPACE library
Summary(pl.UTF-8):	Wiązania Javy do biblioteki OpenPACE
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}
Requires:	jre

%description -n java-openpace
Java binding for OpenPACE library.

%description -n java-openpace -l pl.UTF-8
Wiązania Javy do biblioteki OpenPACE.

%package -n python-openpace
Summary:	Python binding for OpenPACE library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki OpenPACE
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-modules

%description -n python-openpace
Python binding for OpenPACE library.

%description -n python-openpace -l pl.UTF-8
Wiązania Pythona do biblioteki OpenPACE.

%package -n ruby-openpace
Summary:	Ruby binding for OpenPACE library
Summary(pl.UTF-8):	Wiązania języka Ruby do biblioteki OpenPACE
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	ruby

%description -n ruby-openpace
Ruby binding for OpenPACE library.

%description -n ruby-openpace -l pl.UTF-8
Wiązania języka Ruby do biblioteki OpenPACE.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# outdated versions
%{__rm} -r docs/_static/{bootstrap-2.3.2,bootswatch-2.3.2}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PYTHON=%{__python} \
	JAVAC=javac \
	%{?with_golang:--enable-go} \
	%{?with_java:--enable-java} \
	%{?with_python:--enable-python} \
	%{?with_ruby:--enable-ruby} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make} -j 1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# junk
%{__rm} $RPM_BUILD_ROOT%{_bindir}/example
%{__rm} docs/_static/Makefile*
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*eac.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/openpace

%if %{with python}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cvc-create
%attr(755,root,root) %{_bindir}/cvc-print
%attr(755,root,root) %{_bindir}/eactest
%attr(755,root,root) %{_libdir}/libeac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeac.so.3
%dir %{_sysconfdir}/eac
%dir %{_sysconfdir}/eac/cvc
%{_sysconfdir}/eac/cvc/DECVC*
%dir %{_sysconfdir}/eac/x509
%{_sysconfdir}/eac/x509/*
%{_mandir}/man1/cvc-create.1*
%{_mandir}/man1/cvc-print.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeac.so
%{_includedir}/eac
%{_pkgconfigdir}/libeac.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeac.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc docs/{_static,*.html,*.js}

%if %{with golang}
%files -n golang-openpace
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgeac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgeac.so.0
%attr(755,root,root) %{_libdir}/libgeac.so
%endif

%if %{with java}
%files -n java-openpace
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjeac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjeac.so.0
%attr(755,root,root) %{_libdir}/libjeac.so
%dir %{_datadir}/openpace
%{_datadir}/openpace/java
%endif

%if %{with python}
%files -n python-openpace
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cvc_rehash
%attr(755,root,root) %{py_sitedir}/_eac.so
%{py_sitedir}/chat.py[co]
%{py_sitedir}/eac.py[co]
%{py_sitedir}/pace_entity.py[co]
%{py_sitedir}/OpenPACE-%{version}-py*.egg-info
%endif

%if %{with ruby}
%files -n ruby-openpace
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/eac.so
%endif
