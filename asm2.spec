Name:		asm2
Version:	2.2.3
Release:	20
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
BuildRequires:	java-1.6.0-openjdk-devel
BuildArch:      noarch

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
cp -a output/dist/doc/javadoc/user/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

# fix end-of-line
%{__perl} -pi -e 's/\r$//g' README.txt

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

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %dir %{_javadocdir}/%{name}



%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0:2.2.3-10mdv2011.0
+ Revision: 662792
- mass rebuild

* Mon Nov 29 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.2.3-9mdv2011.0
+ Revision: 603186
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.2.3-8mdv2010.1
+ Revision: 522108
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0:2.2.3-7mdv2010.0
+ Revision: 413040
- rebuild

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 0:2.2.3-6mdv2009.0
+ Revision: 220357
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:2.2.3-5mdv2008.1
+ Revision: 120827
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:2.2.3-4mdv2008.0
+ Revision: 87205
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 08 2007 Adam Williamson <awilliamson@mandriva.org> 0:2.2.3-3mdv2008.0
+ Revision: 82310
- rebuild for 2008


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 2.2.3-2mdv2007.1
+ Revision: 144219
- rebuild for 2007.1
- Import asm2

* Mon Jul 24 2006 David Walluck <walluck@mandriva.org> 0:2.2.3-1mdv2007.0
- 2.2.3

* Mon Jun 05 2006 David Walluck <walluck@mandriva.org> 0:2.2.2-2mdv2007.0
- rebuild for libgcj.so.7
- own %%{_libdir}/gcj/%%{name}
- BuildRequires: java-gcj-compat-devel not java-gcj-compat

* Wed Apr 12 2006 David Walluck <walluck@mandriva.org> 0:2.2.2-1mdk
- 2.2.2
- remove Class-Path from asm2-xml manifest

* Wed Dec 07 2005 David Walluck <walluck@mandriva.org> 0:2.2-1mdk
- 2.2
- aot compile

* Sun May 29 2005 David Walluck <walluck@mandriva.org> 0:2.0.RC1-1.1mdk
- release

* Fri Mar 11 2005 Sebastiano Vigna <vigna at acm.org> 0:2.0.RC1-1jpp
- First release of the 2.0 line.

