Summary:	The GNOME desktop programs for the GNOME2 GUI desktop environment
Summary(pl.UTF-8):	Programy dla desktopu środowiska graficznego GNOME2
Name:		gnome-session
Version:	2.24.2
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-session/2.24/%{name}-%{version}.tar.bz2
# Source0-md5:	13e882a8c73bebb5403c207da0455156
Source1:	%{name}-gnome.desktop
Patch0:		%{name}-configure.patch
Patch1:		%{name}-splash.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	PolicyKit-gnome-devel >= 0.7
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-keyring-devel >= 2.24.0
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libglade2-devel >= 1:2.6.2
BuildRequires:	libgnomeui-devel >= 2.24.0
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	startup-notification-devel
BuildRequires:	xorg-lib-xtrans-devel
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,preun):	GConf2
Requires:	PolicyKit-gnome >= 0.7
Requires:	gnome-control-center >= 1:2.24.0
Requires:	gnome-keyring >= 2.24.0
Requires:	gnome-splash
Requires:	gnome-wm
Requires:	libgnomeui >= 2.24.0
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME2 (GNU Network Object Model Environment) is a user-friendly set
of applications and desktop tools to be used in conjunction with a
window manager for the X Window System. GNOME2 is similar in purpose
and scope to CDE and KDE, but GNOME2 is based completely on free
software.

GNOME2 session provides the session tools for the the GNOME desktop.

%description -l pl.UTF-8
GNOME2 (GNU Network Object Model Environment) to zestaw przyjaznych
dla użytkownika aplikacji i narzędzi do używania w połączeniu z
zarządcą okien pod X. GNOME2 ma podobny cel jak CDE i KDE, ale bazuje
całkowicie na wolnym oprogramowaniu.

Pakiet gnome-session zawiera narzędzia do obsługi sesji dla desktopu
GNOME.

%package -n gnome-splash-gnome
Summary:	GNOME splash screen
Summary(pl.UTF-8):	Ekran startowy GNOME
Group:		X11/Amusements
Requires:	%{name} = %{version}-%{release}
Provides:	gnome-splash
Obsoletes:	gnome-splash

%description -n gnome-splash-gnome
Default GNOME splash screen.

%description -n gnome-splash-gnome -l pl.UTF-8
Standardowy ekran startowy GNOME.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-ipv6 \
	--disable-schemas-install \
	X_EXTRA_LIBS="-lXext"

%{__make} \
	ESD_SERVER='%{_bindir}/esd' \
	GNOME_KEYRING_DAEMON='%{_bindir}/gnome-keyring-daemon' \

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/autostart
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/default-session
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/shutdown

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/xsessions
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/xsessions/gnome.desktop

%find_lang %{name} --with-gnome --all-name

%clean
rm -fr $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install gnome-session.schemas
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall gnome-session.schemas

%postun
/sbin/ldconfig
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS *ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnome-session
%attr(755,root,root) %{_bindir}/gnome-session-properties
%attr(755,root,root) %{_bindir}/gnome-session-save
%attr(755,root,root) %{_bindir}/gnome-wm
%dir %{_libexecdir}/gnome-session
%dir %{_libexecdir}/gnome-session/helpers
%attr(755,root,root) %{_libexecdir}/gnome-session/helpers/at-spi-registryd-wrapper
%attr(755,root,root) %{_libexecdir}/gnome-session/helpers/gnome-keyring-daemon-wrapper
%attr(755,root,root) %{_libexecdir}/gnome-session/helpers/gnome-session-splash
%attr(755,root,root) %{_libexecdir}/gnome-session/helpers/gnome-settings-daemon-helper
%{_sysconfdir}/gconf/schemas/gnome-session.schemas
%dir %{_datadir}/gnome/autostart
%{_datadir}/gnome/autostart/at-spi-registryd-wrapper.desktop
%{_datadir}/gnome/autostart/gnome-keyring-daemon-wrapper.desktop
%{_datadir}/gnome/autostart/gnome-session-splash.desktop
%{_datadir}/gnome/autostart/gnome-settings-daemon-helper.desktop
%dir %{_datadir}/gnome/default-session
%dir %{_datadir}/gnome/shutdown
%dir %{_datadir}/gnome-session
%{_datadir}/gnome-session/gsm-inhibit-dialog.glade
%{_datadir}/gnome-session/session-properties.glade
%{_datadir}/xsessions/gnome.desktop
%dir %{_pixmapsdir}/splash
%{_mandir}/man[15]/*
%{_desktopdir}/session-properties.desktop
%{_iconsdir}/hicolor/*/*/session-properties.*

%files -n gnome-splash-gnome
%defattr(644,root,root,755)
%{_pixmapsdir}/splash/gnome-splash.png
