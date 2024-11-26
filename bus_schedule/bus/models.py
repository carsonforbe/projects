from django.db import models

# Create your models here.
class BusStop(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BusSchedule(models.Model):
    bus_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE)
    arrival_time = models.TimeField()
    bus_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.bus_number} at {self.arrival_time}"
