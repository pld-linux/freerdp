Summary:	Remote Desktop Protocol client
Name:		freerdp
Version:	1.0.1
Release:	0.1
License:	ASL 2.0
Group:		Applications/Communications
URL:		http://www.freerdp.com/
Source0:	https://github.com/downloads/FreeRDP/FreeRDP/%{name}-%{version}.tar.gz
# https://github.com/FreeRDP/FreeRDP/commit/165d39a290a109c0af16a1d223d1426cb524a844 backport
Patch0:		fastpath_send_input_pdu-sec_bytes.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	cmake
BuildRequires:	cups-devel
BuildRequires:	desktop-file-utils
BuildRequires:	libXcursor-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXv-devel
BuildRequires:	libxkbfile-devel
BuildRequires:	openssl-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-plugins%{?_isa} = %{version}-%{release}
Provides:	xfreerdp = %{version}-%{release}

%description
The xfreerdp Remote Desktop Protocol (RDP) client from the FreeRDP
project.

xfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.


%package        libs
%description    libs
libfreerdp-core can be embedded in applications.

libfreerdp-channels and libfreerdp-kbd might be convenient to use in X
applications together with libfreerdp-core.

libfreerdp-core can be extended with plugins handling RDP channels.


%package        plugins
%description    plugins
A set of plugins to the channel manager implementing the standard
virtual channels extending RDP core functionality. For instance,
sounds, clipboard sync, disk/printer redirection, etc.


%package        devel
Summary:	Core libraries implementing the RDP protocol
Summary:	Development files for %{name}
Summary:	Plugins for handling the standard RDP channels
Group:		Applications/Communications
Group:		Applications/Communications
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}-libs.


%prep

%setup -q
%patch0 -p1

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

%cmake \
		-DWITH_CUPS=ON \
		-DWITH_PCSC=ON \
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
		.

%{__make} %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

# No need for keymap files when using xkbfile
rm -rf $RPM_BUILD_ROOT%{_datadir}/freerdp

desktop-file-install --dir=$RPM_BUILD_ROOT%{_desktopdir} xfreerdp.desktop
install -p -D resources/FreeRDP_Icon_256px.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png


%clean
rm -rf $RPM_BUILD_ROOT


%post
# This is no gtk application, but try to integrate nicely with GNOME if it is available
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


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
