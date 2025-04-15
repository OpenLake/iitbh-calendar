from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CourseData
from .serializers import CourseSerializer
from .backend import process_submission
@api_view(['GET'])
def get_all_courses(request):
    courses = CourseData.objects.all()  # Fetch all courses
    serializer = CourseSerializer(courses, many=True)  # Serialize the data
    return Response(serializer.data)  # Return JSON response

@api_view(['POST'])
def submit_selection(request):
    data = request.data

    # Validate that 'course_id_list' is in the request and is a list of integers
    if 'course_id_list' not in data or not isinstance(data['course_id_list'], list):
        return Response({'error': 'course_id_list must be provided as a list.'}, status=status.HTTP_400_BAD_REQUEST)

    # Optional: Check if all items in the list are integers
    if not all(isinstance(item, int) for item in data['course_id_list']):
        return Response({'error': 'All items in course_id_list must be integers.'}, status=status.HTTP_400_BAD_REQUEST)

    content = process_submission(data['course_id_list'])
    if type(content) == int:
        return Response({'error': f'Course with id {content} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    else:
        grid_map, clashes, additional_messages = content
        return Response({'mapping': grid_map,'clashes':clashes,'additional_messages':additional_messages}, status=status.HTTP_200_OK)