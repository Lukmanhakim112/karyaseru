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
    post = Post.objects.filter(verified=True).values('title', 'author__full_name', 'author__ig_account','image','category__category' , 'slug')

    # pylint: disable=maybe-no-member
    if category == 'all' or category == 'Semua':
        post.order_by("-updated_at").distinct()

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
        post = list(post.filter(category=cate)[:3])

    return JsonResponse({'post': post})
