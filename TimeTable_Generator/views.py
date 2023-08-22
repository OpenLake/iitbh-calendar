from django.shortcuts import render

from backend import fetch_course_codes_db,fetch_db_data,generate_pdf
from django.http import  HttpResponse
from django.contrib import messages

def index(request):

    if request.method == "POST":
        selected_options = request.POST.getlist('option')
        print(selected_options)
        content = fetch_db_data(user_input=selected_options,db_filepath="db.sqlite3")
        generate_pdf(content=content)

        messages.success(request, "View Pdf")



    context=fetch_course_codes_db("db.sqlite3")

    return render(request, "index.html",context)


def pdf_view(request):
    with open('TT.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=TimeTable.pdf'
        return response


