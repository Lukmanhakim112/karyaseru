from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name="post"),

    path('create/', views.PostCreateView.as_view(), name="post-create"),
    path('create/success/', views.success_post, name="post-create-success"),
]
