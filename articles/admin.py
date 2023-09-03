from django.contrib import admin
from . models import Category, Article, Ratings

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'category_slug' : ('category_name',)}
    list_display = ('category_name', 'category_slug')
    
admin.site.register(Category, CategoryAdmin)

class ArticleModel(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('headline',)}
    list_display=('headline', 'category', 'publishing_time')
    
admin.site.register(Article, ArticleModel)

class RatingModel(admin.ModelAdmin):
    list_display=('user', 'article', 'rating')
    
admin.site.register(Ratings, RatingModel)


