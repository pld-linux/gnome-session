# TODO:
# add all ChageLog and all READMEs to doc
Summary:	The GNOME desktop programs for the GNOME2 GUI desktop environment
Summary(pl):	Programy dla desktopu �rodowiska graficznego GNOME2
Name:		gnome-session
Version:	2.4.0
Release:	2
License:	LGPL
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.4/%{name}-%{version}.tar.bz2
# Source0-md5:	6a7acf3429b927c69e18019f9ec6fa9f
#Patch0:		%{name}-locale-sr.patch
URL:		http://www.gnome.org/
BuildRequires:	GConf2-devel >= 2.4.0
BuildRequires:	Xft-devel >= 2.1
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	esound-devel >= 0.2.30
BuildRequires:	gtk+2-devel >= 2.2.4
BuildRequires:	intltool
BuildRequires:	libgnomecanvas-devel >= 2.4.0
BuildRequires:	libgnomeui-devel >= 2.4.0.1
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	pango-devel >= 1.2.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.1-10
Requires(post,postun):	/sbin/ldconfig
Requires(post):	GConf2
Requires:	control-center >= 2.4.0
Requires:	libgnomeui >= 2.4.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME2 (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME2 is similar in purpose and scope
to CDE and KDE, but GNOME2 is based completely on free software.

GNOME2 session provides the session tools for the the GNOME desktop.

%description -l pl
GNOME2 (GNU Network Object Model Environment) to zestaw przyjaznych
dla u�ytkownika aplikacji i narz�dzi do u�ywania w po��czeniu z
zarz�dc� okien pod X. GNOME2 ma podobny cel jak CDE i KDE, ale bazuje
ca�kowicie na wolnym oprogramowaniu.

Pakiet gnome-session zawiera narz�dzia do obs�ugi sesji dla desktopu
GNOME.

%prep
%setup -q
#%patch0 -p1

# sr_YU is latin2, sr_YU@cyrillic is cyrillic in glibc
#mv -f po/{sr.po,sr@cyrillic.po}
#mv -f po/{sr@Latn.po,sr.po}

%build
intltoolize --copy --force
glib-gettextize --copy --force
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%{_datadir}/control-center-2.0
%{_datadir}/gnome/*
%{_pixmapsdir}/splash
%{_mandir}/man[15]/*
