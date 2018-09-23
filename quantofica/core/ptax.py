import csv

import requests

class CentralBankClient:
    BASE_URL = 'https://ptax.bcb.gov.br/ptax_internet/'
    US_DOLAR = 61
    EURO = 222

    def get(self, endpoint, params):
        url = '%s%s' % (self.BASE_URL, endpoint)
        response = requests.get(url, params)
        decoded_content = response.content.decode('utf-8')
        csv_file = csv.reader(decoded_content.splitlines(), delimiter=';')
        content = list(csv_file)
        return content

    def get_exchange_rate_in_period(self, currency_reference, start_date, end_date):
        params = {
            'method': 'gerarCSVFechamentoMoedaNoPeriodo',
            'ChkMoeda': currency_reference,
            'DATAINI': start_date,
            'DATAFIM': end_date
        }
        return self.get('consultaBoletim.do', params)
