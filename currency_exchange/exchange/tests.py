from django.test import TestCase, Client
from django.urls import reverse
from .models import Currency, ExchangeRate
from django.utils import timezone


class CurrencyViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.currency1 = Currency.objects.create(code='PLN')
        self.currency2 = Currency.objects.create(code='USD')

    def test_currency_list(self):
        response = self.client.get(reverse('currency'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn({'code': 'PLN'}, response.data)
        self.assertIn({'code': 'USD'}, response.data)


class ExchangeRateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.currency1 = Currency.objects.create(code='USD')
        self.currency2 = Currency.objects.create(code='PLN')
        self.rate = 69.420
        self.exchange_rate = ExchangeRate.objects.create(
            from_currency=self.currency1,
            to_currency=self.currency2,
            rate=self.rate,
            date=timezone.now()
        )

    def test_exchange_rate(self):
        response = self.client.get(reverse('rate', args=['USD', 'PLN']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['currency_pair'], 'USDPLN')
        self.assertEqual(float(response.data['exchange_rate']), self.rate)

    def test_exchange_rate_not_found(self):
        response = self.client.get(reverse('rate', args=['USD', 'JPY']))
        self.assertEqual(response.status_code, 404)
