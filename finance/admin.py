from django.contrib import admin
from .models import Tag, Account, Transaction, Category

admin.site.register(Tag)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Category)
