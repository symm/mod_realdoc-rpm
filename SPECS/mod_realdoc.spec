%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo 0)}}

Name:           mod_realdoc
Version:        1.0
Release:        20140808git97808c%{?dist}
Summary:        Apache module to support atomic deploys

License:        MIT
URL:            https://github.com/etsy/mod_realdoc
Source0:        https://github.com/etsy/mod_realdoc/archive/397808c32f7c16d0f2a21cbdcb75523c70ff9931.zip
Source1:        mod_realdoc.conf

BuildRequires:  httpd-devel
Requires:       httpd
Requires:       httpd-mmn = %{_httpd_mmn}


%description
mod_realdoc is an Apache module which does a realpath on the docroot symlink and
sets the absolute path as the real document root for the remainder of the
request.

It executes as soon as Apache is finished reading the request from the client.

By resolving the configurer symlinked docroot directory to an absolute path at
the start of a request we can safely switch this symlink to point to another
directory on a deploy. Requests that started before the symlink change will
continue to execute on the previous symlink target and therefore will not be
vulnerable to deploy race conditions.


%prep
%setup -q -n %{name}-master


%build
apxs -Wc,"%{optflags}" -c mod_realdoc.c


%install
rm -rf $RPM_BUILD_ROOT
mkdir -pm 755 \
    $RPM_BUILD_ROOT%{_libdir}/httpd/modules \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -pm 755 .libs/mod_realdoc.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/


%files
%defattr(-,root,root,-)
%doc README.md LICENSE
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*
%{_libdir}/httpd/modules/*


%changelog
* Sat Oct 18 2014 Gareth Jones <me@gazj.co.uk> - 397808c32f7c16d0f2a21cbdcb75523c70ff9931-1
- Initial package
