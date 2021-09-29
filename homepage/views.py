from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from blog.models import Category, Post

def index(request):
    # pylint: disable=maybe-no-member
    post = Post.objects.all()[:3]
    return render(request, 'homepage/index.html', {'post': post})

def get_post_by_category(request, category):

    # pylint: disable=maybe-no-member
    if category == 'all' or category == 'Semua':
        post = list(Post.objects.filter(verfied=True)[:3].values('title', 'author', 'image', 'ig_account', 'category__category', 'slug'))
    elif category:
        cate = get_object_or_404(Category, category=category)
        post = list(Post.objects.filter(category=cate, verfied=True)[:3].values('title', 'author', 'image', 'ig_account', 'category__category', 'slug'))

    return JsonResponse({'post': post})
