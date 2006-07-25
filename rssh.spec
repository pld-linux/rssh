Summary:	A restricted shell for assigning scp- or sftp-only access
Summary(pl):	Okrojona pow³oka daj±ca dostêp tylko do scp i/lub sftp
Name:		rssh
Version:	2.3.2
Release:	1
License:	BSD-like
Group:		Applications/Shells
Source0:	http://dl.sourceforge.net/rssh/%{name}-%{version}.tar.gz
# Source0-md5:	65712f2c06ff5fc6fc783bc8c2e4e1ba
Patch0:		%{name}-userbuild.patch
Patch1:		%{name}-mkchroot.patch
URL:		http://www.pizzashack.org/rssh/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssh-clients >= 3.5p1
Requires(post):	grep
Requires(preun):	sed >= 4.0
Conflicts:	openssh-server < 3.5p1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	with_ccache

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
install -d $RPM_BUILD_ROOT/bin

%{__make} install \
	 DESTDIR=$RPM_BUILD_ROOT

ln -sf rssh $RPM_BUILD_ROOT%{_bindir}/scpsh
ln -sf rssh $RPM_BUILD_ROOT%{_bindir}/sftpsh

# legacy
ln -s %{_bindir}/%{name} $RPM_BUILD_ROOT/bin/%{name}
ln -s %{_bindir}/scpsh $RPM_BUILD_ROOT/bin/scpsh
ln -s %{_bindir}/sftpsh $RPM_BUILD_ROOT/bin/sftpsh

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /etc/shells ]; then
	umask 022
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
if [ "$1" = "0" ]; then
	%{__sed} -i -e '/^%(echo %{_bindir} | sed -e 's,/,\\/,g')\/\(%{name}\|scpsh\|sftpsh\)$/d' /etc/shells
fi

# make compat symlink, the symlink is discarded using %ghost on package uninstall
%triggerpostun -- %{name} < 2.3.2-0.6
ln -sf %{_bindir}/%{name} /bin/%{name}
ln -sf %{_bindir}/scpsh /bin/scpsh
ln -sf %{_bindir}/sftpsh /bin/sftpsh

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README CHROOT SECURITY mkchroot.sh
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rssh.conf
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/scpsh
%attr(755,root,root) %{_bindir}/sftpsh
%attr(4755,root,root) %{_libdir}/rssh_chroot_helper
%{_mandir}/man?/*
# legacy
%ghost /bin/%{name}
%ghost /bin/scpsh
%ghost /bin/sftpsh
