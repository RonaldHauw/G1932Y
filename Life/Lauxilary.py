from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
import time
import datetime
from threading import Thread
import models
from django.template.response import TemplateResponse
import random
from forms import *





def give_all_active():

    """
    wacht en geeft 4 lijsten terug met actieve objecten van elke soort
    :return:
    """
    #########################
    today = datetime.date.today()
    cur_time = datetime.datetime.now().time()
    day_of_week = datetime.datetime.weekday(today)
    hour = cur_time.hour
    minute = cur_time.minute
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    daycounter = date_to_integer(day,month, year)
    timecounter = time_to_integer(hour,minute)

    ##########################
    active_dead_lines = []
    for deadline in models.deadline.objects.filter(silencedyorN="N"):


        if active_deadline(deadline,day, month, year):
            active_dead_lines.append(deadline)
    ##########################
    active_reminders = []
    nowlist = []
    for reminder in models.reminder.objects.filter(silencedyorN="N"):
        if is_active_reminder(reminder,day, month, year, day_of_week,daycounter,timecounter) == True:
            active_reminders.append(reminder)
        if is_active_reminder(reminder, day, month, year , day_of_week, daycounter, timecounter) =="now":
            nowlist.append(reminder)
    len_now_list = len(nowlist)
    len_filterd_now = (int(len_now_list)+1)/2
    if len_filterd_now>3:
        len_filterd_now =3
    for i in range(0,len_filterd_now):
        randindex = random.randint(0,len_now_list-1-i)
        rem = nowlist[randindex]
        active_reminders.append(rem)
        nowlist.__delitem__(randindex)





    ##########################
    active_repeat = []
    for repeat in models.repeat.objects.filter(silencedyorN="N"):
        if is_active_repeat(repeat,daycounter,timecounter,day_of_week ):
            active_repeat.append(repeat)

    ##########################
    active_flrp = []
    for flrp in models.float_repeat.objects.filter(silencedyorN="N"):
        if is_active_flrp(flrp, daycounter):
            active_flrp.append(flrp)

    active_daily = []
    for daily in models.Daily.objects.filter(silencedyorN="N"):
        if is_active_daily(daily):
            active_daily.append(daily)

        if str(daily.day_added) != str(give_day_integer()):
            if int(give_day_integer()) - int(daily.day_added) == 1:
                daily.show_text = "yesterday"
            elif int(give_day_integer()) - int(daily.day_added) == 2:
                daily.show_text = "yester - yesterday"

    ##########################





    return active_flrp, active_repeat, active_reminders, active_dead_lines, active_daily



def give_all_active_of_days_forward(nb_days_forward):

    """
    wacht en geeft 4 lijsten terug met actieve objecten van elke soort
    :return:
    """
    #########################
    today = datetime.date.today()
    cur_time = datetime.datetime.now().time()
    day_of_week = datetime.datetime.weekday(today)
    day_of_week += nb_days_forward
    if day_of_week > 6:
        rest = day_of_week %6
        day_of_week = rest
    hour = cur_time.hour
    minute = cur_time.minute
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    daycounter = date_to_integer(day,month, year) + nb_days_forward
    timecounter = 0

    ##########################
    active_dead_lines = []
    for deadline in models.deadline.objects.filter(silencedyorN="N"):


        if active_deadline2(deadline,daycounter, year):
            active_dead_lines.append(deadline)
    ##########################





    ##########################
    active_repeat = []
    for repeat in models.repeat.objects.filter(silencedyorN="N"):
        if is_active_repeat(repeat,daycounter,timecounter,day_of_week ):
            active_repeat.append(repeat)

    ##########################
    active_flrp = []
    for flrp in models.float_repeat.objects.filter(silencedyorN="N"):
        if is_active_flrp(flrp, daycounter):
            active_flrp.append(flrp)

    ##########################


    return active_flrp, active_repeat, active_dead_lines




def wait_a_minute(minute):
    time.sleep(minute)

def get_activity_object(unique_id):
    code = str(unique_id)[0:2]
    if code == "04":
        return models.deadline.objects.get(unique_id = unique_id)
    if code == "02":
        return models.repeat.objects.get(unique_id = unique_id)
    if code =="03":
        return models.reminder.objects.get(unique_id=unique_id)
    if code =="01":
        return models.float_repeat.objects.get(unique_id=unique_id)
    if code =="05":
        return models.Daily.objects.get(unique_id=unique_id)
    if code =="06":
        return models.Descision.objects.get(unique_id=unique_id)

def generate_list(input):
    """
    volgens protocol gegenereerde lijst terug omzetten naar python lijst

    """
    input = str(input)
    list = []
    elem = ""
    for i in range(0, len(input)):
        if input[i] != '_':
            elem += input[i]
        else:
            list.append(elem)
            elem = ""


    return list

def is_active_daily(daily_object):
    if daily_object.silencedyorN =="N":
        return True
    else:
        return False

def make_list(input):
    """
    geschikt vor weekdagen
    :param input:
    :return:
    """
    input = str(input)
    list = []
    for i in range(0,len(input)):
        if input[i] != '_':
            list.append(int(input[i])-1)

    return list


def date_to_integer( day, month, year):
    """
    rough approctimation to generating an integer for a day from 0 to 365
    :param old:
    :param day:
    :param month:
    :return:
    """
    inte = 0
    delta_year = int(year)- 2000
    ### aantal jaren tot we aan het huidige jaar zijn, dit jaar telt nog niet mee om dat nog niet opgevuld is
    for i in range(1,delta_year):
        if is_schrikkel_year(year):
            inte += 366
        else:
            inte += 365
    #### aantal dagen van maanden die al gepasseerd zijn, dus niet van de huidige maand ###
    for i in range(1,int(month)):
        if int(i) in [1,3,5,6,8,10,12]:
            inte += 31
        elif int(i) in [4,7,9,11]:
            inte +=30
        elif int(i) == 2:
            if is_schrikkel_year(year):
                inte +=29
            else:
                inte += 28
    inte += int(day)
    return inte






def active_deadline(deadline, curday, curmonth,year):


    d_day = deadline.deadday
    d_month = deadline.deadmonth
    warningtime = int(deadline.warningtime)

    warn_integer = date_to_integer(int(d_day),int(d_month),year) - int(warningtime)
    day_integer = date_to_integer(int(curday), int(curmonth),year)
    if warn_integer <= day_integer:
        return True
    else:
        return False

def active_deadline2(deadline, daycounter, year):


    d_day = deadline.deadday
    d_month = deadline.deadmonth
    warningtime = int(deadline.warningtime)

    warn_integer = date_to_integer(int(d_day),int(d_month),year) - int(warningtime)
    if warn_integer <= daycounter:
        return True
    else:
        return False


def is_active_repeat(repeat, daycounter, timecounter, day_of_week):
    active_week_days = repeat.active_week_days
    activation_time = repeat.remember_time
    activation_hour = activation_time.hour
    activation_minute = activation_time.minute
    activation_integer = time_to_integer(activation_hour, activation_minute)
    list_week_days = make_list(active_week_days)
    last_active = repeat.last_occurence
    if int(activation_integer) <= int(timecounter):
        Time_check = True
    else:
        Time_check = False

    if last_active != str(daycounter):
        already_done = False
    else:
        already_done = True
    for r_day in list_week_days:
        if str(day_of_week) == str(r_day) and not already_done and Time_check:
            return True
    return None

def is_active_flrp(flrp, daycounter):
    dev = flrp.deviation
    rep_hours = flrp.rep_hours
    rep_days = int(rep_hours) / 24
    last_occurence = flrp.last_occurence
    should_day = int(last_occurence) + rep_days - int(dev)  ### moet nog met deviatie rekening worden gehouden
    if daycounter >= should_day:
        return True
    else:
        return None

def is_active_reminder(reminder,day, month, year, day_of_week, daycounter, timecounter ):
    activation = reminder.activation
    if str(activation) == "now":
        return "now"
    else:
        list_unique_id = generate_list(activation)
        for unique in list_unique_id:
            obj = get_activity_object(unique)
            code = str(unique)[0:2]
            if code == "02":
                if is_active_repeat(obj,daycounter,timecounter,day_of_week):
                    return True
            if code == "04":
                if active_deadline(obj, day, month, year):
                    return True
            if code == "01":
                if is_active_flrp(obj,daycounter):
                    return True
            if code =="05":
                if is_active_daily(obj):
                    return True

def give_day_integer():
    today = datetime.date.today()
    day = today.day
    month = today.month
    year = today.year
    return date_to_integer(day, month, year)


def is_schrikkel_year(year):
    four = int(year)%4
    hunderd = int(year)%100
    if four == 0 and hunderd != 0:
        return True
    else:
        return False


def time_to_integer(hour, minute):
    return 60*int(hour) + int(minute)



