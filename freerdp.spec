# TODO:
# - fix DirectFB client build
# - consider coexisting freerdp 1.x and 2.0 (some apps require 1.x version, e.g. vlc)
#
# Conditional build:
%bcond_without	alsa		# ALSA sound support
%bcond_without	cups		# CUPS printing support
%bcond_with	directfb	# DirectFB client
%bcond_without	ffmpeg		# FFmpeg audio/video decoding support
%bcond_without	pcsc		# SmartCard support via PCSC-lite library
%bcond_without	pulseaudio	# Pulseaudio sound support
%bcond_without	wayland		# Wayland client
%bcond_without	x11		# X11 client
%bcond_with	sse2		# SSE2 instructions

%ifarch %{x8664} pentium4
%define	with_sse2	1
%endif
%define	rel	1
%define	snap	20160519
Summary:	Remote Desktop Protocol client
Summary(pl.UTF-8):	Klient protokołu RDP
Name:		freerdp
Version:	2.0.0
Release:	0.%{snap}.%{rel}
License:	Apache v2.0
Group:		Applications/Communications
# https://github.com/FreeRDP/FreeRDP/archive/master.tar.gz
Source0:	%{name}-%{version}-%{snap}.tar.gz
# Source0-md5:	ba0d58f19e6a2bd3ca1ac88593c7ed80
Patch0:		freerdp-DirectFB-include.patch
URL:		http://www.freerdp.com/
%{?with_directfb:BuildRequires:	DirectFB-devel}
%{?with_alsa:BuildRequires:	alsa-lib-devel}
BuildRequires:	cmake >= 2.6
%{?with_cups:BuildRequires:	cups-devel}
BuildRequires:	desktop-file-utils
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel}
BuildRequires:	openssl-devel
%{?with_pcsc:BuildRequires:	pcsc-lite-devel}
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
%{?with_wayland:BuildRequires:	wayland-devel}
%if %{with x11}
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libxkbfile
%endif
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	hicolor-icon-theme
Provides:	xfreerdp = %{version}-%{release}
Conflicts:	xfreerdp < 2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xfreerdp is Remote Desktop Protocol (RDP) client from the FreeRDP
project.

xfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%description -l pl.UTF-8
xfreerdp to klient protokołu RDP (Remote Desktop Protocol) z projektu
FreeRDP.

xfreerdp może łączyć się z serwerami RDP, takimi jak maszyny z
Microsoft Windows, xrdp oraz VirtualBox.

%package dfb
Summary:	DirectFB based Remote Desktop Protocol klient
Summary(pl.UTF-8):	Klient protokołu RDP oparty na DirectFB
Group:		Applications/Communications
Requires:	%{name}-libs = %{version}-%{release}

%description dfb
DirectFB based Remote Desktop Protocol klient.

dfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%description -l pl.UTF-8
Klient protokołu RDP oparty na DirectFB.

dfreerdp może łączyć się z serwerami RDP, takimi jak maszyny z
Microsoft Windows, xrdp oraz VirtualBox.

%package libs
Summary:	Core libraries implementing the RDP protocol
Summary(pl.UTF-8):	Główne biblioteki implementujące protokół RDP
Group:		Libraries

%description libs
libfreerdp-core can be embedded in applications.

libfreerdp-channels and libfreerdp-kbd might be convenient to use in X
applications together with libfreerdp-core.

libfreerdp-core can be extended with plugins handling RDP channels.

%description libs -l pl.UTF-8
libfreerdp-core może być osadzane w aplikacjach.

libfreerdp-channels oraz libfreerdp-kbd mogą być wygodne przy użyciu
wraz z libfreerdp-core w aplikacjach X.

libfreerdp-core można rozszerzać przy użyciu wtyczek obsługujących
kanały RDP.

%package devel
Summary:	Development files for FreeRDP libraries
Summary(pl.UTF-8):	Pliki programistyczne bibliotek FreeRDP
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use FreeRDP libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących biblioteki FreeRDP.

%prep
%setup -q -n FreeRDP-master
%patch0 -p1

cat << EOF > xfreerdp.desktop
[Desktop Entry]
Type=Application
Name=X FreeRDP
NoDisplay=true
Comment=Connect to RDP server and display remote desktop
Comment[pl]=Połączenie z serwerem RDP i wyświetlanie zdalnego pulpitu
Icon=%{name}
Exec=%{_bindir}/xfreerdp
Terminal=false
Categories=Network;RemoteAccess;
EOF

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	%{?with_alsa:-DWITH_ALSA=ON}%{!?with_alsa:-DWITH_ALSA=OFF} \
	-DWITH_CUNIT=OFF \
	%{?with_cups:-DWITH_CUPS=ON}%{!?with_cups:-DWITH_CUPS=OFF} \
	%{?with_directfb:-DWITH_DIRECTFB=ON}%{!?with_directfb:-DWITH_DIRECTFB=OFF} \
	%{?with_ffmpeg:-DWITH_FFMPEG=ON}%{!?with_ffmpeg:-DWITH_FFMPEG=OFF} \
	%{?with_pcsc:-DWITH_PCSC=ON}%{!?with_pcsc:-DWITH_PCSC=OFF} \
	%{?with_pulseaudio:-DWITH_PULSE=ON}%{!?with_pulseaudio:-DWITH_PULSE=OFF} \
	-DWITH_SERVER=ON \
	%{?with_sse2:-DWITH_SSE2=ON}%{!?with_sse2:-DWITH_SSE2=OFF} \
	%{?with_wayland:-DWITH_X11=ON}%{!?with_wayland:-DWITH_X11=OFF} \
	%{?with_x11:-DWITH_X11=ON}%{!?with_x11:-DWITH_X11=OFF} \
	-DWITH_XCURSOR=ON \
	-DWITH_XEXT=ON \
	-DWITH_XINERAMA=ON \
	-DWITH_XKBFILE=ON \
	-DWITH_XV=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/cmake

desktop-file-install --dir=$RPM_BUILD_ROOT%{_desktopdir} xfreerdp.desktop
install -p -D resources/FreeRDP_Icon_256px.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/freerdp-shadow-cli
%if %{with wayland}
%attr(755,root,root) %{_bindir}/wlfreerdp
%endif
%if %{with x11}
%attr(755,root,root) %{_bindir}/xfreerdp
%endif
%attr(755,root,root) %{_bindir}/winpr-hash
%attr(755,root,root) %{_bindir}/winpr-makecert
%{_mandir}/man1/xfreerdp.1*
%{_desktopdir}/xfreerdp.desktop
%{_iconsdir}/hicolor/256x256/apps/freerdp.png

%if %{with directfb}
%files dfb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dfreerdp
%endif

%files libs
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_libdir}/libfreerdp-client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-client.so.2
%attr(755,root,root) %{_libdir}/libfreerdp-server.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-server.so.2
%attr(755,root,root) %{_libdir}/libfreerdp-shadow.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-shadow.so.2
%attr(755,root,root) %{_libdir}/libfreerdp-shadow-subsystem.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-shadow-subsystem.so.2
%attr(755,root,root) %{_libdir}/libfreerdp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp.so.2
%attr(755,root,root) %{_libdir}/libuwac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuwac.so.0
%attr(755,root,root) %{_libdir}/libwinpr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwinpr.so.2
%attr(755,root,root) %{_libdir}/libwinpr-tools.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwinpr-tools.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreerdp-client.so
%attr(755,root,root) %{_libdir}/libfreerdp-server.so
%attr(755,root,root) %{_libdir}/libfreerdp-shadow.so
%attr(755,root,root) %{_libdir}/libfreerdp-shadow-subsystem.so
%attr(755,root,root) %{_libdir}/libfreerdp.so
%attr(755,root,root) %{_libdir}/libuwac.so
%attr(755,root,root) %{_libdir}/libwinpr.so
%attr(755,root,root) %{_libdir}/libwinpr-tools.so
%{_includedir}/freerdp2
%{_includedir}/uwac0
%{_includedir}/winpr2
%{_pkgconfigdir}/freerdp-client2.pc
%{_pkgconfigdir}/freerdp-server2.pc
%{_pkgconfigdir}/freerdp-shadow2.pc
%{_pkgconfigdir}/freerdp2.pc
%{_pkgconfigdir}/uwac0.pc
%{_pkgconfigdir}/winpr-tools2.pc
%{_pkgconfigdir}/winpr2.pc
