from django import template

register = template.Library()


@register.filter
def is_liked_by(post, user):
    """Shablonda {{ post|is_liked_by:request.user }} shaklida ishlatiladi."""
    return post.is_liked_by(user)
