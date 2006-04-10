#
# todo:
# - add all ChageLog and all READMEs to doc
#
Summary:	The GNOME desktop programs for the GNOME2 GUI desktop environment
Summary(pl):	Programy dla desktopu ¶rodowiska graficznego GNOME2
Name:		gnome-session
Version:	2.14.1
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-session/2.14/%{name}-%{version}.tar.bz2
# Source0-md5:	0b7a0fa918f7d0565d6487d06fa4489d
Source1:	%{name}-gnome.desktop
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-less_verbose.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.12.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	esound-devel >= 1:0.2.30
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gnome-keyring-devel >= 0.4.2
BuildRequires:	gtk+2-devel >= 2:2.8.3
BuildRequires:	intltool
BuildRequires:	libgnomeui-devel >= 2.12.0
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	pango-devel >= 1:1.10.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
Requires(post,preun):	GConf2
Requires:	control-center >= 1:2.12.0
Requires:	gnome-keyring >= 0.4.2
Requires:	gnome-splash
Requires:	gnome-wm
Requires:	libgnomeui >= 2.12.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME2 (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME2 is similar in purpose and scope
to CDE and KDE, but GNOME2 is based completely on free software.

GNOME2 session provides the session tools for the the GNOME desktop.

%description -l pl
GNOME2 (GNU Network Object Model Environment) to zestaw przyjaznych
dla u¿ytkownika aplikacji i narzêdzi do u¿ywania w po³±czeniu z
zarz±dc± okien pod X. GNOME2 ma podobny cel jak CDE i KDE, ale bazuje
ca³kowicie na wolnym oprogramowaniu.

Pakiet gnome-session zawiera narzêdzia do obs³ugi sesji dla desktopu
GNOME.

%package -n gnome-splash-gnome
Summary:	GNOME splash screen
Summary(pl):	Ekran startowy GNOME
Group:		X11/Amusements
Requires:	%{name} = %{version}
Provides:	gnome-splash
Obsoletes:	gnome-splash

%description -n gnome-splash-gnome
Default GNOME splash screen.

%description -n gnome-splash-gnome -l pl
Standardowy ekran startowy GNOME.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__intltoolize}
%{__glib_gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	X_EXTRA_LIBS="-lXext"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/autostart

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/xsessions
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/xsessions/gnome.desktop

mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name} --with-gnome --all-name

%clean
rm -fr $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install gnome-session.schemas

%preun
%gconf_schema_uninstall gnome-session.schemas

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS *ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/gnome-session.schemas
%dir %{_datadir}/gnome/autostart
%{_datadir}/gnome/default.session
%{_datadir}/gnome/default.wm
%{_datadir}/xsessions/*.desktop
%dir %{_pixmapsdir}/splash
%{_mandir}/man[15]/*
%{_desktopdir}/*.desktop

%files -n gnome-splash-gnome
%defattr(644,root,root,755)
%{_pixmapsdir}/splash/gnome-splash.png
