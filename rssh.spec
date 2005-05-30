# TODO
# - no need to have have the shell in /bin, as it needs running sshd
#   to work, which itself needs /usr to be mounted. for nice trigger
#   see cvsspam.spec or scponly.spec
Summary:	A restricted shell for assigning scp- or sftp-only access
Summary(pl):	Okrojona pow³oka daj±ca dostêp tylko do scp i/lub sftp
Name:		rssh
Version:	2.2.3
Release:	1
License:	BSD-like
Group:		Applications/Shells
Source0:	http://www.pizzashack.org/rssh/src/%{name}-%{version}.tar.gz
# Source0-md5:	74f40a4fd5d2b097af34a817e21a33cf
Patch0:		%{name}-userbuild.patch
Patch1:		%{name}-mkchroot.patch
URL:		http://rssh.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssh-clients >= 3.5p1
Conflicts:	openssh-server < 3.5p1
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
%patch1

%build
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--with-scp=/usr/bin/scp \
	--with-sftp-server=/usr/%{_lib}/openssh/sftp-server

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	 DESTDIR=$RPM_BUILD_ROOT

ln -sf rssh $RPM_BUILD_ROOT%{_bindir}/scpsh
ln -sf rssh $RPM_BUILD_ROOT%{_bindir}/sftpsh

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
%doc AUTHORS ChangeLog README CHROOT SECURITY mkchroot.sh
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/rssh.conf
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/scpsh
%attr(755,root,root) %{_bindir}/sftpsh
%attr(4755,root,root) %{_libdir}/rssh_chroot_helper
%{_mandir}/man?/*
