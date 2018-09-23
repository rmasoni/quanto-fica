# Quanto Fica

Saiba com precisão quanto vai pagar em Reais por compras internacionais feitas com seu Nubank!


## Instalação

É recomendado instalar o project dentro de um virtualenv.

```text
pip install -r requirements.txt
```

## Setup Inicial

Crie um banco de dados local:

```text
python manage.py migrate
```

Carregue os dados inicias das moedas para atualização diária das taxas de câmbio:

```text
python manage.py loaddata core/fixtures/currencies.json
```

Atualize o banco de dados com as taxas de câmbio atualizadas a partir dos dados disponibilizados pelo Banco Central:

```text
python manage.py update_rates
```

PS: Para atualiação diaria basta criar um cron job executando o comando `update_rates`.
