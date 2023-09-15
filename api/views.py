from django.http import JsonResponse
from rest_framework import viewsets
from products.models import Products, Category
from stockmgmt.models import StockHistory
from .serializer import ProductsSerializer, CategorySerializer, StockHistorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response



@api_view(['GET', 'POST'])
def products_list(request,format=None):

    if request.method == 'GET':
        stocks = Products.objects.all()
        serializer = ProductsSerializer(stocks, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id, format=None):

    try:
        stock = Products.objects.get(pk=id)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductsSerializer(stock)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductsSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def category_list(request,format=None):

    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    



@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, id, format=None):

    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
def products_history(request,format=None):

    if request.method == 'GET':
        stocks = StockHistory.objects.all()
        serializer = StockHistorySerializer(stocks, many=True)
        return Response(serializer.data)
    
