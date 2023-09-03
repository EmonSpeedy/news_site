from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser
from django.contrib.auth.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return self.category_name


CHOICES = (
    (1, '1 star'),
    (2, '2 stars'),
    (3, '3 stars'),
    (4, '4 stars'),
)
class Article(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    headline = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=500, unique=True)
    body = models.TextField(max_length=400, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publishing_time = models.DateField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.headline)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.headline
    
class Ratings(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=CHOICES)

    class Meta:
        unique_together = ('user', 'article')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_average_rating(self):
        ratings = Ratings.objects.filter(article=self.article)
        if ratings.exists():
            total_ratings = sum(rating.rating for rating in ratings)
            return total_ratings / ratings.count()
        else:
            return 0  
    

