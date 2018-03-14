#
# Conditiional build:
%bcond_without	systemd		# disable systemd tracking support
%bcond_without	consolekit	# disable ConsoleKit tracking support (when systemd is enabled use as a fallback)
#
Summary:	Session support tools for the GNOME GUI desktop environment
Summary(pl.UTF-8):	Programy obsługujęce sesję dla środowiska graficznego GNOME
Name:		gnome-session
Version:	3.28.0
Release:	1
Epoch:		1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-session/3.28/%{name}-%{version}.tar.xz
# Source0-md5:	6bdd34c566a0e1d1c7ca7e7dbd6ba055
Source1:	%{name}-gnome.desktop
Source2:	polkit-gnome-authentication-agent-1.desktop
URL:		http://www.gnome.org/
BuildRequires:	EGL-devel
BuildRequires:	Mesa-libGL-devel
BuildRequires:	OpenGLESv2-devel
%{?with_consolekit:BuildRequires:	dbus-glib-devel >= 0.76}
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.46.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gnome-desktop-devel >= 3.18.0
BuildRequires:	gtk+3-devel >= 3.18.0
BuildRequires:	json-glib-devel >= 0.10
BuildRequires:	libepoxy-devel
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.43.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	polkit-devel
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	sed >= 4.0
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXau-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-xtrans-devel
Requires(post,postun):	glib2 >= 1:2.46.0
Requires:	dbus-x11
Requires:	gnome-control-center >= 1:3.4.0
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
%meson build \
	-Dsystemd=%{?with_systemd:true}%{!?with_systemd:false} \
	-Dsystemd=%{?with_consolekit:true}%{!?with_consolekit:false}
%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/autostart
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/default-session
install -d $RPM_BUILD_ROOT%{_datadir}/gnome/shutdown

%meson_install -C build

install -d $RPM_BUILD_ROOT%{_datadir}/xsessions
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/xsessions/gnome.desktop
sed -e 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/polkit-gnome-authentication-agent-1.desktop

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
%doc AUTHORS *ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnome-session
%attr(755,root,root) %{_bindir}/gnome-session-custom-session
%attr(755,root,root) %{_bindir}/gnome-session-inhibit
%attr(755,root,root) %{_bindir}/gnome-session-quit
%attr(755,root,root) %{_libexecdir}/gnome-session-binary
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
%{_mandir}/man1/gnome-session.1*
%{_mandir}/man1/gnome-session-inhibit.1*
%{_mandir}/man1/gnome-session-quit.1*
