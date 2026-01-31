from django.urls import path

from .views import index, other_page, date_input, calc_result

app_name = 'main'
urlpatterns = [
    path('birthday', date_input, name='birthday'),
    path('result/<str:bday>', calc_result, name='result'),
    path('<str:page>', other_page, name='other'),
    path('', index, name='index'),
]
