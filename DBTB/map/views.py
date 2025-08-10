from django.shortcuts import render , redirect

# Create your views here.

def map_view(request):
    return render (request , 'map/index.html')