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

    billing_plan = BillingPlan({
        "name": "Scraping plan",
        "description": "Create Plan for Scraper",
        "merchant_preferences": {
            "auto_bill_amount": "yes",
            "cancel_url": "{}/order/cancel".format(config['host_full']),
            "initial_fail_amount_action": "continue",
            "max_fail_attempts": "1",
            "return_url": "{}/order/return/{}".format(config['host_full'], order_id),
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
            "name": "Scraper subscription",
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

        print('__AGREMENT__', billing_agreement)

        if billing_a_resp:
            db.collections.update_one({
                'structure': '#Order',
                '_id': order['_id']
            },
            {
                '$set': {
                    'billing_plan_id': billing_plan.id
                }
            })

            #if not order['object_id']:
            #    order['object']['billing_plan_id'] = billing_plan.id
            #    order['object']['billing_agreement_id'] = billing_agreement.id
            #
            #    res = db.collections.update_one(order['object'])

            print(billing_agreement)
            for link in billing_agreement.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return redirect(approval_url)

    return 'error'

@bp.route('/return/<order_id>', methods=['POST', 'GET'])
@login_required
def show_return(order_id):
    payment_token = request.args.get('token', '')
    billing_agreement_response = BillingAgreement.execute(payment_token)
    print('AGREEMENT', billing_agreement_response)
    
    if billing_agreement_response:
        agreement_id = billing_agreement_response.agreement_details.id

        order = db.collections.find_one({
            'structure': '#Order',
            '_id': ObjectId(order_id)
        })

        if not order:
            return 'No such order'
        
        #order['object']['billing_plan_id'] = billing_plan.id
        order['object']['billing_agreement_id'] = agreement_id

        res = db.collections.insert_one(order['object'])
        
        return redirect('/admin/scrapers/edit/{}'.format(res.inserted_id))

    return 'error'

@bp.route('/cancel/<order_id>', methods=['POST', 'GET'])
@login_required
def show_cancel(order_id):
    return redirect('/')
