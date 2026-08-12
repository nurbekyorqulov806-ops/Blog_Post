from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post, Comment


class StyledClearableFileInput(forms.ClearableFileInput):
    """Avatar uchun Tailwind bilan bezalgan fayl tanlash widgeti."""
    template_name = 'clearable_file_input.html'


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'avatar', 'bio', 'website', 'social_links']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'avatar': StyledClearableFileInput(),
        }

    def clean_social_links(self):
        value = self.cleaned_data.get('social_links')

        if value is None:
            return {}

        return value


    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'image', 'desc', 'body']
        widgets = {
            'desc': forms.Textarea(attrs={'rows': 3}),
            'body': forms.Textarea(attrs={'rows': 12}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Izoh yozing...'})}






