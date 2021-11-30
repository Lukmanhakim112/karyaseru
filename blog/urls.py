from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name="post"),
    path('c/<str:category>/', views.CategoryPostList.as_view(), name="post-category"),
    path('a/<str:author>/', views.AuthorPostList.as_view(), name="post-author"),

    path('create/', views.post_create, name="post-create"),
    path('p/<slug:slug>/', views.PostDetailView.as_view(), name="post-detail"),
    path('create/success/', views.success_post, name="post-create-success"),
]
