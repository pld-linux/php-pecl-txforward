%define		php_name	php%{?php_suffix}
%define		modname	txforward
%define		status		stable
Summary:	%{modname} - Reverse Proxy (web accelerator) PHP compatibility layer
Name:		%{php_name}-pecl-%{modname}
Version:	1.0.7
Release:	6
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	46b80b0f8acfeda5364d8e0812e0a34f
URL:		http://pecl.php.net/package/txforward/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-txforward < 1.0.7-5
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

In PECL status of this extension is: %{status}.

%prep
%setup -q -c
mv %{modname}-%{version}/* .

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
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
