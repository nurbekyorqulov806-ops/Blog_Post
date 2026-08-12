from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # POSTLAR
    # =========================

    path(
        '',
        views.post_list,
        name='post_list'
    ),

    path(
        'category/<slug:slug>/',
        views.category_detail,
        name='category_detail'
    ),

    path(
        'post/create/',
        views.post_create,
        name='post_create'
    ),

    path(
        'post/<slug:slug>/',
        views.post_detail,
        name='post_detail'
    ),

    path(
        'post/<slug:slug>/edit/',
        views.post_update,
        name='post_update'
    ),

    path(
        'post/<slug:slug>/delete/',
        views.post_delete,
        name='post_delete'
    ),

    path(
        'post/<slug:slug>/comment/',
        views.add_comment,
        name='add_comment'
    ),

    path(
        'post/<slug:slug>/like/',
        views.toggle_like,
        name='toggle_like'
    ),

    # =========================
    # FOYDALANUVCHI
    # =========================

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.custom_login_view,
        name='login'
    ),

    path(
        'logout/',
        views.custom_logout_view,
        name='logout'
    ),

    path(
        'profile/edit/',
        views.profile_edit,
        name='profile_edit'
    ),

    path(
        'favorites/',
        views.my_favorites,
        name='favorites'
    ),

    path(
        'history/',
        views.my_history,
        name='history'
    ),

    path(
        'profile/<str:username>/',
        views.profile_detail,
        name='profile'
    ),
]





