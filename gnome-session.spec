# TODO:
# add all ChageLog and all READMEs to doc
Summary:	The gnome desktop programs for the GNOME2 GUI desktop environment
Summary(pl):	Programy dla desktopu ¶rodowiska graficznego GNOME2
Name:		gnome-session
Version:	2.1.3
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.1/%{name}-%{version}.tar.bz2
Patch0:		%{name}-am.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 1.2.1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	esound-devel >= 0.2.29
BuildRequires:	gnome-common >= 1.2.4
BuildRequires:	gtk+2-devel >= 2.1.0
BuildRequires:	intltool
BuildRequires:	libgnomecanvas-devel >= 2.1.0
BuildRequires:	libgnomeui-devel >= 2.1.2
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
Requires:	libgnomeui >= 2.1.2
Requires:	control-center >= 2.1.2
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	/usr/bin/scrollkeeper-update
Requires(post):	GConf2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix         /usr/X11R6
%define         _mandir         %{_prefix}/man
%define         _sysconfdir     /etc/X11/GNOME2
%define         _omf_dest_dir   %(scrollkeeper-config --omfdir)

%description
GNOME2 (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME2 is similar in purpose and scope
to CDE and KDE, but GNOME2 is based completely on free software.

GNOME2 session provides the session tools for the the gnome desktop.

%description -l pl
GNOME2 (GNU Network Object Model Environment) to zestaw przyjaznych
dla u¿ytkownika aplikacji i narzêdzi do u¿ywania w po³±czeniu z
zarz±dc± okien pod X. GNOME2 ma podobny cel jak CDE i KDE, ale bazuje
ca³kowicie na wolnym oprogramowaniu.

Pakiet gnome-session zawiera narzêdzia do obs³ugi sesji dla desktopu
GNOME.

%prep
%setup -q
%patch0 -p1

%build
intltoolize --copy --force
glib-gettextize --copy --force
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__autoconf}
%{__automake}
%configure 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	omf_dest_dir=%{_omf_dest_dir}/%{name} \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%find_lang %{name} --with-gnome --all-name
mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

%clean
rm -fr $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/usr/bin/scrollkeeper-update
%gconf_schema_install

%postun
/sbin/ldconfig
/usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS *ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/control-center-2.0
%{_datadir}/gnome
%{_datadir}/pixmaps/splash
%{_mandir}/man[15]/*
%{_omf_dest_dir}/%{name}
