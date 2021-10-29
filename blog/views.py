# pylint: disable=maybe-no-member
import requests

from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.core.exceptions import PermissionDenied

from .models import Post
from .forms import PostForm



def index(request):
    return render(request, 'blog/index.html')

def success_post(request):

    # check if the user success post an article
    if not request.session.get('success_post'):
        raise PermissionDenied

    return render(request, 'blog/success-post.html')

def verify_recaptcha(siteverify):
    """
    Check if the reCAPTCHA key is indeed valid
    """
    URL = 'https://www.google.com/recaptcha/api/siteverify'
    resp = requests.post(URL, data={'secret': str(settings.RECAPTCHA_KEY), 'response': str(siteverify)})
    resp = resp.json()

    return resp

class PostList(ListView):
    model = Post
    template_name = 'blog/all-post.html'
    context_object_name = 'posts_list'
    paginate_by = 7

    def get_queryset(self):
        if self.request.GET.get('search'):
            return self.model.objects.filter(title__icontains=self.request.GET['search'], verified=True)
        else:
            return self.model.objects.filter(verified=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rand_post'] = self.model.objects.filter(verified=True).order_by('?')[:5]
        return context

class CategoryPostList(PostList):

    def get_queryset(self):
        return self.model.objects.filter(category=self.kwargs['category'], verified=True)

class AuthorPostList(PostList):

    def get_queryset(self):
        return self.model.objects.filter(author__icontains=self.kwargs['author'], verified=True)

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post-create-success')

    def form_valid(self, form):

        # get the key from reCAPTCHA
        # deny when the key is not supplied
        siteverify = self.request.POST.get('g-recaptcha-response')
        if siteverify:
            siteverify = verify_recaptcha(siteverify)
        else:
            raise PermissionDenied

        # Denied when reCAPTCHA challenge fail
        if not siteverify.get('success'):
            raise PermissionDenied

        # Mark for seeing the success page
        self.request.session['success_post'] = True
        self.request.session.set_expiry(60)

        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pylint: disable=maybe-no-member
        context['rand_post'] = self.model.objects.filter(verified=True).order_by('?')[:5]
        return context   
