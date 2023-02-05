import glob
import pandas as pd

def convert_fahrenheit_to_celsius(temperature_f):
    temperature_c = round((temperature_f-32)*(5/9), 2)
    return temperature_c

def convert_in_to_mm(variable_in):
    variable_mm = round(variable_in*25.4, 2)
    return variable_mm


capital_eeuu = pd.read_csv('data/capital_eeuu/eeuu_states_capital.csv')

csv_weather_files = glob.glob('data/*.csv')
df_weather_list = (pd.read_csv(file) for file in csv_weather_files)

weather_eeuu = pd.concat(df_weather_list, ignore_index=True)

weather_eeuu['date'] = pd.to_datetime(weather_eeuu[['day', 'month', 'year']], format='%d/%m/%Y')
weather_eeuu = weather_eeuu[~((weather_eeuu['day'] == 29) & (weather_eeuu['month'] == 2))]

day_of_year =  pd.PeriodIndex(weather_eeuu['date'], freq ='D')

weather_eeuu['day_of_year'] = day_of_year.dayofyear
weather_eeuu['week_of_year'] = weather_eeuu['date'].apply(lambda x: x.strftime('%V'))
weather_eeuu['day_of_week'] = weather_eeuu['date'].apply(lambda x: x.strftime('%w'))
weather_eeuu['year_str'] = weather_eeuu['year'].astype(str)

weather_eeuu['false_year'] = 2018
weather_eeuu['false_date'] = weather_eeuu[['day',
                                           'month',
                                           'false_year']].apply(lambda x: '/'.join(x.values.astype(str)), 
                                                         axis='columns')
weather_eeuu['false_date'] = pd.to_datetime(weather_eeuu['false_date'], format='%d/%m/%Y')

weather_eeuu = weather_eeuu.merge(
    capital_eeuu, left_on='state', right_on='abbreviation', how='inner', suffixes=('_x', None))
weather_eeuu = weather_eeuu.drop(columns='state_x')

                                                         
weather_eeuu['precipitation'] = weather_eeuu['precipitation'].apply(convert_in_to_mm)
weather_eeuu[['temperature_avg', 
              'temperature_min', 
              'temperature_max']] = weather_eeuu[['temperature_avg', 
                                                'temperature_min', 
                                                'temperature_max']].apply(
                                                    convert_fahrenheit_to_celsius,
                                                    axis=1)

weather_eeuu = weather_eeuu.drop(columns=['dew_point_max', 
                                          'dew_point_min',
                                          'dew_point_avg',
                                          'humidity_max',
                                          'humidity_min',
                                          'humidity_avg',
                                          'wind_speed_max',
                                          'wind_speed_min',
                                          'wind_speed_avg',
                                          'preasure_max',
                                          'preasure_min',
                                          'preasure_avg']) 
                                                                       
weather_eeuu.to_csv('data/data_visualization/weather_eeuu.csv', index = False)