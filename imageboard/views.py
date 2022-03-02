from django.shortcuts import render, get_object_or_404, redirect
from .models import Image, Users
from django.http import HttpResponse
from .forms import *
from django.utils import timezone

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
            image.token = '0' # TODO
            image.save()
            return redirect('image_detail', pk=image.pk)
    else:
        form = ImageForm()
    return render(request, 'imageboard/image_upload.html', {'form': form})

def success(request):
    return HttpResponse('successfully uploaded')

def login_page(request):
    if request.method != 'POST':
        return render(request, 'imageboard/login.html')
    form = UsersForm(request.POST)
    if form.is_valid():
        if Users.objects.filter(login=request.users.login, password=request.users.password).exists():
            return redirect('imageboard/profile.html')
        else:
            return render(request, 'imageboard/registration.html', {'error': "Login or password is wrong!"})

    return render(request, 'imageboard/registration.html', {'error': "Fill or forms correctly!"})

def registration(request):
    if request.method != 'POST':
        return render(request, 'imageboard/registration.html')
    form = UsersForm(request.POST)
    if form.is_valid():
        if Users.objects.filter(login=request.users.login).exists():
            return render(request, 'imageboard/registration.html', {'error': "User with this login already exists!"})
        user = Users.objects.create(login=request.users.login, password=request.users.password)
        user.save()
        return redirect('imageboard/profile.html')

    return render(request, 'imageboard/registration.html', {'error': "Fill or forms correctly!"})

def profile(request):
    return render(request, 'imageboard/profile.html')