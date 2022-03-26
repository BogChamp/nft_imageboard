from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from imageboard.models import Image, History, Image_Likes, ModerationRequest
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from imageboard.forms import (
    NewUserForm, UserInfoForm, PrivacyForm,
    AvatarForm, RecoveryForm, ImageForm, UserInfo, ApprovalForm
)
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from . import recovery
from hashlib import sha256


def image_board(request):
    images = Image.objects.filter(public=True).order_by('-likes')
    return render(request, 'imageboard/image_board.html', {'images': images})


def image_info(request, image_token):
    image = get_object_or_404(Image, token=image_token)
    if not image.public and image.owner != request.user:
        return HttpResponseForbidden()
    history = History.objects.filter(image=image).order_by('-date')
    likes = Image_Likes.objects.filter(image=image).order_by('-date')
    return render(request, 'imageboard/image_info.html',
                  {'image': image, 'history': history,
                   'likes': likes})


def image_upload(request):
    if request.method != 'POST':
        form = ImageForm()
        return render(request, 'imageboard/image_upload.html', {'form': form})

    form = ImageForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "Invalid form!")
        return render(request, 'imageboard/image_upload.html', {'form': form})

    image = form.save(commit=False)
    image.owner = request.user
    secret = recovery.generate_secret()
    secret_str = recovery.get_str_secret(secret)
    if image.publish():
        image.secret = sha256(secret_str.encode()).hexdigest()
        image.public = form.cleaned_data.get('public')
        image.save()
        messages.info(request, secret_str)
        return redirect("image_info", image.token)

    messages.error(request, "This image already exists")
    return render(request, 'imageboard/image_upload.html', {'form': form})


def login_request(request):
    if request.method != "POST":
        form = AuthenticationForm()
        return render(request, 'imageboard/login.html', {"login_form": form})

    form = AuthenticationForm(request, data=request.POST)
    if not form.is_valid():
        messages.error(request, "Invalid username or password.")
        return render(request, 'imageboard/login.html', {"login_form": form})

    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    user = authenticate(username=username, password=password)
    if user is None:
        messages.error(request, "Invalid username or password.")
        return render(request, 'imageboard/login.html', {"login_form": form})

    login(request, user)
    messages.info(request, f"You are now logged in as {username}.")
    return redirect('profile', user.id)


def register_request(request):
    if request.method != "POST":
        form = NewUserForm()
        return render(request, "imageboard/registration.html",
                      {"register_form": form})

    form = NewUserForm(request.POST)
    if not form.is_valid():
        messages.error(request,
                       "Unsuccessful registration. Invalid information.")
        return render(request, "imageboard/registration.html",
                      {"register_form": form})

    user = form.save()
    UserInfo.objects.create(user=user).save()
    messages.success(request, "Registration successful.")
    return redirect("login")


def image_likes(request, image_token):
    image = get_object_or_404(Image, token=image_token)
    if request.method != "POST":
        return redirect('image_info', image.token)

    if not Image_Likes.objects.filter(user=request.user, image=image).exists():
        Image_Likes.objects.create(user=request.user, image=image).save()
        image.likes += 1
        image.save()

    return redirect('image_info', image.token)


def my_profile(request):
    if not User.objects.filter(id=request.user.id).exists():
        return redirect('login')
    return redirect("profile", request.user.id)


def profile(request, id):
    user = get_object_or_404(User, pk=id)
    user_info = get_object_or_404(UserInfo, user=user)

    if user_info.user != request.user:
        user_pics = Image.objects.filter(owner=id, public=True)
        return render(request, 'imageboard/other_profile.html',
                      {'user_info': user_info, 'pics': user_pics})

    user_pics = Image.objects.filter(owner=id)
    pics_forms = [PrivacyForm(instance=image) for image in user_pics]
    avatar = user_pics.filter(avatar=True)
    if avatar.exists():
        avatar = avatar[0]
    avatar_form = AvatarForm()
    return render(request, 'imageboard/profile.html',
                  {'user_info': user_info, 'pics': zip(user_pics, pics_forms),
                   'avatar': avatar, 'avatar_form': avatar_form})


def change_avatar(request, id):
    if id != request.user.id:
        return HttpResponseForbidden()

    if request.method != "POST":
        return redirect('my_profile')

    form = AvatarForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Can't change avatar")
        return redirect('my_profile')

    image = Image.objects.filter(owner=id, public=True)
    if not image.filter(token=form.cleaned_data.get('token')).exists():
        messages.error(request, "Use your public image!!!")
        return redirect('my_profile')

    old_avatar = image.filter(avatar=True)
    if old_avatar.exists():
        old_avatar = old_avatar[0]
        old_avatar.avatar = False
        old_avatar.save()
    image = image.get(token=form.cleaned_data.get('token'))
    image.avatar = True
    image.save()
    messages.success(request, "Avatar changed successfully!")
    return redirect('my_profile')


def change_profile(request, id):
    user_info = get_object_or_404(UserInfo, pk=id)

    if user_info.user != request.user:
        return HttpResponseForbidden()

    if request.method != "POST":
        form = UserInfoForm(instance=user_info)
        return render(request, 'imageboard/change_profile.html',
                      {'form': form})

    form = UserInfoForm(request.POST)
    if form.is_valid():
        user_info = UserInfo.objects.get(user=request.user)
        user_info.name = form.cleaned_data.get('name')
        user_info.second_name = form.cleaned_data.get('second_name')
        user_info.info = form.cleaned_data.get('info')
        user_info.save()
        messages.success(request, "Info changed successfully!")
        return redirect('profile', id)

    messages.error(request, "Something went wrong(")
    return render(request, 'imageboard/change_profile.html', {'form': form})


def image_recover(request):
    if request.method != "POST":
        form = RecoveryForm()
        return render(request, 'imageboard/recovery.html', {'form': form})

    form = RecoveryForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Invalid form.")
        return render(request, 'imageboard/recovery.html', {'form': form})

    secret_str = form.cleaned_data.get('secret')
    secret = sha256(secret_str.encode()).hexdigest()
    if not Image().recover(secret):
        messages.error(request, "Rejected")
        return render(request, 'imageboard/recovery.html', {'form': form})

    image = Image.objects.get(secret=secret)
    if image.public:
        image.owner = request.user
        image.save()
        history_log = History.objects.create(
            owner=request.user,
            image=image,
            date=timezone.now()
        )
        history_log.save()
        messages.success(request, "Recovery successful")
    else:
        moder_req = ModerationRequest.objects.create(
            user=request.user,
            image=image,
        )
        moder_req.save()
        messages.success(request, "Send to moderator approval")
    return redirect('profile', request.user.id)


def approval_requests(request):
    requests = ModerationRequest.objects.filter(accept=False)
    user_info = get_object_or_404(UserInfo, user=request.user)
    if not user_info.moderator:
        return HttpResponseForbidden()
    approval_forms = [ApprovalForm(instance=r) for r in requests]
    return render(request, 'imageboard/approval_requests.html',
                  {'requests': zip(requests, approval_forms)})


def accept_request(request, request_id):
    moderation_request = get_object_or_404(ModerationRequest, id=request_id)
    moderation_request.accept = True
    moderation_request.save()
    image = moderation_request.image
    image.owner = moderation_request.user
    image.save()
    history_log = History.objects.create(
        owner=moderation_request.user,
        image=image,
        date=timezone.now()
    )
    history_log.save()
    return redirect('approval_requests')


def change_privacy(request, image_token):
    image = get_object_or_404(Image, token=image_token)
    if request.user != image.owner:
        return HttpResponseForbidden()

    if request.method != "POST":
        return redirect('my_profile')

    data = PrivacyForm(request.POST)
    if not data.is_valid():
        messages.error(request, "Wrong form of publicity.")
        return redirect('my_profile')

    if image.avatar == True:
        messages.error(request, "Can't change privacy for avatar")
        return redirect('my_profile')

    image.public = data.cleaned_data.get('public')
    image.save()
    return redirect('my_profile')
