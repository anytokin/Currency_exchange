from django.core.management.base import BaseCommand
from exchange.models import Currency, ExchangeRate
import yfinance as yf
from common.utils.currency import supported_currencies_pairs
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        for from_code, to_code in supported_currencies_pairs:
            from_currency, _ = Currency.objects.get_or_create(code=from_code)
            to_currency, _ = Currency.objects.get_or_create(code=to_code)

            try:
                exchange_symbol = f"{from_code}{to_code}=X"
                ticker = yf.Ticker(exchange_symbol)
                ticker_history = ticker.history(period="1d")

                if not ticker_history.empty:
                    rate = ticker_history['Close'].iloc[-1]
                    ExchangeRate.objects.create(
                        from_currency=from_currency,
                        to_currency=to_currency,
                        rate=rate,
                        date=timezone.now()
                    )
                    self.stdout.write(self.style.SUCCESS(f"Loaded rate for {from_code}/{to_code}: {rate}"))
                else:
                    self.stdout.write(self.style.WARNING(f"No data found for {from_code}/{to_code}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error loading {from_code}/{to_code}: {e}"))
