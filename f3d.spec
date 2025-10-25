%define major 1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

# Use only one of this
%bcond_without	java
%bcond_without	python
%bcond_without	plugin_alembic
%bcond_with	plugin_assimp
%bcond_without	plugin_draco
%bcond_without	plugin_exodus
%bcond_without	plugin_occt

Summary:	Fast and minimalist 3D viewer
Name:		f3d
Version:	3.3.0
Release:	1
License:	BSD
Group: 		Graphics
URL:		https://f3d.app
Source0:	https://github.com/%{name}-app/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:	cmake ninja
%if %{with plugin_alembic}
BuildRequires:	cmake(Alembic)
%endif
BuildRequires:	cmake(double-conversion)
BuildRequires:	cmake(expat)
BuildRequires:	cmake(FastFloat)
BuildRequires:	cmake(Imath)
BuildRequires:	cmake(jsoncpp)
%if %{with plugin_occt}
BuildRequires:	cmake(OpenCASCADE)
%endif
BuildRequires:	cmake(nlohmann_json)
BuildRequires:	cmake(netcdf)
BuildRequires:	cmake(pybind11)
BuildRequires:	cmake(tbb)
BuildRequires:	cmake(utf8cpp)
BuildRequires:	cmake(Verdict)
BuildRequires:	cmake(vtk)
BuildRequires:	freeimage-devel
BuildRequires:	hdf5-devel
BuildRequires:	help2man
BuildRequires:	pkgconfig
%if %{with plugin_assimp}
BuildRequires:	pkgconfig(assimp)
%endif
%if %{with plugin_draco}
BuildRequires:	pkgconfig(draco)
%endif
BuildRequires:	pkgconfig(eigen3)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(tbb)
BuildRequires:	pkgconfig(tbbmalloc)
BuildRequires:	stdc++-static-devel

%description
F3D is a VTK-based 3D viewer following the KISS principle, so it is
minimalist, efficient, has no GUI, has simple interaction mechanisms and is
fully controllable using arguments in the command line.

%files
%license LICENSE.md
%doc README.md
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*
%{_libdir}/lib%{name}-plugin-*.so
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-plugin-*.desktop
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/plugins
%{_datadir}/%{name}/plugins/*.json
%{_datadir}/icons/hicolor/*/apps/%{name}.??g
%{_datadir}/icons/HighContrast/scalable/apps/f3d.svg
%{_datadir}/metainfo/app.%{name}.F3D.metainfo.xml
%dir %{_datadir}/thumbnailers
%{_datadir}/thumbnailers/%{name}*.thumbnailer
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}
%{_mandir}/man?/%{name}.*

#---------------------------------------------------------------------------

%package devel
Summary:	Fast and minimalist 3D viewer
License:	BSD
Group:		System/Libraries
Requires:	f3d = %{EVRD}
#Provides:	%{name}-devel = %{version}
#Provides:	lib%{name}-devel = %{version}

%description devel
Development files and samples for the f3d.

%files devel
%license LICENSE.md
%{_libdir}/lib%{name}.so
%{_libdir}/libvtkext.so

#---------------------------------------------------------------------------

%if %{with python}
%package python
Summary:		Python bindings for the %{name}
Group:			Development/Python
BuildRequires:	pkgconfig(python)
Requires:		%{name} = %{EVRD}
Provides:		python-%{name} = %{version}-%{release}

%description python
The python-%{name} package contains Python bindings for %{name}.

%files python
%dir %{python3_sitearch}/%{name}
%{python3_sitearch}/%{name}/__init__.py
%{python3_sitearch}/%{name}/py%{name}.cpython-*-%{_arch}-linux-gnu*.so
%endif

#---------------------------------------------------------------------------

%if %{with java}
%package java
Summary:		Python bindings for the %{name}
Group:			Development/Java
BuildRequires:	jdk-current
BuildRequires:	jre-gui-current
Requires:		%{name} = %{EVRD}
Provides:		python-%{name} = %{version}-%{release}

%description java
The %{name}-java package contains Java bindings for %{name}.

%files java
%{_libdir}/lib%{name}-java.so
%{_datadir}/java/%{name}.jar
%endif

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib"
%cmake \
	-DBUILD_TESTING=%{?with_testing:ON}%{?!with_testing:OFF} \
	-DF3D_BINDINGS_JAVA:BOOL=%{?with_java:ON}%{?!with_java:OFF} \
	-DF3D_BINDINGS_PYTHON:BOOL=%{?with_python:ON}%{?!with_python:OFF} \
	-DF3D_LINUX_APPLICATION_LINK_FILESYSTEM:BOOL=ON \
	-DF3D_LINUX_GENERATE_MAN:BOOL=ON \
	-DF3D_LINUX_INSTALL_DEFAULT_CONFIGURATION_FILE_IN_PREFIX:BOOL=ON \
	-DF3D_MODULE_EXTERNAL_RENDERING:BOOL=OFF \
	-DF3D_MODULE_RAYTRACING:BOOL=OFF \
	-DF3D_PLUGINS_STATIC_BUILD:BOOL=OFF \
	-DF3D_PLUGIN_BUILD_ALEMBIC:BOOL=%{?with_plugin_alembic:ON}%{?!with_plugin_alembic:OFF} \
	-DF3D_PLUGIN_BUILD_ASSIMP:BOOL=%{?with_plugin_assimp:ON}%{?!with_plugin_assimp:OFF} \
	-DF3D_PLUGIN_BUILD_DRACO:BOOL=%{?with_plugin_draco:ON}%{?!with_plugin_draco:OFF} \
	-DF3D_PLUGIN_BUILD_EXODUS:BOOL=%{?with_plugin_exodus:ON}%{?!with_plugin_exodus:OFF} \
	-DF3D_PLUGIN_BUILD_OCCT:BOOL=%{?with_plugin_occt:ON}%{?!with_plugin_occt:OFF} \
	-GNinja
%ninja_build

%install
export LD_LIBRARY_PATH="$(pwd)/build/lib"
%ninja_install -C build

# remove static studd
#rm -fv %{buildroot}%{_libdir}/libVTKExtensions*.a

# install docs manually
rm -frv %{buildroot}%{_datadir}/doc/F3D

%check
%if %{with tests}
LD_LIBRARY_PATH="$(pwd)/build/lib" \
%ninja_test -C build
%endif

