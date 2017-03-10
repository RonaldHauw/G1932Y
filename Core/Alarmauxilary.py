from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
import models
from .forms import AlarmForm, QuickAlarmForm
from django.template.response import TemplateResponse
import time
import timeit
import datetime
from threading import Thread
import views
import pygame
import led_shows



def start(strip):
    print "STARTING DAY"
    p1 = Thread(target=runalarm, args=[strip])
    p1.start()
    print "Launched succesfully"

def runalarm(strip):
    print "succesfull launch confirmed" , strip
    alarmerstatus = False
    loopvariable = True
    while loopvariable == True:
        #########################
        wait_a_minute(56)
        today = datetime.date.today()
        day_of_week = datetime.datetime.weekday(today)
        cur_time = datetime.datetime.now().time()
        hour = cur_time.hour
        minute = cur_time.minute
        print "Alarm is running ... ", hour,minute




        ##########################
        for alarm in models.Alarm.objects.all():



            ################
            alarmdays = alarm.days # 1...7
            alarmdaylist = makelist(alarmdays) #1..7
            cur_week_day = int(day_of_week) + 1
            if cur_week_day in alarmdaylist:
                daytrigger = True
            else:
                daytrigger = False



            ################
            alarmtime = alarm.time
            alarmhour = alarmtime.hour
            alarmminute = alarmtime.minute
            if int(hour) == int(alarmhour):
                hourtrigger = True
            else:
                hourtrigger = False
            if int(minute) == int(alarmminute):
                minutetrigger = True
            else:
                minutetrigger = False
            ##############
            if daytrigger and hourtrigger and minutetrigger and not alarmerstatus:
                p2 = Thread(target=makealarm(str(alarm.type)))
                p2.start()
                alarmerstatus = True
                wait_a_minute(20)
                daytrigger, hourtrigger, minutetrigger = False, False, False
            else:
                daytrigger, hourtrigger, minutetrigger = False, False,False





        ##########################
        for alarm in models.Quickalarm.objects.all():
            alarmtime = alarm.time
            alarmhour = alarmtime.hour
            alarmminute = alarmtime.minute
            if int(hour) == int(alarmhour):
                hourtrigger = True
            else:
                hourtrigger = False
            if int(minute) == int(alarmminute):
                minutetrigger = True
            else:
                minutetrigger = False
            ##############
            if  hourtrigger and minutetrigger and not alarmerstatus:
                makealarm(strip)
                global alarmerstatus
                hourtrigger, minutetrigger = False, False
            else:
                hourtrigger, minutetrigger = False, False














def wait_a_minute(minute):
    time.sleep(minute)

def makelist(alarmdays):
    alarmdays = str(alarmdays)
    listx = []
    for i in range(0,len(alarmdays)):
        if alarmdays[i] != '_':
            listx.append(int(alarmdays[i]))

    return listx


def makealarm(strip):
    led_shows.Gently_wake_up(strip)



