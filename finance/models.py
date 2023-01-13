from django.db import models
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name    

class Account(models.Model):
    name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    def __str__(self):
        return self.name

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.ManyToManyField(to=Tag, related_name='accounts', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.description

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name



