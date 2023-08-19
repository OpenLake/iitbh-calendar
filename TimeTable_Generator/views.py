from django.shortcuts import render
from .models import CourseData

def index(request):
    return render(request, "index.html")
