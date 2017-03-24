from django.db import models

# Create your models here.
class App(models.Model):
    calculationPeriod = models.IntegerField()
    currentCity = models.CharField(max_length = 60)
    periodCounter = models.IntegerField()
    calculationCheck = models.BooleanField()
    
    def getCR(self):
        return self.objects.last()
    
    def setCR(self, App):
        self.calculationPeriod = App.calculationPeriod
        self.currentCity = App.currentCity
        self.periodCounter = App.periodCounter
        self.calculationCheck = App.calculationCheck
        self.save()
        
    def countDown(self):
        if self.periodCounter == 0:
            app = App.getCR(App)
            app.calculationCheck = False
            app.save()
        else:
            app = App.getCR(App)
            app.periodCounter = app.periodCounter -1
            app.save()
        
            