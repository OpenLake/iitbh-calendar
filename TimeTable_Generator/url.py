from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view-pdf/', views.pdf_view,name='pdf_view'),


]