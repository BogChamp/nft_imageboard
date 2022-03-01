from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('image/<int:pk>/', views.image_detail, name='image_detail'),
    path('image/new/', views.image_new, name='image_new'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)