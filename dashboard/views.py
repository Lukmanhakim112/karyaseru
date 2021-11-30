from django.db.models import fields
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http.response import JsonResponse
from django.views.generic import DeleteView, ListView, UpdateView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from .forms import PostFormDashboard

from blog.models import Post, Category, Author
from blog.forms import (
    PostForm, CategoryForm,
    AuthorFormset, AuthorFormSetHelper
)

from homepage.models import Homepage
from homepage.forms import HomepageForms


class UserIsAdmin(UserPassesTestMixin):
    # pylint: disable=maybe-no-member

    def test_func(self):
        return True if self.request.user.is_superuser else False

def admin_check(user):
    return user.is_staff

@user_passes_test(admin_check)
def dashboard(request):
    # pylint: disable=maybe-no-member

    key_search = request.GET.get("search") 
    if key_search:
        posts = Post.objects.filter(title__icontains=key_search)
    else:
        posts = Post.objects.all()

    total_post = posts.count()

    ctx = {
        "posts": posts,
        "total_post": total_post,
    }

    return render(request, "dashboard/dashboard.html", ctx)

@user_passes_test(admin_check)
def post_create(request):

    author_form = AuthorFormset()
    post_form = PostForm()

    if request.method == 'POST':

        author_form = AuthorFormset(request.POST)
        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid() and author_form.is_valid():

            # TODO: Refactor this section
            # create author object if does not exsist
            # retrive otherwise
            authors_list = []
            for author in author_form:
                obj = Author.objects.get_or_create(
                    ig_account=author.cleaned_data.get('ig_account'),
                    defaults={
                        'full_name': author.cleaned_data.get('full_name'),
                        'ig_account': author.cleaned_data.get('ig_account')
                    }
                )
                authors_list.append(obj[0])

            post = post_form.save()
            # Set author
            post.author.set(authors_list)

            # Mark for seeing the success page
            request.session['success_post'] = True
            request.session.set_expiry(60)

            return redirect('dashboard')


    context = {
        'author_form_helper': AuthorFormSetHelper(),
        'author_form': author_form,
        'post_form': post_form,
    }

    return render(request, 'dashboard/post_form.html', context)


@user_passes_test(admin_check)
def verify_post(request):
    # pylint: disable=maybe-no-member

    if request.method != "POST" or request.headers.get("X-Requested-With") != "XMLHttpRequest":
        raise PermissionDenied

    try:
        post = Post.objects.filter(slug=request.POST.get("slug-post"))

        if request.POST.get("verify") == "True":
            post.update(verified=False)
        else:
            post.update(verified=True)

    except Post.DoesNotExist:
        return JsonResponse({"success": False, "message": "Post Not Found!"}, status=404)

    return JsonResponse({"success": True})

def edit_homepage(request):
    # pylint: disable=maybe-no-member

    if not request.user.is_superuser:
        raise PermissionDenied

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

class AuthorListView(UserIsAdmin, ListView):
    model = Author
    template_name = "dashboard/author_list.html"
    context_object_name = "authors"

class AuthorDeleteView(UserIsAdmin, DeleteView):
    model = Author
    success_url = reverse_lazy('all-author')

class AuthorUpdateView(UserIsAdmin, UpdateView):
    model = Author
    fields = '__all__'
    template_name = "dashboard/author_form.html"
    success_url = reverse_lazy("all-author")

class AuthorCreateView(UserIsAdmin, CreateView):
    model = Author
    fields = '__all__'
    template_name = 'dashboard/author_form.html'
    success_url = reverse_lazy("all-author")

class CategoryListView(UserIsAdmin, ListView):
    model = Category
    template_name = "dashboard/category_list.html"
    context_object_name = "categories"

class CategoryDeleteView(UserIsAdmin, DeleteView):
    model = Category
    success_url = reverse_lazy("all-category")

class CategoryCreateView(UserIsAdmin, CreateView):
    model = Category
    form_class = CategoryForm 
    template_name = "dashboard/category_form.html"
    success_url = reverse_lazy("all-category")

class UpdateCategoryView(UserIsAdmin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/category_form.html"
    success_url = reverse_lazy("all-category")

class CreatePostView(UserIsAdmin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post_form.html"
    success_url = reverse_lazy("dashboard")

class UpdatePostView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostFormDashboard
    template_name = "dashboard/post_form_update.html"
    success_url = reverse_lazy("dashboard")

    def test_func(self):
        return True if self.request.user.is_staff else False

class DeletePostView(UserIsAdmin, DeleteView):
    model = Post
    success_url = reverse_lazy("dashboard")

