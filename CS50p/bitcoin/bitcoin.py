import requests
import sys


if len(sys.argv) != 2:
    sys.exit("Missing command-line argument")
else:
    try:
        n =  float(sys.argv[1])
    except:
        sys.exit("Command-line argument is not a number")

try:
    response = (requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')).json()
    bitcoin_value = response.get('bpi').get('USD').get('rate_float')
    print(f"${n * bitcoin_value:,}")
except requests.RequestException:
    pass
