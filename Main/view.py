
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from Main import *
from django.http import HttpResponseRedirect




def Start(request):
    return HttpResponseRedirect('/C')




