from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, ArticleCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib import messages
from articles.models import Article
from django.http import HttpResponseForbidden

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile') 
        else:
            if 'password2' in form.errors:
                messages.error(request, 'Password confirmation does not match.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been successfully logged in.')
                return redirect('profile')  
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')  

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleCreationForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author=request.user
            article.save()
            return redirect('article_detail', article_id=article.pk) 
    else:
        form = ArticleCreationForm()
    return render(request, 'accounts/create_article.html', {'form': form})

@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user == article.author:
        if request.method == 'POST':
            form = ArticleCreationForm(request.POST, instance=article)
            if form.is_valid():
                edited_article = form.save()
                return redirect('article_detail', article_id=edited_article.id)
        else:
            form = ArticleCreationForm(instance=article)
        return render(request, 'accounts/create_article.html', {'form': form, 'article': article})
    else:
        return HttpResponseForbidden("You do not have permission to edit this article.")
    
@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user == article.author:
        article.delete()
        return redirect('profile')
    else:
        return HttpResponseForbidden("You do not have permission to delete this article.")

def profile(request):
    user = request.user
    articles = Article.objects.filter(author=user)
    return render(request, 'accounts/profile.html', {'user': user, 'articles': articles})
