py_LCD
======
06.11.2014, arieedzig

Python package for using MOD Nokia 3310 with Olinuxino A20 on UEXT2

This is only a fork from HenningAust py_LCD:
https://github.com/HenningAust/py_LCD
I only adapt this script to the newer version of pyA20

===============================================================================

Download the pyA20EVB package: 

      # svn export https://github.com/OLIMEX/OLINUXINO/trunk/SOFTWARE/Python/
      # cd pyA10Lime
      # python setup.py install

or

      pip install pyA20EVB

===============================================================================
Using py_LCD together with sys_info.py to show CPU-Load, Uptime etc 
+ making sys_info.py start at system start.

Note: This works on Debian not Android

To start the python script at system start do the following steps:
-download the files from git:

	git clone https://github.com/arieedzig/py_LCD

-copy the folder to /opt:

	cp -r py_LCD /opt

-to run the scipt at system start we need to add an init script. I create on based on the skeleton file in /etc/init.d/ it is in the support folder, copy it over to /etc/init.d/

	cp support/lcdSysInfo /etc/init.d/

-you can check if everything works up to here by starting the script:

	cd /etc/init.d
	./lcdSysInfo start

-If it works we have to add it to the standard default runlevel to start the script at boot time:

	update-rc.d lcdSysInfo defaults
