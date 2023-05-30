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


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=200)
    simbol = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, blank=True, null=True
    )
    tags = models.ManyToManyField(to=Tag, related_name="accounts", blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.date} - {self.place} - {self.description}"

    # Meta class to order the queryset
    class Meta:
        ordering = ["-date"]


class FinancialGoals(models.Model):
    name = models.CharField(max_length=200)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    def _is_goal_achieved(self):
        return self.current_amount >= self.goal_amount

    # Meta class to order the queryset
    class Meta:
        ordering = ["-start_date"]

class Income(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    description = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.date} - {self.description}"

    # Meta class to order the queryset
    class Meta:
        ordering = ["-date"]

    # on save, update the account balance
    def save(self, *args, **kwargs):
        """Update the account balance"""
        self.account.balance += self.amount
        self.account.save()
        super(Income, self).save(*args, **kwargs)

    # on delete, update the account balance
    def delete(self, *args, **kwargs):
        """Update the account balance"""
        self.account.balance -= self.amount
        self.account.save()
        super(Income, self).delete(*args, **kwargs)

    # on update, update the account balance
    def update(self, *args, **kwargs):
        """Update the account balance"""
        self.account.balance -= self.amount
        self.account.save()
        super(Income, self).update(*args, **kwargs)