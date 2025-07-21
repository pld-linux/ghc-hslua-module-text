#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	hslua-module-text
Summary:	Lua module for text
Summary(pl.UTF-8):	Moduł Lua do tekstu
Name:		ghc-%{pkgname}
Version:	0.2.1
Release:	2
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/hslua-module-text
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	d1adac4b2fb77447a48baf1b011d053f
URL:		http://hackage.haskell.org/package/hslua-module-text
BuildRequires:	ghc >= 7.8.1
BuildRequires:	ghc-base >= 4.7
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.10.2
BuildRequires:	ghc-bytestring < 0.11
BuildRequires:	ghc-hslua >= 1.0.3
BuildRequires:	ghc-hslua < 1.2
BuildRequires:	ghc-text >= 1
BuildRequires:	ghc-text < 1.3
%if %{with prof}
BuildRequires:	ghc-prof >= 7.8.1
BuildRequires:	ghc-base-prof >= 4.7
BuildRequires:	ghc-bytestring-prof >= 0.10.2
BuildRequires:	ghc-hslua-prof >= 1.0.3
BuildRequires:	ghc-text-prof >= 1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4.7
Requires:	ghc-bytestring >= 0.10.2
Requires:	ghc-hslua >= 1.0.3
Requires:	ghc-text >= 1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
UTF-8 aware subset of Lua's string module.

%description -l pl.UTF-8
Obsługujący UTF-8 podzbiór modułu Lua string.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.7
Requires:	ghc-bytestring-prof >= 0.10.2
Requires:	ghc-hslua-prof >= 1.0.3
Requires:	ghc-text-prof >= 1

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build

runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc ChangeLog.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Module
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Module/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Module/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Foreign/Lua/Module/*.p_hi
%endif
