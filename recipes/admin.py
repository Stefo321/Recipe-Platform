from django.contrib import admin
from .models import Category, Recipe, Review, UserProfile, Collection


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'is_published')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_at', 'is_public')
    list_filter = ('is_public', 'created_at')
