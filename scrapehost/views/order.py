from flask import Blueprint, render_template, request, jsonify, redirect
from scrapehost.config import config
from scrapehost.utils import login_required
from scrapehost.mongo import db
from scrapehost.models import Order
from scrapehost.paypal import api
import paypalrestsdk
from paypalrestsdk import BillingPlan, BillingAgreement, Payment
from paypalrestsdk.exceptions import ServerError
from bson.objectid import ObjectId
from datetime import datetime, timedelta


bp = Blueprint(__name__, __name__, template_folder='templates', url_prefix='/order')

@bp.route('/', methods=['POST', 'GET'])
@login_required
def show_order_scraper():
    if not request.args.get('order_id'):
        return jsonify({'error': 'no order_id'})
    
    order_id = request.args.get('order_id')
    
    order = db.collections.find_one({
        'structure': '#Order',
        '_id': ObjectId(order_id)
    })

    scraper_price = order['price']
    order_type = order['object']['structure']


    '''payment = Payment({
        "intent": "order",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "{}/order/return".format(config['host_full']),
            "cancel_url": "{}/order/cancel".format(config['host_full'])
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": order_type,
                    "sku": order_type,
                    "price": str(scraper_price),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "currency": "USD",
                "total": str(scraper_price)
            },
            "description": "Scraper for scraping web information."
        }]
    }, api=api)'''

    billing_plan = BillingPlan({
        "name": "Fast Speed Plan",
        "description": "Create Plan for Regular",
        "merchant_preferences": {
            "auto_bill_amount": "yes",
            "cancel_url": "{}/order/cancel".format(config['host_full']),
            "initial_fail_amount_action": "continue",
            "max_fail_attempts": "1",
            "return_url": "{}/order/return".format(config['host_full']),
            "setup_fee": {
                "currency": "USD",
                "value": str(scraper_price)
            }
        },
        "payment_definitions": [
            {
                "amount": {
                    "currency": "USD",
                    "value": str(scraper_price)
                },
                "charge_models": [
                    {
                        "amount": {
                            "currency": "USD",
                            "value": str(scraper_price)
                        },
                        "type": "SHIPPING"
                    },
                    {
                        "amount": {
                            "currency": "USD",
                            "value": str(scraper_price)
                        },
                        "type": "TAX"
                    }
                ],
                "cycles": "0",
                "frequency": "MONTH",
                "frequency_interval": "1",
                "name": "Regular 1",
                "type": "REGULAR"
            }
        ],
        "type": "INFINITE"
    })

    billing_resp = billing_plan.create()
    print(billing_resp, billing_plan, billing_plan.error)

    if billing_resp:
        billing_plan.activate()
        billing_agreement = BillingAgreement({
            "name": "Organization plan name",
            "description": "Scraper subscription",
            "start_date": (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            "plan": {
                "id": billing_plan.id
            },
            "payer": {
                "payment_method": "paypal"
            }
        })

        billing_a_resp = billing_agreement.create()
        
        print(billing_a_resp, billing_agreement.error, billing_agreement)

        if billing_a_resp:
            db.collections.update_one({
                'structure': '#Order',
                '_id': order['_id']
            },
            {
                '$set': {
                    'billing_plan_id': billing_plan.id,
                    'billing_agreement_id': billing_agreement.id
                }
            })

            if not order['object_id']:
                res = db.collections.insert_one(order['object'])

            print(billing_agreement)
            for link in billing_agreement.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return redirect(approval_url)

    '''try:
        if payment.create():
            db.collections.update_one({
                'structure': '#Order',
                '_id': order['_id']
            },
            {
                '$set': {
                    'payment_id': payment['id']    
                }
            })
            
            if not order['object_id']:
                res = db.collections.insert_one(order['object'])

                db.collections.update_one({
                    'structure': '#Order',
                    '_id': order['_id']
                },
                {
                    '$set': {
                        'object_id': res.inserted_id    
                    }
                })
            else:
                db.collections.update_one({
                    'structure': order['object']['structure'],
                    '_id': order['object_id']
                },
                {
                    '$set': {
                        'plan': int(order['object']['plan'])
                    }
                })

            for link in payment.links:
                if link.method == "REDIRECT":
                    redirect_url = str(link.href)
                    return redirect(redirect_url)
    except ServerError as e:
        return 'Paypal has some problems right now, try again later' 
    else:
        return 'ERROR'
    '''


@bp.route('/return', methods=['POST', 'GET'])
@login_required
def show_return():
    '''payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    
    try:
        payment = paypalrestsdk.BillingPlan.find(
            payment_id,
            api=api
        )

        if payment.execute({'payer_id': payer_id}):
            order = db.collections.find_one({
                'structure': '#Order',
                'payment_id': payment_id
            })

            if 'object_id' not in order:
                return 'order has no object id'

            return redirect('/admin/scrapers/edit/{}'.format(order['object_id']))

        else:
            return str(payment.error)

    except ServerError as e:
        return 'Paypal has some problems right now, try again later'
    '''
    payment_token = request.args.get('token', '')
    billing_agreement_response = BillingAgreement.execute(payment_token)
    print('AGREEMENT', billing_agreement_response)
    if billing_agreement_response:
        return redirect('/admin/scrapers')
    return billing_agreement_response.id

@bp.route('/cancel', methods=['POST', 'GET'])
@login_required
def show_cancel():
    return redirect('/')
