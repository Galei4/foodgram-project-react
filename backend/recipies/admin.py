from django.contrib import admin

from recipies.models import Favorite, Ingredient, Recipe, ShoppingList, Tag


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(BaseAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(BaseAdmin):
    list_display = (
        'id',
        'pub_date',
        'name',
        'author',
        'cooking_time',
        'in_favorite',
    )
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')

    @admin.display(description='В избранном')
    def in_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(ShoppingList)
class ShoplistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
