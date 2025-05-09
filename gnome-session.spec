# TODO: is polkit-gnome still used?
Summary:	Session support tools for the GNOME GUI desktop environment
Summary(pl.UTF-8):	Programy obsługujęce sesję dla środowiska graficznego GNOME
Name:		gnome-session
Version:	48.0
Release:	1
Epoch:		1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-session/48/%{name}-%{version}.tar.xz
# Source0-md5:	7b06c3d7aff4c13be55fe90a3a8bb0c4
Source1:	polkit-gnome-authentication-agent-1.desktop
URL:		https://wiki.gnome.org/Projects/SessionManagement
BuildRequires:	EGL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGLESv2-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.46.0
BuildRequires:	gnome-desktop-devel >= 3.34.2
BuildRequires:	gtk+3-devel >= 3.22.0
BuildRequires:	json-glib-devel >= 0.10
BuildRequires:	libepoxy-devel
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.60.0
BuildRequires:	ninja >= 1.5
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	systemd-devel >= 1:242
BuildRequires:	systemd-units >= 1:242
BuildRequires:	tar >= 1:1.22
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-xtrans-devel
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.46.0
Requires:	dbus-x11
Requires:	glib2 >= 1:2.46.0
Requires:	gnome-desktop >= 3.34.2
Requires:	gnome-settings-daemon >= 3.26.0
Requires:	gnome-shell >= 3.24.0
Requires:	gnome-wm
Requires:	gsettings-desktop-schemas >= 3.4.0
Requires:	gtk+3 >= 3.22.0
Requires:	json-glib >= 0.10
Requires:	polkit-gnome >= 0.101
Requires:	systemd-libs >= 1:242
Requires:	systemd-units >= 1:242
# needs notification-daemon in fallback mode to function
Requires:	dbus(org.freedesktop.Notifications)
Obsoletes:	gnome-splash-gnome < 1:2.32.0
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

%build
%meson \
	-Dsession_selector=true \
	-Dsystemduserunitdir=%{systemduserunitdir}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart
install -d $RPM_BUILD_ROOT%{systemduserunitdir}/gnome-session.target.wants
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/{autostart,default-session,shutdown}

%meson_install

sed -e 's,@LIBDIR@,%{_libdir},' %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/polkit-gnome-authentication-agent-1.desktop

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/gnome-session/dbus/*.html

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas

%postun
if [ "$1" = "0" ]; then
	/sbin/ldconfig
	%glib_compile_schemas
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README.md build/doc/dbus/gnome-session.html
%attr(755,root,root) %{_bindir}/gnome-session
%attr(755,root,root) %{_bindir}/gnome-session-custom-session
%attr(755,root,root) %{_bindir}/gnome-session-inhibit
%attr(755,root,root) %{_bindir}/gnome-session-quit
%attr(755,root,root) %{_bindir}/gnome-session-selector
%attr(755,root,root) %{_libexecdir}/gnome-session-binary
%attr(755,root,root) %{_libexecdir}/gnome-session-ctl
%attr(755,root,root) %{_libexecdir}/gnome-session-check-accelerated
%attr(755,root,root) %{_libexecdir}/gnome-session-check-accelerated-gl-helper
%attr(755,root,root) %{_libexecdir}/gnome-session-check-accelerated-gles-helper
%attr(755,root,root) %{_libexecdir}/gnome-session-failed
%{_sysconfdir}/xdg/autostart/polkit-gnome-authentication-agent-1.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.SessionManager.gschema.xml
%dir %{_datadir}/gnome/autostart
%dir %{_datadir}/gnome/default-session
%dir %{_datadir}/gnome/shutdown
%dir %{_datadir}/gnome-session
%dir %{_datadir}/gnome-session/sessions
%{_datadir}/gnome-session/hardware-compatibility
%{_datadir}/gnome-session/session-selector.ui
%{_datadir}/gnome-session/sessions/gnome.session
%{_datadir}/gnome-session/sessions/gnome-dummy.session
%{_datadir}/wayland-sessions/gnome.desktop
%{_datadir}/wayland-sessions/gnome-wayland.desktop
%{_datadir}/xdg-desktop-portal/gnome-portals.conf
%{_datadir}/xsessions/gnome.desktop
%{_datadir}/xsessions/gnome-custom-session.desktop
%{_datadir}/xsessions/gnome-xorg.desktop
%dir %{systemduserunitdir}/gnome-launched-.scope.d
%{systemduserunitdir}/gnome-launched-.scope.d/override.conf
%{systemduserunitdir}/gnome-session-failed.service
%{systemduserunitdir}/gnome-session-failed.target
%{systemduserunitdir}/gnome-session-initialized.target
%{systemduserunitdir}/gnome-session-manager.target
%{systemduserunitdir}/gnome-session-manager@.service
%{systemduserunitdir}/gnome-session-monitor.service
%{systemduserunitdir}/gnome-session-pre.target
%{systemduserunitdir}/gnome-session-restart-dbus.service
%{systemduserunitdir}/gnome-session-shutdown.target
%{systemduserunitdir}/gnome-session-signal-init.service
%{systemduserunitdir}/gnome-session-wayland.target
%{systemduserunitdir}/gnome-session-wayland@.target
%{systemduserunitdir}/gnome-session-x11-services.target
%{systemduserunitdir}/gnome-session-x11-services-ready.target
%{systemduserunitdir}/gnome-session-x11.target
%{systemduserunitdir}/gnome-session-x11@.target
%{systemduserunitdir}/gnome-session.target
%dir %{systemduserunitdir}/gnome-session.target.wants
%{systemduserunitdir}/gnome-session@.target
%dir %{systemduserunitdir}/gnome-session@gnome.target.d
%{systemduserunitdir}/gnome-session@gnome.target.d/gnome.session.conf
%{_mandir}/man1/gnome-session.1*
%{_mandir}/man1/gnome-session-inhibit.1*
%{_mandir}/man1/gnome-session-quit.1*
%{_mandir}/man1/gnome-session-selector.1*
