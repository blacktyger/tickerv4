from django.contrib import admin
from django.urls import path, include  # add this
from rest_framework import routers, serializers, viewsets
from background_task.models import Task

from app import views
from app.tasks import clear_db_task, update_all, save_history
from . import settings

router = routers.DefaultRouter()
router.register(r'data', views.DataViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("", include("authentication.urls")),
    path("", include("app.urls")),
    path("calc/", include("calc.urls")),
    path('api/', include(router.urls)),
    ]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),
                      ] + urlpatterns

clear_db_task(save_history())
save_history(repeat=Task.HOURLY)
clear_db_task(update_all())
update_all(repeat=500, verbose_name='update_all')


