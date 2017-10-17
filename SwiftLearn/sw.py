#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import itchat
import datetime
import tushare as ts

stock_symbol = input('请输入股票代码 \n>  ')
price_low = input('请输入最低预警价格 \n>  ')
price_high = input('请输入最高预警价格 \n>  ')


# 登陆微信
def login():
    itchat.auto_login()


# 获取股价并发送提醒
def stock():
    
	# 获取当前时间
    time = datetime.datetime.now()
    now = time.strftime('%H:%M:%S')
    # 获取股票信息
    data = ts.get_realtime_quotes(stock_symbol)
    r1 = float(data['price'])
    r2 = str(stock_symbol) + ' 的当前价格为 ' + str(r1)
    content = now + '\n' + r2

    # 设置预警价格并发送预警信息
    if r1 <= float(price_low):
        itchat.send(content, '低于最低预警价格', toUserName='filehelper')
        print('低于最低预警价格')
    elif r1 >= float(price_high):
        itchat.send(content, '高于最高预警价格', toUserName='filehelper')
        print('高于最高预警价格')
    else:
        pass

if __name__ == '__main__':
    login()
    while True:   
        try:
			# 每3秒循环执行
            stock()
            time.sleep(3)
        except KeyboardInterrupt:
            itchat.send('Stock_WeChat 已执行完毕！\n', 
                toUserName='filehelper')
            print('Stock_WeChat 已执行完毕！\n')
            break



