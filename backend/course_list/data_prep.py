import os
import csv
import django

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from api.models import CourseData


def backup_courses(path="Backup/db_courses.csv"):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id","code", "name", "num_credits", "department", "professor"])
        for obj in CourseData.objects.all():
            writer.writerow([obj.id,obj.code, obj.name, obj.num_credits, obj.department, obj.professor])

def clear_coursedata():
    backup_courses()
    # Delete all student records
    CourseData.objects.all().delete()
    print("✅ All courses have been deleted!")


def create_import_csv(csv_filepath="courses.csv", output_filepath="import_courses.csv"):
    data = []

    with open(csv_filepath, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header

        count = 1
        for line in reader:
            if len(line) < 6:  # malformed
                continue

            course_code = line[0].strip()[:19]
            course_name = line[1].strip()[:254]
            discipline = line[2].strip()[:254]
            slot = line[3].strip()
            instructor = line[4].strip()[:254]
            room = line[5].strip()[:254]

            data.append([count,course_code,course_name,discipline,slot,instructor,room])
            count+=1


                # Writing filtered data to new CSV file
    with open(output_filepath, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)  # Ensures fields are properly quoted

        # Write the header
        writer.writerow(["id","course_code","course_name","discipline","slot","instructor","room"])

        # Write the filtered data
        writer.writerows(data)

    with open(output_filepath, "r", encoding="utf-8") as file:
        content = file.read().replace("\xa0", " ")

    with open(output_filepath, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Filtered data written to {output_filepath} 🚀")


if __name__ =="__main__":
    create_import_csv()