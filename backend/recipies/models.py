from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from rest_framework import status
from users.models import User

TAG_SLUG_MAX_LENGTH = 200


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=TAG_SLUG_MAX_LENGTH,
        verbose_name='Название',
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        null=True,
        blank=True,
        verbose_name='Цвет в HEX',
    )
    slug = models.SlugField(
        unique=True,
        max_length=TAG_SLUG_MAX_LENGTH,
        null=True,
        blank=True,
        verbose_name='Уникальный слаг',
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                code=status.HTTP_400_BAD_REQUEST,
            ),
        ],
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        default_related_name = 'tag'

    def __str__(self) -> str:
        return self.name[:30]


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингредиенты'
        default_related_name = 'ingredient'

    def __str__(self) -> str:
        return self.name[:30]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='username пользователя',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тегов',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Список ингредиентов',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    image = models.ImageField(
        upload_to='recipies/images/',
        verbose_name='Ссылка на картинку на сайте',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.SmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[MinValueValidator(1)],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipies'

    def __str__(self) -> str:
        return self.name[:30]


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.SmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Жанры и произведения'
        default_related_name = 'ingredient_amount'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_amount',
            ),
        ]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            ),
        ]

    def __str__(self):
        return f'{self.user.username} добавил в избранное {self.recipe.name}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shopping_list'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list',
            ),
        ]

    def __str__(self):
        return f'{self.user.username} добавил в корзину' f'{self.recipe.name}'
