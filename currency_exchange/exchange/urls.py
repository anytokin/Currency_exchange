from django.urls import path
from .views import CurrencyListView, ExchangeRateView

urlpatterns = [
    path('currency/', CurrencyListView.as_view(), name='currency'),
    path('currency/<str:from_code>/<str:to_code>/', ExchangeRateView.as_view(), name='rate'),
]