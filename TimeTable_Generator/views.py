from django.shortcuts import render
from .models import CourseData # data base

from backend import fetch_course_codes_db,fetch_db_data,generate_pdf
def index(request):

    if request.method == "POST":
        selected_options = request.POST.getlist('option')
        print(selected_options)
        index = fetch_db_data(user_input=selected_options,db_filepath="db.sqlite3")
        generate_pdf(index=index)


    context=fetch_course_codes_db("db.sqlite3")

    return render(request, "index.html",context)
