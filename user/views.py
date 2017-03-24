from django.shortcuts import render
from .models import User
from app.models import App

from django.http import HttpResponseRedirect
from django.template import Context
# Create your views here.
def getUser(request):  
    if request.method == 'POST':
        newUserName = request.POST.get('userName',None)
        newUserFirstName = request.POST.get('userFirstName', None)
        newUserLastName = request.POST.get('userLastName', None)
        newUserEmail = request.POST.get('userEmail', None)
        point = App.getCR(App)
        try:
            data = User.objects.get(userName = newUserName)
            return HttpResponseRedirect('user/showUsers/')            
        except User.DoesNotExist:
            newUser = User(userName = newUserName,userFirstName = newUserFirstName , userSurname = newUserLastName, userEmail = newUserEmail,userPoints = point.calculationPeriod)
            newUser.save()
            return HttpResponseRedirect('user/showUsers/')
            
    else:
        return HttpResponseRedirect('user/showUsers/')

    
def showUsers(request):
    users = User.getUsers(User)
    context = Context({'users' : users})
    return render(request,'users.html',context)

def addUser(request):
    return render(request,'AddUser.html')
    
    
def updateDirect(request):
    if request.method == 'POST':
        inUserName = request.POST.get('userName',None)
        user = User.objects.get(userName = inUserName)
    context = Context({'user' : user})
    return render(request,'updateUser.html',context)

def update(request):
     if request.method == 'POST':
        oldUserName = request.POST.get('oldUserName',None)
        newUserName = request.POST.get('userName',None)
        newUserFirstName = request.POST.get('userFirstName', None)
        newUserLastName = request.POST.get('userLastName', None)
        newUserEmail = request.POST.get('userEmail', None)
        point = App.getCR(App)
        upUser = User(userName = newUserName,userFirstName = newUserFirstName , userSurname = newUserLastName, userEmail = newUserEmail,userPoints = point.calculationPeriod)
        User.updateUser(User,upUser,oldUserName)
        return HttpResponseRedirect('user/showUsers/')
     else:
        return HttpResponseRedirect('user/showUsers/')
    
def delete(request):
     if request.method == 'POST':
        delUserName = request.POST.get('userName',None)
        User.deleteUser(User,delUserName)
        return HttpResponseRedirect('user/showUsers/')
     else:
        return HttpResponseRedirect('user/showUsers/')