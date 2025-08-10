from django.shortcuts import render , redirect

# Create your views here.

def mymap(request):
    return render (request , 'map/mymap.html')