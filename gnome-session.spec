# TODO:
# add all ChageLog and all READMEs to doc
Summary:	The GNOME desktop programs for the GNOME2 GUI desktop environment
Summary(pl):	Programy dla desktopu ¶rodowiska graficznego GNOME2
Name:		gnome-session
Version:	2.5.3
Release:	1
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.5/%{name}-%{version}.tar.bz2
# Source0-md5:	b2b6760b9c91cc4b41abc7d9699e417f
Source1:	%{name}-gnome.desktop
Source2:	http://krzak.linux.net.pl/pld-gnome-splash.png
# Source2-md5:	f1dbeb6a93c0ebf68239f495b23b22f0
Patch0:		%{name}-default-session.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	libwrap-devel
BuildRequires:	esound-devel >= 0.2.30
BuildRequires:	gtk+2-devel >= 2.3.1
BuildRequires:	Xft-devel >= 2.1
BuildRequires:	GConf2-devel >= 2.5.0
BuildRequires:	gnome-common >= 2.4.0
BuildRequires:	libgnomecanvas-devel >= 2.5.0
BuildRequires:	libgnomeui-devel >= 2.5.0
BuildRequires:	libbonoboui-devel >= 2.5.0
BuildRequires:	pango-devel >= 1.3.1
BuildRequires:	rpm-build >= 4.1-10
Requires(post,postun):	/sbin/ldconfig
Requires(post):	GConf2
Requires:	control-center >= 2.5.0
Requires:	libgnomeui >= 2.5.0
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
%configure \
	--disable-schemas-install \
	X_EXTRA_LIBS="-lXext"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_datadir}/xsessions
install %{SOURCE1} $RPM_BUILD_ROOT/%{_datadir}/xsessions/gnome.desktop

install -d $RPM_BUILD_ROOT%{_datadir}/gnome/capplets
mv $RPM_BUILD_ROOT%{_datadir}/control-center-2.0/capplets/*.desktop $RPM_BUILD_ROOT%{_datadir}/gnome/capplets

cp -f %{SOURCE2} $RPM_BUILD_ROOT/%{_pixmapsdir}/splash/gnome-splash.png

mv ChangeLog main-ChangeLog
find . -name ChangeLog |awk '{src=$0; dst=$0;sub("^./","",dst);gsub("/","-",dst); print "cp " src " " dst}'|sh

%find_lang %{name} --with-gnome --all-name

%clean
rm -fr $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS *ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/gnome/capplets/*.desktop
%{_datadir}/gnome/default.session
%{_datadir}/gnome/default.wm
%{_datadir}/xsessions/*.desktop
%{_pixmapsdir}/splash
%{_mandir}/man[15]/*
