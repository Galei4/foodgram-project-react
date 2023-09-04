from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status

from users.models import Subscription, User
from recipies.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                             ShoppingList, Tag)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__',)


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = (
            'is_subscribed',
            'id',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request').user

        return (
            request.is_authenticated
            and Subscription.objects.filter(user=request, author=obj).exists()
        )


class IngredientAmountPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class IngredientAmountGetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientAmount
        fields = '__all__'


class RecipeGetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientAmountGetSerializer(
        many=True,
        required=True,
        source='ingredient_amount',
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and Favorite.objects.filter(
                user=request.user,
                recipe=obj.id,
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and ShoppingList.objects.filter(
                user=request.user,
                recipe=obj.id,
            ).exists()
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('recipe', 'user')

    def validate(self, data):
        if data['user'].favorites.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError('Рецепт уже в избранном')
        return data

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')},
        ).data


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('recipe', 'user')
        model = ShoppingList

    def validate(self, data):
        if data['user'].shopping_list.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError('Рецепт уже корзине')
        return data

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')},
        ).data


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count',
        )
        read_only_fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
        )

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscription.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                detail='Вы уже подписаны на данного пользователя',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise serializers.ValidationError(
                detail='Нельзя подписаться на самого себя',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipies.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = ShortRecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipies.count()


class RecipePostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountPostSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
        )

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError('Не выбраны тэги')
        for tag in tags:
            if not Tag.objects.filter(id=tag.id).exists():
                raise serializers.ValidationError(
                    'Указанного тэга не существует',
                )
        return tags

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError('Не выбраны ингредиенты')

        ingredients_list = []
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError(
                    'Вы уже использовали данный ингредиент',
                )
            ingredients_list.append(ingredient['id'])

            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError(
                    'Укажите верное количество ингредиента',
                )
        return ingredients

    def validate_cooking_time(self, cooking_time):
        if cooking_time <= 1:
            raise serializers.ValidationError(
                'Слишком маленькое время приготовления',
            )
        return cooking_time

    def to_representation(self, instance):
        return RecipeGetSerializer(
            instance,
            context={'request': self.context.get('request')},
        ).data

    @staticmethod
    def create_ingredients(recipe, ingredients):
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_list.append(
                IngredientAmount(
                    ingredient_id=ingredient['id'],
                    amount=ingredient['amount'],
                    recipe=recipe,
                ),
            )
        IngredientAmount.objects.bulk_create(ingredient_list)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        instance.tags.clear()
        instance.tags.set(tags)
        self.create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)
