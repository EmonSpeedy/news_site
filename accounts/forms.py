from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from articles.models import Article

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'last_name', 'password1', 'password2', 'user_choice']
        
class ArticleCreationForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['headline', 'body', 'category']
