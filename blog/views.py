import requests

from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.core.exceptions import PermissionDenied

from .models import Post
from .forms import PostForm



def index(request):
    return render(request, 'blog/index.html')

def success_post(request):
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

        return super().form_valid(form)
