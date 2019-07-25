

import time
import qrcode
import json
from flask import Flask, current_app, redirect, url_for ,render_template, session,request
from .alipay_fun import init_alipay


payment_app = Flask('payment')


out_trade_no = 11111111111
@payment_app.route('/')
def index():
    return render_template('payment.html')

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

def alipay_query_order(out_trade_no:int, cancel_time:int and 'secs'):
    '''
    :param out_trade_no: 商户订单号
    :return: None
    '''
    _time = 0
    for i in range(10):
        time.sleep(5)
 
        result = init_alipay().api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            print('订单已支付!')
            print('订单查询返回值：',result)
            break
 
        _time += 5
        if _time >= cancel_time:
            alipay_cancel_order(out_trade_no,cancel_time)
            return


@payment_app.route('/alipay/<method>',methods=['POST'])
def alipay_request(method):
    order = dict(request.form)
    order['out_trade_no']=out_trade_no
    alipay_obj = init_alipay()
    if method == 'page_pay':
        res = alipay_obj.api_alipay_trade_page_pay(
            return_url="http://127.0.0.1:8888/payment/",
            notify_url="http://127.0.0.1:8888/payment/",
            **order
        )
        return res
    elif method == 'code_pay':
        code_url = alipay_obj.api_alipay_trade_page_pay(
            return_url="http://127.0.0.1:8888/payment/",
            notify_url="http://127.0.0.1:8888/payment/",
            **order
        )
        qr = qrcode.QRCode(version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,border=1)
        qr.add_data(code_url)  # 二维码所含信息
        img = qr.make_image()  # 生成二维码图片
        # img.save(r'qr_test_ali.png')
        return img
    






