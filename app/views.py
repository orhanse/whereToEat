from django.shortcuts import render
from .models import App
from user.models import User
import time
from django.http import HttpResponseRedirect
from django.template import Context
from threading import Thread
from calculation.models import Weather
from calculation.models import Calculation
from django.utils import timezone
import datetime
from django.core.mail import send_mail
from _datetime import timedelta
from django.template.context_processors import request
from restaurant.models import Restaurant
from tkinter.constants import CURRENT
import requests
from random import randint
class ProcessThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        

    def run(self):
        currentCR = App.getCR(App)
        now = timezone.now()
        next = now + timedelta(minutes = 5)
        counter = currentCR.periodCounter
        while currentCR.periodCounter > 0 and currentCR.calculationCheck == True:
            rand = randint(0, 10)
            if rand > 5:
                weatherCondition = False
                Weather.setCurrent(Weather, 'bad')
            else:
                weatherCondition = True
                Weather.setCurrent(Weather, 'good')
            #weatherCondition = conditionCheck()
            successFlag = Calculation.makePrediction(Calculation, weatherCondition)
            currentCR.countDown()
            if currentCR.periodCounter == 0:
                break
            time.sleep(2)
        currentCR.calculationCheck = False
        currentCR.save()
def app(request):
    return render(request,'header.html')


def home(request):
    if App.getCR(App) is None:
        context = Context({'grading': True,})
        return render(request,'home.html',context)
    else:
        currentCity = App.getCR(App).currentCity
        rules = App.getCR(App)
        flag = rules.calculationCheck
        if flag == True:
            lastCal = Calculation.getCurrent(Calculation)
            context = Context({'currentCity': currentCity,'flag':flag,'rest':lastCal.restaurant.restName})
        else:
            context = Context({'currentCity': currentCity,'flag':flag})
        return render(request,'home.html',context)

def setCR(request):
    if request.method == 'POST':
        newPeriod = request.POST.get('period',None)
        newCity = request.POST.get('currentCity',None) 
        newApp = App(calculationPeriod = newPeriod,currentCity = newCity,periodCounter = newPeriod,calculationCheck = False)
        newApp.save()
        currentCR = App.getCR(App)
        context = Context({'Context': currentCR})
       
        return render(request,'setCR.html',context)
    
    else:
        currentCR = App.getCR(App)
        context = Context({'Context': currentCR})
        return render(request,'setCR.html',context)
    
    
def conditionCheck():
    city = App.getCR(App).currentCity
    getWeather = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+ city +'&APPID=b9dd3952f36a165aecc5518e9e0a5117')
    weatherJson = getWeather.json()
    newWeather = weatherJson['weather'][0]['main']
    Weather.setCurrent(Weather, newWeather)
    weatherId = weatherJson['weather'][0]['id']
    if  (weatherId >= 600 and weatherId <=699 ) or (weatherId >= 200 and weatherId <= 299 )  or weatherId >= 900  or ( weatherId >= 501 and weatherId <=599 ) or ( weatherId >= 312 and weatherId <= 321 ) and weatherId == 302 :
        return False
    else:
        return True    
def startApp(request):
    userPointCount = User.objects.filter(userPoints__gt = 0).count()
    if userPointCount == 0:  
        Calculation.setRestCounters(Calculation)
        rules = App.getCR(App)
        rules.calculationCheck = True
        rules.save()
        my_thread = ProcessThread("CacheClassroom")
        my_thread.start()
        return HttpResponseRedirect('calculation/getRecords')
    else:
        rules = App.getCR(App)
        flag = rules.calculationCheck
        context = Context({'grading': False,'flag':flag})
        return render(request,'home.html',context)
        
    


def resetApp(request):
    rules = App.getCR(App)
    rules.calculationCheck = False
    rules.periodCounter = rules.calculationPeriod
    rules.save()
    Calculation.objects.all().delete()
    Restaurant.resetServiceCounters(Restaurant)
    flag = False
    context = Context({'flag':flag,'grading':True})
    return render(request,'home.html',context)