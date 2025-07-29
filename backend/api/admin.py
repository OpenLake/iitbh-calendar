from django.contrib import admin

from .models import CourseData

class CourseDataAdmin(admin.ModelAdmin):
    list_display = ("course_code","course_name", "slot")
    list_filter = ("discipline",)
    search_fields = ("course_code","course_name")

admin.site.register(CourseData,CourseDataAdmin)
