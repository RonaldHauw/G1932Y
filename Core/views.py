from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
import models
from .forms import AlarmForm, QuickAlarmForm
from django.template.response import TemplateResponse
import Alarmauxilary
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from forms import *
from threading import Thread
import led_functions
from neopixel import *
import led_shows


## views zal altijd de ledstrip initialiseren !! elke functionaliteit met leds verloopt dus via views
# LED strip configuration:
LED_1_COUNT = 60  # Number of LED pixels.
LED_1_PIN = 18  # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA = 5  # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 128  # Set to 0 for darkest and 255 for brightest
LED_1_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL = 0  # 0 or 1
LED_1_STRIP = ws.SK6812_STRIP_GRBW


# Create NeoPixel objects with appropriate configuration for each strip.
strip1 = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL, LED_1_STRIP)

# Intialize the library (must be called once before other functions).
strip1.begin()

global Alarmisrunning





def Change_led(request,id):
    global strip1
    if id == "0":
        if request.method == 'POST':

            form = change_led_1(request.POST)
            R  = int(form['R'].value())
            G = int(form['G'].value())
            B = int(form['B'].value())
            W = int(form['W'].value())
            Brig = int(form['Brig'].value())
            x = int(form['x'].value())
            y = int(form['y'].value())
            color = Color(R,G,B,W)
            led_functions.Turn_leds_on_one_by_one(strip1, 0.1, color, x, y)
            led_functions.Change_global_brightness(strip1, Brig)


    if id == "1":
        if request.method == 'POST':
            form = change_led_1(request.POST)
            R = int(form['R'].value())
            G = int(form['G'].value())
            B = int(form['B'].value())
            W = int(form['W'].value())
            x = int(form['x'].value())
            y = int(form['y'].value())
            led_functions.Color_pattern(strip1, R, G, B, W, x, y)

    if id =="2":
        if request.method == 'POST':
            form = dynamic_input(request.POST)
            x = int(form['x'].value())
            y = int(form['y'].value())
            a = int(form['a'].value())
            b = int(form['b'].value())
            fad = int(form['fad'].value())
            timeabrupt = int(form['timeabrupt'].value())
            color1 = form['color1'].value()
            color2 = form['color2'].value()
            color3 = form['color3'].value()
            color4 = form['color4'].value()
            colorgen = form['colorgen'].value()
            c1 = form['c1'].value()
            c2 = form['c2'].value()
            c3 = form['c3'].value()
            action = form['action'].value()

            colorlist = [color1, color2, color3, color4]
            clist = [c1, c2, c3]

            led_shows.dynamicinput(strip1, colorlist, clist, colorgen, action, a, b, x, y, fad, timeabrupt)

    if id =="01":
        proc = Thread(target =led_shows.music_maestro, args=[strip1])
        proc.start()
                    



    if id == "02":
        led_shows.run_slowchange = False

    return HttpResponseRedirect("/C/controller/#about")


def CLogin(request):

    username = request.POST['inputUser']
    password = request.POST['inputPassword']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/C/")
    else:
        template = loader.get_template('Denied.html')
        return HttpResponse(template.render(request))

def CShowlogin(request):
    template = loader.get_template('CSignin.html')
    return HttpResponse(template.render(request))

def Controller(request):
    template = loader.get_template('ledstrip.html')
    return HttpResponse(template.render(request))



def Startday(request):
    global strip1
    if not 'Alarmisrunning' in globals():
        Alarmisrunning = False
    if not Alarmisrunning:
        Alarmauxilary.start(strip1)
        Alarmisrunning = True
        global Alarmisrunning
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request))

@login_required(login_url='/C/login')
def Setalarm(request):
    if request.method == 'POST':

        form = AlarmForm(request.POST)

        curalarm = models.Alarm()


        name = form['name'].value()
        time = form.data['time']
        type = form['type'].value()
        days = request.POST.getlist('days[]')
        curalarm.__addalarm__(name, time,days,type)

    return HttpResponseRedirect('/C/thanks/')

@login_required(login_url='/C/login')
def Setquickalarm(request):
    if request.method == 'POST':

        form = QuickAlarmForm(request.POST)

        curalarm = models.Quickalarm()

        time = form.data['time']
        type = form['type'].value()
        curalarm.__addquickalarm__(time,type)

        return HttpResponseRedirect('/C/Clock/')

@login_required(login_url='/C/login')
def Alarmoff(request):
    led_functions.All_off(strip1)
    return HttpResponseRedirect('/C/Clock/')



@login_required(login_url='/C/login')
def Quickdelete(request,id):
    curalarm = models.Quickalarm.objects.get(id = id)
    curalarm.__delete__()
    return HttpResponseRedirect('/C/Clock/')


@login_required(login_url='/C/login')
def Delete(request,id):
    curalarm = models.Alarm.objects.get(id=id)
    curalarm.__delete__()
    return HttpResponseRedirect('/C/Clock/')



@login_required(login_url='/C/login')
def Viewalarm(request,id):
    curalarm = models.Alarm.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {"alarm": curalarm}
    return TemplateResponse(request, template, context)



@login_required(login_url='/C/login')
def Quickalarm(request):
    template = loader.get_template('quickalarm.html')
    return HttpResponse(template.render(request))



@login_required(login_url='/C/login')
def Index(request):
    global strip1
    if not 'Alarmisrunning' in globals():
        Alarmisrunning = False
    if not Alarmisrunning:
        Alarmauxilary.start(strip1)
        Alarmisrunning = True
        global Alarmisrunning
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request))


@login_required(login_url='/C/login')
def Clock(request):
    Allalarms = models.Alarm.objects.all()
    AllQuickalarms = models.Quickalarm.objects.all()
    template = loader.get_template('clock.html')
    context = {"Allalarms": Allalarms, "AllQuickalarms": AllQuickalarms}
    return TemplateResponse(request, template, context)



@login_required(login_url='/C/login')
def Alarm(request):
    template = loader.get_template('alarm.html')
    return HttpResponse(template.render(request))



@login_required(login_url='/C/login')
def Thanks(request):
    template = loader.get_template('thanks.html')
    return HttpResponse(template.render(request))

@login_required(login_url='/C/login')
def Devices(request):
    template = loader.get_template('devices.html')
    return HttpResponse(template.render(request))


@login_required(login_url='/C/login')
def Ledstrip(request):
    template = loader.get_template('ledstrip.html')
    return HttpResponse(template.render(request))

def print_status_1(name,time,type,days):
    pass

@login_required(login_url='/C/login')
def Intensiteit(request):
    template = loader.get_template('intensiteit.html')
    return HttpResponse(template.render(request))
