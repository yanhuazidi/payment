

import time
import qrcode
import json
from flask import Flask, current_app, redirect, url_for ,render_template, session,request
from .alipay_fun import init_alipay


payment_app = Flask('payment')


@payment_app.route('/')
def index():
    return render_template('payment.html',out_trade_no=int(time.time()))

def alipay_cancel_order(out_trade_no:int, cancel_time=None):
    result = init_alipay().api_alipay_trade_cancel(out_trade_no=out_trade_no)
    resp_state = result.get('msg')
    action = result.get('action')
    if resp_state=='Success':
        if action=='close':
            if cancel_time:
                print("%s秒内未支付订单，订单已被取消！" % cancel_time)
        elif action=='refund':
            print('该笔交易目前状态为：',action)
 
        return action
 
    else:
        print('请求失败：',resp_state)
        return


@payment_app.route('/alipay/refund')
def alipay_order_refund():
    '''
    退款
    :param out_trade_no: 商户订单号
    :return: None
    '''
    order = dict(request.args)
    result = init_alipay().api_alipay_trade_query(out_trade_no=order['out_trade_no'])
    if result.get("trade_status", "") == "TRADE_SUCCESS":
        result = init_alipay().api_alipay_trade_refund(refund_amount=order['total_amount'],out_trade_no=order['out_trade_no'])
        print(result)

        return json.dumps({'code':1,'msg':f"成功退款 {result.get('refund_fee')} 元"})
    else:
        return json.dumps({'code':0,'msg':result.get('sub_msg')})
            

@payment_app.route('/alipay/page_pay/return')
def allipay_page_pay_return():
    '''页面支付同步返回'''
    order = dict(request.args)
    sign = order.pop('sign')
    if init_alipay().verify(order,sign):
        return render_template('order_info.html',order=order)
    else:
        return render_template('order_info.html',msg='验证不通过')
    

@payment_app.route('/notify')
def allipay_notify_return():
    '''异步通知接收'''
    order = dict(request.args)
    sign = order.pop('sign')
    if init_alipay().verify(order,sign):
        print(order)
    else:
        print('验证不通过')

@payment_app.route('/alipay/<method>',methods=['POST'])
def alipay_request(method):
    '''支付请求'''
    alipay_obj = init_alipay()
    order = dict(request.form)

    result = alipay_obj.api_alipay_trade_query(out_trade_no=order['out_trade_no'])
    if result.get("trade_status", "") == "TRADE_SUCCESS":
        return json.dumps({'code':0,'msg':'已支付'})

    if method == 'page_pay':
        res = alipay_obj.api_alipay_trade_page_pay(
            return_url="http://127.0.0.1:8888/payment/alipay/page_pay/return",
            notify_url="http://127.0.0.1:8888/payment/notify",
            **order
        )
        return json.dumps({'code':1,'msg':res})

    elif method == 'code_pay':
        result = alipay_obj.api_alipay_trade_precreate(
            notify_url="http://127.0.0.1:8888/payment/notify",
            **order
        )
        return json.dumps({'code':1,'msg':result.get('qr_code')})

    elif method == 'barcode_pay':
        order['scene'] = 'bar_code'
        result = alipay_obj.api_alipay_trade_pay(
            notify_url="http://127.0.0.1:8888/payment/notify",
            **order
        )
        if result.get('code')=='10000':
            return json.dumps({'code':1,'msg':'支付成功'})
        elif result.get('code')=='10003':
            return json.dumps({'code':0,'msg':'order success pay inprocess'})
        else:
            return json.dumps({'code':0,'msg':result.get('sub_msg')})









