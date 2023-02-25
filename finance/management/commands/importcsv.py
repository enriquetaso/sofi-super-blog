import csv

from django.core.management.base import BaseCommand, CommandError
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
                place = row[1]
                description = row[2]
                category = row[3]
                card = row[4]
                amount = row[5]
                tags = row[6]

                # “01/02/2023” value has an invalid date format. It must be in YYYY-MM-DD format.
                date_formatted = timezone.datetime.strptime(date, "%d/%m/%Y").date()

                # Get or create category
                # Returns a tuple of (object, created)
                categorie_info = Category.objects.get_or_create(name=category)
                category_obj = categorie_info[0]
                if categorie_info[1]:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully created category {category_obj.name}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Category {category_obj.name} already exists"
                        )
                    )

                # Get or create tags
                tag_info = Tag.objects.get_or_create(name=tags)
                tag = tag_info[0]
                if tag_info[1]:
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully created tag {tag.name}")
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f"Tag {tag.name} already exists")
                    )
                try:
                    if card == "cash":
                        card = "Cash"
                    account = Account.objects.get(name=card)
                except Account.DoesNotExist:
                    self.stderr.write(
                        self.style.ERROR(f"Account {card} does not exist")
                    )
                    # raise CommandError(f"Account {card} does not exist")
                    continue

                if description == "":
                    description = place

                # Get or create transaction
                transaction_info = Transaction.objects.get_or_create(
                    date=date_formatted,
                    account=account,
                    description=description,
                    place=place,
                    amount=float(amount),
                    category=category_obj,
                )
                transaction = transaction_info[0]
                if transaction_info[1]:
                    transaction.tags.add(tag)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully created transaction {transaction.description}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Transaction {transaction.description} already exists"
                        )
                    )
