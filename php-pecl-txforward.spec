%define		_modname	txforward
%define		_status		stable
Summary:	%{_modname} - Reverse Proxy (web accelerator) PHP compatibility layer
#Summary(pl.UTF-8):	%{_modname} -
Name:		php-pecl-%{_modname}
Version:	1.0.7
Release:	3
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	46b80b0f8acfeda5364d8e0812e0a34f
URL:		http://pecl.php.net/package/txforward/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Makes reverse-proxing (web accelerator) totally invisible for php
applications. Doesn't require php code modifications to handle
X-Forwarded-For IP.
- Stills allows proxy-aware applications to work with X-Forwarded
  headers and proxy IP address.
- Should work with any web server
- Should work with any proxy server

Using this extension with on a non reverse proxied system will result
in a security issue.

In PECL status of this extension is: %{_status}.

%prep
%setup -q -c
mv %{_modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
