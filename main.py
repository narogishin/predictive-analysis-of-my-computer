import psutil
import serial
from time import sleep
from datetime import datetime
import pandas as pd

arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)

while True :
    data = pd.read_csv('data.csv')
    new_data = {
    "time":datetime.now(),
    "CPU":psutil.cpu_percent(interval=1),
    "memory":psutil.virtual_memory().percent,
    "cpu_temp":arduino.readline().decode().rstrip(),
        }
    new_data = pd.DataFrame([new_data])
    df = pd.concat([data, new_data], ignore_index=True)
    df.to_csv("data.csv", index=False)
    sleep(1)
