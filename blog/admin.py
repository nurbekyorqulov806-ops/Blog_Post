from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Post, Comment, Like, PostViewHistory




@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ("Qo'shimcha ma'lumot", {'fields': ('avatar', 'bio', 'website', 'social_links')}),
    )




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)





@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'views_count', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'author__username', 'body')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status',)
    actions = ['make_published', 'make_pending']


    @admin.action(description="Tanlangan postlarni chop etish (PUBLISHED)")
    def make_published(self, request, queryset):
        queryset.update(status=Post.Status.PUBLISHED)

    @admin.action(description="Tanlangan postlarni moderatsiyaga qaytarish (PENDING)")
    def make_pending(self, request, queryset):
        queryset.update(status=Post.Status.PENDING)




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('body', 'author__username')




@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')





@admin.register(PostViewHistory)
class PostViewHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'viewed_at')
    list_filter = ('viewed_at',)
