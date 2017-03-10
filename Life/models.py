from __future__ import unicode_literals
from django.db import models

from django.db import models
import Lauxilary



class Welcome_phrase(models.Model):
    phrase = models.CharField(max_length=140)
    part_of_day = models.CharField(max_length=1)
    def __addphrase__(self, phrase, part_of_day):
        self.phrase = phrase
        self.part_of_day= part_of_day
        self.save()
    def __delete__(self):
        self.delete()

class Quote(models.Model):
    quote = models.CharField(max_length=500)
    silencedyorN = models.CharField(max_length=1, default="N")
    def __addquote__(self, quote):
        self.quote = quote
        self.silencedyorN = "N"
        self.save()
    def __delete__(self):
        self.silencedyorN ="y"
        self.save()


class Descision(models.Model):
    name = models.CharField(max_length=50)
    silencedyorN = models.CharField(max_length=1, default="N")
    unique_id = models.CharField(max_length=10, default="Zero")


    def __adddescision__(self,name):
        self.name = name
        self.silencedyorN = "N"
        self.save()
        self.unique_id = "06" + str(self.id)
        self.save()

class DCriteria(models.Model):
    name = models.CharField(max_length=50)
    descision_to  = models.ForeignKey(Descision)


class Doption(models.Model):
    name = models.CharField(max_length=90)
    crit_scores = models.CharField(max_length=100)
    descision_to = models.ForeignKey(Descision)



class DDpositive(models.Model):
    argument = models.CharField(max_length=500)
    Doption = models.ForeignKey(Doption)


class DDnegative(models.Model):
    argument = models.CharField(max_length=500)
    Doption = models.ForeignKey(Doption)



class Video(models.Model):
    description = models.CharField(max_length=500, default="No description")
    name = models.CharField(max_length=50)
    htmlembedder = models.CharField(max_length=1000)
    silenced = models.CharField(max_length=1, default="N")
    def __addvideo__(self,name,description, htmlembedder):
        self.name = name
        self.description = description
        self.htmlembedder = htmlembedder
        self.save()
    def __delete__(self):
        self.delete()

class Article(models.Model):
    description = models.CharField(max_length=500, default="No description")
    name = models.CharField(max_length=50)
    silenced = models.CharField(max_length=1, default="N")
    article = models.CharField(max_length=6000, default="Go to link")
    link = models.CharField(max_length=500, default="None")
    def __addarticle__(self,name, description, article, link="None"):
        self.name = name
        self.description = description
        self.article = article
        self.link = link
        self.save()

##############
# float rep - floating repeat: e.g. sporting, want it to be done every time instance but can move
# rep - repeat: e.g. learning a new course: each week on the same day a reminder will be sent
# simp rem - simple reminder: A reminder time can be given, every time instance a reminder will appear: e.g. lifestyle
# dead - deadline: has to be done before a date, or before an other event.
##############

class float_repeat(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500,default="No description")
    rep_hours = models.CharField(max_length=10, default="0") ### om de hoeveel uur herhaling, moet nog omgerekend worden
    last_occurence = models.IntegerField(default=0) ### laatste gebeurtenis
    deviation = models.CharField(max_length=10, default="1") ### Welke uitwijking wordt toegestaan
    unique_id = models.CharField(max_length=30, default="Zero")
    silencedyorN = models.CharField(max_length=1, default="N")
    def __addflrp__(self, rep_hours, deviation, description="No description"):
        self.rep_hours = rep_hours
        self.deviation = deviation
        self.description = description
        self.save()

    def __simpleaddflrp__(self,name):
        self.name = str(name)
        self.save()
        self.unique_id = "01" + str(self.id)
        self.save()


    def addoccurence(self,datetimefield):
        self.last_occurence = datetimefield
        self.save()

    def __delete__(self):
        self.delete()


class repeat(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500, default="No description")
    active_week_days = models.CharField(max_length=20)
    remindtilldoneYorN = models.CharField(max_length=1) ### herrinering laten staan tot aangevinkt als uitgevoerd
    remember_time = models.TimeField(default="7:00") ### hoelaat de herrinering gegeven moet worden - voorbeel
    # smorgens bij het wakker worden al aangeven, of achteraan laten staan in lijst voor activiteiten doorheen dag
    unique_id = models.CharField(max_length=10, default="Zero")
    silencedyorN = models.CharField(max_length=1, default="N")
    last_occurence = models.CharField(max_length=20, default="00")

    def __addrepe__(self, active_week_days, remindtilldoneYorN, remember_time="7:00", description="No description"):
        self.active_week_days = active_week_days
        self.remindtilldoneYorN = remindtilldoneYorN
        self.remember_time = remember_time
        self.description = description
        self.save()
    def __simpleaddrepe__(self,name):
        self.name = name
        self.save()
        self.unique_id = "02" + str(self.id)
        self.save()

    def __delete__(self):
        self.delete()


class reminder(models.Model):
    summary = models.CharField(max_length=140)
    text = models.CharField(max_length=500, default="no text")
    silencedyorN = models.CharField(max_length=1, default="N") ## indien hij al veel is geweest niet meer laten verschijnen maar wel opslaan
    activation = models.CharField(max_length=10, default="None")
    unique_id = models.CharField(max_length=10,default="Zero")
    ##########
    # nu - NOW --> zal afhankelijk van tijdstip vanaf nu kunnen worden verschijnen
    # datum - dd-mm-yyyy --> zal sochtends op afgesproken dag verschijnen
    # samen met een andere activiteit - Unique_id van die activiteit
    #######
    def __addremi__(self, text, activation):
        self.text = text
        self.activation = activation
        self.save()
    def __simpleaddremi__(self,summary):
        self.summary = summary
        self.save()
        self.unique_id = "03" + str(self.id)
        self.save()

    def __delete__(self):
        self.delete()

class deadline(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, default="No descpription")
    deadday = models.IntegerField(default="0")
    deadmonth = models.IntegerField(default="0")
    warningtime = models.IntegerField(max_length=5, default="0") ## aantal dagen op voorhadn meldingen beginnen tonen
    unique_id = models.CharField(max_length=10, default="Zero")
    silencedyorN = models.CharField(max_length=1, default="N")


    def __adddead__(self, description, deadday, deadmonth, warningtime):
        self.description = description
        self.deadday = deadday
        self.deadmonth = deadmonth
        self.warningtime = warningtime
        self.save()
    def __delete__(self):
        self.delete()

    def __simpleadddead__(self,name):
        self.name = name
        self.save()
        self.unique_id = "04" + str(self.id)
        self.save()

class Daily(models.Model):
    name = models.CharField(max_length=140)
    day_added = models.CharField(max_length=10)
    silencedyorN = models.CharField(max_length=1)
    unique_id = models.CharField(max_length=10, default="Zero")
    show_text = models.CharField(max_length=20, default="Today")
    def __adddaily__(self,name):
        self.name = name
        self.silencedyorN = "N"
        self.day_added = Lauxilary.give_day_integer()
        self.save()
        self.unique_id = "05" + str(self.id)
        self.save()
