export SHELL = sh
PACKAGE = wisqi
ICON = data/images/Wubi.ico
REVISION = 1
VERSION = 12.04
COPYRIGHTYEAR = 2009
AUTHOR = Agostino Russo
EMAIL = agostino.russo@gmail.com

all: build check

build: wisqi

wisqi: wisqi-pre-build
	PYTHONPATH=src tools/pywine -OO src/pypack/pypack --verbose --bytecompile --outputdir=build/wisqi src/main.py data build/bin build/version.py build/winboot build/translations
	PYTHONPATH=src tools/pywine -OO build/pylauncher/pack.py build/wisqi
	mv build/application.exe build/wisqi.exe

wisqizip: wisqi-pre-build
	PYTHONPATH=src tools/pywine src/pypack/pypack --verbose --outputdir=build/wisqi src/main.py data build/bin build/version.py build/winboot build/translations
	cp wine/drive_c/Python23/python.exe build/wisqi #TBD
	cd build; zip -r wisqi.zip wisqi

wisqi-pre-build: check_wine pylauncher winboot2 src/main.py src/wisqi/*.py cpuid version.py translations
	rm -rf build/wisqi
	rm -rf build/bin
	cp -a blobs build/bin
	cp wine/drive_c/windows/system32/python23.dll build/pylauncher || cp wine/drive_c/windows/syswow64/python23.dll build/pylauncher #TBD
	cp build/cpuid/cpuid.dll build/bin

pot:
	xgettext --default-domain="$(PACKAGE)" --output="po/$(PACKAGE).pot" $(shell find src/wisqi -name "*.py" | sort)
	sed -i 's/SOME DESCRIPTIVE TITLE/Translation template for $(PACKAGE)/' po/$(PACKAGE).pot
	sed -i "s/YEAR THE PACKAGE'S COPYRIGHT HOLDER/$(COPYRIGHTYEAR)/" po/$(PACKAGE).pot
	sed -i 's/FIRST AUTHOR <EMAIL@ADDRESS>, YEAR/$(AUTHOR) <$(EMAIL)>, $(COPYRIGHTYEAR)/' po/$(PACKAGE).pot
	sed -i 's/Report-Msgid-Bugs-To: /Report-Msgid-Bugs-To: $(EMAIL)/' po/$(PACKAGE).pot
	sed -i 's/CHARSET/UTF-8/' po/$(PACKAGE).pot
	sed -i 's/PACKAGE VERSION/$(VERSION)-r$(REVISION)/' po/$(PACKAGE).pot
	sed -i 's/PACKAGE/$(PACKAGE)/' po/$(PACKAGE).pot

update-po: pot
	for i in po/*.po ;\
	do \
	mv $$i $${i}.old ; \
	(msgmerge $${i}.old po/wisqi.pot | msgattrib --no-obsolete > $$i) ; \
	rm $${i}.old ; \
	done

translations: po/*.po
	mkdir -p build/translations/
	@for po in $^; do \
		language=`basename $$po`; \
		language=$${language%%.po}; \
		target="build/translations/$$language/LC_MESSAGES"; \
		mkdir -p $$target; \
		msgfmt --output=$$target/$(PACKAGE).mo $$po; \
	done

version.py:
	$(shell echo 'version = "$(VERSION)"' > build/version.py)
	$(shell echo 'revision = $(REVISION)' >> build/version.py)
	$(shell echo 'application_name = "$(PACKAGE)"' >> build/version.py)

pylauncher: 7z src/pylauncher/*
	cp -rf src/pylauncher build
	cp "$(ICON)" build/pylauncher/application.ico
	sed -i 's/application_name/$(PACKAGE)/' build/pylauncher/pylauncher.exe.manifest
	cd build/pylauncher; make

cpuid: src/cpuid/cpuid.c
	cp -rf src/cpuid build
	cd build/cpuid; make

winboot2:
	mkdir -p build/winboot
	cp -f data/wisildr.cfg data/wisildr-bootstrap.cfg build/winboot/
	grub-ntldr-img --grub2 --boot-file=wisildr -o build/winboot/wisildr.mbr
	cd build/winboot && tar cf wisildr.tar wisildr.cfg
	mkdir -p build/grubutil
	grub-mkimage -O i386-pc -c build/winboot/wisildr-bootstrap.cfg -m build/winboot/wisildr.tar -o build/grubutil/core.img \
		loadenv biosdisk part_msdos part_gpt fat ntfs ext2 ntfscomp iso9660 loopback search linux boot minicmd cat cpuid chain halt help ls reboot \
		echo test configfile gzio normal sleep memdisk tar font gfxterm gettext true vbe vga video_bochs video_cirrus probe
	cat /usr/lib/grub/i386-pc/lnxboot.img build/grubutil/core.img > build/winboot/wisildr

winboot: grub4dos grubutil
	mkdir -p build/winboot
	cp -f data/menu.winboot build/winboot/menu.lst
	cp -f build/grub4dos/stage2/grldr build/winboot/wisildr
	cp -f build/grub4dos/stage2/grub.exe build/winboot/wisildr.exe
	dd if=build/winboot/wisildr of=build/winboot/wisildr.mbr bs=1 count=8192
	cd build/winboot; ../grubutil/grubinst/grubinst -o -b=wisildr wisildr.mbr

grub4dos: src/grub4dos/*
	cp -rf src/grub4dos build
	cd build/grub4dos;./configure --enable-preset-menu=../../data/menu.winboot
	cd build/grub4dos; make

grubutil: src/grubutil/grubinst/*
	cp -rf src/grubutil build
	cd build/grubutil/grubinst; make

# not compiling 7z at the moment, but source is used by pylauncher
7z: src/7z/C/*.c
	cp -rf src/7z build

runbin: wisqi
	rm -rf build/test
	mkdir build/test
	cd build/test; ../../tools/wine ../wisqi.exe --test

check_wine: tools/check_wine
	tools/check_wine

unittest:
	tools/pywine tools/test

check: wisqi
	tests/run

runpy:
	PYTHONPATH=src tools/pywine src/main.py --test

clean:
	rm -rf dist/*
	rm -rf build/*

.PHONY: all build test wisqi wisqizip wisqi-pre-build pot runpy runbin ckeck_wine unittest
	7z translations version.py pylauncher winboot grubutil grub4dos
