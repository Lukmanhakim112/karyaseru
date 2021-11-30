from django.urls import path

from . import views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    path('post/verify/', views.verify_post, name="verify-post"),
    path('post/create/', views.post_create, name="create-post"),
    path('post/delete/<slug:slug>/', views.DeletePostView.as_view(), name="delete-post"),
    path('post/update/<slug:slug>/', views.UpdatePostView.as_view(), name="update-post"),

    path('category/', views.CategoryListView.as_view(), name="all-category"),
    path('category/create/', views.CategoryCreateView.as_view(), name="create-category"),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view(), name="delete-category"),
    path('category/update/<int:pk>/', views.UpdateCategoryView.as_view(), name="update-category"),

    path('author/', views.AuthorListView.as_view(), name="all-author"),
    path('author/create/', views.AuthorCreateView.as_view(), name="create-author"),
    path('author/delete/<int:pk>/', views.AuthorDeleteView.as_view(), name="delete-author"),
    path('author/update/<int:pk>/', views.AuthorUpdateView.as_view(), name="update-author"),

    path('home-form/', views.edit_homepage, name="homepage-edit"),
]
