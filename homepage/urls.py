from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('post-category/<str:category>/', views.get_post_by_category, name="fect-post"),
]
