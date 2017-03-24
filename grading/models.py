from django.db import models
from user.models import User
from restaurant.models import Restaurant
# Create your models here.
class Points(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    point = models.IntegerField()
    
    def newPoint(self,User,Restaurant,inPoint):
        if Points.objects.filter(user = User,restaurant = Restaurant).count() == 0:
            newPoint = Points(user = User,restaurant = Restaurant,point =inPoint)
        else:
            newPoint = Points.objects.get(user = User,restaurant = Restaurant)
            newPoint.point = int(inPoint) + newPoint.point

            
        newPoint.save()