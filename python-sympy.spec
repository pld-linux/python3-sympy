#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	A Python library for symbolic mathematics
Name:		python-sympy
Version:	0.7.4
Release:	6
License:	BSD
Group:		Libraries/Python
Source0:	https://github.com/sympy/sympy/releases/download/sympy-%{version}/sympy-%{version}.tar.gz
# Source0-md5:	12432b35af31b31864a10993710f61a6
# Upstream tried to graft in another project as a private copy; we rip
# it out (rhbz# 551576):
Patch0:		strip-internal-mpmath.patch
Patch1:		sympy-doc.patch
URL:		http://sympy.org/
BuildRequires:	gettext
BuildRequires:	graphviz
%if %{with python2}
BuildRequires:	python-Sphinx
BuildRequires:	python-devel
BuildRequires:	python-mpmath
BuildRequires:	python-numpy
%endif
%if %{with python3}
BuildRequires:	python3-Sphinx
BuildRequires:	python3-devel
BuildRequires:	python3-devel-tools
BuildRequires:	python3-mpmath
BuildRequires:	python3-numpy
%endif
BuildRequires:	texlive-latex
BuildRequires:	texlive-latex-pgf
Requires:	python-matplotlib
Requires:	python-mpmath
Requires:	python-pyglet
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SymPy aims to become a full-featured computer algebra system (CAS)
while keeping the code as simple as possible in order to be
comprehensible and easily extensible. SymPy is written entirely in
Python and does not require any external libraries.

%package -n python3-sympy
Summary:	A Python3 library for symbolic mathematics
Group:		Libraries/Python
Requires:	python3-matplotlib
Requires:	python3-mpmath
Requires:	python3-pyglet

%description -n python3-sympy
SymPy aims to become a full-featured computer algebra system (CAS)
while keeping the code as simple as possible in order to be
comprehensible and easily extensible. SymPy is written entirely in
Python and does not require any external libraries.

%package doc
Summary:	Documentation for sympy
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description doc
HTML documentation for sympy.

%prep
%setup -q -n sympy-%{version}
%patch0
%patch1 -p1
%{__rm} -rf sympy/mpmath doc/src/modules/mpmath

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

# Build the documentation
cd doc
%{__make} html
%{__make} cheatsheet

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_bindir}/isympy{,3}

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-sympy-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-sympy-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-sympy-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE PKG-INFO doc/_build/cheatsheet/cheatsheet.pdf
%attr(755,root,root) %{_bindir}/isympy
%{py_sitescriptdir}/sympy
%{py_sitescriptdir}/sympy-%{version}-*.egg-info
%{_mandir}/man1/isympy.1*
%{_examplesdir}/%{name}-%{version}

%files -n python3-sympy
%defattr(644,root,root,755)
%doc AUTHORS LICENSE PKG-INFO doc/_build/cheatsheet/cheatsheet.pdf
%attr(755,root,root) %{_bindir}/isympy3
%{py3_sitescriptdir}/sympy
%{py3_sitescriptdir}/sympy-%{version}-*.egg-info
%{_examplesdir}/python3-sympy-%{version}

%files doc
%defattr(644,root,root,755)
%doc doc/_build/html/*
