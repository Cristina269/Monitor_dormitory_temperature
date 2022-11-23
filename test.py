import pymysql
import api

a=api.Airconditioner(2).get_weather()
print(a[0])