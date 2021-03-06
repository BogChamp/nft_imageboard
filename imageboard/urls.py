from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('board', views.image_board, name='image_board'),
    path('image/upload/', views.image_upload, name='image_upload'),
    path('image/<str:image_token>/', views.image_info, name='image_info'),
    path('image/<str:image_token>/ban_image', views.ban_image,
         name='ban_image'),
    path('profile/recovery', views.image_recover, name='recover'),
    path('', views.login_request, name='login'),
    path('login', views.login_request, name='login'),
    path('registration', views.register_request, name='registration'),
    path('profile/<int:id>', views.profile, name="profile"),
    path('profile/<int:id>/ban_user', views.ban_user, name='ban_user'),
    path('profile/<int:id>/unban_user', views.unban_user, name='unban_user'),
    path('profile/<int:id>/change_profile/', views.change_profile,
         name="change_profile"),
    path('my_profile/', views.my_profile, name="my_profile"),
    path('privacy/<str:image_token>', views.change_privacy,
         name="change_privacy"),
    path('profile/<int:id>/change_avatar', views.change_avatar,
         name="change_avatar"),
    path('profile/<int:id>/get_images', views.get_images,
         name="get_images"),
    path('profile/<int:id>/get_images/<str:image_token>', views.get_image,
         name="get_image"),
    path('image/<str:image_token>/likes/', views.image_likes,
         name='image_likes'),
    path('moderation/accept/<int:request_id>', views.accept_request,
         name="accept_request"),
    path('moderation/approval_requests', views.approval_requests,
         name='approval_requests'),
    path('moderation/complaints', views.approval_complaints,
         name='complaints'),
    path('moderation/accept_complaint/<int:complaint_id>',
         views.accept_complaint,
         name="accept_complaint"),
    path('transfer', views.transfer, name='transfer'),
    path('image/<str:image_token>/add_comment', views.add_comment,
         name='add_comment'),
    path('image/<str:image_token>/complaint', views.add_complaint,
         name='complaint'),
    path('image/<str:image_token>/<int:id>', views.complaint_comment,
         name='complaint_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
