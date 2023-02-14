# NOTE: for freerdp 2.x see freerdp2.spec
#
# Conditional build:
%bcond_without	alsa		# ALSA sound support
%bcond_without	cups		# CUPS printing support
%bcond_without	directfb	# DirectFB client
%bcond_without	ffmpeg		# FFmpeg audio/video decoding support
%bcond_without	pcsc		# SmartCard support via PCSC-lite library
%bcond_without	pulseaudio	# Pulseaudio sound support
%bcond_without	x11		# X11 client
%bcond_with	sse2		# SSE2 instructions

%ifarch %{x8664} pentium4
%define	with_sse2	1
%endif
Summary:	Remote Desktop Protocol client
Summary(pl.UTF-8):	Klient protokołu RDP
Name:		freerdp
Version:	1.0.2
Release:	9
License:	Apache v2.0
Group:		Applications/Communications
Source0:	http://pub.freerdp.com/releases/%{name}-%{version}.tar.gz
# Source0-md5:	08f0e07d8d77e142f7dc39e4033a458d
Patch0:		%{name}-ffmpeg.patch
Patch1:		ffmpeg3.patch
Patch2:		ffmpeg4.patch
Patch3:		%{name}-openssl.patch
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
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-plugins = %{version}-%{release}
Requires:	hicolor-icon-theme
Provides:	xfreerdp = %{version}-%{release}
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
Requires:	%{name}-plugins = %{version}-%{release}

%description dfb
DirectFB based Remote Desktop Protocol klient.

dfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%description dfb -l pl.UTF-8
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

%package plugins
Summary:	Plugins for handling the standard RDP channels
Summary(pl.UTF-8):	Wtyczki do obsługi standardowych kanałów RDP
Group:		Applications/Communications
Requires:	%{name}-libs = %{version}-%{release}

%description plugins
A set of plugins to the channel manager implementing the standard
virtual channels extending RDP core functionality. For instance,
sounds, clipboard sync, disk/printer redirection, etc.

%description plugins -l pl.UTF-8
Zestaw wtyczek zarządcy kanałów, implementujących standardowe
kanały wirtualne rozszerzające podstawową funkcjonalność RDP -
na przykład dźwięk, synchronizację schowka, przekierowanie
dysku/drukarki.

%package plugins-alsa
Summary:	ALSA plugins for handling RDP audio
Summary(pl.UTF-8):	Wtyczki ALSA do obsługi dźwięku RDP
Group:		Libraries
Requires:	%{name}-plugins = %{version}-%{release}

%description plugins-alsa
ALSA plugins for handling RDP audio.

%description plugins-alsa -l pl.UTF-8
Wtyczki ALSA do obsługi dźwięku RDP.

%package plugins-ffmpeg
Summary:	FFmpeg plugin for decoding RDP audio/video
Summary(pl.UTF-8):	Wtyczka FFmpeg do dekodowania dźwięku/obrazu RDP
Group:		Libraries
Requires:	%{name}-plugins = %{version}-%{release}

%description plugins-ffmpeg
FFmpeg plugin for decoding RDP audio/video.

%description plugins-ffmpeg -l pl.UTF-8
Wtyczka FFmpeg do dekodowania dźwięku/obrazu RDP.

%package plugins-pcsc
Summary:	PC/SC plugin for RDP smartcard support
Summary(pl.UTF-8):	Wtyczka PC/SC do obsługi kart procesorowych w RDP
Group:		Libraries
Requires:	%{name}-plugins = %{version}-%{release}

%description plugins-pcsc
PC/SC plugin for RDP smartcard support.

%description plugins-pcsc -l pl.UTF-8
Wtyczka PC/SC do obsługi kart procesorowych w RDP.

%package plugins-pulse
Summary:	PulseAudio plugins for handling RDP audio
Summary(pl.UTF-8):	Wtyczki PulseAudio do obsługi dźwięku RDP
Group:		Libraries
Requires:	%{name}-plugins = %{version}-%{release}

%description plugins-pulse
PulseAudio plugins for handling RDP audio.

%description plugins-pulse -l pl.UTF-8
Wtyczki PulseAudio do obsługi dźwięku RDP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
	%{!?with_alsa:-DWITH_ALSA=OFF} \
	-DWITH_CUNIT=OFF \
	%{!?with_cups:-DWITH_CUPS=OFF} \
	%{?with_directfb:-DWITH_DIRECTFB=ON} \
	%{!?with_ffmpeg:-DWITH_FFMPEG=OFF} \
	%{?with_pcsc:-DWITH_PCSC=ON} \
	%{?with_pulseaudio:-DWITH_PULSEAUDIO=ON} \
	-DWITH_SERVER=ON \
	%{!?with_sse2:-DWITH_SSE2=OFF} \
	-DWITH_X11=ON \
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

# No need for keymap files when using xkbfile
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/freerdp

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
%attr(755,root,root) %{_bindir}/xfreerdp
%{_mandir}/man1/xfreerdp.1*
%{_desktopdir}/xfreerdp.desktop
%{_iconsdir}/hicolor/256x256/apps/freerdp.png

%files dfb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dfreerdp

%files libs
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_libdir}/libfreerdp-cache.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-cache.so.1.0
%attr(755,root,root) %{_libdir}/libfreerdp-channels.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-channels.so.1.0
%attr(755,root,root) %{_libdir}/libfreerdp-codec.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-codec.so.1.0
%attr(755,root,root) %{_libdir}/libfreerdp-core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-core.so.1.0
%attr(755,root,root) %{_libdir}/libfreerdp-gdi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-gdi.so.1.0
%attr(755,root,root) %{_libdir}/libfreerdp-kbd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-kbd.so.1.0
%attr(755,root,root) %{_libdir}/libfreerdp-rail.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-rail.so.1.0
%attr(755,root,root) %{_libdir}/libfreerdp-utils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreerdp-utils.so.1.0
%dir %{_libdir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreerdp-cache.so
%attr(755,root,root) %{_libdir}/libfreerdp-channels.so
%attr(755,root,root) %{_libdir}/libfreerdp-codec.so
%attr(755,root,root) %{_libdir}/libfreerdp-core.so
%attr(755,root,root) %{_libdir}/libfreerdp-gdi.so
%attr(755,root,root) %{_libdir}/libfreerdp-kbd.so
%attr(755,root,root) %{_libdir}/libfreerdp-rail.so
%attr(755,root,root) %{_libdir}/libfreerdp-utils.so
%{_includedir}/freerdp
%{_pkgconfigdir}/freerdp.pc

%files plugins
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/audin.so
%attr(755,root,root) %{_libdir}/%{name}/cliprdr.so
%attr(755,root,root) %{_libdir}/%{name}/disk.so
%attr(755,root,root) %{_libdir}/%{name}/drdynvc.so
%attr(755,root,root) %{_libdir}/%{name}/parallel.so
%attr(755,root,root) %{_libdir}/%{name}/printer.so
%attr(755,root,root) %{_libdir}/%{name}/rail.so
%attr(755,root,root) %{_libdir}/%{name}/rdpdbg.so
%attr(755,root,root) %{_libdir}/%{name}/rdpdr.so
%attr(755,root,root) %{_libdir}/%{name}/rdpsnd.so
%attr(755,root,root) %{_libdir}/%{name}/serial.so
%attr(755,root,root) %{_libdir}/%{name}/tsmf.so

%if %{with alsa}
%files plugins-alsa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/audin_alsa.so
%attr(755,root,root) %{_libdir}/%{name}/rdpsnd_alsa.so
%attr(755,root,root) %{_libdir}/%{name}/tsmf_alsa.so
%endif

%if %{with ffmpeg}
%files plugins-ffmpeg
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/tsmf_ffmpeg.so
%endif

%if %{with pcsc}
%files plugins-pcsc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/scard.so
%endif

%if %{with pulseaudio}
%files plugins-pulse
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/audin_pulse.so
%attr(755,root,root) %{_libdir}/%{name}/rdpsnd_pulse.so
%attr(755,root,root) %{_libdir}/%{name}/tsmf_pulse.so
%endif
