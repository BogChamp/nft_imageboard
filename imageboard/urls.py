from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('board', views.image_board, name='image_board'),
    path('image/upload/', views.image_upload, name='image_upload'),
    path('image/<str:image_token>/', views.image_info, name='image_info'),
    path('profile/recovery', views.image_recover, name='recover'),
    path('', views.login_request, name='login'),
    path('login', views.login_request, name='login'),
    path('registration', views.register_request, name='registration'),
    path('profile/<int:id>', views.profile, name="profile"),
    path('profile/<int:id>/change_profile/', views.change_profile,
         name="change_profile"),
    path('my_profile/', views.my_profile, name="my_profile"),
    path('privacy/<str:image_token>', views.change_privacy, name="change_privacy"),
    path('image/<str:image_token>/likes/', views.image_likes,
         name='image_likes'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
