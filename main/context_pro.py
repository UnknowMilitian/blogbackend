# context_pro.py

from django.db.models import Count
from .models import CustomUser, BlogCategory, Blog
from django.core.paginator import Paginator


def pagination_context(request):
    # Assuming you want 10 blogs per page by default
    blogs = Blog.objects.select_related("author", "category").all()
    paginator = Paginator(blogs, 2)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return {
        "blogs": page_obj,  # 'blogs' is now paginated
    }


def my_custom_context_processor(request):
    # Annotate each CustomUser object with the count of related Blog objects
    users = CustomUser.objects.annotate(blog_count=Count("blog")).order_by(
        "-blog_count"
    )[:10]

    return {
        "users": users,
        "all_blogs": Blog.objects.all(),
        "all_categories": BlogCategory.objects.all(),
    }
