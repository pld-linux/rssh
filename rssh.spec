Summary:	A restricted shell for assigning scp- or sftp-only access
Summary(pl):	Okrojona pow³oka daj±ca dostêp tylko do scp i sftp
Name:		rssh
Version:	0.9
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.pizzashack.org/rssh/%{name}.c
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

%build
%{__cc} %{rpmcflags} %{rpmldflags} -o %{name} %{name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install %{name} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
