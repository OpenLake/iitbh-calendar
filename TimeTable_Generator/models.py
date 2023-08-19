from django.db import models

class CourseData(models.Model):
    course_code = models.CharField(max_length=20,unique=True)
    course_name = models.CharField(max_length=20)
    slot = models.CharField(max_length=20)
    room = models.CharField(max_length=20)
    discipline = models.CharField(max_length=20)
    instructor = models.CharField(max_length=20)


    def __str__(self):
        return self.course_code
        

