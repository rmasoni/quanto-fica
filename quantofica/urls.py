from django.urls import path

from quantofica.core import views


urlpatterns = [
    path('', views.home, name='home'),
]
