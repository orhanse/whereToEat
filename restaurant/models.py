from django.db import models
from app.models import App
import datetime
import math
# Create your models here.

class Restaurant(models.Model):
    restName = models.CharField(max_length = 50)
    weatherCondition = models.BooleanField()
    modeOfTransport = models.BooleanField()
    serviceStatus = models.BooleanField()
    serviceCounter = models.IntegerField()
    
    def deleteRest(self,delRestName):
        status = Restaurant.updateRestStatus(Restaurant,False,delRestName)
        if status == True:
            self.objects.get(restName = delRestName).delete()
            return True
        else:
            return False
        
    def updateRestStatus(self,newStatus,upRestName):
        rules = App.getCR(App)
        upRestaurant = self.objects.get(restName = upRestName)
        if rules.calculationCheck == True:
            if newStatus == False:
                activeCounter = self.objects.filter(serviceCounter__gt = 0,serviceStatus=True).count()
                counter = upRestaurant.serviceCounter
                if activeCounter!= 0 and counter!= 0:
                    for activeRest in self.objects.filter(serviceCounter__gt = 0,serviceStatus=True).order_by('-serviceCounter'):
                        activeRest.serviceCounter = activeRest.serviceCounter+1
                        activeRest.save()
                        counter = counter -1
                        if counter == 0:
                            break
                else:
                    return False
                            
            else:
                activeRests = self.objects.filter(serviceCounter__gt = 0,serviceStatus=True)
                activeCounter = self.objects.filter(serviceCounter__gt = 0,serviceStatus=True).count()

                counter = upRestaurant.serviceCounter
                if activeCounter!= 0 and counter!= 0:
                    for activeRest in self.objects.filter(serviceCounter__gt = 0,serviceStatus=True).order_by('-serviceCounter'):
                        if activeRest.serviceCounter > 0:
                            activeRest.serviceCounter = activeRest.serviceCounter-1
                            activeRest.save()
                            counter = counter -1
                        if counter == 0:
                            break
                            
                else:
                    return False
                        
        upRestaurant.serviceStatus = newStatus
        upRestaurant.save()
        return True
        
    def updateRestName(self,upRestName,curRestName):
        upRestaurant = self.objects.get(restName = curRestName)
        upRestaurant.restName = upRestName
        upRestaurant.save()    
        
    def updateModeOfTransport(self,newMode,upRestName):
        upRestaurant = self.objects.get(restName = upRestName)
        upRestaurant.modeOfTransport = newMode
        upRestaurant.save()
        
        
    def updateWeatherCondition(self,newCondition,upRestName):
        upRestaurant = self.objects.get(restName = upRestName)
        upRestaurant.weatherCondition = newCondition
        upRestaurant.save()
    
    def getRestaurants(self):
        return self.objects.values()
    
    def getGrade(self):
        return self.Points
            
    def serviceCounters(self):
        rules = App.getCR(App)
        counter = rules.periodCounter
        for rest in Restaurant.objects.filter(serviceStatus = True):
            counter = counter - rest.serviceCounter
        while counter > 0:
            for rest in Restaurant.objects.filter(serviceStatus = True).order_by('-serviceCounter'):
                rest.serviceCounter = rest.serviceCounter + 1
                rest.save()
                counter = counter -1
                if counter == 0:
                    break
        while counter < 0:
            for rest in Restaurant.objects.filter(serviceStatus = True).order_by('serviceCounter'):
                if rest.serviceCounter > 1:
                    rest.serviceCounter = rest.serviceCounter - 1
                    rest.save()
                    counter = counter +1
                if counter == 0:
                    break
               
        vehicleRestaurants = Restaurant.objects.filter(modeOfTransport = True,serviceStatus = True,weatherCondition = True)
        vrestCounter = 0
        for vrest in vehicleRestaurants:
            vrestCounter = vrest.serviceCounter + vrestCounter
        
        constantIstanbul = [17.5 , 15.3   , 13.8 ,  10.4  , 8.1  , 6.1  ,  4.2  ,  4.9  ,  7.4  , 11.3  ,  13.2  , 17.2]        
        currentDate = datetime.datetime.now()
        currentDay = currentDate.day
        totalDays = rules.periodCounter
        totalMonthsFloat = totalDays/30
        totalMonthsRound = math.ceil(totalMonthsFloat)
        badWeatherProbability = ((30 - currentDay)*constantIstanbul[currentDate.month - 1])/30
        for  i in range(1,totalMonthsRound):
            if (i - totalMonthsFloat + 1) > 0:
                badWeatherProbability = (30*(i - totalMonthsFloat)*constantIstanbul[currentDate.month - 1 + i])/30 + badWeatherProbability
            badWeatherProbability = constantIstanbul[currentDate.month - 1 + i] + badWeatherProbability      
       
        
        if vrestCounter < int((rules.periodCounter/badWeatherProbability)):
            
            transporBalanceCounter =   int((rules.periodCounter/badWeatherProbability)) - vrestCounter
            counter = transporBalanceCounter
            while transporBalanceCounter > 0:
                for rest in Restaurant.objects.filter(modeOfTransport=False,serviceStatus = True,weatherCondition = False).order_by('serviceCounter'):
                    rest.serviceCounter = rest.serviceCounter - 1
                    rest.save()
                    counter = counter -1
                    if counter == 0:
                        break
                    
                for rest in vehicleRestaurants.order_by('-serviceCounter'):
                    rest.serviceCounter = rest.serviceCounter + 1
                    rest.save()
                    transporBalanceCounter = transporBalanceCounter -1
                    if transporBalanceCounter == 0:
                        break
                    
                    
    def restaurantBalance(self):
        rests = Restaurant.objects.filter(serviceStatus = True).count()
        if rests == 0:
            return True
        vehicleRests = Restaurant.objects.filter(modeOfTransport = True,serviceStatus = True).count()
        if vehicleRests/rests > 0.8:
            return False
        else:
            return True
        
    def terraceCheck(self):
        rests = Restaurant.objects.filter(serviceStatus = True,serviceCounter__gt = 0).count()
        if rests == 0:
            return False
        terraceRests = Restaurant.objects.filter(weatherCondition = True,serviceStatus = True,serviceCounter__gt = 0).count()
        if terraceRests/rests >= 0.4:
            return True
        else:
            return False
    def vehicleCheck(self):
        rests = Restaurant.objects.filter(modeOfTransport = True,serviceStatus = True,serviceCounter__gt = 0).count()
        if rests == 0:
            return False
        vehicleRests = Restaurant.objects.filter(modeOfTransport = True,serviceStatus = True,serviceCounter__gt = 0).count()
        if vehicleRests/rests >= 0.5:
            return True
        else:
            return False        
    def resetServiceCounters(self):
        rests = Restaurant.objects.all()
        for rest in rests:
            rest.serviceCounter = 0
            rest.save()
            
            