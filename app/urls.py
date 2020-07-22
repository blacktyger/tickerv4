from django.urls import path, re_path
from .views import IndexView, index, pages

urlpatterns = [
    # Matches any html file 
    re_path(r'^.*\.html', pages, name='pages'),

    # The home page
    path('', index, name='home'),
    path('test/', IndexView.as_view(), name='test'),
]

