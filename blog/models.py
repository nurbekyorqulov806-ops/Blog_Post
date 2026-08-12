from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify




# ---------------------------------------------------------------------------
# 2.1 — Custom User modeli
# ---------------------------------------------------------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to='avatars/', default='avatars/default.png', blank=True
    )
    bio = models.TextField(blank=True, help_text="Foydalanuvchi haqida qisqacha ma'lumot")
    website = models.URLField(blank=True)
    social_links = models.JSONField(
        blank=True, default=dict,
        help_text="Masalan: {'telegram': 'https://t.me/...'}"
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.username})


# ---------------------------------------------------------------------------
# 2.2 — Category modeli
# ---------------------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


# ---------------------------------------------------------------------------
# 2.3 — Post modeli
# ---------------------------------------------------------------------------
class Post(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Moderatsiyada'
        PUBLISHED = 'PUBLISHED', "Chop etilgan"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts'
    )
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    desc = models.TextField(max_length=300, help_text="Maqola haqida qisqacha ko'chirma")
    body = models.TextField(help_text="Maqolaning to'liq matni")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:250]
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    @property
    def likes_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()


# ---------------------------------------------------------------------------
# 2.4 — Comment modeli
# ---------------------------------------------------------------------------
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments'
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author} -> {self.post} izohi'


# ---------------------------------------------------------------------------
# Like modeli — bosilgan post = sevimli post
# ---------------------------------------------------------------------------
class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} ♥ {self.post}'


# ---------------------------------------------------------------------------
# PostViewHistory modeli — foydalanuvchi bosgan postlar tarixi
# ---------------------------------------------------------------------------
class PostViewHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='view_history'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='view_history')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        verbose_name_plural = 'Post view history'

    def __str__(self):
        return f'{self.user} -> {self.post} ({self.viewed_at:%Y-%m-%d %H:%M})'




