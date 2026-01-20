import os
import math
import json
import random
import requests
import datetime


def _get_default_weather_info():
    """返回默认的天气信息（当API调用失败时使用）"""
    return {
        'city_name': '未知',
        'province': '',
        'weather': '未知',
        'temperature': 0,
        'wind_direction': '未知',
        'wind_power': '未知',
        'humidity': '未知',
        'report_time': ''
    }


# 获取天气和温度 - 使用高德地图API
def get_weather():
    # 高德地图天气API
    # 文档: https://lbs.amap.com/api/webservice/guide/api/weatherinfo
    amap_key = os.environ.get('AMAP_KEY')
    if not amap_key:
        raise ValueError("AMAP_KEY environment variable is not set")
    
    city = os.environ.get('CITY')
    if not city:
        raise ValueError("CITY environment variable is not set")
    
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        'key': amap_key,
        'city': city,
        'extensions': 'base'  # base: 实时天气, all: 预报天气
    }
    
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()  # 抛出HTTP错误
        data = res.json()
        
        # 检查API返回状态
        if data.get('status') != '1':
            raise Exception(f"高德地图API错误: {data.get('info', 'Unknown error')}")
        
        # 获取实时天气信息
        lives = data.get('lives', [])
        if not lives:
            raise Exception("未获取到天气数据")
        
        weather_data = lives[0]
        
        # 提取更多天气信息
        city_name = weather_data.get('city', '未知')
        province = weather_data.get('province', '')
        weather = weather_data.get('weather', '未知')
        temperature = weather_data.get('temperature', '0')
        wind_direction = weather_data.get('winddirection', '未知')
        wind_power = weather_data.get('windpower', '未知')
        humidity = weather_data.get('humidity', '未知')
        report_time = weather_data.get('reporttime', '')
        
        # 返回天气详细信息字典
        return {
            'city_name': city_name,
            'province': province,
            'weather': weather,
            'temperature': int(float(temperature)),
            'wind_direction': wind_direction,
            'wind_power': wind_power,
            'humidity': humidity,
            'report_time': report_time
        }
    except requests.RequestException as e:
        # 处理网络请求异常（包括超时）
        print(f"Error fetching weather data: {e}")
        return _get_default_weather_info()
    except (ValueError, KeyError) as e:
        # 处理数据解析异常
        print(f"Error parsing weather data: {e}")
        return _get_default_weather_info()
    except Exception as e:
        # 处理其他异常
        print(f"Unexpected error in get_weather: {e}")
        return _get_default_weather_info()



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
    except (requests.RequestException, ValueError) as e:
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
    city = os.environ.get('CITY')
    token_dd = os.environ.get('TOKEN_DD')
    
    if not city:
        raise ValueError("CITY environment variable is not set")
    if not token_dd:
        raise ValueError("TOKEN_DD environment variable is not set")
    
    # city = "北京"
    # token_dd = '你自己的webhook后面的access_token复制在此'
    weather_info = get_weather()

    # 构建更详细的天气信息
    note_str = (
        f"📍 当前城市：{weather_info['city_name']}\n"
        f"☁️ 今日天气：{weather_info['weather']}\n"
        f"🌡️ 当前温度：{weather_info['temperature']}℃\n"
        f"💨 风向风力：{weather_info['wind_direction']} {weather_info['wind_power']}\n"
        f"💧 空气湿度：{weather_info['humidity']}%\n"
        f"\n{get_words()}"
    )

    send_msg(token_dd, note_str, True)
