import paypalrestsdk
from scrapehost.config import config


paypal_config = config['paypal']

api = paypalrestsdk.Api({
  'mode': paypal_config['mode'],
  'client_id': paypal_config['client_id'],
  'client_secret': paypal_config['client_secret']})
