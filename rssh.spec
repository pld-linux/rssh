Summary:	A restricted shell for assigning scp- or sftp-only access
Summary(pl):	Okrojona pow³oka daj±ca dostêp tylko do scp i sftp
Name:		rssh
Version:	0.9
Release:	1
License:	BSD-style
Group:		Applications/Shells
Source0:	http://www.pizzashack.org/rssh/%{name}.c
Patch0:		%{name}-sftp.patch
URL:		http://www.pizzashack.org/rssh/
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
%setup -c -T -q
install %{SOURCE0} .
%patch0 -p1

%build
%{__cc} %{rpmcflags} %{rpmldflags} -o %{name} %{name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install %{name} $RPM_BUILD_ROOT%{_bindir}

ln -sf %{name} $RPM_BUILD_ROOT%{_bindir}/scpsh
ln -sf %{name} $RPM_BUILD_ROOT%{_bindir}/sftpsh

%clean
rm -rf $RPM_BUILD_ROOT

%post
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
if [ "$1" = "0" ]; then
	grep -v %{_bindir}/%{name} /etc/shells | grep -v %{_bindir}/scpsh | grep -v %{_bindir}/sftpsh > /etc/shells.new
	mv -f /etc/shells.new /etc/shells
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/scpsh
%attr(755,root,root) %{_bindir}/sftpsh
