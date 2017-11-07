import paypalrestsdk
from scrapehost.config import config
import os
import datetime


paypal_config = config['paypal']

api = paypalrestsdk.Api({
  'mode': paypal_config['mode'],
  'client_id': paypal_config['client_id'],
  'client_secret': paypal_config['client_secret']})

os.environ['PAYPAL_CLIENT_ID'] = paypal_config['client_id']
os.environ['PAYPAL_CLIENT_SECRET'] = paypal_config['client_secret']


def is_billing_due(agreement_id):
    billing_agreement = paypalrestsdk.BillingAgreement.find(agreement_id)
    
    if billing_agreement is None:
        return False

    if billing_agreement.agreement_details is None:
        return False
    
    now = datetime.datetime.now()
    next_date = billing_agreement.agreement_details.next_billing_date

    return next_date <= now
