from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CourseData
from .serializers import CourseSerializer
@api_view(['GET'])
def get_all_courses(request):
    courses = CourseData.objects.all()  # Fetch all courses
    serializer = CourseSerializer(courses, many=True)  # Serialize the data
    return Response(serializer.data)  # Return JSON response
