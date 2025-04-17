import os
import csv
import django

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from api.models import CourseData


def backup_courses(path="backup_courses_db.csv"):
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["id","course_code", "course_name", "slot", "room", "discipline","instructor"])
        for obj in CourseData.objects.all():
            writer.writerow([obj.id,obj.course_code, obj.course_name, obj.slot, obj.room, obj.discipline,obj.instructor])


def clear_courses():
    CourseData.objects.all().delete()


if __name__ == "__main__":
    #backup_courses()
    clear_courses()

