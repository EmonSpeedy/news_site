from django.shortcuts import render, get_object_or_404, redirect
from . models import Article, Category, Ratings, CHOICES
from django.db.models import F, Window, Avg
from django.db.models.functions import RowNumber
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, RatingForm
from accounts.models import CustomUser
from django.urls import reverse


@login_required
def rate_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # Check if the user has already rated this article
    existing_rating = Ratings.objects.filter(user=request.user, article=article).first()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']

            if existing_rating:
                existing_rating.rating = rating
                existing_rating.save()
            else:
                Ratings.objects.create(user=request.user, article=article, rating=rating)


            return redirect('article_detail', article_id=article.id)
    else:
        form = RatingForm()
    return render(request, 'articles/rate_article.html', {'article': article, 'form': form, 'user_rating': existing_rating})


def home(request):
    articles = Article.objects.all()
    category = Category.objects.all()
    top_rated_articles = (
    Article.objects
    .annotate(
        ranking=Window(
            expression=RowNumber(),
            partition_by=F('category'),
            order_by=F('ratings').desc()
        )
    ).filter(ranking__lte=2).order_by('category', 'ranking')
    )
    context = {'articles' : top_rated_articles, 'category' : category}
    return render(request, 'articles/home.html', context)



def articles_by_category(request, category_slug):
    category = get_object_or_404(Category, category_slug=category_slug)
    articles = Article.objects.filter(category=category).order_by('-ratings')
    
    context = {
        'category': category,
        'articles': articles,
    }
    return render(request, 'articles/category.html', context)

def article_detail(request, article_id):
    
    article = get_object_or_404(Article, pk=article_id)
    category = article.category
    
    average_rating = Ratings.objects.filter(article=article).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    related_articles = Article.objects.filter(category=category).exclude(pk=article_id)[:2]
    context = {'article' : article,'related_articles' : related_articles, 'average_rating':average_rating}
    
    return render(request, 'articles/article_detail.html', context)
