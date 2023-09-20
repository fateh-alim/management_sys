from rest_framework.views import APIView
from rest_framework.response import Response
from stockmgmt.models import StockHistory
from .serializer import  StockHistorySerializer


class ProductsHistory(APIView):
    def get(self, request, format=None):
        stocks = StockHistory.objects.all()
        serializer = StockHistorySerializer(stocks, many=True)
        return Response(serializer.data)

