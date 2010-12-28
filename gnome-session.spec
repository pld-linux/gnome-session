Summary:	The GNOME desktop programs for the GNOME2 GUI desktop environment
Summary(pl.UTF-8):	Programy dla desktopu środowiska graficznego GNOME2
Name:		gnome-session
Version:	2.91.4
Release:	0.1
Epoch:		1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-session/2.91/%{name}-%{version}.tar.bz2
# Source0-md5:	fcdfb55c1ea67df1391947c32e6efbcc
Source1:	%{name}-gnome.desktop
URL:		http://www.gnome.org/
BuildRequires:	GConf2
BuildRequires:	GConf2-devel >= 2.26.0
BuildRequires:	UPower-devel >= 0.9.0
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.16.0
BuildRequires:	gnome-common >= 2.24.0
BuildRequires:	gtk+3-devel >= 2.91.7
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 0.9.0
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sed >= 4.0
BuildRequires:	startup-notification-devel
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-xtrans-devel
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,preun):	GConf2
Requires:	UPower
Requires:	gnome-control-center >= 1:2.26.0
Requires:	gnome-wm
Requires:	polkit-gnome
# sr@Latn vs. sr@latin
Obsoletes:	gnome-splash-gnome < 1:2.32.0
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

%prep
%setup -q

sed -i -e 's/^en@shaw//' po/LINGUAS
%{__rm} po/en@shaw.po

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
	--with-gtk=3.0 \
	--with-default-wm=gnome-wm \
	--disable-schemas-install \
	--disable-silent-rules \
	--enable-docbook-docs \
	X_EXTRA_LIBS="-lXext"

%{__make}

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
%doc AUTHORS *ChangeLog NEWS README doc/dbus/gnome-session.html
%attr(755,root,root) %{_bindir}/gnome-session
%attr(755,root,root) %{_bindir}/gnome-session-properties
%attr(755,root,root) %{_bindir}/gnome-session-save
%attr(755,root,root) %{_bindir}/gnome-wm
%attr(755,root,root) %{_libdir}/gnome-session-is-accelerated
%{_sysconfdir}/gconf/schemas/gnome-session.schemas
%dir %{_datadir}/gnome/autostart
%dir %{_datadir}/gnome/default-session
%dir %{_datadir}/gnome/shutdown
%dir %{_datadir}/gnome-session
%dir %{_datadir}/gnome-session/sessions
%{_datadir}/gnome-session/gsm-inhibit-dialog.ui
%{_datadir}/gnome-session/session-properties.ui
%{_datadir}/gnome-session/sessions/classic-gnome.session
%{_datadir}/gnome-session/sessions/gnome.session
%{_datadir}/xsessions/gnome.desktop
%{_mandir}/man[15]/*
%{_desktopdir}/session-properties.desktop
%{_desktopdir}/gnome-wm.desktop
%{_iconsdir}/hicolor/*/*/session-properties.*
