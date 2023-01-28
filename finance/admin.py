from django.contrib import admin
from finance.models import Tag, Account, Transaction, Category

admin.site.register(Tag)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Category)
