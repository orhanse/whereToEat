from django.shortcuts import render
from .models import Weather
from .models import Calculation
from django.http import HttpResponseRedirect
from django.template import Context
from grading.models import Points
from restaurant.models import Restaurant
from app.models import App
from user.models import User

def setWeather(request):
    if request.method == 'POST':
        newCurrentWeather = request.POST.get('weather',None)
        Weather.setCurrent(Weather,newCurrentWeather)
        currentWt = Weather.getCurrent(Weather)
        context = Context({'Context': currentWt})
        return render(request,'calNweather.html',context)
    
    else:
        currentWt = Weather.getCurrent(Weather)
        context = Context({'Context': currentWt})
        return render(request,'calNweather.html',context)
        
    
    
    
def serviceRecord(request):
    row = []
    returnList = []
    counter = 1
    for record in Calculation.objects.all():
                rest = Restaurant.objects.get(restName = record.restaurant.restName ) 
                row = {'counter':counter,'restaurant':rest.restName,'date':record.date,'modeOfTransport':rest.modeOfTransport,'weather':record.weather.currentWeather}
                counter = counter+1
                returnList.append(row)
    context = Context({'Records' : returnList})
    return render(request,'records.html',context)
def statistics(request):
    rules = App.getCR(App)
    restList = []
    counter = 1
    userCount = User.objects.all().count()
    totalPoints = rules.calculationPeriod * userCount
    total =  Restaurant.objects.all().count()
    vehicleCount = Restaurant.objects.filter(modeOfTransport = True).count()
    pedestrianCount = Restaurant.objects.filter(modeOfTransport = True).count()
    aviableInBadWeather = Restaurant.objects.filter(weatherCondition = True).count()
    AnaviableInBadWeather = Restaurant.objects.filter(weatherCondition = False).count()
    activeRests = Restaurant.objects.filter(serviceStatus = True).count()
    inactiveRests = Restaurant.objects.filter(serviceStatus = False).count()
    infoList = [{'userCount':userCount,'totalPoints':totalPoints,'totalRests':total,'vehicleRests':vehicleCount,'pedestrianRests':pedestrianCount,'aviableInBadWeather':aviableInBadWeather,'AnaviableInBadWeather':AnaviableInBadWeather,'activeRests':activeRests,'inactiveRests':inactiveRests}]
    allCalculations = Calculation.objects.all().count()
    restNames = []
    restFlag = False
    for record in Calculation.objects.all():
                restFlag = False
                for restName in restNames:
                    if record.restaurant.restName == restName:
                        restFlag = True
                        break
                if restFlag == True:
                    continue
                restNames.append(record.restaurant.restName)
                restObject = Restaurant.objects.get(restName = record.restaurant.restName )
                rest = Calculation.objects.filter(restaurant = restObject).count()
                restPoint = Points.objects.filter(restaurant = restObject)
                finalPoint = 0
                for point in restPoint:
                    finalPoint = finalPoint+point.point
                row = {'restName':record.restaurant.restName,'wentCount':rest,'point' : finalPoint,'serviceCounter':restObject.serviceCounter,'modeOfTransport':restObject.modeOfTransport,'weatherCondition':restObject.weatherCondition,'serviceStatus':restObject.serviceStatus}
                restList.append(row)
                
    context = Context({'app':rules,'Calculation' : restList,'infoList':infoList})
    return render(request,'statistics.html',context)
        
    