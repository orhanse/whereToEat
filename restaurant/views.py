from django.shortcuts import render
from .models import Restaurant
from django.http import HttpResponseRedirect
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from calculation.models import Calculation
# Create your views here.
def getRestaurant(request):  
    if request.method == 'POST':
        newRestName = request.POST.get('restName',None)
        newWeatherCondition = request.POST.get('weatherMode', None)
        newModeOfTransport = request.POST.get('modeOfTransport', None)
        
        if newModeOfTransport == "on":
            boolOfTransport = True
        else:
            boolOfTransport = False
            
        if newWeatherCondition == "on":
            boolOfCondition = True
        else:
            boolOfCondition = False
        try:
            data = Restaurant.objects.get(restName = newRestName)
            return HttpResponseRedirect('restaurant/Rest/')            
        except Restaurant.DoesNotExist:
            newRest = Restaurant(restName = newRestName,weatherCondition = boolOfCondition , modeOfTransport = boolOfTransport,serviceStatus = True,serviceCounter = 0)
            newRest.save()
            return HttpResponseRedirect('restaurant/Rest/')
        
        
    
    else:
        restaurants = Restaurant.getRestaurants(Restaurant)
        context = Context({'Restaurants' : restaurants})
        return render(request,'restaurants.html',context)
    
@csrf_exempt
def setStatus(request):
    if request.method == 'POST':
        restName = request.POST.get('name',None)
        newStatus = request.POST.get('status', None)
        if newStatus == "activated":
            successFlag = Restaurant.updateRestStatus(Restaurant,True,restName)
        else:
            successFlag = Restaurant.updateRestStatus(Restaurant,False,restName)
            
        if successFlag == False:
            Calculation.setRestCounters(Calculation)
        restaurants = Restaurant.getRestaurants(Restaurant)
        context = Context({'Restaurants' : restaurants})
        return render(request,'restaurants.html',context)
    else:
        return HttpResponseRedirect('restaurant/Rest/')
    
def update(request):
    if request.method == 'POST':
        newRestName = request.POST.get('restName',None)
        newWeatherCondition = request.POST.get('weatherMode', None)
        newModeOfTransport = request.POST.get('modeOfTransport', None)
        oldRestName = request.POST.get('oldRestName',None)
        Restaurant.updateRestName(Restaurant,newRestName,oldRestName)
        Restaurant.updateModeOfTransport(Restaurant,newModeOfTransport,newRestName)
        Restaurant.updateWeatherCondition(Restaurant,newWeatherCondition,newRestName)
        restaurants = Restaurant.getRestaurants(Restaurant)
        context = Context({'Restaurants' : restaurants})
        return render(request,'restaurants.html',context)
    else:
        return HttpResponseRedirect('restaurant/Rest/')
    
    
def delete(request):
    if request.method == 'POST':
        restName = request.POST.get('restName',None)
        Restaurant.deleteRest(Restaurant,restName)
        return HttpResponseRedirect('restaurant/Rest/')
    else:
        return HttpResponseRedirect('restaurant/Rest/')