from __future__ import unicode_literals
from django.db import models

from django.db import models

class Alarm(models.Model):

    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name
    type = models.CharField(max_length=10)
    time = models.TimeField()
    days = models.CharField(max_length=50)
    def __addalarm__(self,name, time, days, type):
        self.name = name
        self.time = time
        self.type = type
        teststring = ''
        for day in days:
            teststring += str(day)
            teststring += str('_')
        self.days = teststring
        self.save()
    def __delete__(self):
        self.delete()


class Quickalarm(models.Model):
    type = models.CharField(max_length=10)
    time = models.TimeField()
    def __addquickalarm__(self, time, type):
        self.time = time
        self.type = type
        self.save()
    def __delete__(self):
        self.delete()




class Ledstrip(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=20)
