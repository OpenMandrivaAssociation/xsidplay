Name:		xsidplay
Summary:	A Commdore 64 music player and SID chip emulator for X11
Version:	2.0.3
Release:	6
License:	GPLv2+
Group:		Sound
URL:		https://sf.net/projects/xsidplay2
Source:		http://prdownloads.sourceforge.net/xsidplay2/%{name}-%{version}.tar.bz2
Source1:	%{name}-48.png
Source2:	%{name}-32.png
Source3:	%{name}-16.png
BuildRequires:	libsidplay-devel < 2
BuildRequires:	qt3-devel
BuildRequires:	tsid-devel >= 0.6
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(esound)
BuildRequires:	pkgconfig(libsidplay2)

%description
This is a music player and SID chip emulator based in the SIDPLAY
library. With it you can listen to more than 10000 musics from old
and new C64 programs. The majority of available musics is in the
High Voltage SID Collection.

%package libsidplay2
#stupid rpmlint: %mklibname
Summary:	Xsidplay version based on libsidplay2
Group:		Sound
Requires:	%{name} = %{version}
BuildRequires:	automake1.4

%description libsidplay2
This is a music player and SID chip emulator based in the SIDPLAY
library. With it you can listen to more than 10000 musics from old
and new C64 programs. The majority of available musics is in the
High Voltage SID Collection.

This package contains the version of xsidplay linked against the new version
of libsidplay, it needs much more processor power, but it has a much better 
sound quality.

%prep
%setup -q

#fix path in man page
perl -pi -e "s!%{_datadir}/doc/%{name}!%{_datadir}/doc/%{name}-%{version}!" xsidplay.1

%build
export LDFLAGS="-lsidplay2"
export CC=g++
%configure2_5x --with-qt-dir=%{_prefix}/lib/qt3 --with-qt-libraries=%{_prefix}/lib/qt3/%{_lib} --with-sidplay2 --with-sidplay-lib=%{_libdir}
%make LIBS=-lasound
mv src/xsidplay xsidplay-libsidplay2
make clean
rm -f config.cache
unset LDFLAGS
%configure2_5x --with-qt-dir=%{_prefix}/lib/qt3 --with-qt-libraries=%{_prefix}/lib/qt3/%{_lib}
%make LIBS=-lasound

%install
%makeinstall_std pkgdatadir=%{_iconsdir}
# menu causes rpmlint warning, but that's ok, xsidplay is provided by
# alternative
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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
mkdir -p %{buildroot}{%{_liconsdir},%{_iconsdir},%{_miconsdir}}
cp %{SOURCE1} %{buildroot}%{_liconsdir}/xsidplay.png
cp %{SOURCE2} %{buildroot}%{_iconsdir}/xsidplay.png
cp %{SOURCE3} %{buildroot}%{_miconsdir}/xsidplay.png

cp xsidplay-libsidplay2 %{buildroot}%{_bindir}
cd %{buildroot}%{_bindir}
mv xsidplay xsidplay-libsidplay1

rm -f %{buildroot}%{_datadir}/icons/mini/xsidplay.xpm
rm -f %{buildroot}%{_datadir}/icons/xsidplay.xpm

%post
update-alternatives --install %{_bindir}/xsidplay xsidplay %{_bindir}/xsidplay-libsidplay1 10
[ -e %{_bindir}/%{name} ] || update-alternatives --auto %{name}

%postun
[ "$1" = "0" ] || exit 0
update-alternatives --remove xsidplay %{_bindir}/xsidplay-libsidplay1

%post libsidplay2
update-alternatives --install %{_bindir}/xsidplay xsidplay %{_bindir}/xsidplay-libsidplay2 20

%postun libsidplay2
[ $1 = 0 ] || exit 0
update-alternatives --remove xsidplay %{_bindir}/xsidplay-libsidplay2

%files
%doc AUTHORS README README.LIRC README.QT README.TSID README.music 
%doc hv_sids.faq STIL.faq
%{_bindir}/xsidplay-libsidplay1
%{_iconsdir}/xsidplay.png
%{_iconsdir}/mini/xsidplay.png
%{_liconsdir}/xsidplay.png
%{_datadir}/applications/mandriva-*
%{_mandir}/man1/xsidplay.1*

%files libsidplay2
%doc README.sidplay2
%{_bindir}/xsidplay-libsidplay2

