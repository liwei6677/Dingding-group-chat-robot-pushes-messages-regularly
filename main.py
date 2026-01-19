import os
import math
import json
import random
import requests
import datetime


# 获取天气和温度
def get_weather():
    try:
        url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
        res = requests.get(url, timeout=10).json()
        
        # Check if the response contains the expected data structure
        if 'data' in res and 'list' in res['data'] and len(res['data']['list']) > 0:
            weather = res['data']['list'][0]
            # Validate that required keys exist in weather data
            if 'weather' in weather and 'temp' in weather:
                return weather['weather'], math.floor(weather['temp'])
            else:
                print(f"Weather data missing required fields: {weather}")
                return "未知", 0
        else:
            # Fallback when weather data is unavailable
            print(f"Weather API returned unexpected response: {res}")
            return "未知", 0
    except (requests.RequestException, ValueError, KeyError) as e:
        # Handle network errors, JSON parsing errors, or key errors
        print(f"Error fetching weather data: {e}")
        return "未知", 0


# 每日一句
def get_words():
    try:
        words = requests.get("https://api.shadiao.pro/chp", timeout=10)
        if words.status_code != 200:
            return "祝你今天有个好心情！"
        data = words.json()
        if 'data' in data and 'text' in data['data']:
            return data['data']['text']
        else:
            return "祝你今天有个好心情！"
    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"Error fetching daily words: {e}")
        return "祝你今天有个好心情！"


# 字体随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def send_msg(token_dd, msg, at_all=False):
    """
    通过钉钉机器人发送内容
    @param date_str:
    @param msg:
    @param at_all:
    @return:
    """
    try:
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token_dd
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        content_str = "早上好！\n\n{0}\n".format(msg)

        data = {
            "msgtype": "text",
            "text": {
                "content": content_str
            },
            "at": {
                "isAtAll": at_all
            },
        }
        res = requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
        print(res.text)
        return res.text
    except requests.RequestException as e:
        print(f"Error sending message to DingTalk: {e}")
        return None


if __name__ == '__main__':
    city = os.environ['CITY']
    token_dd = os.environ['TOKEN_DD']
    # city = "北京"
    # token_dd = '你自己的webhook后面的access_token复制在此'
    wea, temperature = get_weather()

    note_str = "当前城市：{0}\n今日天气：{1}\n当前温度：{2}\n{3}".format(city, wea, temperature, get_words())

    send_msg(token_dd, note_str, True)
