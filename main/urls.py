from django.urls import path

from .views import index, other_page, DateInputView

app_name = 'main'
urlpatterns = [
    path('<str:page>', other_page, name='other'),
    path('', index, name='index'),
    path('birthday', DateInputView.as_view(), name='birthday')
]
