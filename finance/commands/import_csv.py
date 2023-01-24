import csv

from django.core.management.base import BaseCommand
from django.utils import timezone

from finance.models import Transaction, Account, Tag, Category


class Command(BaseCommand):
    help = "Import csv file to database"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                date = row[0]
                description = row[1]
                place = row[2]
                amount = row[3]
                tags = row[4]
                category = row[5]

                # Create transaction
                transaction = Transaction.objects.create(
                    date=date,
                    description=description,
                    place=place,
                    amount=amount,
                    tags=tags,
                    category=category,
                )
                transaction.save()

                # Create account
                account = Account.objects.create(
                    name="My Account", balance=amount, transaction=transaction
                )
                account.save()

                # Create tags
                tag = Tag.objects.create(name=tags, transaction=transaction)
                tag.save()

                # Create category
                category = Category.objects.create(
                    name=category, transaction=transaction
                )
                category.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully imported transaction {transaction.description}"
                    )
                )
