from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import BusStop, BusSchedule
from datetime import datetime

def bus_schedule(request):
    bus_stops = BusStop.objects.all()
    next_buses = []

    if request.method == "POST":
        selected_stop = BusStop.objects.get(id=request.POST['bus_stop'])
        next_buses = BusSchedule.objects.filter(bus_stop=selected_stop, arrival_time__gte=datetime.now().time()).order_by('arrival_time')

    return render(request, 'bus_schedule.html', {'bus_stops': bus_stops, 'next_buses': next_buses})

