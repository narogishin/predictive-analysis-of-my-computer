import psutil
import serial
from time import sleep
from datetime import datetime, timedelta
import pandas as pd

convert = lambda date : datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

def classify(dt):
    if len(dt) > 2 :
        return 0 if convert(dt[len(dt) - 1]) - convert(dt[len(dt) - 2]) < timedelta(hours=0, minutes=0, seconds=3) else 1
    else :
        return 0
    
arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)

while True :
    data = pd.read_csv('data.csv')
    new_data = {
    "time":str(datetime.now()),
    "CPU":psutil.cpu_percent(interval=1),
    "memory":psutil.virtual_memory().percent,
    "cpu_temp":arduino.readline().decode().rstrip(),
    "output":classify(data['time'])
        }
    new_data = pd.DataFrame([new_data])
    df = pd.concat([data, new_data], ignore_index=True)
    df['time'] = pd.to_datetime(df['time'])
    df.to_csv("data.csv", index=False)
    sleep(1)
