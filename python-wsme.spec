
# FIXME(ykarel) Disable tests in fedora as upstream has upperbound for sqlalchemy
# set to 0.7.99, while we have > 1.2.5, in centos we are not hitting this currently
# because tests are not running(because setuptools is 22.0.5), after updating it
# we will hit in centos as well.
%global with_tests 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name WSME
%global lpypi_name wsme

Name:           python-%{lpypi_name}
Version:        XXX
Release:        XXX
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
%{?python_provide:%python_provide python2-%{lpypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-six
BuildRequires:  python3-webob
BuildRequires:  python3-netaddr
BuildRequires:  python3-pytz

BuildRequires:  python3-webtest
BuildRequires:  python3-simplegeneric

Requires:       python3-six
Requires:       python3-webob
Requires:       python3-netaddr
Requires:       python3-pytz
Requires:       python3-simplegeneric

%description -n python3-%{lpypi_name}
Web Services Made Easy, simplifies the implementation of
multiple protocol REST web services by providing simple yet
powerful typing which removes the need to directly
manipulate the request and the response objects.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

%build
%{py3_build}

%install
%{py3_install}

%if 0%{?with_tests}
%check
python3 setup.py test
%endif

%files -n python3-%{lpypi_name}
%doc README.rst examples/
%license LICENSE
%{python3_sitelib}/wsme
%{python3_sitelib}/wsmeext
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/*.pth

%changelog
