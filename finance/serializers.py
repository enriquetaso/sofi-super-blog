# Serializers allow complex data such as querysets and model
# instances to be converted to native Python datatypes that
# can then be easily rendered into JSON, XML or other content
# types.
#
# Serializers also provide deserialization, allowing parsed
# data to be converted back into complex types, after first
# validating the incoming data.
#
# https://www.django-rest-framework.org/api-guide/serializers/
from rest_framework import serializers

from finance.models import Account
from finance.models import Category
from finance.models import Tag
from finance.models import Transaction


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True, required=False)

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

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        category = Category.objects.get_or_create(**category_data)[0]

        tags_data = validated_data.pop("tags")

        transaction = Transaction.objects.create(category=category, **validated_data)

        for tag in tags_data:
            t = Tag.objects.get_or_create(**tag)[0]
            transaction.tags.add(t.pk)

        return transaction

    def update(self, instance, validated_data):
        category_data = validated_data.pop("category")
        category = Category.objects.get_or_create(**category_data)[0]

        tags_data = validated_data.pop("tags")
        for tag in tags_data:
            t = Tag.objects.get_or_create(**tag)[0]
            instance.tags.add(t.pk)

        instance.category = category
        instance.account = validated_data.get("account", instance.account)
        instance.date = validated_data.get("date", instance.date)
        instance.description = validated_data.get("description", instance.description)
        instance.place = validated_data.get("place", instance.place)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.save()
        return instance


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ("id", "name", "balance", "owner", "transactions")
