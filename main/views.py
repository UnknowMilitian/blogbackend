from django.contrib.auth import logout, authenticate, login as auth_login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.text import slugify
from .models import CustomUser, BlogCategory, Blog
from .forms import BlogForm
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.contrib import messages


def home(request):
    query = request.GET.get("q")
    if query:
        blogs_list = Blog.objects.filter(title__icontains=query).select_related(
            "author", "category"
        )
    else:
        blogs_list = Blog.objects.all().distinct()

    paginator = Paginator(blogs_list, 2)  # Adjust the number per page as needed

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "blogs": page_obj,  # Paginated queryset or search results
        "query": query,  # Pass the query to display in the search input
    }
    return render(request, "index.html", context)


def blogs(request):
    return render(request, "blogs.html")


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    # Increment the view count only if the user hasn't viewed this blog yet
    if request.user.is_authenticated:
        if not blog.viewed_by.filter(id=request.user.id).exists():
            blog.views += 1
            blog.viewed_by.add(request.user)
            blog.save()

    return render(request, "blog_detail.html", {"blog": blog})


def author_blogs(request, slug):
    author = get_object_or_404(CustomUser, slug=slug)
    blogs = Blog.objects.filter(author=author).select_related("author", "category")
    return render(request, "author_blogs.html", {"blogs": blogs, "author": author})


def categories(request, slug):
    cat = get_object_or_404(BlogCategory, slug=slug)
    blogs = Blog.objects.filter(category=cat).select_related("author", "category")
    return render(request, "categories.html", {"cat": cat, "blogs": blogs})


@login_required
def my_blogs(request):
    user = request.user
    blogs = Blog.objects.filter(author=user).select_related("author", "category")
    paginator = Paginator(blogs, 1)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "my_blogs.html", {"blogs": page_obj})


@login_required
def add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect(
                "blogs"
            )  # Redirect to the blog listing page or any other page
    else:
        form = BlogForm()
    return render(request, "add_blog.html", {"form": form})


# Authentication Functions
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        description = request.POST.get("description")
        password = request.POST.get("password")
        image = request.FILES.get("image")

        # Check if required fields are filled
        if not (username and email and description and password and image):
            context = {"message": "All fields are required"}
            return render(request, "auth_pages/register.html", context)

        try:
            slug = slugify(username)
            custom_user = CustomUser(
                username=username,
                email=email,
                description=description,
                image=image,
                slug=slug,
            )
            custom_user.set_password(password)
            custom_user.save()

            return HttpResponseRedirect(reverse("login"))
        except Exception as e:
            context = {
                "message": username + " username is already taken or smth went wrong"
            }
            return render(request, "auth_pages/register.html", context)

    return render(request, "auth_pages/register.html")


def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            context = {"message": "Invalid credentials"}
            return render(request, "auth_pages/login.html", context)
    else:
        return render(request, "auth_pages/login.html")


@login_required
def custom_logout_view(request):
    logout(request)
    return redirect("home")


# Deleting and Changing the BLogs


@login_required
def delete_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
    return redirect("my_blogs")


@login_required
def edit_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug, author=request.user)

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully.")
            return redirect(
                "my_blogs"
            )  # Redirect to the user's blog page after editing
    else:
        form = BlogForm(instance=blog)

    return render(request, "edit_blog.html", {"form": form, "blog": blog})
