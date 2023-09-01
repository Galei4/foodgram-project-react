from django.contrib import admin
from recipies.admin import BaseAdmin
from users.models import Subscription, User


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_filter = (
        'username',
        'email',
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')


@admin.register(Subscription)
class SubscriptionAdmin(BaseAdmin):
    list_filter = ('user', 'author')
    search_fields = ('user', 'author')
