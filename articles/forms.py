
from django import forms
from .models import Article, CHOICES

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['headline', 'body', 'category']
        
class RatingForm(forms.Form):
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
