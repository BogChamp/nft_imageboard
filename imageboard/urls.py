from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('main', views.image_list, name='image_list'),
    path('image/<int:pk>/', views.image_detail, name='image_detail'),
    path('image/new/', views.image_new, name='image_new'),
    path('', views.login_page, name='login_page'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)