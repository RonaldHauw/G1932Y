from django.conf.urls import url
from django.conf.urls.static import static
import views

urlpatterns = [ url(r'^$', views.Index, name='Core'),
                url(r'^Clock/', views.Clock , name='Clock'),
                url(r'^Alarm/', views.Alarm , name='Alarm'),
                url(r'^setalarm',views.Setalarm, name="Setalarm"),
                url(r'^thanks', views.Thanks, name="Thanks"),
                url(r'^quickalarm', views.Quickalarm, name="Quickalarm"),
                url(r'^setquickalarm', views.Setquickalarm, name="Setquickalarm"),
                url(r'^quickdelete/(?P<id>[0-9]+)$', views.Quickdelete,name="Quickdelete"),
                url(r'^delete/(?P<id>[0-9]+)$', views.Delete,name="Delete"),
                url(r'^detail/(?P<id>[0-9]+)$', views.Viewalarm, name="Viewalarm"),
                url(r'^devices/', views.Devices, name="Devices"),
                url(r'^ledstrip/', views.Ledstrip, name="Ledstrip"),
                url(r'^intensiteit/', views.Intensiteit, name="Intensiteit"),
                url(r'^submitlogin', views.CLogin, name="Clogin"),
                url(r'^login', views.CShowlogin, name="CShowlogin"),
                url(r'^startday', views.Startday, name="Startday"),
                url(r'^alarmoff', views.Alarmoff, name="Alarmoff"),
                url(r'^controller', views.Controller, name="controller"),
                url(r'^change_leds/(?P<id>[0-9]+)$', views.Change_led, name="Change_led"),

                ]

