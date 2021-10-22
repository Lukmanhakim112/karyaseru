from django.urls import path

from . import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    path('post/verify/', views.verify_post, name="verify-post"),
    path('post/delete/<slug:slug>/', views.DeletePostView.as_view(), name="delete-post"),
    path('post/update/<slug:slug>/', views.UpdatePostView.as_view(), name="update-post"),

    path('category/', views.CategoryListView.as_view(), name="all-category"),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name="delete-category"),

    path('home-form/', views.edit_homepage, name="homepage-edit"),
]
