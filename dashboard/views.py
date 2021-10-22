from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http.response import JsonResponse
from django.views.generic import DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from blog.models import Post, Category
from blog.forms import PostForm

from homepage.models import Homepage
from homepage.forms import HomepageForms


class UserIsAdmin(UserPassesTestMixin):
    # pylint: disable=maybe-no-member

    def test_func(self):
        return True if self.request.user.is_staff else False

def admin_check(user):
    return user.is_staff

@user_passes_test(admin_check)
def dashboard(request):
    # pylint: disable=maybe-no-member

    posts = Post.objects.all()
    total_post = posts.count()

    ctx = {
        "posts": posts,
        "total_post": total_post,
    }

    return render(request, "dashboard/dashboard.html", ctx)

@user_passes_test(admin_check)
def verify_post(request):
    # pylint: disable=maybe-no-member

    if request.method != "POST" or request.headers.get("X-Requested-With") != "XMLHttpRequest":
        raise PermissionDenied

    try:
        Post.objects.filter(slug=request.POST.get("slug-post")).update(verified=True)
    except Post.DoesNotExist:
        return JsonResponse({"success": False, "message": "Post Not Found!"}, status=404)

    return JsonResponse({"success": True})

@user_passes_test(admin_check)
def edit_homepage(request):
    # pylint: disable=maybe-no-member

    try:
        home = Homepage.objects.get(pk=1)
    except Homepage.DoesNotExist:
        home = None

    if request.method != "POST":
        ctx = { "form": HomepageForms(instance=home) }
        return render(request, "dashboard/homepage_form.html", ctx)

    form = HomepageForms(request.POST, request.FILES, instance=home)

    if not form.is_valid():
        return render(request, "dashboard/homepage_form.html", {"form": form})

    form.save()
    return redirect("homepage-edit")


class CategoryListView(UserIsAdmin, ListView):
    model = Category
    template_name = "dashboard/category_list.html"
    context_object_name = "categories"

class CategoryDeleteView(UserIsAdmin, DeleteView):
    model = Category
    success_url = reverse_lazy("all-category")

class UpdatePostView(UserIsAdmin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post_form.html"
    success_url = reverse_lazy("dashboard")

class DeletePostView(UserIsAdmin, DeleteView):
    model = Post
    success_url = reverse_lazy("dashboard")

