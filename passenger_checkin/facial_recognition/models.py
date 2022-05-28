from django.db import models

# Create your models here.
class Passenger(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    seat = models.CharField(max_length=3)
    e_ticket_number = models.CharField(max_length=50,primary_key=True)
    pnr = models.CharField(max_length=10)
    Class = models.CharField(max_length=20)
    flight_no = models.CharField(max_length=30)
    facedetected = models.BooleanField(default=False)

class flight(models.Model):
    flight_no = models.CharField(max_length=30,primary_key=True)
    departure_loc = models.CharField(max_length=50)
    arrival_loc = models.CharField(max_length=50)
    flight_date = models.DateField()
    dept_time = models.TimeField()
    arrival_time = models.TimeField()
    terminal = models.CharField(max_length=10)
    gate = models.CharField(max_length=10)
    boarding_time = models.TimeField()
