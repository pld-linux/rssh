Summary:	A restricted shell for assigning scp- or sftp-only access
Summary(pl):	Okrojona pow³oka daj±ca dostêp tylko do scp i sftp
Name:		rssh
Version:	2.0.0
Release:	1
License:	BSD-like
Group:		Applications/Shells
Source0:	http://www.pizzashack.org/rssh/src/%{name}-%{version}.tar.gz
Patch0:		%{name}-userbuild.patch
URL:		http://www.pizzashack.org/rssh/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssh-clients >= 3.5p1
Requires:	openssh-server >= 3.5p1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin

%description
rssh is a small shell that provides the ability for system
administrators to give specific users access to a given system via scp
or sftp only.

%description -l pl
rssh jest ma³ym shellem, który pozwala administratorowi ograniczyæ
dostêp na danym koncie tylko do scp i/lub sftp.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--with-scp=/usr/bin/scp \
	--with-sftp-server=/usr/lib/openssh/sftp-server

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

ln -sf rssh $RPM_BUILD_ROOT/bin/scpsh
ln -sf rssh $RPM_BUILD_ROOT/bin/sftpsh

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
if [ ! -f /etc/shells ]; then
	echo "%{_bindir}/%{name}" > /etc/shells
	echo "%{_bindir}/scpsh" >> /etc/shells
	echo "%{_bindir}/sftpsh" >> /etc/shells
else
	if ! grep -q '^%{_bindir}/%{name}$' /etc/shells; then
		echo "%{_bindir}/%{name}" >> /etc/shells
	fi
	if ! grep -q '^%{_bindir}/scpsh$' /etc/shells; then
		echo "%{_bindir}/scpsh" >> /etc/shells
	fi
	if ! grep -q '^%{_bindir}/sftpsh$' /etc/shells; then
		echo "%{_bindir}/sftpsh" >> /etc/shells
	fi
fi

%preun
umask 022
if [ "$1" = "0" ]; then
	grep -v %{_bindir}/%{name} /etc/shells | grep -v %{_bindir}/scpsh | grep -v %{_bindir}/sftpsh > /etc/shells.new
	mv -f /etc/shells.new /etc/shells
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/scpsh
%attr(755,root,root) %{_bindir}/sftpsh
%attr(4755,root,root) %{_bindir}/rssh_chroot_helper
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) /etc/rssh.conf
%{_mandir}/man?/*
