from rest_framework import serializers
from stockmgmt.models import StockHistory

class StockHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockHistory
        fields = '__all__'

        