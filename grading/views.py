from django.shortcuts import render
from .models import Points
from user.models import User
from restaurant.models import Restaurant
from app.models import App
from django.http import HttpResponseRedirect
from django.template import Context
# Create your views here.

def grading(request):
    users = User.getUsers(User)
    gradingFlag = Restaurant.restaurantBalance(Restaurant)
    context = Context({'users' : users,'flag':gradingFlag})
    return render(request,'gradingUser.html',context)

def direct(request):
    if request.method == 'POST':
        newUserName = request.POST.get('userName',None)
        user = User.objects.get(userName = newUserName)
        restaurants = Restaurant.getRestaurants(Restaurant)
        context = Context({'Restaurants' : restaurants,'user':user})
        return render(request,'gradingPoints.html',context)
        
        
def getPoint(request):
    if request.method == 'POST':
        gradUserName = request.POST.get('userName',None)
        inRestName = request.POST.getlist('restName[]',None)
        points = request.POST.getlist("points[]")
        counter = 0
        user = User.objects.get(userName = gradUserName)
        for point in points:
            if point != '':
                counter = counter + int(point)
            
        if counter <= user.userPoints:
            i = 0
            for point in points:
                if point != '':
                    restN = inRestName[i]
                    rest = Restaurant.objects.get(restName = restN)
                    Points.newPoint(Points,user,rest,point)
                    user.grade(int(point))
                i = i + 1 
            user.save()
            row = []
            returnList = []
            enteredPoints = Points.objects.all()
            for point in enteredPoints:
                rest = point.restaurant.restName
                user = point.user.userName
                row = {'restaurant':rest,'user':user,'point':point.point}
                returnList.append(row)
            context = Context({'Points' : returnList})
            return render(request,'enteredPoints.html',context)
        else:
            restaurants = Restaurant.getRestaurants(Restaurant).filter(serviceStatus = True)
            context = Context({'Restaurants' : restaurants})
            return render(request,'restaurants.html',context)
    else:
        row = []
        returnList = []
        enteredPoints = Points.objects.all()
        for point in enteredPoints:
                rest = point.restaurant.restName
                user = point.user.userName
                row = {'restaurant':rest,'user':user,'point':point.point}
                returnList.append(row)
        context = Context({'Points' : returnList})
        return render(request,'enteredPoints.html',context) 
    
    
def resetGrading(request):
    points = Points.objects.all().delete()
    return HttpResponseRedirect('grading/')           
           