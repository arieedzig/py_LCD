#!/usr/bin/env python

from pyA20EVB.gpio import gpio as GPIO
from pyA20EVB.gpio import port
#import A20_GPIO as GPIO
from time import sleep
#from PIL import Image
from font import default_FONT
import struct



# Some constants / parameter
SEND_CHR = 1
SEND_CMD = 2
X_RANGE = 84
#Y_RANGE = 48
Y_RANGE = 50
DEFAULT_CONTRAST = 0xC0
LCD_CACHE_SIZE = X_RANGE*Y_RANGE/8
LCD_Memory = [0 for i in range(LCD_CACHE_SIZE)]
LCD_TEMP = [0 for i in range(X_RANGE)],[0 for i in range(Y_RANGE)]


GPIO.init();
# UEXT2
pin_CS = port.PI16 # SPI1-CS
pin_MOSI = port.PI18 #SPI1- MOSI
pin_MISO = port.PI19 #SPI1 MISO
pin_CLK = port.PI17 #SPI1 CLK
pin_RST = port.PB18 #UEXT PIN 5 LCD RESET
pin_DC = port.PB19 #UEXT PIN 6 LCD DC

# UEXT1
#pin_CS = port.PC19 # SPI2-CS
#pin_MOSI = port.PC21 #SPI2- MOSI
#pin_MISO = port.PC22 #SPI2 MISO
#pin_CLK = port.PC20 #SPI2 CLK
#pin_RST = port.PB20 #UEXT PIN 5 LCD RESET
#pin_DC = port.PB21 #UEXT PIN 6 LCD DC


GPIO.setcfg(pin_CS,GPIO.OUTPUT) # SPI1-CS
GPIO.setcfg(pin_MOSI,GPIO.OUTPUT)  #SPI1- MOSI
GPIO.setcfg(pin_MISO,GPIO.INPUT) #SPI1 MISO
GPIO.setcfg(pin_CLK,GPIO.OUTPUT) #SPI1 CLK
GPIO.setcfg(pin_RST,GPIO.OUTPUT) #UEXT PIN 5 LCD RESET
GPIO.setcfg(pin_DC,GPIO.OUTPUT) #UEXT PIN 6 LCD DC

def send(cmd,type):
	GPIO.output(pin_CS, GPIO.LOW)
	if(type == SEND_CHR):
		GPIO.output(pin_DC, GPIO.HIGH)
	else:	
		GPIO.output(pin_DC, GPIO.LOW)
	SPIsendByte(cmd)
	GPIO.output(pin_CS, GPIO.HIGH)


def SPIsendByte(byteTosend):
	i = 0
	for i in range(1,9):
		if (byteTosend & 0x80):
			GPIO.output(pin_MOSI, GPIO.HIGH)
		else:
			GPIO.output(pin_MOSI, GPIO.LOW)
		#sleep(0.00001)
		GPIO.output(pin_CLK, GPIO.LOW)
		#sleep(0.00001)
		GPIO.output(pin_CLK, GPIO.HIGH)
		byteTosend = byteTosend << 1

	return 

def update():
	x = 0
	y = 0
	for y in range(0,Y_RANGE/8):
		send(0x80,SEND_CMD)
#		send(0x40 | y, SEND_CMD)
		send(0x40 | (y+1), SEND_CMD)
		for x in range(X_RANGE):
			send(LCD_Memory[y*X_RANGE + x],SEND_CHR)

def clear():
	for i in range(len(LCD_Memory)):
			LCD_Memory[i]=0


def drawPoint(x,y):
	row = y/8
	i = x + row * 84
	LCD_Memory[i] |= 1 << (y % 8)

def drawLine(x1,y1,x2,y2):
	dx=abs(x2-x1)
	dy=abs(y2-y1)
	if(x1 < x2):	sx=1
	else:		sx=-1
	if(y1 < y2):	sy=1
	else:		sy=-1
	err=dx-dy
	while(1):
		drawPoint(x1,y1)
		if((x1==x2) & (y1==y2)):
			break
		e2 = 2*err
		if(e2 > -dy):
			err = err-dy
			x1 = x1+sx
		if(e2 < dx):
			err=err+dx
			y1=y1+sy

def drawRect(x1,y1,x2,y2):
	drawLine(x1,y1,x1,y2)
	drawLine(x1,y1,x2,y1)
	drawLine(x2,y1,x2,y2)
	drawLine(x1,y2,x2,y2)

def setContrast(contrast):
	send(0x21,SEND_CMD)
	send(0x14,SEND_CMD)
	send(contrast,SEND_CMD)
	send(0x20,SEND_CMD)
	send(0x0C,SEND_CMD)

def write(string):
	font = default_FONT
	i=0
	for i in string:
		tmp = font[i]
		for x in tmp:
			send(x,SEND_CHR)

def chrXY(x, y, chr):
	index=0
	offset=0
	i=0
	font = default_FONT
	
	if(x > X_RANGE): return
	if(y > Y_RANGE): return

	#index=x*6+y*84 
        index=x*5+y*84
	for i in range(6):
		if(i==5):
			LCD_Memory[index]=0
			break
		offset = font[chr][i]
		LCD_Memory[index]=offset
		index= index +1

def chrXYInverse(x, y, chr):
        index=0
        offset=0
        i=0
        font = default_FONT

        if(x > X_RANGE): return
        if(y > Y_RANGE): return

        index=x*5+y*84
        for i in range(6):
                if(i==5):
                        LCD_Memory[index]=255
                        break
                offset = ~(font[chr][i])
                LCD_Memory[index]=offset
                index= index +1


def str(row,string,inv=0):
	x = 0
	for i in string:
		if(inv):
		   chrXYInverse(x,row,i)
		else:
		   chrXY(x,row,i)
		x=x+1
	#update()

def longstr(row,string,inv=0):
        x = 0
        for i in string:
		if(inv):
                   chrXYInverse(x,row,i)
		else:
		   chrXY(x,row,i)
                x=x+1
		if(x==16):
			row=row+1
			x=0


# Reset LCD
def init():
	# SET CS HIGH
	GPIO.output(pin_CS, GPIO.HIGH)

	#Reset LCD
	GPIO.output(pin_RST, GPIO.LOW)
	sleep(1)
	GPIO.output(pin_RST, GPIO.HIGH)
	sleep(1)
	send(0x21,SEND_CMD)
	send(0xC8,SEND_CMD)
	send(0x04,SEND_CMD)
	send(0x40,SEND_CMD)
	send(0x12,SEND_CMD)
	send(0xE4,SEND_CMD)# Set Display offset line 1
	send(0x45,SEND_CMD)# Set Display offset line 2: shiftet 5  pixels up and then use lines 1 to 6
	send(0x20,SEND_CMD)
	send(0x08,SEND_CMD)
	send(0x0C,SEND_CMD)
	setContrast(DEFAULT_CONTRAST)
	clear()
	update()

