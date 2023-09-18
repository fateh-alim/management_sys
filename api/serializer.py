from rest_framework import serializers
from products.models import Products, Category
from stockmgmt.models import StockHistory


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class StockHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockHistory
        fields = '__all__'