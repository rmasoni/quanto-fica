import decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from quantofica.core.models import Currency, Rate
from quantofica.core.ptax import CentralBankClient


DATE_INDEX = 0
SELL_RATE_INDEX = 5

class Command(BaseCommand):
    help = 'Update exchange rates'

    def handle(self, *args, **kwargs):
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(weeks=1)
        end_date = end_date.strftime('%d/%m/%Y')
        start_date = start_date.strftime('%d/%m/%Y')
        client = CentralBankClient()
        currencies = Currency.objects.all()
        for currency in currencies:
            rates = client.get_exchange_rate_in_period(currency.central_bank_reference, start_date, end_date)
            current_rate = rates[-1]
            str_date = current_rate[DATE_INDEX]
            rate_date = timezone.datetime.strptime(str_date, '%d%m%Y').date()
            str_sell_rate = current_rate[SELL_RATE_INDEX]
            sell_rate = decimal.Decimal(str_sell_rate.replace(',', '.'))
            Rate.objects.update_or_create(currency=currency, date=rate_date, defaults={
                'value': sell_rate
            })
            self.stdout.write(self.style.SUCCESS('Updated rate: {currency} - {date} - {value}'.format(
                currency=currency.code, date=rate_date, value=sell_rate
            )))
