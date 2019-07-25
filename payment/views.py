

import time
import qrcode
from flask import Flask, current_app, redirect, url_for ,render_template, session
from .alipay import AliPay


payment_app = Flask('payment')



@payment_app.route('/')
def index():
    return render_template('payment.html')

@payment_app.route('/alipay/<method>',method=['POST'])
def alipay_request(method):
    var = request.form.get('order')
    a = init_alipay_cfg()
    if method == 'alipay.trade.page.pay':
        res = 

    data = a.api(
        'alipay.trade.page.pay',
        subject=subject,
        out_trade_no=out_trade_no,
        total_amount=total_amount,
        return_url=None,
        notify_url=None)
    url = a.gateway + "?" + data
    return res

