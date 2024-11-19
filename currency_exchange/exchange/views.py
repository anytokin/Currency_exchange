from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from .models import Currency, ExchangeRate
from .serializers import CurrencySerializer, ExchangeRateSerializer, ExchangeRateListSerializer
from django.shortcuts import get_object_or_404


class CurrencyListView(APIView):
    @staticmethod
    def get(request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)


class ExchangeRateView(APIView):
    @staticmethod
    def get(request, from_code, to_code):
        from_currency = get_object_or_404(Currency, code=from_code)
        to_currency = get_object_or_404(Currency, code=to_code)
        exchange_rate = ExchangeRate.objects.filter(
            from_currency=from_currency,
            to_currency=to_currency
        ).order_by('-date').first()
        if exchange_rate:
            serializer = ExchangeRateSerializer(exchange_rate)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Exchange rate not found'}, status=status.HTTP_404_NOT_FOUND)


class ExchangeRateList(generics.ListAPIView):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rate', 'date']
    ordering = ['-date']
