#
# Conditional build:
%bcond_without	doc	# HTML and PDF documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Python 2 library for symbolic mathematics
Summary(pl.UTF-8):	Biblioteka Pythona 2 do matematyki symbolicznej
Name:		python-sympy
Version:	1.5.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sympy/
Source0:	https://files.pythonhosted.org/packages/source/s/sympy/sympy-%{version}.tar.gz
# Source0-md5:	b11b310c3e1642bf66e51038cb3c0021
Patch0:		%{name}-nodisplay.patch
URL:		https://www.sympy.org/
BuildRequires:	gettext
BuildRequires:	graphviz
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-devel-tools
BuildRequires:	python-mpmath >= 0.19
BuildRequires:	python-numpy
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-devel-tools
BuildRequires:	python3-mpmath >= 0.19
BuildRequires:	python3-numpy
%endif
%endif
%if %{with doc}
BuildRequires:	pydoc3
BuildRequires:	python3-matplotlib
BuildRequires:	python3-mpmath >= 0.19
BuildRequires:	python3-sphinx_math_dollar
BuildRequires:	sphinx-pdg-3
# for cmex/fmex9.pfb
BuildRequires:	texlive-fonts-other
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex
BuildRequires:	texlive-latex-ams
BuildRequires:	texlive-latex-pgf
%endif
Requires:	python-matplotlib
Requires:	python-modules >= 1:2.7
Requires:	python-pyglet
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SymPy aims to become a full-featured computer algebra system (CAS)
while keeping the code as simple as possible in order to be
comprehensible and easily extensible. SymPy is written entirely in
Python and does not require any external libraries.

%description -l pl.UTF-8
SymPy ma być w pełni funkcjonalnym systemem algebry komputerowej
(CAS), a jednocześnie mieć jak najprostszy, czytelny i łatwo
rozszerzalny kod. Jest pisany całkowicie w Pythonie i nie wymaga
żadnych zewnętrznych bibliotek.

%package -n python3-sympy
Summary:	Python 3 library for symbolic mathematics
Summary(pl.UTF-8):	Biblioteka Pythona 3 do matematyki symbolicznej
Group:		Libraries/Python
Requires:	python3-matplotlib
Requires:	python3-modules >= 1:3.5
Requires:	python3-pyglet

%description -n python3-sympy
SymPy aims to become a full-featured computer algebra system (CAS)
while keeping the code as simple as possible in order to be
comprehensible and easily extensible. SymPy is written entirely in
Python and does not require any external libraries.

%description -n python3-sympy -l pl.UTF-8
SymPy ma być w pełni funkcjonalnym systemem algebry komputerowej
(CAS), a jednocześnie mieć jak najprostszy, czytelny i łatwo
rozszerzalny kod. Jest pisany całkowicie w Pythonie i nie wymaga
żadnych zewnętrznych bibliotek.

%package doc
Summary:	Documentation for SymPy module
Summary(pl.UTF-8):	Dokumentacja do SymPy
Group:		Documentation

%description doc
HTML documentation for SymPy.

%description doc -l pl.UTF-8
Dokumentacja do SymPy w formacie HTML.

%prep
%setup -q -n sympy-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
pydir=$(pwd)/build-3/lib
cd doc
PYTHONPATH=$pydir \
%{__make} html \
	SPHINXBUILD=sphinx-build-3
%{__make} cheatsheet
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/isympy{,3}

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-sympy-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-sympy-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-sympy-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%if %{with python2}
%py_install

%py_postclean

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%attr(755,root,root) %{_bindir}/isympy
%{py_sitescriptdir}/isympy.py[co]
%{py_sitescriptdir}/sympy
%{py_sitescriptdir}/sympy-%{version}-*.egg-info
%{_mandir}/man1/isympy.1*
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-sympy
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%attr(755,root,root) %{_bindir}/isympy3
%{py3_sitescriptdir}/isympy.py
%{py3_sitescriptdir}/__pycache__/isympy.cpython-*.py[co]
%{py3_sitescriptdir}/sympy
%{py3_sitescriptdir}/sympy-%{version}-*.egg-info
%{_examplesdir}/python3-sympy-%{version}
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/_build/html/{_images,_static,modules,pics,special_topics,tutorial,*.html,*.js} doc/_build/cheatsheet/cheatsheet.pdf
%endif
