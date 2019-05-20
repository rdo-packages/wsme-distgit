# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

# FIXME(ykarel) Disable tests in fedora as upstream has upperbound for sqlalchemy
# set to 0.7.99, while we have > 1.2.5, in centos we are not hitting this currently
# because tests are not running(because setuptools is 22.0.5), after updating it
# we will hit in centos as well.
%global with_tests 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name WSME
%global lpypi_name wsme

Name:           python-%{lpypi_name}
Version:        0.9.3
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

%package -n python%{pyver}-%{lpypi_name}
Summary:        Web Services Made Easy
%{?python_provide:%python_provide python2-%{lpypi_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-six
BuildRequires:  python%{pyver}-webob
BuildRequires:  python%{pyver}-netaddr
BuildRequires:  python%{pyver}-pytz

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-webtest
BuildRequires:  python-simplegeneric
%else
BuildRequires:  python%{pyver}-webtest
BuildRequires:  python%{pyver}-simplegeneric
%endif

Requires:       python%{pyver}-six
Requires:       python%{pyver}-webob
Requires:       python%{pyver}-netaddr
Requires:       python%{pyver}-pytz
# Handle python2 exception
%if %{pyver} == 2
Requires:       python-simplegeneric
%else
Requires:       python%{pyver}-simplegeneric
%endif

%description -n python%{pyver}-%{lpypi_name}
Web Services Made Easy, simplifies the implementation of
multiple protocol REST web services by providing simple yet
powerful typing which removes the need to directly
manipulate the request and the response objects.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

%build
%{pyver_build}

%install
%{pyver_install}

%if 0%{?with_tests}
%check
%{pyver_bin} setup.py test
%endif

%files -n python%{pyver}-%{lpypi_name}
%doc README.rst examples/
%license LICENSE
%{pyver_sitelib}/wsme
%{pyver_sitelib}/wsmeext
%{pyver_sitelib}/*.egg-info
%{pyver_sitelib}/*.pth

%changelog
* Sun Jul 15 2018 Jon Schlueter <jschluet@redhat.com> 0.9.3-1
- Update to 0.9.3
