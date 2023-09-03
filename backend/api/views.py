from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipePostSerializer,
    ShoppingListSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserSerializer,
)
from api.utils import ingredients_download, post_delete
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipies.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    ShoppingList,
    Tag,
)
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Subscription, User


class CreateListDestroyGenericMixins(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class TagViewSet(CreateListDestroyGenericMixins):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(CreateListDestroyGenericMixins):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    filter_backends = (DjangoFilterBackend,)


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscriptions(self, request):
        return self.get_paginated_response(
            SubscriptionSerializer(
                self.paginate_queryset(
                    User.objects.filter(following__user=request.user),
                ),
                many=True,
                context={'request': request},
            ).data,
        )

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)

        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                author,
                data=request.data,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            Subscription.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        get_object_or_404(Subscription, user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeGetSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return RecipeGetSerializer
        return RecipePostSerializer

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        return post_delete(FavoriteSerializer, Favorite, request, pk)

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=[permissions.IsAuthenticated],
        url_path='shopping_cart',
    )
    def shopping_list(self, request, pk):
        return post_delete(ShoppingListSerializer, ShoppingList, request, pk)

    @action(
        detail=False,
        methods=('GET',),
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientAmount.objects.filter(
                recipe__shopping_list__user=self.request.user,
            )
            .values('ingredient__name', 'ingredient__measurement_unit')
            .order_by('ingredient__name')
            .annotate(quantity=Sum('amount'))
        )
        return ingredients_download(self, request, ingredients)
