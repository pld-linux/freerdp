# Conditional build:
#
%bcond_with	pcsc		# SmartCard support via PCSC-lite library

Summary:	Remote Desktop Protocol client
Name:		freerdp
Version:	1.0.1
Release:	0.1
License:	ASL 2.0
Group:		Applications/Communications
URL:		http://www.freerdp.com/
Source0:	https://github.com/downloads/FreeRDP/FreeRDP/%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	cups-devel
BuildRequires:	desktop-file-utils
BuildRequires:	openssl-devel
%{?with_pcsc:BuildRequires:	pcsc-lite-devel}
BuildRequires:	pulseaudio-devel
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libxkbfile
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-plugins = %{version}-%{release}
Provides:	xfreerdp = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The xfreerdp Remote Desktop Protocol (RDP) client from the FreeRDP
project.

xfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%package libs
Summary:	Core libraries implementing the RDP protocol
Group:		Applications/Communications

%description    libs
libfreerdp-core can be embedded in applications.

libfreerdp-channels and libfreerdp-kbd might be convenient to use in X
applications together with libfreerdp-core.

libfreerdp-core can be extended with plugins handling RDP channels.

%package plugins
Summary:	Plugins for handling the standard RDP channels
Group:		Applications/Communications
Requires:	%{name}-libs = %{version}-%{release}

%description    plugins
A set of plugins to the channel manager implementing the standard
virtual channels extending RDP core functionality. For instance,
sounds, clipboard sync, disk/printer redirection, etc.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}-libs.

%prep
%setup -q

cat << EOF > xfreerdp.desktop
[Desktop Entry]
Type=Application
Name=X FreeRDP
NoDisplay=true
Comment=Connect to RDP server and display remote desktop
Icon=%{name}
Exec=%{_bindir}/xfreerdp
Terminal=false
Categories=Network;RemoteAccess;
EOF

%build
install -d build
cd build
%cmake \
	-DWITH_CUPS=ON \
	%{?with_pcsc:-DWITH_PCSC=ON} \
	-DWITH_PULSEAUDIO=ON \
	-DWITH_X11=ON \
	-DWITH_XCURSOR=ON \
	-DWITH_XEXT=ON \
	-DWITH_XINERAMA=ON \
	-DWITH_XKBFILE=ON \
	-DWITH_XV=ON \
	-DWITH_ALSA=OFF \
	-DWITH_CUNIT=OFF \
	-DWITH_DIRECTFB=OFF \
	-DWITH_FFMPEG=OFF \
	-DWITH_SSE2=OFF \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	..

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
# This is no gtk application, but try to integrate nicely with GNOME if it is available
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xfreerdp
%{_mandir}/man1/xfreerdp.*
%{_desktopdir}/xfreerdp.desktop
%{_iconsdir}/hicolor/256x256/apps/%{name}.png

%files libs
%defattr(644,root,root,755)
%doc LICENSE README ChangeLog
%{_libdir}/lib%{name}-*.so.*
%dir %{_libdir}/%{name}/

%files plugins
%defattr(644,root,root,755)
%{_libdir}/%{name}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}/
%{_libdir}/lib%{name}-*.so
%{_pkgconfigdir}/%{name}.pc
