Summary:	The gnome desktop programs for the GNOME2 GUI desktop environment.
Name:		gnome-session
Version:	1.5.18
Release:	0.1
License:	LGPL
Group:		X11/Applications
Source0:	ftp://ftp.gnome.org/pub/gnome/pre-gnome2/sources/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
URL:		http://www.gnome.org/
BuildRequires:	libgnomecanvas-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	pkgconfig

%define         _prefix         /usr/X11R6
%define         _mandir         %{_prefix}/man
%define         _omf_dest_dir   %(scrollkeeper-config --omfdir)

%description
GNOME2 (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME2 is similar in purpose and scope
to CDE and KDE, but GNOME2 is based completely on free software. The
gnome-core package includes the basic programs and libraries that are
needed to install GNOME2.

GNOME2 session provides the session tools for the the gnome desktop.

%prep
%setup -q

%build
%configure \
	--enable-gtk-doc=no
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	omf_dest_dir=%{_omf_dest_dir}/%{name}

gzip -9nf AUTHORS ChangeLog NEWS README

%find_lang %{name} --with-gnome --all-name

%clean
rm -fr $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/usr/bin/scrollkeeper-update

%postun
/sbin/ldconfig
/usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_datadir}/control-center
%{_datadir}/control-center-2.0
%{_datadir}/gnome
%{_datadir}/pixmaps/splash
%{_mandir}/man[15]/*
%{_omf_dest_dir}/%{name}
