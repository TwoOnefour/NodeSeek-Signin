# -- coding: utf-8 --
import os
import sys
from curl_cffi import requests
from aqua import CF_Solver


NS_RANDOM = os.environ.get("NS_RANDOM","true")
NS_COOKIE = os.environ.get("NS_COOKIE","")
COOKIE = os.environ.get("COOKIE", "")
COOKIE_ENV = NS_COOKIE or COOKIE

pushplus_token = os.environ.get("PUSHPLUS_TOKEN")
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN","")
chat_id = os.environ.get("CHAT_ID","")
telegram_api_url = os.environ.get("TELEGRAM_API_URL","https://api.telegram.org") # 代理api,可以使用自己的反代
def telegram_Bot(token,chat_id,message):
    url = f'{telegram_api_url}/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    r = requests.post(url, json=data)
    response_data = r.json()
    msg = response_data['ok']
    print(f"telegram推送结果：{msg}\n")
def pushplus_ts(token, rw, msg):
    url = 'https://www.pushplus.plus/send/'
    data = {
        "token": token,
        "title": rw,
        "content": msg
    }
    r = requests.post(url, json=data)
    msg = r.json().get('msg', None)
    print(f'pushplus推送结果：{msg}\n')

def load_send():
    global send
    global hadsend
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
            hadsend=True
        except:
            print("加载notify.py的通知服务失败，请检查~")
            hadsend=False
    else:
        print("加载通知服务失败,缺少notify.py文件")
        hadsend=False
load_send()

if COOKIE_ENV:
    cf = CF_Solver("https://www.nodeseek.com/board")
    url = f"https://www.nodeseek.com/api/attendance?random={NS_RANDOM}"
    headers = {
        'Cookie': f'{COOKIE_ENV}'
    }

    try:
        # response = requests.post(url, headers=headers)
        cf = CF_Solver("https://www.nodeseek.com/board", headers=headers)
        response = cf.client.post(url)
        response_data = response.json()
        print(response_data)
        print(COOKIE_ENV)
        message = response_data.get('message')
        success = response_data.get('success')
        send("nodeseek签到", message)
        if success == "true":
            print(message)
            if telegram_bot_token and chat_id:
                telegram_Bot(telegram_bot_token, chat_id, message)
        else:
            print(message)
            if telegram_bot_token and chat_id:
                telegram_Bot(telegram_bot_token, chat_id, message)
            if pushplus_token:
                pushplus_ts(pushplus_token, "nodeseek签到", message)
    except Exception as e:
        print("发生异常:", e)
        print("实际响应内容:", response.text)
else:
    print("请先设置Cookie")
