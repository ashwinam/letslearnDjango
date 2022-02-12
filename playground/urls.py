from django.urls import path
from . import views

urlpatterns = [
    # do need to call function we jst pass a reference
    path('hello/', views.say_hello)
]
