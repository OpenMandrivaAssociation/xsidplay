%define name xsidplay
%define version 1.6.5.2
%define release %mkrel 4

Name: %{name}
Summary: A Commdore 64 music player and SID chip emulator for X11
Version: %{version}
Release: %{release}
Icon: %{name}.xpm
License: GPL
URL: http://www.geocities.com/SiliconValley/Lakes/5147/
Group: Sound
Source: http://www.geocities.com/SiliconValley/Lakes/5147/sidplay/packages/%{name}-%{version}.tar.bz2
Source1: %{name}-48.png
Source2: %{name}-32.png
Source3: %{name}-16.png
Patch: xsidplay-1.6.5.2-gcc4.patch.bz2
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: qt3-devel 
BuildRequires: libsidplay-devel < 2
BuildRequires: sidplay2-devel >= 2.1.0-0.20020903.1mdk
BuildRequires: tsid-devel >= 0.6
BuildRequires: libarts-devel
BuildRequires: libesound-devel	

%description
This is a music player and SID chip emulator based in the SIDPLAY
library. With it you can listen to more than 10000 musics from old
and new C64 programs. The majority of available musics is in the
High Voltage SID Collection.

%package libsidplay2
#stupid rpmlint: %mklibname
Summary: Xsidplay version based on libsidplay2
Group: Sound
Requires: %{name} = %{version}
BuildRequires: automake1.4

%description libsidplay2
This is a music player and SID chip emulator based in the SIDPLAY
library. With it you can listen to more than 10000 musics from old
and new C64 programs. The majority of available musics is in the
High Voltage SID Collection.

This package contains the version of xsidplay linked against the new version
of libsidplay, it needs much more processor power, but it has a much better 
sound quality.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q
%patch -p1

#fix path in man page
perl -pi -e "s!%{_datadir}/doc/%{name}!%{_datadir}/doc/%{name}-%{version}!" xsidplay.1

%build
export LDFLAGS="-lsidplay2"
export CC=g++
%configure2_5x --with-qt3 --with-qt-dir=%{_prefix}/lib/qt3 --with-qt-libraries=%_prefix/lib/qt3/%_lib --with-sidplay2 --with-sidplay-lib=%_libdir
%make 
mv src/xsidplay xsidplay-libsidplay2
make clean
rm -f config.cache
unset LDFLAGS
%configure2_5x --with-qt3 --with-qt-dir=%{_prefix}/lib/qt3 --with-qt-libraries=%{_prefix}/lib/qt3/%_lib
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std pkgdatadir=%{_iconsdir}
mkdir -p $RPM_BUILD_ROOT/%{_menudir}
# menu causes rpmlint warning, but that's ok, xsidplay is provided by
# alternative
cat << EOF > $RPM_BUILD_ROOT/%{_menudir}/xsidplay
?package(xsidplay):\
needs="x11"\
section="Multimedia/Sound"\
title="Xsidplay"\
longtitle="QT version of the C64 music player"\
command="xsidplay"\
icon="xsidplay.png" xdg="true"
EOF
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Xsidplay
Comment=QT version of the C64 music player
Exec=%{_bindir}/%{name} %U
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-Multimedia-Sound;AudioVideo;Audio;Player;
EOF
mkdir -p $RPM_BUILD_ROOT{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_liconsdir}/xsidplay.png
cp %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/xsidplay.png
cp %{SOURCE3} $RPM_BUILD_ROOT%{_miconsdir}/xsidplay.png

cp xsidplay-libsidplay2 $RPM_BUILD_ROOT%{_bindir}
cd $RPM_BUILD_ROOT%{_bindir}
mv xsidplay xsidplay-libsidplay1

rm -f %buildroot%{_datadir}/icons/mini/xsidplay.xpm
rm -f %buildroot%{_datadir}/icons/xsidplay.xpm

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}
update-alternatives --install %{_bindir}/xsidplay xsidplay %{_bindir}/xsidplay-libsidplay1 10
[ -e %{_bindir}/%{name} ] || update-alternatives --auto %{name}

%postun
%{clean_menus}
[ "$1" = "0" ] || exit 0
update-alternatives --remove xsidplay %{_bindir}/xsidplay-libsidplay1


%post libsidplay2
update-alternatives --install %{_bindir}/xsidplay xsidplay %{_bindir}/xsidplay-libsidplay2 20

%postun libsidplay2
[ $1 = 0 ] || exit 0
update-alternatives --remove xsidplay %{_bindir}/xsidplay-libsidplay2

%files
%defattr(-,root,root)
%doc AUTHORS README README.LIRC README.QT README.TSID README.music 
%doc hv_sids.faq STIL.faq
%{_bindir}/xsidplay-libsidplay1
%{_iconsdir}/xsidplay.png
%{_iconsdir}/mini/xsidplay.png
%{_liconsdir}/xsidplay.png
%_datadir/applications/mandriva-*
%{_menudir}/xsidplay
%{_mandir}/man1/xsidplay.1*

%files libsidplay2
%defattr(-,root,root)
%doc README.sidplay2
%{_bindir}/xsidplay-libsidplay2
