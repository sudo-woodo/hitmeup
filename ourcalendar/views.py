from django.shortcuts import render
from .models import *

# Create your views here.
def calendar(request):
    context = {'events': Event.objects.all()}
    return render(request, 'ourcalendar/index.jinja',context)