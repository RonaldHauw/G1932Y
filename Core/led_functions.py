# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
from threading import Thread
from neopixel import *



# Black out any LEDs that may be still on for the last run

def Color_all_leds(strip1,R,G,B, W):
    """
    geeft elke led in de ledstrip een kleur zoals opgegeven in color
    :param color:
    :return:
    """
    color = Color(R,G,B,W)
    for i in range(0, 60):
        strip1.setPixelColor(i, color)
    strip1.show()


def Color_pattern(strip, R, G, B, W, x, y):
    color = Color(R, G, B, W)
    for i in range(0,60, y):
        for k in range(0,x):
            strip.setPixelColor(i+k, color)
            strip.show()

def All_leds_off(strip1):
    for i in range(max(strip1.numPixels(), strip1.numPixels())):
        strip1.setPixelColor(i, Color(0, 0, 0))
        strip1.show()


def Change_global_brightness(strip1,brightness):
    if brightness > 0 and brightness< 256:
        strip1.setBrightness(brightness)
        strip1.show()
    else:
        print "ERROR!!"


def Led_train(strip1, color, time, direction, length):
    wait_time = float(time)/float(60)
    mem = []
    for index in range(0,60 + length-1):
        if index < 60:
            oldcol = strip1.getPixelColor(index)
            mem.append(oldcol)
            strip1.setPixelColor(index, color)
        if index - length + 1 >= 0:
            strip1.setPixelColor(index-length, mem[index-length + 1])


def Turn_leds_on_one_by_one(strip1, total_time, colorb, start, stop):
    if total_time == "pass":
        skip = True
    else:
        skip = False
    if start > stop:
        direc = -1
    else:
        direc = 1
    intermed_time = float(total_time) / float(60)

    for i in range(start, stop + 1, direc):
        strip1.setPixelColor(i, colorb)
        strip1.show()
        if not skip:
            time.sleep(intermed_time)


def Let_leds_run(strip1, total_time, start_begin, stop_begin, change, coloractive, colorpassive):
    if change < 0:
        direc = -1
        change = -change
    else:
        direc = 1
    intermed_time = float(total_time) / float(change)
    for k in range(1, change + 1):
        new = stop_begin + direc * k
        old = start_begin + direc * (k - 1)
        strip1.setPixelColor(new, coloractive)
        strip1.setPixelColor(old, colorpassive)
        strip1.show()
        time.sleep(intermed_time)


def Turn_leds_on_merging(strip1, total_time, colorb, max_leds_zone):
    """ Divides strip in 6 zones with 10 leds and turns those leds on one by one
"""
    intermed_time = float(total_time) / float(10)
    for k in range(0, max_leds_zone):
        for i in range(0, 6):
            begin_led = i * 10
            cur_led = begin_led + k
            strip1.setPixelColor(cur_led, colorb)
            strip1.show()
        time.sleep(intermed_time)


def multiColorWipe(strip1, color1, wait_ms=5):
    """Wipe color across multiple LED strips a pixel at a time."""
    for i in range(strip1.numPixels()):
        if i % 2:
            # even number
            strip1.setPixelColor(i, color1)
            strip1.show()
            time.sleep(wait_ms / 1000.0)
        else:
            # odd number
            strip1.setPixelColor(i, color1)
            strip1.show()
            time.sleep(wait_ms / 1000.0)
    time.sleep(1)


def blackout(strip1):
    for i in range(max(strip1.numPixels(), strip1.numPixels())):
        strip1.setPixelColor(i, Color(0, 0, 0))
        strip1.show()


def All_off(strip1):
    blackout(strip1)







