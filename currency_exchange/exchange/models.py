from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.code


class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, related_name='rates_from', on_delete=models.CASCADE)
    to_currency = models.ForeignKey(Currency, related_name='rates_to', on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=25, decimal_places=17)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_currency.code}/{self.to_currency.code} rate:{self.rate} date:{self.date}"
