# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class CustomUser(AbstractUser):
    username = models.CharField("User username", max_length=150, unique=True)
    slug = models.SlugField("User slug", max_length=150, unique=True, blank=True)
    description = models.CharField(
        "User description", max_length=150, blank=True, null=True
    )
    email = models.EmailField("User email", max_length=150, unique=True)
    password = models.CharField("User password", max_length=150)
    image = models.ImageField("User image", upload_to="avatar/", blank=True, null=True)
    date = models.DateField("User date", auto_now_add=True)

    USERNAME_FIELD = (
        "username"  # Указываем email как уникальный идентификатор пользователя
    )
    REQUIRED_FIELDS = ["email"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class BlogCategory(models.Model):
    title = models.CharField("Category title", max_length=150)
    slug = models.SlugField("Category slug", max_length=150, unique=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blogs Category"
        verbose_name_plural = "Blogs Categories"


class Blog(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField("Blog title", max_length=150)
    slug = models.SlugField("Blog slug", max_length=150, unique=True, blank=True)
    text = models.TextField("Blog text", blank=True)
    image = models.ImageField(
        "Blog image", upload_to="blog_image/", blank=True, null=True
    )
    date = models.DateTimeField("Blog date", auto_now_add=True)
    views = models.IntegerField("Blog views", default=1)
    viewed_by = models.ManyToManyField(
        CustomUser, related_name="viewed_blogs", blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
