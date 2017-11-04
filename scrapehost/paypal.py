import paypalrestsdk
from scrapehost.config import config
import os


paypal_config = config['paypal']

api = paypalrestsdk.Api({
  'mode': paypal_config['mode'],
  'client_id': paypal_config['client_id'],
  'client_secret': paypal_config['client_secret']})

os.environ['PAYPAL_CLIENT_ID'] = paypal_config['client_id']
os.environ['PAYPAL_CLIENT_SECRET'] = paypal_config['client_secret']
