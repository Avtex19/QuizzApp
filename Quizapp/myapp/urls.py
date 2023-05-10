from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('question/<str:category_id>/', views.question, name='question'),
    path('result',views.result,name='result'),
    path('play_again',views.play_again,name='play_again'),
]
