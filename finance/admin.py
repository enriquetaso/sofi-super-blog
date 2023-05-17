from django.contrib import admin

from finance.models import Account
from finance.models import Category
from finance.models import Tag
from finance.models import Transaction

admin.site.register(Tag)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Category)
