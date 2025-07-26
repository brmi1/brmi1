from django.contrib import admin
from django.urls import path
from uploader import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload),
    path('data_list/', views.data_list)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)