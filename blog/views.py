from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm

from .forms import RegisterForm, ProfileEditForm, PostForm, CommentForm
from .models import (
    CustomUser,
    Category,
    Post,
    Comment,
    Like,
    PostViewHistory,
)


# ============================================================
# 3.1 — REGISTER
# ============================================================

def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Muvaffaqiyatli ro'yxatdan o'tdingiz!"
            )

            return redirect('/')

    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


# ============================================================
# LOGIN
# ============================================================

def custom_login_view(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            next_url = (
                request.POST.get('next')
                or request.GET.get('next')
            )

            if next_url:
                return redirect(next_url)

            return redirect('/')

    else:

        form = AuthenticationForm()

    return render(
        request,
        'login.html',
        {
            'form': form
        }
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required
def custom_logout_view(request):

    logout(request)

    return redirect('/')


# ============================================================
# PROFILE EDIT
# ============================================================

@login_required
def profile_edit(request):

    if request.method == 'POST':

        form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Profil yangilandi.'
            )

            return redirect(
                'profile',
                username=request.user.username
            )

    else:

        form = ProfileEditForm(
            instance=request.user
        )

    return render(
        request,
        'profile_edit.html',
        {
            'form': form
        }
    )


# ============================================================
# PROFILE DETAIL
# ============================================================

def profile_detail(request, username):

    profile_user = get_object_or_404(
        CustomUser,
        username=username
    )

    posts = Post.objects.filter(
        author=profile_user
    ).order_by('-created_at')

    return render(
        request,
        'profile_detail.html',
        {
            'profile_user': profile_user,
            'posts': posts
        }
    )


# ============================================================
# 3.2 — POST LIST
# ============================================================

def post_list(request):

    posts = Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).select_related(
        'author',
        'category'
    )

    # -------------------------
    # SEARCH
    # -------------------------

    query = request.GET.get('q')

    if query:

        posts = posts.filter(
            Q(title__icontains=query)
            |
            Q(body__icontains=query)
            |
            Q(author__username__icontains=query)
        )

    # -------------------------
    # SORT
    # -------------------------

    sort = request.GET.get('sort')

    if sort == 'popular':

        posts = posts.order_by(
            '-views_count'
        )

    else:

        posts = posts.order_by(
            '-created_at'
        )

    # -------------------------
    # PAGINATION
    # -------------------------

    paginator = Paginator(
        posts,
        9
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    categories = Category.objects.all()

    return render(
        request,
        'post_list.html',
        {
            'posts': page_obj,
            'page_obj': page_obj,
            'categories': categories,
            'query': query or ''
        }
    )


# ============================================================
# CATEGORY DETAIL
# ============================================================

def category_detail(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug
    )

    posts = Post.objects.filter(
        category=category,
        status=Post.Status.PUBLISHED
    ).order_by(
        '-created_at'
    )

    paginator = Paginator(
        posts,
        9
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    categories = Category.objects.all()

    return render(
        request,
        'category_detail.html',
        {
            'posts': page_obj,
            'page_obj': page_obj,
            'category': category,
            'categories': categories
        }
    )


# ============================================================
# POST DETAIL
# ============================================================

def post_detail(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )
# -------------------------
# VIEWS COUNT + HISTORY
# -------------------------

    if request.user.is_authenticated:

        already_viewed = PostViewHistory.objects.filter(
            user=request.user,
            post=post
        ).exists()

        if not already_viewed:

            PostViewHistory.objects.create(
                user=request.user,
                post=post
            )

            Post.objects.filter(
                pk=post.pk
            ).update(
                views_count=post.views_count + 1
            )

            post.refresh_from_db()



    # -------------------------
    # COMMENTS
    # -------------------------

    comments = post.comments.select_related(
        'author'
    )

    # -------------------------
    # COMMENT FORM
    # -------------------------

    comment_form = CommentForm()

    # -------------------------
    # RELATED POSTS
    # -------------------------

    related_posts = Post.objects.filter(
        category=post.category,
        status=Post.Status.PUBLISHED
    ).exclude(
        pk=post.pk
    )[:3]

    # -------------------------
    # LIKE
    # -------------------------

    is_liked = post.is_liked_by(
        request.user
    )

    return render(
        request,
        'post_detail.html',
        {
            'post': post,
            'comments': comments,
            'comment_form': comment_form,
            'related_posts': related_posts,
            'is_liked': is_liked
        }
    )


# ============================================================
# POST CREATE
# ============================================================

@login_required
def post_create(request):

    if request.method == 'POST':

        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            post = form.save(
                commit=False
            )

            post.author = request.user

            # Moderatsiyaga yuboriladi
            post.status = Post.Status.PENDING

            post.save()

            messages.success(
                request,
                "Post yuborildi, moderator tekshiruvidan so'ng chop etiladi."
            )

            return redirect(
                'post_detail',
                slug=post.slug
            )

    else:

        form = PostForm()

    return render(
        request,
        'post_form.html',
        {
            'form': form
        }
    )


# ============================================================
# POST UPDATE
# ============================================================

@login_required
def post_update(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    # -------------------------
    # PERMISSION
    # -------------------------

    if (
        request.user != post.author
        and not request.user.is_superuser
    ):
        raise PermissionDenied

    # -------------------------
    # UPDATE
    # -------------------------

    if request.method == 'POST':

        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():

            post = form.save()

            return redirect(
                'post_detail',
                slug=post.slug
            )

    else:

        form = PostForm(
            instance=post
        )

    return render(
        request,
        'post_form.html',
        {
            'form': form,
            'post': post
        }
    )


# ============================================================
# POST DELETE
# ============================================================

@login_required
def post_delete(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    # -------------------------
    # PERMISSION
    # -------------------------

    if (
        request.user != post.author
        and not request.user.is_superuser
    ):
        raise PermissionDenied

    # -------------------------
    # DELETE
    # -------------------------

    if request.method == 'POST':

        post.delete()

        return redirect(
            'post_list'
        )

    return render(
        request,
        'post_confirm_delete.html',
        {
            'post': post
        }
    )


# ============================================================
# COMMENT
# ============================================================

@login_required
@require_POST
def add_comment(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    form = CommentForm(
        request.POST
    )

    if form.is_valid():

        comment = form.save(
            commit=False
        )

        comment.post = post
        comment.author = request.user

        comment.save()

    return redirect(
        'post_detail',
        slug=post.slug
    )


# ============================================================
# LIKE / UNLIKE
# ============================================================

@login_required
@require_POST
def toggle_like(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:

        like.delete()

        liked = False

    else:

        liked = True

    # -------------------------
    # AJAX
    # -------------------------

    if request.headers.get(
        'x-requested-with'
    ) == 'XMLHttpRequest':

        return JsonResponse(
            {
                'liked': liked,
                'likes_count': post.likes_count
            }
        )

    return redirect(
        'post_detail',
        slug=post.slug
    )


# ============================================================
# FAVORITES
# ============================================================

@login_required
def my_favorites(request):

    posts = Post.objects.filter(
        likes__user=request.user
    ).order_by(
        '-likes__created_at'
    )

    return render(
        request,
        'favorites.html',
        {
            'posts': posts
        }
    )


# ============================================================
# HISTORY
# ============================================================

@login_required
def my_history(request):

    history = request.user.view_history.select_related(
        'post'
    ).order_by(
        '-viewed_at'
    )

    return render(
        request,
        'history.html',
        {
            'history': history
        }
    )
