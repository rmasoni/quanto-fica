# coding: utf-8

from django.db import models
from django.utils import timezone

from quantofica.core.utils import previous_weekday


class Currency(models.Model):
    code = models.CharField('código', max_length=3, primary_key=True)
    name = models.CharField('nome', max_length=100)
    symbol = models.CharField('símbolo', max_length=5)
    central_bank_reference = models.IntegerField()
    updated_at = models.DateTimeField(default=timezone.now)

    __current_rate = None

    class Meta:
        verbose_name = 'moeda'
        verbose_name_plural = 'moedas'

    def __str__(self):
        return self.symbol

    @property
    def current_rate(self):
        if self.__current_rate is None:
            date = previous_weekday(timezone.now())
            try:
                self.__current_rate = self.rates.get(date=date)
            except Rate.DoesNotExist:
                self.__current_rate = self.rates.order_by('-date').first()
        return self.__current_rate


class Rate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='moeda', related_name='rates')
    date = models.DateField('data')
    value = models.DecimalField('valor', max_digits=10, decimal_places=5)

    class Meta:
        verbose_name = 'taxa de câmbio'
        verbose_name_plural = 'taxas de câmbio'

    def __str__(self):
        return '%s - %s - %s' % (self.currency.code, self.value, self.date)
