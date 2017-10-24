from flask import Blueprint, render_template, request, jsonify, redirect
from scrapehost.config import config
from scrapehost.utils import login_required
from scrapehost.mongo import db
from scrapehost.models import Order
from scrapehost.paypal import api
import paypalrestsdk
from paypalrestsdk import Payment
from paypalrestsdk.exceptions import ServerError
from bson.objectid import ObjectId


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
    order_type = order['structure']


    payment = Payment({
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
    }, api=api)


    try:
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

            for link in payment.links:
                if link.method == "REDIRECT":
                    redirect_url = str(link.href)
                    return redirect(redirect_url)
    except ServerError as e:
        return 'Paypal has some problems right now, try again later' 
    else:
        return 'ERROR'


@bp.route('/return', methods=['POST', 'GET'])
@login_required
def show_return():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    
    try:
        payment = paypalrestsdk.Payment.find(
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

@bp.route('/cancel', methods=['POST', 'GET'])
@login_required
def show_cancel():
    return redirect('/')
