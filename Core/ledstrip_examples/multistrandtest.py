# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *

# LED strip configuration:
LED_1_COUNT      = 60      # Number of LED pixels.
LED_1_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA        = 5       # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL    = 0       # 0 or 1
LED_1_STRIP      = ws.SK6812_STRIP_GRBW	

LED_2_COUNT      = 15      # Number of LED pixels.
LED_2_PIN        = 13      # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_2_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_2_CHANNEL    = 1       # 0 or 1
LED_2_STRIP      = ws.WS2811_STRIP_GRB	

def multiColorWipe(color1, color2, wait_ms=5):
	global strip1
	global strip2
	"""Wipe color across multiple LED strips a pixel at a time."""
	for i in range(strip1.numPixels()):
		if i % 2:
			# even number
			strip1.setPixelColor(i, color1)
			strip2.setPixelColor(i / 2, color2)
			strip1.show()
			time.sleep(wait_ms/1000.0)
			strip2.show()
			time.sleep(wait_ms/1000.0)
		else:
			# odd number
			strip1.setPixelColor(i, color1)
			strip1.show()
			time.sleep(wait_ms/1000.0)
	time.sleep(1)


def heavy_flash(strip):
        a = 0.055
        b = 0.007
        while True:
                for i in range(0,60,1):
                        strip.setPixelColor(i, Color(200,0,255,100))
                strip.show()
                time.sleep(b)
                for i in range(0,60,1):
                        strip.setPixelColor(i, Color(0,0,0,0))
                strip.show()
                time.sleep(a)
                
                


def blackout(strip):
	for i in range(max(strip1.numPixels(), strip1.numPixels())):
		strip.setPixelColor(i, Color(0,0,0))
		strip.show()

# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel objects with appropriate configuration for each strip.
	strip1 = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL, LED_1_STRIP)

	# Intialize the library (must be called once before other functions).
	strip1.begin()

	print ('Press Ctrl-C to quit.')

	# Black out any LEDs that may be still on for the last run
	blackout(strip1)

##	while True:
##
##		# Multi Color wipe animations.
##		multiColorWipe(Color(255, 0, 0), Color(255, 0, 0))  # Red wipe
##		multiColorWipe(Color(0, 255, 0), Color(0, 255, 0))  # Blue wipe
##		multiColorWipe(Color(0, 0, 255), Color(0, 0, 255))  # Green wipe
##		multiColorWipe(Color(255, 255, 255), Color(255, 255, 255))  # Composite White wipe
##		multiColorWipe(Color(0, 0, 0, 255), Color(0, 0, 0))  # White wipe
##		multiColorWipe(Color(255, 255, 255, 255), Color(0, 0, 0))  # Composite White + White LED wipe
##
        while True:
                heavy_flash(strip1)
                
