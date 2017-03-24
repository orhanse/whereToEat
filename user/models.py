from django.db import models

# Create your modeclls here.
class User(models.Model):
    userName = models.CharField(max_length= 40)
    userSurname = models.CharField(max_length= 40)
    userFirstName = models.CharField(max_length= 40)
    userEmail = models.EmailField()
    userPoints = models.IntegerField()
    
    
    
    def updateUser(self,User,oldUserName):
        upUser = self.objects.get(userName = oldUserName)
        upUser.userName = User.userName
        upUser.userSurname = User.userSurname
        upUser.userFirstName = User.userFirstName
        upUser.userEmail = User.userEmail
        upUser.save()
        
    
    def deleteUser(self,delUser):
        self.objects.get(userName = delUser).delete()
        
    def getUsers(self):
        return self.objects.values()
    
    def grade(self,points):
        self.userPoints = self.userPoints - points