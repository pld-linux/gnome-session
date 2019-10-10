# TODO: is polkit-gnome still used?
#
# Conditiional build:
%bcond_without	systemd		# disable systemd tracking support
%bcond_without	consolekit	# disable ConsoleKit tracking support (when systemd is enabled use as a fallback)
#
Summary:	Session support tools for the GNOME GUI desktop environment
Summary(pl.UTF-8):	Programy obsługujęce sesję dla środowiska graficznego GNOME
Name:		gnome-session
Version:	3.34.1
Release:	1
Epoch:		1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-session/3.34/%{name}-%{version}.tar.xz
# Source0-md5:	1a9c10d5468b3ba8abee94653692fe0d
Source1:	%{name}-gnome.desktop
Source2:	polkit-gnome-authentication-agent-1.desktop
URL:		http://www.gnome.org/
BuildRequires:	EGL-devel
BuildRequires:	Mesa-libGL-devel
BuildRequires:	OpenGLESv2-devel
%{?with_consolekit:BuildRequires:	dbus-glib-devel >= 0.76}
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.46.0
BuildRequires:	gnome-desktop-devel >= 3.18.0
BuildRequires:	gtk+3-devel >= 3.18.0
BuildRequires:	json-glib-devel >= 0.10
BuildRequires:	libepoxy-devel
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.43.0
BuildRequires:	ninja >= 1.5
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-xtrans-devel
Requires(post,postun):	glib2 >= 1:2.46.0
%{?with_consolekit:Requires:	dbus-glib >= 0.76}
Requires:	dbus-x11
Requires:	glib2 >= 1:2.46.0
Requires:	gnome-desktop >= 3.18.0
Requires:	gnome-settings-daemon >= 3.26.0
Requires:	gnome-shell >= 3.24.0
Requires:	gnome-wm
Requires:	gsettings-desktop-schemas >= 3.4.0
Requires:	gtk+3 >= 3.18.0
Requires:	json-glib >= 0.10
Requires:	polkit-gnome >= 0.101
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

mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

%build
%meson build \
	-Dsystemd=%{?with_systemd:true}%{!?with_systemd:false} \
	-Dsystemd=%{?with_consolekit:true}%{!?with_consolekit:false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/autostart
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/default-session
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/shutdown

%ninja_install -C build

install -d $RPM_BUILD_ROOT%{_datadir}/xsessions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/xsessions/gnome.desktop
sed -e 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/polkit-gnome-authentication-agent-1.desktop

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/gnome-session/dbus/*.html

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
%doc AUTHORS MAINTAINERS NEWS README build/doc/dbus/gnome-session.html
%attr(755,root,root) %{_bindir}/gnome-session
%attr(755,root,root) %{_bindir}/gnome-session-custom-session
%attr(755,root,root) %{_bindir}/gnome-session-inhibit
%attr(755,root,root) %{_bindir}/gnome-session-quit
%attr(755,root,root) %{_libexecdir}/gnome-session-binary
%attr(755,root,root) %{_libexecdir}/gnome-session-ctl
%attr(755,root,root) %{_libexecdir}/gnome-session-check-accelerated
%attr(755,root,root) %{_libexecdir}/gnome-session-check-accelerated-gl-helper
%attr(755,root,root) %{_libexecdir}/gnome-session-check-accelerated-gles-helper
%attr(755,root,root) %{_libexecdir}/gnome-session-failed
%{_sysconfdir}/xdg/autostart/polkit-gnome-authentication-agent-1.desktop
%{_datadir}/GConf/gsettings/gnome-session.convert
%{_datadir}/glib-2.0/schemas/org.gnome.SessionManager.gschema.xml
%dir %{_datadir}/gnome/autostart
%dir %{_datadir}/gnome/default-session
%dir %{_datadir}/gnome/shutdown
%dir %{_datadir}/gnome-session
%dir %{_datadir}/gnome-session/sessions
%{_datadir}/gnome-session/hardware-compatibility
%{_datadir}/gnome-session/sessions/gnome.session
%{_datadir}/gnome-session/sessions/gnome-dummy.session
%{_datadir}/wayland-sessions/gnome.desktop
%{_datadir}/xsessions/gnome.desktop
%{_datadir}/xsessions/gnome-xorg.desktop
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
%{systemduserunitdir}/gnome-session-stable.target
%{systemduserunitdir}/gnome-session-stable.timer
%{systemduserunitdir}/gnome-session-wayland.target
%{systemduserunitdir}/gnome-session-wayland@.target
%{systemduserunitdir}/gnome-session-x11-services.target
%{systemduserunitdir}/gnome-session-x11.target
%{systemduserunitdir}/gnome-session-x11@.target
%{systemduserunitdir}/gnome-session.target
%{systemduserunitdir}/gnome-session@.target
%{_mandir}/man1/gnome-session.1*
%{_mandir}/man1/gnome-session-inhibit.1*
%{_mandir}/man1/gnome-session-quit.1*
