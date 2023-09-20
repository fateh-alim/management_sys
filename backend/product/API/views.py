from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Category
from .serializer import ProductsSerializer, CategorySerializer


class ProductsList(APIView):
    def get(self, request, format=None):
        stocks = Product.objects.all()
        serializer = ProductsSerializer(stocks, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetail(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, id, format=None):
        stock = self.get_object(id)
        serializer = ProductsSerializer(stock)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        stock = self.get_object(id)
        serializer = ProductsSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        stock = self.get_object(id)
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class CategoryList(APIView):
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    def get_object(self, id):
        try:
            return Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, id, format=None):
        category = self.get_object(id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        category = self.get_object(id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        category = self.get_object(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddItems(APIView):
    def post(self, request, format=None):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)