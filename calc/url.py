from django.urls import path, re_path
from . import views

app_name = 'calc'


urlpatterns = [
    # The home page
    path('', views.index, name='home'),
]