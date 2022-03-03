from django.shortcuts import render, get_object_or_404, redirect
from .models import Image
from django.http import HttpResponse
from .forms import *
from django.utils import timezone
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
import hashlib


def image_list(request):
    images = Image.objects.filter(public=True).order_by('likes')
    return render(request, 'imageboard/image_list.html', {'images': images})


def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    return render(request, 'imageboard/image_detail.html', {'image': image})


def image_new(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.published_date = timezone.now()
            image.owner = request.user
            image.likes = 0
            # image.token = hashlib.sha1(image.image.instance).hexdigest()
            image.token = 0
            image.save()
            return redirect('image_detail', pk=image.pk)
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
                return redirect('imageboard/profile.html')
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
            return redirect("imageboard/profile.html")
        messages.error(request,
                       "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request,
                  template_name="imageboard/registration.html",
                  context={"register_form": form})


def profile(request):
    return render(request, 'imageboard/profile.html')
