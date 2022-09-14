from powerservice import trading
import pandas as pd
import numpy as np
from datetime import datetime
import csv




todaytrades = trading.get_trades(date='21/01/2022')
yesterdaytrades = trading.get_trades(date='20/01/2022')

dftoday= pd.DataFrame(todaytrades[1])

todaytime = pd.to_datetime(dftoday.time)

todaytimegrouped = dftoday.groupby([todaytime.dt.hour]).agg(volume=('volume', 'sum'))

output = todaytimegrouped.reset_index()[['time', 'volume']]

"""convert time column to datetime 24 hour format, shifting las row to first"""
output['time'] = pd.to_datetime(output.time, format='%H')
output['time'] = output['time'].dt.strftime('%H:%M')
output=output.apply(np.roll, shift=1)

output2 = output[["time","volume"]]

"""get current date/time and create file name""" 
dateTimeObj = datetime.now()
dt_string = dateTimeObj.strftime("%Y%m%d_%H%M")

"""CSV file"""
file_name="PowerService_" + dt_string + ".csv"
output2.to_csv(file_name,  index=False)
datetime_series = pd.to_datetime(dftoday['time'])
datetime_index = pd.DatetimeIndex(datetime_series.values)
df3=dftoday.set_index(datetime_index)

df4 = df3.resample('5T').mean()
df3=df3.set_index(df4.index)
df3=df3.set_index(df4.index).reset_index()
df3 = df3.fillna(0)
df_quality1= df3[df3['time'] == 0]
df_quality1['index'] = df_quality1['index'].dt.strftime('%H:%M')

df_quality1.rename(columns = {'index':'missed_intervals'}, inplace = True)
df_quality1 = df_quality1[["date","missed_intervals","id"]]

"""CSV data quality file"""
file_name="PowerService_" + dt_string + "_data_quality.csv"

fields=['<< TIME INTERVAL VALIDATION >>']
with open(file_name, 'a') as f:
     writer = csv.writer(f)
     writer.writerow([fields])
     
"""export csv file"""
df_quality1.to_csv(file_name, mode='a', index=False)

df_quality2=df3[(df3['volume'] == 0) & (df3['time'] != 0)]
df_quality2 = df_quality2[["date","time","volume","id"]]

fields=['<< MISSING VALUES VALIDATION >>']
with open(file_name, 'a') as f:
     writer = csv.writer(f)
     writer.writerow([fields])

"""export csv file"""
df_quality2.to_csv(file_name, mode='a', index=False)

"""Print the datetime_index"""
print(df4.describe())

"""Start/End time validation"""
if output2.time[0] == '23:00' and output2.time[23] == '22:00':
     print('START AND END TIME: CORRECT')
     validationtime = 'START AND END TIME: CORRECT'
else:
     print('START AND END TIME: INCORRECT')
     validationtime ='START AND END TIME: INCORRECT'

with open(file_name, 'a') as f:
     writer = csv.writer(f)
     writer.writerow([validationtime])

try:
    pd.to_datetime(output2['time'], format='%H:%M', errors='raise')
    print('Valid')
    validationformat = 'TIME FORMAT: VALID'
except ValueError:
    print('Invalid')
    validationformat = 'TIME FORMAT: INVALID'

with open(file_name, 'a') as f:
     writer = csv.writer(f)
     writer.writerow([validationformat])


file_name2="PowerService_" + dt_string + "_data_profiling.csv"
fields=file_name2
with open(file_name2, 'a') as f:
     writer = csv.writer(f)
     writer.writerow([fields])