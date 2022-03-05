from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('board', views.image_list, name='image_list'),
    path('image/new/', views.image_new, name='image_new'),
    path('image/<str:image_token>/', views.image_detail, name='image_detail'),
    path('profile/recovery', views.image_recover, name='recover'),
    path('', views.login_request, name='login'),
    path('registration', views.register_request, name='registration'),
    path('profile/<int:id>', views.profile, name="profile"),
    path('image/<str:image_token>/preference/', views.image_preference,
         name='image_preference'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
