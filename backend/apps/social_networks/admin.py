from django.contrib import admin
from apps.social_networks.models import Account, Token

class TokenInLine(admin.TabularInline):
    model = Token
    extra = 0

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'username', )
    inlines = [TokenInLine]
