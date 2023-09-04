from django.shortcuts import HttpResponse, get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from recipies.models import Recipe


def post_delete(add_serializer, model, request, recipe_id):
    user = request.user
    data = {'user': user.id, 'recipe': recipe_id}
    serializer = add_serializer(data=data, context={'request': request})
    if request.method == 'POST':
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    get_object_or_404(
        model,
        user=user,
        recipe=get_object_or_404(Recipe, id=recipe_id),
    ).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def ingredients_download(self, request, ingredients):
    filename = 'shopping_list.txt'
    shopping_list = (
        f'Список покупок для пользователя: {self.request.user.username}\n\n'
    )
    shopping_list += '\n'.join(
        [
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["quantity"]}'
            for ingredient in ingredients
        ],
    )
    shopping_list += f'\n\nFoodgram ({timezone.localdate():%Y})'

    response = HttpResponse(
        shopping_list,
        content_type='text.txt; charset=utf-8',
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
