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
import Lauxilary
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test

def email_check(user):
    return user.email.endswith('hauwaerts@gmail.com')




global last_daily_day ## om bij te houden wanneer de laatste keer de dagelijkse shizzle is bijgewerkt








@user_passes_test(email_check)
@login_required(login_url="/L/login")
def Editdescription(request, unique_id):
    obj = Lauxilary.get_activity_object(unique_id)
    code = unique_id[0:2]
    if request.method == 'POST':
        form = Description(request.POST)
        description = str(form['description'].value())
        if code == "03":
            obj.text = description
            obj.save()
        else:
            obj.description = description
            obj.save()
    return HttpResponseRedirect('/L/more/%s' % unique_id)

















@user_passes_test(email_check)
@login_required(login_url="/L/login")
def Showalldescisions(request):
    descisions= models.Descision.objects.all()
    template = loader.get_template('Alldescisions.html')
    context = {"descisions": descisions}
    return TemplateResponse(request, template, context)


@user_passes_test(email_check)
@login_required(login_url="/L/login")
def Submitdescision(request):
    if request.method == 'POST':
        form = Descisionbasic(request.POST)
        name = str(form['name'].value())
        cur = models.Descision()
        cur.__adddescision__(name)
    return HttpResponseRedirect('/L/#descision')

@user_passes_test(email_check)
@login_required(login_url="/L/login")
def Delofficial(request,unique_id):
    cur = Lauxilary.get_activity_object(unique_id)
    cur.delete()
    return HttpResponseRedirect('/L/showalldescisions')


@user_passes_test(email_check)
@login_required(login_url="/L/login")
def Editdescision(request, id):
    cur = models.Descision.objects.get(id=id)
    options = models.Doption.objects.filter(descision_to=cur)
    criteria = models.DCriteria.objects.filter(descision_to=cur)
    template = loader.get_template('Editdescision2.html')
    context = {"descision": cur, "options":options, "criteria": criteria}
    return TemplateResponse(request, template, context)




@user_passes_test(email_check)
@login_required(login_url="/L/login")
def Adddescposneg(request, posneg, descid, optid):
    descision = models.Descision.objects.get(id = descid)
    option = models.Doption.objects.get(id=optid)

    if request.method == 'POST':
        form = Argument(request.POST)
        argument = str(form['argument'].value())
        if int(posneg) == 1:
            cur_posneg_arg = models.DDpositive()
            cur_posneg_arg.argument = argument
            cur_posneg_arg.Doption_id = optid
            cur_posneg_arg.save()
        elif int(posneg) == 0:
            cur_posneg_arg = models.DDnegative()
            cur_posneg_arg.argument = argument
            cur_posneg_arg.Doption_id = optid
            cur_posneg_arg.save()

    return HttpResponseRedirect('/L/editdescision/%s/#%s' % (descision.id,option.name))

@user_passes_test(email_check)
@login_required(login_url="/L/login")
def Submitcriteria(request,  descid):
    descision = models.Descision.objects.get(id = descid)
    cur_crit = models.DCriteria()
    if request.method == 'POST':
        form = Option(request.POST)
        name = str(form['name'].value())
        cur_crit.name = name
        cur_crit.descision_to_id = descision.id
        cur_crit.save()
    Editdescision(request,descid)


    return HttpResponseRedirect('/L/editdescision/%s' % descision.id)




@user_passes_test(email_check)
@login_required(login_url="/L/login")
def Submitoption(request,  descid):
    descision = models.Descision.objects.get(id = descid)
    cur_option = models.Doption()
    if request.method == 'POST':
        form = Option(request.POST)
        name = str(form['name'].value())
        cur_option.name = name
        cur_option.crit_scores= 'None'
        cur_option.descision_to_id = descision.id
        cur_option.save()


    return HttpResponseRedirect('/L/editdescision/%s/#%s' % (descision.id, name))

def get_all_of_the_day():
    if not 'last_daily_day' in globals():
        last_daily_day = 0
        global last_daily_day
    today =  datetime.date.today()
    day = today.day
    month = today.month
    year = today.year
    int_day = Lauxilary.date_to_integer(day,month,year)
    if not 'Daily' in globals() or int(last_daily_day) != int(int_day):
        # pick new ones
        Allquotes = models.Quote.objects.filter(silencedyorN="N")
        Dayquote = random.sample(Allquotes, 1)[0]
        Video = models.Video.objects.filter(silenced="N")
        Dayvideo = random.sample(Video, 1)[0]
        Articles = models.Article.objects.filter(silenced="N")
        Dayarticle = random.sample(Articles, 1)[0]
        last_daily_day = int_day
        global last_daily_day
        Daily = [Dayquote, Dayvideo, Dayarticle]
        global Daily
    return Daily



@user_passes_test(email_check)
@login_required(login_url="/L/login")
def Adddescision(request):
    template = loader.get_template('Adddescision.html')
    return HttpResponse(template.render(request))


@login_required(login_url='/L/login')
def Showallarticles(request):
    template = loader.get_template('Allarticles.html')
    allartic = models.Article.objects.filter(silenced="N")
    context = {"articles":allartic}
    return TemplateResponse(request, template, context)



def Logout(request):
    logout(request)
    return HttpResponseRedirect("/C/")



def Login(request):

    username = request.POST['inputUser']
    password = request.POST['inputPassword']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/L/")
    else:
        template = loader.get_template('Denied.html')
        return HttpResponse(template.render(request))

def Showlogin(request):
    template = loader.get_template('Signin.html')
    return HttpResponse(template.render(request))

@user_passes_test(email_check)
@login_required(login_url='/L/login')
def LIndex(request):
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    today = {"day": day, "month":month, "year": year}
    Welcome_phrase = generate_welcome()
    Dailystuff = get_all_of_the_day()
    active_flrp, active_repeat, active_reminder, active_deadline, active_daily = Lauxilary.give_all_active()
    template = loader.get_template('Lindex.html')
    open_desc = models.Descision.objects.filter(silencedyorN="N")

    context = {"Welcome": Welcome_phrase, "Quote": Dailystuff[0], "flrp": active_flrp, "repe": active_repeat,
               "remi": active_reminder, "dead":active_deadline, "vid":Dailystuff[1], "today": today,
               "article": Dailystuff[2], "daily":active_daily, "desc":open_desc}
    return TemplateResponse(request, template, context)



@login_required(login_url='/L/login')
def Submitwelcome(request):
    if request.method == 'POST':

        form = Welcome(request.POST)




        phrase = form['phrase'].value()
        part_of_days = request.POST.getlist('time[]')
        for part in part_of_days:
            curphrase = models.Welcome_phrase()
            curphrase.__addphrase__(phrase,str(part))


    return HttpResponseRedirect('/L/addwelcome')

@login_required(login_url='/L/login')
def Addwelcome(request):
    template = loader.get_template('AddWelcome.html')
    All = models.Welcome_phrase.objects.all()
    pref = None

    context = {"Allphrases": All}
    return TemplateResponse(request, template, context)

@login_required(login_url='/L/login')
def Addquote(request):
    template = loader.get_template('Addquote.html')
    All = models.Quote.objects.all()

    context = {"Allquotes": All}
    return TemplateResponse(request, template, context)


@user_passes_test(email_check)
@login_required(login_url='/L/login')
def Deletephrase(request, id):
    obj = models.Welcome_phrase.objects.get(id=id)
    obj.__delete__()
    return HttpResponseRedirect('/L/addwelcome/')


@user_passes_test(email_check)
@login_required(login_url='/L/login')
def Deletequote(request, id):
    obj = models.Quote.objects.get(id=id)
    obj.__delete__()
    return HttpResponseRedirect('/L/addquote/')


@user_passes_test(email_check)
@login_required(login_url='/L/login')
def Submitquote(request):
    if request.method == 'POST':

        form = Quotes(request.POST)



        curquote = models.Quote()
        quote = form['quote'].value()
        print quote
        curquote.__addquote__(quote)



    return HttpResponseRedirect('/L/addquote')


@user_passes_test(email_check)
@login_required(login_url='/L/login')
def Addactivity(request):
    template = loader.get_template('Addactivity.html')
    return HttpResponse(template.render(request))



@user_passes_test(email_check)
@login_required(login_url='/L/login')
def Addingactivity(request):
    if request.method == 'POST':
        form = Activitybasic(request.POST)
        name = str(form['name'].value())
        type = form['type'].value()
        type = str(type)

        if type == '01':
            cur = models.float_repeat()
            cur.__simpleaddflrp__(name)
            return HttpResponseRedirect('/L/completactivityflrp/'+str(cur.id))

        if type == '02':
            cur = models.repeat()
            cur.__simpleaddrepe__(name)
            return HttpResponseRedirect('/L/completactivityrepe/'+str(cur.id))

        if type =='03':
            cur = models.reminder()
            cur.__simpleaddremi__(name)
            return HttpResponseRedirect('/L/completactivityremi/'+str(cur.id))

        if type == '04':
            cur = models.deadline()
            cur.__simpleadddead__(name)
            return HttpResponseRedirect('/L/completactivitydead/'+str(cur.id))
        if type == '05':
            cur = models.Daily()
            cur.__adddaily__(name)
            return HttpResponseRedirect('/L/')





@user_passes_test(email_check)
@login_required(login_url='/L/login')
def Completeactivityflrp(request,id):
    cur = models.float_repeat.objects.get(id=id)
    template = loader.get_template('Completeactivityflrp.html')
    context = {"cur": cur}
    return TemplateResponse(request, template, context)

@login_required(login_url='/L/login')
def Completeactivityrepe(request,id):
    cur = models.repeat.objects.get(id=id)
    template = loader.get_template('Completeactivityrepe.html')
    context = {"cur": cur}
    return TemplateResponse(request, template, context)


@login_required(login_url='/L/login')
def Completeactivityremi(request,id):
    cur = models.reminder.objects.get(id=id)
    template = loader.get_template('Completeactivityremi.html')
    context = {"cur": cur}
    return TemplateResponse(request, template, context)


@login_required(login_url='/L/login')
def Completeactivitydead(request,id):
    cur = models.deadline.objects.get(id=id)
    template = loader.get_template('Completeactivitydead.html')
    context = {"cur": cur}
    return TemplateResponse(request, template, context)




@login_required(login_url='/L/login')
def Submitflrp(request,id):
    if request.method == 'POST':

        form = flrp(request.POST)

        cur = models.float_repeat.objects.get(id=id)
        description = form['description'].value()
        times = form['times'].value()
        ina = form['ina'].value()
        deviation = form['deviation'].value()

        if str(ina) == 'week':
            tothours = 168
            rep_hours = int(int(tothours)/int(times))

        elif str(ina) =='day':
            tothours = 24
            rep_hours = int(int(tothours)/int(times))

        else:
            print "ERROR - no ina recognized"
            tothours = 1
            rep_hours = 0

        deviation = (tothours*int(deviation))/100

        cur.__addflrp__(rep_hours, int(deviation), description)

        return HttpResponseRedirect('/L/thanks/')


@login_required(login_url='/L/login')
def Submitrepe(request, id):
    if request.method == 'POST':

        form = repe(request.POST)

        cur = models.repeat.objects.get(id=id)

        description = form['description'].value()
        time = form['time'].value()
        rtd = form['rtd'].value()
        days = request.POST.getlist('days[]')
        teststring = ''
        for day in days:
            teststring += str(day)
            teststring += str('_')


        #active_week_days, remindtilldoneYorN, remember_time="7:00", description="No description"

        cur.__addrepe__(teststring, str(rtd), time, description)

        return HttpResponseRedirect('/L/thanks/')



@login_required(login_url='/L/login')
def Submitremi_(request, id):
    form = remi(request.POST)

    cur = models.reminder.objects.get(id=id)

    text = form['text'].value()
    acti = form['acti'].value()
    if str(acti) == "now":
        #summary, text, silencedYorN, activation
        cur.__addremi__(str(text),"now" )
        return HttpResponseRedirect('/L/thanks/')
    elif str(acti) == "activity":
        cur = models.reminder.objects.get(id=id)
        cur.text = str(text)
        cur.save()
        a = get_all_activity_of("01")
        b = get_all_activity_of("02")
        c = get_all_activity_of("03")
        d = get_all_activity_of("04")
        template = loader.get_template('Completeactivityremi_.html')
        context = {"flrp": a, "repe":b, "remi":c, "dead": d, "cur":cur}
        return TemplateResponse(request, template, context)


@login_required(login_url='/L/login')
def Submitremi(request, id):
    if request.method == 'POST':

        cur = models.reminder.objects.get(id=id)

        act = request.POST.getlist('act[]')
        teststring = ''
        for ac in act:
            teststring += str(ac)
            teststring += str('_')

        cur.activation = teststring
        cur.save()

        return HttpResponseRedirect('/L/thanks/')

@login_required(login_url='/L/login')
def Submitdead(request, id):
    if request.method == 'POST':

        form = dead(request.POST)

        cur = models.deadline.objects.get(id=id)

        description = form['description'].value()
        month = form['month'].value()
        day = form['day'].value()
        warning = form['warning'].value()
        #description, deadday, deadtime, warningtime
        cur.__adddead__(description,day,month,int(warning))
        return HttpResponseRedirect('/L/thanks/')



def generate_welcome():
    day_of_week, hour, minute = get_dayofweek_hour_minute()
    part_of_day = get_part_of_day(hour,minute)
    phrase = get_phrase(part_of_day)
    return phrase


def get_dayofweek_hour_minute():
    """
    Day of week is an integer from 0 to 6, hour and minute are given as integers
    :return: three elements
    """
    today = datetime.date.today()
    day_of_week = datetime.datetime.weekday(today)
    cur_time = datetime.datetime.now().time()
    hour = cur_time.hour
    minute = cur_time.minute

    return int(day_of_week), int(hour), int(minute)

def get_part_of_day(hour, minute):
    """
    given an hour and minute, this will return whether it is:
    4 - 6 : Earyly morning (1)
    6 - 9,5 : Morning (2)
    9,5 - 12 : Before noon (3)
    12 - 2 : Noon (4)
    14 - 18 : Afternoon (5)
    18 - 20 : Early evening (6)
    20 - 22 : Evening (7)
    22 - 0 : Night (8)
    0 - 4: Midnight (9)
    """
    if hour >= 4 and hour < 6:  # 4:00 - 5:59
        return 1
    if hour >= 6 and hour * 10 + (minute / 6) < 95:  # 6:00 - 9:29
        return 2
    if hour * 10 + (minute / 6) >= 95 and hour < 12:  # 9:30 - 11:59
        return 3
    if hour >= 12 and hour < 14:  # 12:00 - 13:59
        return 4
    if hour >= 14 and hour < 18:  # 14:00 - 17:59
        return 5
    if hour >= 18 and hour < 20:
        return 6
    if hour >= 20 and hour < 22:
        return 7
    if hour >= 22 and hour <= 23:
        return 8
    if hour >= 0 and hour < 4:
        return 9

def get_phrase(part_of_day):
    matching_phrases = models.Welcome_phrase.objects.filter(part_of_day=part_of_day)
    print matching_phrases
    matching_phrase = random.sample(matching_phrases,1)
    print matching_phrase[0]
    return matching_phrase[0]


def Thanks(request):
    template = loader.get_template('LThanks.html')
    return HttpResponse(template.render(request))




def get_all_activity_of(type):
    if type =="01":
        all = models.float_repeat.objects.filter(silencedyorN="N")
    if type =="03":
        all = models.reminder.objects.filter(silencedyorN="N")
    if type =="02":
        all = models.repeat.objects.filter(silencedyorN="N")
    if type == "04":
        all = models.deadline.objects.filter(silencedyorN="N")
    return all


@login_required(login_url='/L/login')
def Addvideo(request):
    template = loader.get_template('AddVideo.html')
    Videos = models.Video.objects.filter(silenced="N")
    context = {"Video": Videos}
    return TemplateResponse(request, template, context)

@login_required(login_url='/L/login')
def Submitvideo(request):
    if request.method == 'POST':

        form = video(request.POST)

        cur = models.Video()

        description = form['description'].value()
        name = form['name'].value()
        htmlembedder = form['htmlembedder'].value()
        print htmlembedder
        cur.__addvideo__(name,description,htmlembedder)
        return HttpResponseRedirect('/L')

@login_required(login_url='/L/login')
def Delete(request, unique_id):
    obj = Lauxilary.get_activity_object(unique_id)
    obj.silencedyorN = "y"
    obj.save()
    return HttpResponseRedirect('/L/#about')

@login_required(login_url='/L/login')
def Editproperties(request,unique_id):
    cur = Lauxilary.get_activity_object(unique_id)
    if request.method == 'POST':

        form = dead(request.POST)


        description = cur.description
        month = form['month'].value()
        day = form['day'].value()
        warning = form['warning'].value()
        #description, deadday, deadtime, warningtime
        cur.__adddead__(description,day,month,int(warning))
        return HttpResponseRedirect('/L/more/%s' % unique_id)

@user_passes_test(email_check)
@login_required(login_url='/L/login')
def More(request, unique_id):
    obj = Lauxilary.get_activity_object(unique_id)
    if str(unique_id)[0:2] == "04":
        template= loader.get_template('Mored.html')
        context = {"obj": obj}
        return TemplateResponse(request, template, context)
    else:
        template = loader.get_template('More.html')
        context = {"obj": obj}
        return TemplateResponse(request, template, context)

@user_passes_test(email_check)
@login_required(login_url='/L/login')
def Delvid(request, id):
    obj = models.Video.objects.get(id=id)
    obj.silenced = "y"
    obj.save()
    return HttpResponseRedirect('/L/#contact')


@user_passes_test(email_check)
@login_required(login_url='/L/login')
def Morevid(request, id):
    obj = models.Video.objects.get(id=id)
    template = loader.get_template('Morevid.html')
    context = {"video":obj}
    return TemplateResponse(request, template, context)



@login_required(login_url='/L/login')
def Done(request, unique_id):
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    obj = Lauxilary.get_activity_object(unique_id)
    obj.last_occurence = int(Lauxilary.date_to_integer(day, month, year))
    obj.save()
    return HttpResponseRedirect('/L/#about')

@login_required
def Addarticle(request):
    if email_check(request.user):
        check = "oke"
    else:
        check = "false"
    template = loader.get_template('Addarticle.html')
    context = {"check": check}
    return TemplateResponse(request, template, context)

@login_required(login_url='/L/login')
def Submitarticle(request):
    if request.method == 'POST':

        form = article(request.POST)
        cur = models.Article()

        description = form['description'].value()
        name = form['name'].value()
        art = form['article'].value()
        link = form['link'].value()
        if str(link)=="":
            link = "None"
        cur.__addarticle__(name,description,art, link)
        return HttpResponseRedirect('/L/#article')



@login_required(login_url='/L/login')
def Read(request, id):
    obj = models.Article.objects.get(id = id)
    print "h", str(obj.link)
    if str(obj.link) == "None":
        template = loader.get_template('Read.html')
        print "here!"
        context = {"Article": obj}
        return TemplateResponse(request, template, context)
    else:
        link = str(obj.link)
        return HttpResponseRedirect('%s' % link)

@user_passes_test(email_check)
@login_required(login_url='/L/login')
def Deletearticle(request, id):
    obj = models.Article.objects.get(id=id)
    obj.silenced="y"
    obj.save()
    return HttpResponseRedirect('/L/#article')


@login_required(login_url='/L/login/')
def About(request):
    template = loader.get_template('About.html')
    return HttpResponse(template.render(request))


@login_required(login_url='/L/login')
def Addnote(request):
    template = loader.get_template('Addnote.html')
    return HttpResponse(template.render(request))


@login_required(login_url='/L/login')
def Submitnote(request):
    if request.method == 'POST':

        form = note(request.POST)
        day = datetime.date.today().day
        month = datetime.date.today().month
        year = datetime.date.today().year
        file_name = str(day) + "-" + str(month) + "-" + str(year)
        tex_subtitle = "\subsection{"
        tex_title = "\section{"
        tex_end = "}\n"
        tex_input = "\input{"
        title = form['title'].value()
        subtitle = form['subtitle'].value()
        nte = form['note'].value()
        path = "./../../../../../home/pi/Desktop/Homecontrol21/Life/TEx/"
        finish = "\n"
        if title == "":
            with open('%s%s.tex' % (path ,file_name), 'a') as dayfile:
                print('  writing data to', file_name)

                dayfile.write(tex_subtitle + str(subtitle) + tex_end)
                dayfile.write('%s' % str(nte))
                dayfile.write('%s' % finish)

        elif subtitle =="":
            with open('%s%s.tex' % (path ,file_name), 'a') as dayfile:
                print('  writing data')
                dayfile.write(tex_title + str(title) + tex_end)
                dayfile.write('%s' % nte)
                dayfile.write('%s' % finish)


        else:
            with open('%s%s.tex' % (path ,file_name), 'a') as dayfile:
                print('  writing data')
                dayfile.write(tex_title + str(title) + tex_end)
                dayfile.write(tex_subtitle + str(subtitle) + tex_end)
                dayfile.write('%s' % nte)
                dayfile.write('%s' % finish)

        return HttpResponseRedirect('/L')



@login_required(login_url='/L/login')
def Donerep(request, unique_id):
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    obj = models.repeat.objects.get(unique_id = unique_id)
    obj.last_occurence = str(Lauxilary.date_to_integer(day, month, year))
    obj.save()
    return HttpResponseRedirect('/L/#about')

