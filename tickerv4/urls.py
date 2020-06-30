from django.contrib import admin
from django.urls import path, include  # add this
from rest_framework import routers, serializers, viewsets

from app import views
from app.tasks import clear_db_task, up_data1, up_data2, up_exchanges

router = routers.DefaultRouter()
router.register(r'data', views.DataViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("", include("authentication.urls")),
    path("", include("app.urls")),
    path('api/', include(router.urls)),
    ]

TASKS = {'up_data1': up_data1, 'up_exchanges': up_exchanges, 'up_data2': up_data2}

for name, task in TASKS.items():
    clear_db_task(name)
    task(repeat=300, verbose_name=name)


