#  provide a way of serializing and deserializing the Transacction
# instances into representations such as json.
#  This is used by the API views.

from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'account', 'date', 'description', 'place', 'amount', 'tags', 'category')
        