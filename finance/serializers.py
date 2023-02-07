#  provide a way of serializing and deserializing the Transacction
# instances into representations such as json.
#  This is used by the API views.

from rest_framework import serializers
from finance.models import Transaction, Account, Tag, Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "account",
            "date",
            "description",
            "place",
            "amount",
            "tags",
            "category",
        )


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ("id", "name", "balance", "owner", "transactions")
