from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from blog.models import Category, Post
from .models import Homepage

def index(request):
    # pylint: disable=maybe-no-member
    post = Post.objects.all()[:3]
    homepage = Homepage.objects.all().first()

    return render(request, 'homepage/index.html', {'post': post, 'homepage': homepage})

def get_post_by_category(request, category):

    # pylint: disable=maybe-no-member
    if category == 'all' or category == 'Semua':
        post = list(Post.objects.filter(verified=True)[:3].values('title', 'author', 'image', 'ig_account', 'category__category', 'slug'))
    elif category:
        cate = get_object_or_404(Category, category=category)
        post = list(Post.objects.filter(category=cate, verified=True)[:3].values('title', 'author', 'image', 'ig_account', 'category__category', 'slug'))

    return JsonResponse({'post': post})
