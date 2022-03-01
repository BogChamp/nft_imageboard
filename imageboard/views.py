from django.shortcuts import render, get_object_or_404
from .models import Image

def image_list(request):
    images = Image.objects.order_by('likes')
    return render(request, 'imageboard/image_list.html', {'images': images})

def image_detail(request, pk):
    image = get_object_or_404(Image, pk=pk)
    return render(request, 'imageboard/image_detail.html', {'image': image})
