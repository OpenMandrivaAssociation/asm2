%define gcj_support 1
%define section	free

Name:		asm2
Version:	2.2.3
Release:	%mkrel 6
Epoch:		0
Summary:	A code manipulation tool to implement adaptable systems
License:	BSD-like
URL:		http://asm.objectweb.org/
Group:		Development/Java
#Vendor:		JPackage Project
#Distribution:	JPackage
Source0:	http://download.fr2.forge.objectweb.org/asm/asm-2.2.3.tar.bz2
BuildRequires:	ant
BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	objectweb-anttask
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ASM is a code manipulation tool to implement adaptable systems.

%package	javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description	javadoc
Javadoc for %{name}.

%prep
%setup -q -n asm-%{version}
find . -name "*.jar" -exec %{__rm} -f {} \;
%{__mkdir_p} test/lib
%{__perl} -pi -e 's|.*<attribute name="Class-path".*||' archive/asm-xml.xml

%build
export CLASSPATH=
export OPT_JAR_LIST=
%ant -Dobjectweb.ant.tasks.path=$(build-classpath objectweb-anttask) jar jdoc

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}/%{name}

for jar in output/dist/lib/*.jar; do
newjar=${jar/asm-/asm2-}
%{__install} -m 644 ${jar} \
%{buildroot}%{_javadir}/%{name}/`basename ${newjar}`
done

(cd %{buildroot}%{_javadir}/%{name} && for jar in *-%{version}*; do \
%{__ln_s} ${jar} ${jar/-%{version}/}; done)

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a output/dist/doc/javadoc/user/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

# fix end-of-line
%{__perl} -pi -e 's/\r$//g' README.txt

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc README.txt
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %dir %{_javadocdir}/%{name}

