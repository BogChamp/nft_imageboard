from django.shortcuts import render, get_object_or_404, redirect
from .models import Image, Users
from django.http import HttpResponse
from .forms import *
from django.utils import timezone

def image_list(request):
    images = Image.objects.order_by('likes')
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
            image.public = False
            image.token = '0' # TODO
            image.save()
            return redirect('image_detail', pk=image.pk)
    else:
        form = ImageForm()
    return render(request, 'imageboard/image_upload.html', {'form': form})

def success(request):
    return HttpResponse('successfully uploaded')

def login_page(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            if Users.objects.filter(login=request.POST.login, password=request.POST.password).exists():
                return redirect('/profile/'+request.POST.login)
            else:
                return render(request, 'imageboard/index.html', {'er': "Login or Password is wrong!"})
        else:
            return render(request, 'imageboard/index.html', {'er': "Fill all fields correctly."})
    return render(request, 'imageboard/index.html')

def register(request):
    if request.method != 'POST':
        return redirect('')
    form = UsersForm(request.POST)
    if form.is_valid():
        if Users.objects.filter(login=request.POST.login).exists():
            return render(request, 'imageboard/index.html', {'er': "User with this login already exists!"})
        user = Users.objects.create(login=request.POST.login, password=request.POST.password)
        user.save()
        return redirect('/profile/'+request.POST.login)
    else:
        return render(request, 'imageboard/index.html', {'er': "Fill all fields correctly."})
    