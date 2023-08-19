from django.contrib import admin

from .models import CourseData

class CourseDataAdmin(admin.ModelAdmin):
    list_display = ("course_code", "slot")
    list_filter = ("discipline",)
    search_fields = ("course_code",)

admin.site.register(CourseData,CourseDataAdmin)
