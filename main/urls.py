from django.views.decorators.cache import cache_page
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("blogs/", views.blogs, name="blogs"),
    path("blog_detail/<slug:slug>", views.blog_detail, name="blog_detail"),
    path("author_blogs/<slug:slug>/", views.author_blogs, name="author_blogs"),
    path("categories/<slug:slug>", views.categories, name="categories"),
    path("my_blogs/", views.my_blogs, name="my_blogs"),
    path("add_blog/", views.add_blog, name="add_blog"),
    path("register/", views.register, name="register"),
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout_view, name="logout"),
    path("delete/<slug:slug>/", views.delete_blog, name="delete_blog"),
    path("edit/<slug:slug>/", views.edit_blog, name="edit_blog"),
]
