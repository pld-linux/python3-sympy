#
# Conditional build:
%bcond_without	doc	# HTML and PDF documentation
%bcond_without	tests	# unit tests

Summary:	Python 3 library for symbolic mathematics
Summary(pl.UTF-8):	Biblioteka Pythona 3 do matematyki symbolicznej
Name:		python3-sympy
Version:	1.14.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sympy/
Source0:	https://files.pythonhosted.org/packages/source/s/sympy/sympy-%{version}.tar.gz
# Source0-md5:	9872deb5bd7816dfbc89bec086b9e522
Patch0:		docs-build.patch
URL:		https://www.sympy.org/
BuildRequires:	gettext
BuildRequires:	graphviz
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-devel-tools
BuildRequires:	python3-mpmath >= 0.19
BuildRequires:	python3-numpy
%endif
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	fonts-TTF-DejaVu
BuildRequires:	pydoc3
BuildRequires:	python3-furo
BuildRequires:	python3-intersphinx_registry
BuildRequires:	python3-linkify-it-py
BuildRequires:	python3-matplotlib
BuildRequires:	python3-mpmath >= 0.19
BuildRequires:	python3-myst_parser
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinx_math_dollar >= 1.2.1
BuildRequires:	python3-sphinx_reredirects
BuildRequires:	sphinx-pdg-3
# for cmex/fmex9.pfb
BuildRequires:	texlive-fonts-other
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex
BuildRequires:	texlive-latex-ams
BuildRequires:	texlive-latex-pgf
%endif
Requires:	python3-matplotlib
Requires:	python3-modules >= 1:3.8
Requires:	python3-pyglet
Conflicts:	python-sympy < 1.5.1-2
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

%package doc
Summary:	Documentation for SymPy module
Summary(pl.UTF-8):	Dokumentacja do SymPy
Group:		Documentation
Obsoletes:	python-sympy-doc = 1.7.1

%description doc
HTML documentation for SymPy.

%description doc -l pl.UTF-8
Dokumentacja do SymPy w formacie HTML.

%prep
%setup -q -n sympy-%{version}
%patch -P 0 -p1

%build
# some tests (for example such that require GUI) are not run on their CI systems, so use that
export CI=true
%py3_build %{?with_tests:test}

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

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/isympy{,3}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md
%attr(755,root,root) %{_bindir}/isympy3
%{py3_sitescriptdir}/isympy.py
%{py3_sitescriptdir}/__pycache__/isympy.cpython-*.py[co]
%{py3_sitescriptdir}/sympy
%{py3_sitescriptdir}/sympy-%{version}-*.egg-info
%{_mandir}/man1/isympy.1*

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/_build/html/{_images,_static,modules,pics,special_topics,tutorial,*.html,*.js} doc/_build/cheatsheet/cheatsheet.pdf
%endif
