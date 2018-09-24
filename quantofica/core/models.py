# coding: utf-8

from django.db import models


class Currency(models.Model):
    code = models.CharField('código', max_length=3, primary_key=True)
    name = models.CharField('nome', max_length=100)
    symbol = models.CharField('símbolo', max_length=5)
    central_bank_reference = models.IntegerField()

    __current_rate = None

    class Meta:
        verbose_name = 'moeda'
        verbose_name_plural = 'moedas'

    def __str__(self):
        return self.symbol

    @property
    def current_rate(self):
        if self.__current_rate is None:
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
        return '%s - %s' % (self.currency.code, self.value)
