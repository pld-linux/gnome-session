Summary:	Session support tools for the GNOME GUI desktop environment
Summary(pl.UTF-8):	Programy obsługujęce sesję dla środowiska graficznego GNOME
Name:		gnome-session
Version:	2.32.1
Release:	4
Epoch:		1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-session/2.32/%{name}-%{version}.tar.bz2
# Source0-md5:	222bad6b446cb19a6b9028ea24538002
Source1:	%{name}-gnome.desktop
Source2:	polkit-gnome-authentication-agent-1.desktop
URL:		http://www.gnome.org/
BuildRequires:	GConf2
BuildRequires:	GConf2-devel >= 2.26.0
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gtk+2-devel >= 2:2.16.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	startup-notification-devel
BuildRequires:	upower-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-xtrans-devel
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,preun):	GConf2
Requires:	gnome-control-center >= 1:2.26.0
Requires:	gnome-wm
Requires:	polkit-gnome >= 0.101
Requires:	upower
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
	--disable-schemas-install \
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
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/xsessions/gnome.desktop
sed -e 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/polkit-gnome-authentication-agent-1.desktop

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_sysconfdir}/gconf/schemas/gnome-session.schemas
%{_sysconfdir}/xdg/autostart/polkit-gnome-authentication-agent-1.desktop
%dir %{_datadir}/gnome/autostart
%dir %{_datadir}/gnome/default-session
%dir %{_datadir}/gnome/shutdown
%dir %{_datadir}/gnome-session
%{_datadir}/gnome-session/gsm-inhibit-dialog.ui
%{_datadir}/gnome-session/session-properties.ui
%{_datadir}/xsessions/gnome.desktop
%{_mandir}/man[15]/*
%{_desktopdir}/session-properties.desktop
%{_iconsdir}/hicolor/*/*/session-properties.*
