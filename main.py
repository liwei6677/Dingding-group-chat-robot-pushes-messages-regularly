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
        'temperature_high': 0,
        'temperature_low': 0,
        'wind_direction': '未知',
        'wind_power': '未知',
        'date': ''
    }


# 获取天气和温度 - 使用高德地图API
def get_weather():
    # 高德地图天气API
    # 文档: https://lbs.amap.com/api/webservice/guide/api/weatherinfo
    # 支持多个城市查询，用逗号分隔城市编码
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
        'extensions': 'all'  # base: 实时天气, all: 预报天气
    }
    
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()  # 抛出HTTP错误
        data = res.json()
        
        # 检查API返回状态
        if data.get('status') != '1':
            raise Exception(f"高德地图API错误: {data.get('info', 'Unknown error')}")
        
        # 获取天气预报信息列表
        forecasts = data.get('forecasts', [])
        if not forecasts:
            raise Exception("未获取到天气数据")
        
        # 处理所有城市的天气数据
        weather_list = []
        for forecast_data in forecasts:
            # 获取城市信息
            city_name = forecast_data.get('city', '未知')
            province = forecast_data.get('province', '')
            
            # 获取预报天气信息
            casts = forecast_data.get('casts', [])
            if not casts or len(casts) < 2:
                raise Exception("未获取到明天的天气预报数据")
            
            # 获取明天的天气（索引1是明天，索引0是今天）
            tomorrow_weather = casts[1]
            
            # 提取天气信息
            weather = tomorrow_weather.get('dayweather', '未知')
            temperature_high = tomorrow_weather.get('daytemp', '0')
            temperature_low = tomorrow_weather.get('nighttemp', '0')
            wind_direction = tomorrow_weather.get('daywind', '未知')
            wind_power = tomorrow_weather.get('daypower', '未知')
            date = tomorrow_weather.get('date', '')
            
            weather_list.append({
                'city_name': city_name,
                'province': province,
                'weather': weather,
                'temperature_high': round(float(temperature_high)),
                'temperature_low': round(float(temperature_low)),
                'wind_direction': wind_direction,
                'wind_power': wind_power,
                'date': date
            })
        
        # 返回所有城市的天气信息列表
        return weather_list
    except requests.RequestException as e:
        # 处理网络请求异常（包括超时）
        print(f"Error fetching weather data: {e}")
        return [_get_default_weather_info()]
    except (ValueError, KeyError) as e:
        # 处理数据解析异常
        print(f"Error parsing weather data: {e}")
        return [_get_default_weather_info()]
    except Exception as e:
        # 处理其他异常
        print(f"Unexpected error in get_weather: {e}")
        return [_get_default_weather_info()]



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


def send_msg(token_dd, title, msg, at_all=False, msg_type="markdown"):
    """
    通过钉钉机器人发送内容
    @param token_dd: 钉钉机器人access_token
    @param title: 消息标题（markdown类型时使用）
    @param msg: 消息内容
    @param at_all: 是否@所有人
    @param msg_type: 消息类型，支持 "text" 或 "markdown"
    @return:
    """
    try:
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token_dd
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        
        if msg_type == "markdown":
            # 使用markdown格式
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": msg
                },
                "at": {
                    "isAtAll": at_all
                },
            }
        else:
            # 使用text格式
            content_str = "晚上好！\n\n{0}\n".format(msg)
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
    weather_list = get_weather()
    
    # 获取每日一句
    daily_words = get_words()
    
    # 构建markdown格式的天气信息
    # 标题
    if len(weather_list) == 1:
        title = f"晚安，{weather_list[0]['city_name']}明日天气播报"
    else:
        title = f"晚安，{len(weather_list)}个城市明日天气播报"
    
    # 正文内容（使用markdown格式）
    markdown_text = "## 晚上好！ 🌙\n\n"
    
    # 遍历所有城市的天气信息
    for idx, weather_info in enumerate(weather_list, 1):
        # 处理风力显示
        wind_power_display = weather_info['wind_power']
        if wind_power_display and not wind_power_display.endswith('级'):
            wind_power_display = f"{wind_power_display}级"
        
        # 如果有多个城市，添加序号和分隔
        if len(weather_list) > 1:
            markdown_text += f"### {idx}. {weather_info['city_name']} \n\n"
        else:
            markdown_text += f"### 📍 {weather_info['city_name']} \n\n"
        
        # 如果有日期信息，显示
        if weather_info['date']:
            markdown_text += f"> 📅 **日期**：{weather_info['date']} \n\n"
        
        # 天气详情
        markdown_text += f"> ☁️ **天气**：{weather_info['weather']} \n\n"
        markdown_text += f"> 🌡️ **温度**：{weather_info['temperature_low']}℃ ~ {weather_info['temperature_high']}℃ \n\n"
        markdown_text += f"> 💨 **风向风力**：{weather_info['wind_direction']} {wind_power_display} \n\n"
        
        # 如果是多个城市，添加分隔线
        if len(weather_list) > 1 and idx < len(weather_list):
            markdown_text += "---\n\n"
    
    # 添加每日一句
    markdown_text += f"\n💬 **每日一句**：{daily_words}\n"
    
    # 发送markdown格式消息
    send_msg(token_dd, title, markdown_text, True, "markdown")
