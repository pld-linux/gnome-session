Summary:	Session support tools for the GNOME GUI desktop environment
Summary(pl.UTF-8):	Programy obsługujęce sesję dla środowiska graficznego GNOME
Name:		gnome-session
Version:	3.2.1
Release:	1
Epoch:		1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-session/3.2/%{name}-%{version}.tar.xz
# Source0-md5:	05012cdf82e48feab17b5bc1804e37cf
Source1:	%{name}-gnome.desktop
Source2:	polkit-gnome-authentication-agent-1.desktop
URL:		http://www.gnome.org/
BuildRequires:	GConf2
BuildRequires:	GConf2-devel >= 2.26.0
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.10
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	json-glib-devel >= 0.10
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	pkgconfig(gl)
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	sed >= 4.0
BuildRequires:	upower-devel >= 0.9.0
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-xtrans-devel
Requires(post,postun):	glib2 >= 1:2.28.0
Requires:	dbus-x11
Requires:	gnome-control-center >= 1:3.0.0
Requires:	gnome-screensaver >= 3.0.0
Requires:	gnome-wm
Requires:	gsettings-desktop-schemas >= 3.2.0
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires:	polkit-gnome >= 0.101
Requires:	upower >= 0.9.0
# needs notification-daemon in fallback mode to function
Requires:	dbus(org.freedesktop.Notifications)
# sr@Latn vs. sr@latin
Obsoletes:	gnome-splash-gnome < 1:2.32.0
Conflicts:	glibc-misc < 6:2.7
Conflicts:	polkit-gnome < 0.101
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software.

GNOME session provides the session tools for the the GNOME desktop.

%description -l pl.UTF-8
GNOME (GNU Network Object Model Environment) to zestaw przyjaznych dla
użytkownika aplikacji i narzędzi do używania w połączeniu z zarządcą
okien pod X. GNOME ma podobny cel jak CDE i KDE, ale bazuje całkowicie
na wolnym oprogramowaniu.

Pakiet gnome-session zawiera narzędzia do obsługi sesji dla środowiska
graficznego GNOME.

%prep
%setup -q

mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-ipv6 \
	--disable-silent-rules \
	X_EXTRA_LIBS="-lXext"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/autostart
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/default-session
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/shutdown

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/xsessions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/xsessions/gnome.desktop
sed -e 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/polkit-gnome-authentication-agent-1.desktop

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas
%update_icon_cache hicolor

%postun
if [ "$1" = "0" ]; then
	/sbin/ldconfig
	%update_icon_cache hicolor
	%glib_compile_schemas
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS *ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnome-session
%attr(755,root,root) %{_bindir}/gnome-session-properties
%attr(755,root,root) %{_bindir}/gnome-session-quit
%attr(755,root,root) %{_libdir}/gnome-session-check-accelerated
%attr(755,root,root) %{_libdir}/gnome-session-check-accelerated-helper
%{_sysconfdir}/xdg/autostart/polkit-gnome-authentication-agent-1.desktop
%{_datadir}/GConf/gsettings/gnome-session.convert
%{_datadir}/glib-2.0/schemas/org.gnome.SessionManager.gschema.xml
%dir %{_datadir}/gnome/autostart
%dir %{_datadir}/gnome/default-session
%dir %{_datadir}/gnome/shutdown
%dir %{_datadir}/gnome-session
%dir %{_datadir}/gnome-session/sessions
%{_datadir}/gnome-session/gsm-inhibit-dialog.ui
%{_datadir}/gnome-session/session-properties.ui
%{_datadir}/gnome-session/sessions/gnome-fallback.session
%{_datadir}/gnome-session/sessions/gnome.session
%{_datadir}/xsessions/gnome.desktop
%{_mandir}/man[15]/*
%{_desktopdir}/session-properties.desktop
%{_iconsdir}/hicolor/*/*/session-properties.*
