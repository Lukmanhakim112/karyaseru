from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from blog.models import Category, Post
from .models import Homepage

def index(request):
    # pylint: disable=maybe-no-member
    post = Post.objects.filter(verified=True).order_by("-updated_at")
    homepage = Homepage.objects.all().first()
    categories = Category.objects.all()

    return render(request, 'homepage/index.html', {'post': post, 'homepage': homepage, 'categories': categories})

def get_post_by_category(request, category):

    # pylint: disable=maybe-no-member
    if category == 'all' or category == 'Semua':
        post = Post.objects.filter(verified=True).values('title', 'author', 'image','category__category' ,'ig_account', 'slug').order_by("-updated_at").distinct()

        # need refectoring of this section
        data = []
        data_before = ""

        # Create unique list of post
        for p in post:
            if not p.get("title") in data_before:
                data.append(p)  
                data_before = p.get("title")

        post = data

    elif category:
        cate = get_object_or_404(Category, slug=category)
        post = list(Post.objects.filter(category=cate, verified=True)[:3]
                .values('title', 'author', 'image', 'ig_account', 'category__category', 'slug'))

    return JsonResponse({'post': post})
