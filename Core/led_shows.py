import time
from threading import Thread
from neopixel import *
from led_functions import *

run_slowchange = True

def music_maestro(strip):

    global  run_slowchange
    magic_purple = Color(255,0,170,5)
    warm_orange = Color(255,40,0,0)
    under_water = Color(0,255,255,0)
    greenery = Color(0,255,100,0)
    false_white = Color(150,150,255,0)
    UV_purple = Color(30,0,255,0)


    bright_red = Color(255,0,0,70)
    bright_green = Color(0,255,0,70)
    run_slowchange = True
    z = 0
    while z < 15:
        Turn_leds_on_one_by_one(strip, 3, magic_purple, 0,59  )
        time.sleep(10)
        Turn_leds_on_one_by_one(strip, 3, warm_orange, 59, 0)
        time.sleep(1)
        Turn_leds_on_one_by_one(strip, 1.5, magic_purple, 0, 29)
        time.sleep(1)
        Turn_leds_on_one_by_one(strip, 1.5, magic_purple, 59, 30)
        time.sleep(10)
        Turn_leds_on_merging(strip, 3, warm_orange, 10)
        time.sleep(3)
        Turn_leds_on_merging(strip, 2, under_water, 10)
        time.sleep(3)
        Turn_leds_on_one_by_one(strip, 0.05,  UV_purple, 0, 59)
        time.sleep(10)
        Turn_leds_on_one_by_one(strip, 0.05, bright_green, 59, 0)
        time.sleep(5)
        i = 0
        while i < 3:
            i +=1
            Turn_leds_on_merging(strip, 0.5, false_white, 10)
            time.sleep(1.5)
            Turn_leds_on_merging(strip, 0.5, greenery, 10)
            time.sleep(1.5)
            Turn_leds_on_merging(strip, 0.5, bright_red, 10)
            time.sleep(1.5)
        while i < 3:
            i +=1
            Turn_leds_on_merging(strip, 0.5, magic_purple, 10)
            time.sleep(1.5)
            Turn_leds_on_merging(strip, 0.5, bright_green, 10)
            time.sleep(1.5)
            Turn_leds_on_merging(strip, 0.5, under_water, 10)
            time.sleep(1.5)

        z += 1



#strip1, total_time, colorb, start, stop













def Gently_wake_up(strip1):
    All_off(strip1)
    bright_color = Color(0, 0, 0)  # simulates sunlight
    shine_color = Color(252, 239, 157)  # simulates morning light
    sky_color = Color(116, 198, 238)  # simulates blue sky

    Turn_leds_on_one_by_one(strip1, 100, Color(120, 10, 0, 40), 0, 60)  ## rode ochtendgloed
    time.sleep(10)
    Turn_leds_on_merging(strip1,20, Color(160, 30, 10, 100), 5)
    sunintro1 = Thread(target=Turn_leds_on_one_by_one, args=(strip1, 100, Color(130, 60, 80, 180), 59, 44))
    sunintro1.start()
    sunintro2 = Thread(target=Turn_leds_on_one_by_one, args=( strip1, 100, Color(130, 60, 80, 180), 0, 16))
    sunintro2.start()
    time.sleep(30)
    Turn_leds_on_merging(strip1, 120, Color(20, 60, 255, 255), 6)


def dynamicinput(strip, colorlist, clist, colorgen, action, a, b, x, y, fad, timeabrupt):

    ##### pick colors out of colorlist ####
    color1 = return_color(colorlist[0])
    color2 = return_color(colorlist[1])
    color3 = return_color(colorlist[2])
    color4 = return_color(colorlist[3])



    color_inputs = []
    for i in range(0,3):
        if clist[i] == "01":
            color_inputs.append(color1)
        if clist[i] == "02":
            color_inputs.append(color2)
        if clist[i] == "03":
            color_inputs.append(color3)
        if clist[i] == "04":
            color_inputs.append(color4)

    if colorgen == "01":
        colorask = 1
    if colorgen == "02":
        colorask = 2
    if colorgen =="03":
        colorask = 3












def return_color(color_code):
    colors = [Color(0,0,0,0),Color(0,0,0,0),Color(0,0,0,0),Color(0,0,0,0),Color(0,0,0,0),Color(0,0,0,0),Color(0,0,0,0),Color(0,0,0,0),Color(0,0,0,0),Color(0,0,0,0) ]




    if color_code == "01":
        c = colors[0]
    if color_code == "02":
        c = colors[1]
    if color_code == "03":
        c = colors[2]
    if color_code == "04":
        c = colors[3]
    if color_code == "05":
        c = colors[4]
    if color_code == "06":
        c = colors[5]
    if color_code == "07":
        c = colors[6]
    if color_code == "08":
        c = colors[7]
    if color_code == "09":
        c = colors[8]
    if color_code == "10":
        c = colors[9]


def give_colornow(colorask, color_inputs):
    if colorask == 1:
        return color_inputs[0]
