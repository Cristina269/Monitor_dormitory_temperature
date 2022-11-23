import json
import time

import pymysql
import requests


class Airconditioner(object):
    def __init__(self, authorization):
        self.authorization = authorization

    def get_indoor_temperature(self):
        url = 'https://hxz.haier.net/api/member/uhome/deviceInfo?uhomeDeviceId=YOUR_ID'
        headers = {
            'Authorization': self.authorization,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'MicroMessenger/6.8.0(0x16080000) MacWechat/3.5.5(0x13050510) Safari/605.1.15 NetType/WIFI',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        r = requests.get(url=url, headers=headers)
        result = json.loads(r.text)["body"]["result"]
        indoorTemperature = result['indoorTemperature']
        outdoorTemperature = result['outdoorTemperature']
        # msg = '室内温度: ' + str(indoorTemperature) + '\n' + '室外温度: ' + str(outdoorTemperature)
        return indoorTemperature, outdoorTemperature

    def open(self):
        url = 'https://hxz.haier.net/api/member/uhome/open'
        headers = {

            'Authorization': self.authorization,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'MicroMessenger/6.8.0(0x16080000) MacWechat/3.5.5(0x13050510) Safari/605.1.15 NetType/WIFI',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = 'uhomeDeviceId=296787'
        r = requests.post(url=url, headers=headers, data=data)
        return r.text

    def close(self):
        url = 'https://hxz.haier.net/api/member/uhome/close'
        headers = {

            'Authorization': self.authorization,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'MicroMessenger/6.8.0(0x16080000) MacWechat/3.5.5(0x13050510) Safari/605.1.15 NetType/WIFI',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = 'uhomeDeviceId=YOUR_ID'

        r = requests.post(url=url, headers=headers, data=data)
        return r.text

    def get_weather(self):
        # 这里用的是和风天气API
        url = ''
        result = json.loads(requests.get(url=url).text)
        weather = result['now']['temp']
        weather_text = result['now']['text']
        return weather, weather_text

    def error(self=0):
        # 这里用的是bark进行消息通知
        url = ''
        requests.post(url=url)


class Major(object):
    def __init__(self=0):
        pass

    def now_time(self=0):
        return time.strftime("%H%M%S", time.localtime())

    def now_date(self=0):
        return time.strftime("%Y%m%d", time.localtime())

    def trigger(self=0):
        return time.strftime("%M", time.localtime())


class Database(object):
    def __init__(self, riqi, shijian, in_temp, out_temp, weather, weather_status):
        self.riqi = riqi
        self.shijian = shijian
        self.in_temp = in_temp
        self.out_temp = out_temp
        self.weather = weather
        self.weather_status = weather_status

    def print(self):
        print(self.riqi)

    def insert(self):
        # insert riqi , shijian , in_temp , out_temp TO air_conditioner;
        db = pymysql.connect(host='localhost', user='root', password='# PASSWORK', database='',
                             port=3306)

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 插入语句
        sql = "INSERT INTO ROOM223(date,time, indoor_temperature, outdoor_temperature,weather,weather_status) VALUES " \
              "(%s, %s,%s,%s,%s ,'%s')" % (
            self.riqi, self.shijian, self.in_temp, self.out_temp, self.weather, self.weather_status)

        # 执行sql语句
        cursor.execute(sql)

        # 提交到数据库执行
        db.commit()
        print('success db')

        # 关闭数据库连接
        db.close()
