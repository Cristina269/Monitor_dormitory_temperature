import time

import api

authorization = ''

while 1:
    timer = api.Major.trigger()
    time.sleep(0.1)
    while int(timer)%5 == 0 or int(timer) == 0:
        riqi = api.Major.now_date()
        shijian = api.Major.now_time()
        try:
            in_temp, out_temp = api.Airconditioner(authorization).get_indoor_temperature()
            weather = api.Airconditioner(authorization).get_weather()
            print(riqi, shijian, in_temp, out_temp, weather[0], weather[1])
            api.Database(riqi, shijian, in_temp, out_temp, weather[0], weather[1]).insert()
            time.sleep(62)
            timer = api.Major.trigger()
        except:
            api.Airconditioner.error()
            time.sleep(5)
            timer = api.Major.trigger()
