from django.shortcuts import render, get_object_or_404, redirect
from .models import Image, History, Image_Likes
from django.http import HttpResponse, HttpResponseForbidden
from .forms import *
from django.utils import timezone
from .forms import NewUserForm, UserInfoForm
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
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
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
            else:
                messages.error(request, "This image already exists")
                return render(request, 'imageboard/image_upload.html',
                              {'form': form})
    
    form = ImageForm()
    return render(request, 'imageboard/image_upload.html', {'form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('profile', user.id)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'imageboard/login.html', {"login_form": form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserInfo.objects.create(user=user).save()
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.error(request,
                       "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "imageboard/registration.html", {"register_form": form})


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
        return HttpResponseForbidden()
    return redirect("profile", request.user.id)


def profile(request, id):
    user_info = get_object_or_404(UserInfo, pk=id) 
    
    if user_info.user != request.user:
        user_pics = Image.objects.filter(owner=id, public=True)
        return render(request, 'imageboard/other_profile.html', {'user_info':user_info, 'pics':user_pics})
    
    user_pics = Image.objects.filter(owner=id)
    return render(request, 'imageboard/profile.html', {'user_info': user_info, 'pics': user_pics})


def change_profile(request, id):
    user_info = get_object_or_404(UserInfo, pk=id)
  
    if user_info.user != request.user:
        return HttpResponseForbidden()

    if request.method != "POST":
        form = UserInfoForm(instance=user_info)
        return render(request, 'imageboard/change_profile.html', {'form':form})
    
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
    return render(request, 'imageboard/change_profile.html', {'form':form})


def image_recover(request):
    if request.method == "POST":
        form = RecoveryForm(request.POST)
        if form.is_valid():
            secret_str = form.cleaned_data.get('secret')
            secret = sha256(secret_str.encode()).hexdigest()
            if Image().recover(secret):
                image = Image.objects.get(secret=secret)
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
                messages.error(request, "Rejected")
            return render(request, 'imageboard/recovery.html', {'form': form})
    
    form = RecoveryForm()
    return render(request, 'imageboard/recovery.html', {'form': form})
