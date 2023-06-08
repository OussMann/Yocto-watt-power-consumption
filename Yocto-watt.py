import os
import sys
import pandas as pd
from yoctopuce.yocto_api import *
from yoctopuce.yocto_power import *
from yoctopuce.yocto_datalogger import *
from datetime import date, datetime

def export_data_to_csv(data_logger, data_sets):
    for data_set in data_sets:
        filename = "data_{}_{}.csv".format(data_set.get_startTimeUTC(), data_set.get_endTimeUTC())
        data_set.exportCSV(filename)
        print("Exported data to:", filename)

def die(msg):
    sys.exit(msg + ' (check USB cable)')

errmsg = YRefParam()

target = 'any'

# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("Init error" + errmsg.value)

if target == 'any':
    # Retrieve any Power sensor
    sensor = YPower.FirstPower()
    if sensor is None:
        die('No module connected')
else:
    sensor = YPower.FindPower(target + '.power')

if not sensor.isOnline():
    die('Device not connected')

# Find and open the data logger
data_logger = YDataLogger.FirstDataLogger()
if data_logger is None:
    sys.exit("No data logger found!")

try:
    while sensor.isOnline():
        # Print current power value
        value = sensor.get_currentValue()
        date = datetime.today()
        power_summary = [{'date': date.strftime("%d-%m-%Y %H:%M:%S"), 'power': value}]
        print(power_summary)
        df = pd.DataFrame(power_summary)
        df.to_csv('test1.csv', index=False, mode='a', header=False)

        # Retrieve the list of recorded data sets
        data_sets = data_logger.get_dataSets()
 
        YAPI.Sleep(1000)
finally:
    # Disconnect from the Yoctopuce API
    YAPI.FreeAPI()

