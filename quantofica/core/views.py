from django.shortcuts import render

from quantofica.core.forms import NubankExchangeRateForm


def home(request):
    output = None
    if 'moeda' in request.GET and 'valor' in request.GET:
        form = NubankExchangeRateForm(request.GET)
        if form.is_valid():
            output = form.calculate()
    else:
        form = NubankExchangeRateForm()
    return render(request, 'index.html', {
        'form': form,
        'output': output
    })
