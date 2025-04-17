from django.db import models

class CourseData(models.Model):
    course_code = models.CharField(max_length=50,unique=True)
    course_name = models.CharField(max_length=255)
    slot = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    discipline = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)


    def __str__(self):
        return self.course_code