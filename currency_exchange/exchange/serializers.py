from rest_framework import serializers
from .models import Currency, ExchangeRate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code']


class ExchangeRateSerializer(serializers.ModelSerializer):
    currency_pair = serializers.SerializerMethodField()
    exchange_rate = serializers.DecimalField(source='rate', max_digits=25, decimal_places=17)

    class Meta:
        model = ExchangeRate
        fields = ['currency_pair', 'exchange_rate']

    @staticmethod
    def get_currency_pair(obj):
        return f"{obj.from_currency.code}{obj.to_currency.code}"


class ExchangeRateListSerializer(serializers.ModelSerializer):
    currency_pair = serializers.SerializerMethodField()
    exchange_rate = serializers.DecimalField(source='rate', max_digits=25, decimal_places=17)
    timestamp = serializers.DateTimeField()

    class Meta:
        model = ExchangeRate
        fields = ['currency_pair', 'exchange_rate', 'timestamp']

    @staticmethod
    def get_currency_pair(obj):
        return f"{obj.base_currency.code}{obj.target_currency.code}"
