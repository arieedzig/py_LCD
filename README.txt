===============================================================================
24.03.2014, Henning Aust

Using Nokia 3310 UEXT-Module on UEXT2 of Olimexino A20

This work is derived from the mod-lcd3310 for iMX233:
https://github.com/OLIMEX/OLINUXINO/tree/master/SOFTWARE/iMX233/MOD-LCD3310

and the pcd8544 python module:
https://github.com/N8body/pcd8544

===============================================================================
How it works: As there seems to be no working out of the box support for spi
on the A20-Chips I implemented soft-spi using the GPIO packeage.

In order to be able to use the UEXT-pins as GPIOs you have to edit the 
script.bin/fex file. You also have to add the PIN-names to the pyA20 package.

That's it.

===============================================================================

Download the pyA20 package: 

https://pypi.python.org/pypi/pyA20/0.1.3

and add the UEXT2 Pins to the file:

diff:

35a36,44
> // UEXT2
> #define PIN_PI16      SUNXI_GPI(16)
> #define PIN_PI17      SUNXI_GPI(17)
> #define PIN_PI18      SUNXI_GPI(18)
> #define PIN_PI19      SUNXI_GPI(19)
> #define PIN_PB18      SUNXI_GPB(18)
> #define PIN_PB19      SUNXI_GPB(19)
>
>
297a307
> // UEXT 2
298a309,314
>       PyModule_AddObject(module, "PIN_PI16", Py_BuildValue("i", PIN_PI16));
>       PyModule_AddObject(module, "PIN_PI17", Py_BuildValue("i", PIN_PI17));
>       PyModule_AddObject(module, "PIN_PI18", Py_BuildValue("i", PIN_PI18));
>       PyModule_AddObject(module, "PIN_PI19", Py_BuildValue("i", PIN_PI19));
>       PyModule_AddObject(module, "PIN_PB18", Py_BuildValue("i", PIN_PB18));
>       PyModule_AddObject(module, "PIN_PB19", Py_BuildValue("i", PIN_PB19));


then make and reinstall the package

===============================================================================
Copy script.bin and use bin2fex from the sunxi-tools to convert into a readable 
fex-file, see this manual to bin/fex-file:
http://linux-sunxi.org/Fex_Guide

You maybe will need to download and install the sunxi-tools.

edit script.fex so that the UEXT2 pins are configured as GPIOs at startup:

turn off twi1:

[twi1_para]
twi1_used = 0

turn off spi1 (we are using soft-spi on the spi pins, as there is no out of 
the box supprt for spi on A20 up to now that seems to work):

[spi1_para]
spi_used = 0

Change number of GPIOS:


[gpio_para]
gpio_used = 1
gpio_num = 81

add the lines  for the UEXT pins to the big GPIO-para-block:

gpio_pin_76 = port:PI16<1><default><default><default>
gpio_pin_77 = port:PI17<1><default><default><default>
gpio_pin_78 = port:PI18<1><default><default><default>
gpio_pin_79 = port:PI19<0><default><default><default>
gpio_pin_80 = port:PB18<1><default><default><default>
gpio_pin_81 = port:PB19<1><default><default><default>

and the pins to the gpio-init-block:

pin_76 = port:PI16<1><default><default><default>
pin_77 = port:PI17<1><default><default><default>
pin_78 = port:PI18<1><default><default><default>
pin_79 = port:PI19<0><default><default><default>
pin_80 = port:PB18<1><default><default><default>
pin_81 = port:PB19<1><default><default><default>


Reboot and enjoy soft-spi on UEXT2!

===============================================================================
Using py_LCD together with sys_info.py to show CPU-Load, Uptime etc 
+ making sys_info.py start at system start.

Note: This works on Debian not Android

To start the python script at system start do the following steps:
-download the files from git:
	git clone https://github.com/HenningAust/py_LCD

-copy the folder to /opt: 
	cp -r py_LCD /opt

-to run the scipt at system start we need to add an init script. I create on based on the skeleton file in /etc/init.d/ it is in the support folder, copy it over to /etc/init.d/
	cp support/lcdSysInfo /etc/init.d/

-you can check if everything works up to here by starting the script:
	cd /etc/init.d
	./lcdSysInfo start

-If it works we have to add it to the standard default runlevel to start the script at boot time:
	update-rc.d lcdSysInfo defaults


