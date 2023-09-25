
# FIXME(ykarel) Disable tests in fedora as upstream has upperbound for sqlalchemy
# set to 0.7.99, while we have > 1.2.5, in centos we are not hitting this currently
# because tests are not running(because setuptools is 22.0.5), after updating it
# we will hit in centos as well.
%global with_tests 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order transaction sphinx

%global pypi_name WSME
%global lpypi_name wsme

Name:           python-%{lpypi_name}
Version:        0.12.1
Release:        1%{?dist}
Summary:        Web Services Made Easy

License:        MIT
URL:            https://pypi.python.org/pypi/WSME
Source0:        https://pypi.python.org/packages/source/W/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
Web Services Made Easy, simplifies the implementation of
multiple protocol REST web services by providing simple yet
powerful typing which removes the need to directly
manipulate the request and the response objects.

%package -n python3-%{lpypi_name}
Summary:        Web Services Made Easy

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description -n python3-%{lpypi_name}
Web Services Made Easy, simplifies the implementation of
multiple protocol REST web services by providing simple yet
powerful typing which removes the need to directly
manipulate the request and the response objects.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
# We have to tell tox to use coverage and nosetests binary from package
# instead of tox binary directory defined explicitly.
sed -i 's|{envbindir}|/usr/bin|g' tox.ini
# We don't care testing the integration in Sphinxfor making clean documentation 
# with wsmeext.sphinxext so let's remove it to avoid pulling Sphinx.
sed -i 's|tests/test_sphinxext.py ||' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_tests}
%check
# test_default_transaction is importing transaction module which is 
# not yet packaged, so we need to ignore it for now.
%tox -e %{default_toxenv} -- -- -e 'test_default_transaction'
%endif

%files -n python3-%{lpypi_name}
%doc README.rst examples/
%license LICENSE
%{python3_sitelib}/wsme
%{python3_sitelib}/wsmeext
%{python3_sitelib}/*.dist-info
%{python3_sitelib}/*.pth

%changelog
* Mon Sep 25 2023 RDO <dev@lists.rdoproject.org> 0.12.1-1
- Update to 0.12.1

