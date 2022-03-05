from django.shortcuts import render, get_object_or_404, redirect
from .models import Image, History, Preference
from django.http import HttpResponse
from .forms import *
from django.utils import timezone
from .forms import NewUserForm, UserInfoForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from . import recovery
from hashlib import sha256

def image_list(request):
    images = Image.objects.filter(public=True).order_by('likes')
    return render(request, 'imageboard/image_list.html', {'images': images})


def image_detail(request, image_token):
    image = get_object_or_404(Image, token=image_token)
    history = History.objects.filter(image=image).order_by('date')
    preferences = Preference.objects.filter(image=image).order_by('date')
    return render(request, 'imageboard/image_detail.html',
                  {'image': image, 'history': history,
                   'preferences': preferences})


def image_new(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.owner = request.user
            secret = recovery.generate_secret()
            secret_str = recovery.get_str_secret(secret)
            print(secret_str) # TODO
            if image.publish():
                image.secret = sha256(secret_str.encode()).hexdigest()
                image.save()
                return image_detail(request, image.token)
            else:
                messages.error(request, "This image already exists")
                return render(request, 'imageboard/image_upload.html',
                              {'form': form})
    else:
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
    return render(request=request,
                  template_name='imageboard/login.html',
                  context={"login_form": form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            UserInfo.objects.create(user=request.user).save()
            return redirect("profile", user.id)
        messages.error(request,
                       "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request,
                  template_name="imageboard/registration.html",
                  context={"register_form": form})


def image_preference(request, image_token):
    if request.method == "POST":
        image = get_object_or_404(Image, token=image_token)

        try:
            Preference.objects.get(user=request.user, image=image)
            return image_detail(request, image.token)

        except Preference.DoesNotExist:
            upref = Preference()
            upref.user = request.user
            upref.image = image
            image.likes += 1
            upref.save()
            image.save()
            return image_detail(request, image.token)
    else:
        image = get_object_or_404(Image, token=image_token)
        return image_detail(request, image.token)


def profile(request, id):
    user_info = UserInfo.objects.get(id=id)
    form = UserInfoForm()
    user_pics = Image.objects.filter(owner=request.user)
    if request.method == "POST":
        form = UserInfoForm(request.POST, instance=user_info)
        if form.is_valid():
            form.save()
            return render(request, 'imageboard/profile.html', {'user_info': user_info, 'form': form, 'pics': user_pics})
        messages.error(request,
                       "AAA.")
    user_info = get_object_or_404(UserInfo, pk=id) 
    return render(request, 'imageboard/profile.html', {'user_info': user_info, 'form': form, 'pics': user_pics})

def image_recover(request):
    if request.method == "POST":
        form = RecoveryForm(request.POST)
        if form.is_valid():
            secret_str = form.cleaned_data.get('secret')
            secret = sha256(secret_str.encode()).hexdigest()
            owner = request.user
            if Image().recover(secret):
                messages.success(request, "Recovery successful")
            else:
                messages.error(request, "Rejected")
            return render(request, 'imageboard/recovery.html', {'form': form})
    else:
        form = RecoveryForm()
    return render(request, 'imageboard/recovery.html', {'form': form})
