# Blog Platform

Django 5.x + Tailwind CSS (CDN). Loyihada **bitta ilova** (`blog`) bor — ichida
CustomUser, Category, Post, Comment, Like, PostViewHistory modellari, barcha
view'lar, formalar va URL'lar shu bitta ilovada joylashgan.

## Papka tuzilishi

```
blog_platform/
├── manage.py, requirements.txt, .env.example, .gitignore
├── config/                 → loyiha sozlamalari (settings, urls, wsgi/asgi)
├── blog/                   → YAGONA ilova
│   ├── models.py           → CustomUser, Category, Post, Comment, Like, PostViewHistory
│   ├── forms.py            → RegisterForm, ProfileEditForm, PostForm, CommentForm
│   ├── views.py            → auth, CRUD, like, sevimlilar, tarix, qidiruv
│   ├── urls.py
│   ├── admin.py
│   └── templatetags/blog_extras.py
├── templates/               → BARCHA html fayllar shu yerda (subpapkasiz), Tailwind CDN
│   ├── base.html
│   ├── like_button.html
│   ├── pagination.html
│   ├── post_list.html, post_detail.html, post_form.html, post_confirm_delete.html
│   ├── category_detail.html
│   ├── register.html, login.html
│   ├── profile_detail.html, profile_edit.html
│   ├── favorites.html, history.html
└── media/                   → yuklangan rasmlar (avatar, post, kategoriya)
```

## O'rnatish

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Funksiyalar

- **Like** — `Like` modeli, post ustida ♡ bosilsa AJAX orqali (`toggle_like` view) sahifa qayta yuklanmasdan yoqtiriladi/bekor qilinadi.
- **Sevimli postlar** (`/favorites/`) — foydalanuvchi like bosgan postlar shu yerda chiqadi (alohida model shart emas).
- **Tarix** (`/history/`) — `PostViewHistory` modeli: post ochilganda (bosilganda) avtomatik yozuv qo'shiladi, vaqt bo'yicha tartiblanadi.





