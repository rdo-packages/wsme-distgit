# Created by pyp2rpm-1.0.1

%if 0%{?fedora}
%global with_python3 1
# FIXME(ykarel) Disable tests in fedora as upstream has upperbound for sqlalchemy
# set to 0.7.99, while we have > 1.2.5, in centos we are not hitting this currently
# because tests are not running(because setuptools is 22.0.5), after updating it
# we will hit in centos as well.
%global with_tests 0
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

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

%package -n python2-%{lpypi_name}
Summary:        Web Services Made Easy
%{?python_provide:%python_provide python2-%{lpypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
BuildRequires:  python2-six
BuildRequires:  python-webob
BuildRequires:  python2-netaddr
BuildRequires:  python2-pytz
BuildRequires:  python-webtest
BuildRequires:  python-simplegeneric

Requires:       python-simplegeneric
Requires:       python2-six
Requires:       python-webob
Requires:       python2-netaddr
Requires:       python2-pytz

%description -n python2-%{lpypi_name}
Web Services Made Easy, simplifies the implementation of
multiple protocol REST web services by providing simple yet
powerful typing which removes the need to directly
manipulate the request and the response objects.

%if 0%{?with_python3}
%package -n python3-%{lpypi_name}
Summary:        Web Services Made Easy
%{?python_provide:%python_provide python3-%{lpypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-six
BuildRequires:  python3-webob
BuildRequires:  python3-pytz
BuildRequires:  python3-simplegeneric
BuildRequires:  python3-netaddr

Requires:       python3-simplegeneric
Requires:       python3-six
Requires:       python3-webob
Requires:       python3-netaddr
Requires:       python3-pytz

%description -n python3-%{lpypi_name}
Web Services Made Easy, simplifies the implementation of
multiple protocol REST web services by providing simple yet
powerful typing which removes the need to directly
manipulate the request and the response objects.
%endif

%prep
%setup -q -n %{pypi_name}-%{upstream_version}

%build
%{__python2} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif

%if 0%{?with_tests}
%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif
%endif

%files -n python2-%{lpypi_name}
%doc README.rst examples/
%license LICENSE
%{python2_sitelib}/wsme
%{python2_sitelib}/wsmeext
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/*.pth

%if 0%{?with_python3}
%files -n python3-%{lpypi_name}
%doc README.rst examples/
%license LICENSE
%{python3_sitelib}/wsme
%{python3_sitelib}/wsmeext
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/*.pth
%endif

%changelog
* Thu Aug 16 2018 RDO <dev@lists.rdoproject.org> 0.9.3-1
- Update to 0.9.3

