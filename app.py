# -*- coding: utf-8 -*-
'''
Created on Mon Jan 30 09:55:10 2023

@author: iarevalo
'''

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from plotnine import *
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import folium
import branca.colormap as cmp
import calendar
import locale
from PIL import Image

#locale.setlocale(locale.LC_ALL, 'esp')

capital_eeuu = pd.read_csv('scrapy_weather/data/capital_eeuu/eeuu_states_capital.csv')
weather_eeuu = pd.read_csv('scrapy_weather/data/data_visualization/weather_eeuu.csv')

weather_eeuu['date'] = pd.to_datetime(weather_eeuu['date'], format='%Y-%m-%d').dt.date
weather_eeuu['false_date'] = pd.to_datetime(weather_eeuu['false_date'], format='%Y-%m-%d').dt.date

COLOR_2018 = '#228eff'
COLOR_2019 = '#f33e80'
COLOR_2020 = '#69da4f'
COLOR_2021 = '#f7d539'
COLOR_2022 = '#b33e38'

COLOR_TEMP_MIN = 'dodgerblue'
COLOR_FILL_TEMP_MIN = 'lightblue'
COLOR_TEMP_MAX = 'tomato'
COLOR_TEMP_AVG = '#07332f'
COLOR_PREC = 'mediumseagreen'

color_map_temperature_avg = ['darkblue', 'lightblue', 'lightcoral', 'firebrick']
color_map_temperature_max = ['mistyrose', 'lightcoral', 'tomato', 'firebrick']
color_map_temperature_min = ['darkblue', 'dodgerblue', 'lightblue', 'lightcyan']
color_map_precipitation = ['honeydew', 'lightgreen', 'mediumseagreen', 'seagreen']

variables_temperatura = {
    'temperature_min': 'Temperatura mínima',
    'temperature_avg': 'Temperatura media',
    'temperature_max': 'Temperatura máxima'}

variables_mapa = {
    'temperature_min': {'text': 'Temperatura mínima (ºC): ', 
                        'color': color_map_temperature_min},
    'temperature_avg': {'text':'Temperatura media (ºC): ', 
                        'color': color_map_temperature_avg},
    'temperature_max': {'text':'Temperatura máxima (ºC): ', 
                        'color': color_map_temperature_max},
    'precipitation': {'text':'Precipitaciones (mm/h): ', 
                      'color': color_map_precipitation}
    }

functions = {
    'mean': 'Media',
    'max': 'Máxima',
    'min': 'Mínima'}

functions_2 = {
    'mean': 'Media',
    'max': 'Máxima'}

functions_3 = {
    'mean': 'Media',
    'max': 'Máxima',
    'sum': 'Acumulada'}

months = {
    1: 'Enero',
    2: 'Febrero',
    3: 'Marzo',
    4: 'Abril',
    5: 'Mayo',
    6: 'Junio',
    7: 'Julio',
    8: 'Agosto',
    9: 'Septiembre',
   10: 'Octubre',
   11: 'Noviembre',
   12: 'Diciembre'}


def return_capital_state(state, df_capital_state=capital_eeuu):
    capital_state = df_capital_state[df_capital_state['state'] == state].capital.reset_index(drop=True)
    return capital_state[0]

st.set_page_config(layout='wide')


with st.sidebar:
    selected = option_menu('¿Cambio climático?', 
                           ['Introducción',
                            'Temperaturas',
                            'Precipitaciones',
                            'Mapas'],
                           icons=['info',
                                  'thermometer-half', 
                                  'cloud-rain', 
                                  'geo-alt'],
                           menu_icon='globe-americas', default_index=0)
    
if selected == 'Introducción':
    intro_col1, intro_col2, intro_col3 = st.columns([5,1,1], gap='large')
    
    with intro_col1:
        st.title('¿Cambio climático?')
        st.write('')
        st.markdown('<div style="text-align: justify;">Con este <i>dashboard</i> pretendemos \
                    analizar si de verdad el clima está cambiando. Para ello, \
                 hemos obtenido las temperaturas y precipitaciones diarias de las \
                     capitales de Estados Unidos desde 2018 hasta 2022 mediante \
                         <i>web scraping</i> de la web <a href="https://www.wunderground.com/">\
                             Weather Underground</a>.</div>', unsafe_allow_html=True)
                             
        st.markdown('<br><div style="text-align: justify;">Se han incluido diferentes tipos de gráficos dinámicos \
                    (gráficos de líneas, barras, mapas, etc.) y tablas para estudiar tanto la evolución \
                        como la comparación entre estados de las siguientes variables: <ul><li>Temperatura media</li>\
                            <li>Temperatura mínima</li><li>Temperatura máxima</li><li>Precipitaciones\
                                </li></ul></div>', unsafe_allow_html=True)
                            
        st.markdown('<br><div style="text-align: justify;"><b>Nota:</b> No se\
                    ha incluido información del estado de Colorado ya que no se han \
                        podido obtener registros de su capital.</div>', unsafe_allow_html=True)

    
    with intro_col2:
        image_weather = Image.open('visualization//image//weather.png')
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.image(image_weather, caption=None, use_column_width='auto' )
        
        image_weather_underground = Image.open('visualization/image/weather_underground.png')
        st.markdown('<br><br>', unsafe_allow_html=True)
        st.image(image_weather_underground, caption=None, use_column_width='auto' )

        

elif selected == 'Temperaturas':
    selected_temperature = option_menu(None, ['Histórico', 'Evolución', 'Comparación'],
                                       icons=['calendar', 'reception-4', 'rulers'],
                                       menu_icon='cast', default_index=0, orientation='horizontal')
    if selected_temperature == 'Histórico':

        historico_col1, historico_col2 = st.columns([5, 2], gap='medium')

        with historico_col2:
            container_historico = st.container()
            with container_historico:
                st.text('')
                st.text('')

                temperature_select_state = st.selectbox(
                    label='**Estado**', options=weather_eeuu.state.unique())

                st.write('')

                st.write('**Temperaturas extremas**')
                temperature_multiselect_min = st.checkbox(label='Temperaturas mínimas',
                                                          value=True)
                temperature_multiselect_max = st.checkbox(label='Temperaturas máximas',
                                                          value=True)

        with historico_col1:
            data_to_plot = weather_eeuu[weather_eeuu.state ==
                                        temperature_select_state]

            fig_historico = make_subplots(specs=[[{'secondary_y': True}]])

            if temperature_multiselect_max and temperature_multiselect_min:
                
                fig_historico.add_trace(go.Scatter(
                    name='Temp. mínima',
                    x=data_to_plot.date, 
                    y=data_to_plot.temperature_min,
                    fill=None,
                    line=dict(color=COLOR_TEMP_MIN)))
                
                fig_historico.add_trace(go.Scatter(
                    name='Temp. media',
                    x=data_to_plot.date, 
                    y=data_to_plot.temperature_avg, 
                    showlegend=False,
                    fill='tonexty',
                    fillcolor=COLOR_FILL_TEMP_MIN,
                    line=dict(color=COLOR_TEMP_AVG)))
                
                fig_historico.add_trace(go.Scatter(
                    name='Temp. máxima',
                    x=data_to_plot.date, 
                    y=data_to_plot.temperature_max,
                    fill='tonexty',
                    line=dict(color=COLOR_TEMP_MAX)))
        

            elif temperature_multiselect_min and temperature_multiselect_max == False:
                
                fig_historico.add_trace(go.Scatter(
                    name='Temp. mínima',
                    x=data_to_plot.date, 
                    y=data_to_plot.temperature_min,
                    fill=None,
                    line=dict(color=COLOR_TEMP_MIN)))
                
                fig_historico.add_trace(go.Scatter(
                    name='Temp. media',
                    x=data_to_plot.date, 
                    y=data_to_plot.temperature_avg, 
                    fill='tonexty',
                    fillcolor=COLOR_FILL_TEMP_MIN,
                    line=dict(color=COLOR_TEMP_AVG)))

            elif temperature_multiselect_max and temperature_multiselect_min == False:
                
                fig_historico.add_trace(go.Scatter(
                    name='Temp. media',
                    x=data_to_plot.date, 
                    y=data_to_plot.temperature_avg,
                    fill=None,
                    line=dict(color=COLOR_TEMP_AVG)))
                
                fig_historico.add_trace(go.Scatter(
                    name='Temp. máxima',
                    x=data_to_plot.date, 
                    y=data_to_plot.temperature_max,
                    fill='tonexty',
                    line=dict(color=COLOR_TEMP_MAX)))

            else:
                
                fig_historico.add_trace(go.Scatter(
                    name='Temp. media',
                    x=data_to_plot.date, 
                    y=data_to_plot.temperature_avg, 
                    fill=None,
                    line=dict(color=COLOR_TEMP_AVG)))

            title_figure = 'Temperaturas de la ciudad de ' + return_capital_state(temperature_select_state) + ' (' + temperature_select_state + ')'

            fig_historico.update_layout(
                title=title_figure,
                yaxis_title='Temperatura (ºC)',
                hovermode='x',
                showlegend=False,
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(step='all',
                                 label='Todo'),
                            dict(count=1,
                                 label='Mensual',
                                 step='month',
                                 stepmode='backward'),
                            dict(count=6,
                                 label='Semestral',
                                 step='month',
                                 stepmode='backward'),
                            dict(count=1,
                                 label='Anual',
                                 step='year',
                                 stepmode='backward')
                            ])
                        ),
                    rangeslider=dict(
                        visible=True
                        ),
                    type='date',
                    range=['2022-01-01', '2022-12-31']
                    )
                )

            st.plotly_chart(fig_historico, use_container_width=True)

    elif selected_temperature == 'Evolución':
        
        evolucion_col1, evolucion_col2 = st.columns([5, 2], gap='medium')
        with evolucion_col2:
            container_evolucion = st.container()
            with container_evolucion:
                st.text('')
                st.text('')

                evolucion_select_state = st.selectbox(
                    label='**Estado**', options=weather_eeuu.state.unique())

                st.write('')
                
                evolucion_select_year = st.multiselect(
                    label='**Años**', 
                    options=weather_eeuu.year.unique(),
                    default=[2022,2020],
                    max_selections=5)

                st.write('')
                
                evolucion_radio_temperature = st.radio(label='**Temperaturas**',
                                                       options=['temperature_min', 
                                                                'temperature_avg',
                                                                'temperature_max'],
                                                       format_func = variables_temperatura.get,
                                                       index=1)

        with evolucion_col1:
            data_to_plot_evolucion = weather_eeuu[weather_eeuu.state == evolucion_select_state]
            data_to_plot_evolucion = data_to_plot_evolucion[data_to_plot_evolucion['year'].isin(evolucion_select_year)]
            
            data_2022 = data_to_plot_evolucion[data_to_plot_evolucion['year']==2022]
            data_2021 = data_to_plot_evolucion[data_to_plot_evolucion['year']==2021]
            data_2020 = data_to_plot_evolucion[data_to_plot_evolucion['year']==2020]
            data_2019 = data_to_plot_evolucion[data_to_plot_evolucion['year']==2019]
            data_2018 = data_to_plot_evolucion[data_to_plot_evolucion['year']==2018]
            
            wide_table_evolucion_week_2022 = data_2022[['week_of_year',
                                                        'day_of_week',
                                                        evolucion_radio_temperature]].pivot_table(
                                                            index='day_of_week', 
                                                            columns='week_of_year',
                                                            values=evolucion_radio_temperature)
            fig_evolucion = go.Figure()
            
            fig_evolucion.add_trace(go.Scatter(
                name='2022',
                x=data_2022.false_date, 
                y=data_2022[evolucion_radio_temperature], 
                line=dict(color=COLOR_2022)))
            
            fig_evolucion.add_trace(go.Scatter(
                name='2021',
                x=data_2021.false_date, 
                y=data_2021[evolucion_radio_temperature], 
                line=dict(color=COLOR_2021)))
            
            fig_evolucion.add_trace(go.Scatter(
                name='2020',
                x=data_2020.false_date, 
                y=data_2020[evolucion_radio_temperature], 
                line=dict(color=COLOR_2020)))
            
            fig_evolucion.add_trace(go.Scatter(
                name='2019',
                x=data_2019.false_date, 
                y=data_2019[evolucion_radio_temperature], 
                line=dict(color=COLOR_2019)))
            
            fig_evolucion.add_trace(go.Scatter(
                name='2018',
                x=data_2018.false_date, 
                y=data_2018[evolucion_radio_temperature], 
                line=dict(color=COLOR_2018)))
            
            title_fig_evolucion = ''
            if evolucion_radio_temperature=='temperature_avg':
                title_fig_evolucion = 'Evolución de la temperatura media de la ciudad de ' + \
                    return_capital_state(evolucion_select_state) + \
                        ' (' + evolucion_select_state + ')'
            elif evolucion_radio_temperature=='temperature_max':
                title_fig_evolucion = 'Evolución de la temperatura máxima de la ciudad de ' + \
                    return_capital_state(evolucion_select_state) + \
                        ' (' + evolucion_select_state + ')'
            else:
                title_fig_evolucion = 'Evolución de la temperatura mínima de la ciudad de ' + \
                    return_capital_state(evolucion_select_state) + \
                        ' (' + evolucion_select_state + ')'
            
            fig_evolucion.update_layout(
                title=title_fig_evolucion,
                yaxis_title='Temperatura (ºC)',
                hovermode='x',
                xaxis=dict(
                    tickformat='%-d %b',
                    rangeselector=dict(
                        buttons=list([
                            dict(count=7,
                                 label='Semanal',
                                 step='day',
                                 stepmode='backward'),
                            dict(count=1,
                                 label='Mensual',
                                 step='month',
                                 stepmode='backward'),
                            dict(count=6,
                                 label='Semestral',
                                 step='month',
                                 stepmode='backward'),
                            dict(step='all',
                                 label='Todo')
                            ])
                        ),
                    rangeslider=dict(
                        visible=True
                        ),
                    type='date',
                    range=['2018-12-01', '2018-12-31']
                    ))
            
            st.plotly_chart(fig_evolucion, use_container_width=True)
            
            
            with st.expander('Ver datos mensuales'):
                
                evolucion_radio_mensual = st.radio(label='**Temperaturas mensuales (ºC)**',
                                                       options=['min', 
                                                                'mean',
                                                                'max'],
                                                       format_func=functions.get,
                                                       horizontal=True,
                                                       index=1)
                
                data_table_evolucion = data_to_plot_evolucion.groupby(['year','month'])
                data_table_evolucion = data_table_evolucion.agg(evolucion_radio_mensual)[evolucion_radio_temperature].reset_index()

                wide_table_evolucion = data_table_evolucion.pivot(index='month', 
                                                        columns='year', 
                                                        values=evolucion_radio_temperature)         
                wide_table_evolucion.index = wide_table_evolucion.index.map(lambda x: calendar.month_name[x])

                st.table(wide_table_evolucion.style.format('{:.2f}'))          
    
    elif selected_temperature == 'Comparación':
        comparacion_col1, comparacion_col2 = st.columns([5, 2], gap='medium')
        with comparacion_col2:
            container_comparacion = st.container()
            with container_comparacion:
                st.text('')
                st.text('')
                
                with st.expander('**Estados**'):
                    comparacion_select_state = st.multiselect(
                        label='**Estados**', 
                        options=weather_eeuu.state.unique(),
                        max_selections=4,
                        label_visibility='collapsed',
                        default=['Alaska', 'Nevada'])
                
                with st.expander('**Años**'):
                    comparacion_select_year = st.multiselect(
                        label='**Años**', 
                        options=weather_eeuu.year.unique(),
                        label_visibility='collapsed',
                        default=[2022,2021],
                        max_selections=5)

                with st.expander('**Meses**'):
                    comparacion_select_month = st.multiselect(
                        label='', 
                        options=weather_eeuu.month.unique(),
                        format_func = months.get,
                        label_visibility='collapsed',
                        default=[1,2,3,4,5,6,7,8,9,10,11,12])
                
                comparacion_radio_temperature = st.radio(label='**Temperaturas**',
                                                       options=['temperature_min', 
                                                                'temperature_avg',
                                                                'temperature_max'],
                                                       format_func = variables_temperatura.get,
                                                       index=1)
                
                comparacion_radio_mensual = st.radio(label='**Temperatura mensual**',
                                                       options=['min', 
                                                                'mean',
                                                                'max'],
                                                       format_func = functions.get,
                                                       horizontal=True,
                                                       index=1)
        
        with comparacion_col1:
            data_to_plot_comparacion = weather_eeuu[weather_eeuu['state'].isin(comparacion_select_state)]
            data_to_plot_comparacion = data_to_plot_comparacion[data_to_plot_comparacion['year'].isin(comparacion_select_year)]
            data_to_plot_comparacion = data_to_plot_comparacion[data_to_plot_comparacion['month'].isin(comparacion_select_month)]
            data_to_plot_comparacion = data_to_plot_comparacion.groupby(['state','year','month'])
            data_to_plot_comparacion = data_to_plot_comparacion.agg(comparacion_radio_mensual).reset_index().round(2)
            
            figure_comparacion = go.Figure()
            
            for state in comparacion_select_state:
                plot_df = data_to_plot_comparacion[data_to_plot_comparacion.state == state]
                figure_comparacion.add_trace(
                    go.Bar(x=[plot_df.year, plot_df.month], y=plot_df[comparacion_radio_temperature], name=state),
                    )
            
            figure_comparacion.update_layout(
                title='Comparación temperaturas mensuales',
                yaxis_title='Temperatura (ºC)',
                hovermode='x',
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1))
            
            st.plotly_chart(figure_comparacion, use_container_width=True)
            
elif selected == 'Precipitaciones':
    selected_rainfall = option_menu(None, ['Histórico', 'Evolución', 'Comparación'],
                                       icons=['calendar', 'reception-4', 'rulers'],
                                       menu_icon='cast', default_index=0, orientation='horizontal')
    if selected_rainfall == 'Histórico':

        rainfall_historico_col1, rainfall_historico_col2 = st.columns([5, 2], gap='medium')

        with rainfall_historico_col2:
            rainfall_container_historico = st.container()
            with rainfall_container_historico:
                st.text('')
                st.text('')

                rainfall_select_state = st.selectbox(
                    label='**Estado**', options=weather_eeuu.state.unique())

                st.write('')

        with rainfall_historico_col1:
            data_to_plot_rainfall = weather_eeuu[weather_eeuu.state == rainfall_select_state]

            fig_rainfall_historico = go.Figure()

            fig_rainfall_historico.add_trace(go.Bar(name='Precipitación',
                                     x=data_to_plot_rainfall.date,
                                     y=data_to_plot_rainfall.precipitation))
            title_figure_rainfall = 'Precipitaciones de la ciudad de ' + \
                    return_capital_state(rainfall_select_state) + \
                        ' (' + rainfall_select_state + ')'

            fig_rainfall_historico.update_layout(
                title=title_figure_rainfall,
                yaxis_title='Precipitaciones (mm/h)',
                hovermode='x',
                showlegend=False,
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(step='all',
                                 label='Todo'),
                            dict(count=1,
                                 label='Mensual',
                                 step='month',
                                 stepmode='backward'),
                            dict(count=6,
                                 label='Semestral',
                                 step='month',
                                 stepmode='backward'),
                            dict(count=1,
                                 label='Anual',
                                 step='year',
                                 stepmode='backward')
                            ])
                        ),
                    rangeslider=dict(
                        visible=True
                        ),
                    type='date',
                    range=['2022-01-01', '2022-12-31']
                    )
                )

            st.plotly_chart(fig_rainfall_historico, use_container_width=True)

    elif selected_rainfall == 'Evolución':
        
        rainfall_evolucion_col1, rainfall_evolucion_col2 = st.columns([5, 2], gap='medium')
        
        with rainfall_evolucion_col2:
            rainfall_container_evolucion = st.container()
            with rainfall_container_evolucion:
                st.text('')
                st.text('')

                rainfall_evolucion_select_state = st.selectbox(
                    label='**Estado**', options=weather_eeuu.state.unique())

                st.write('')
                
                rainfall_evolucion_select_year = st.multiselect(
                    label='**Años**', 
                    options=weather_eeuu.year.unique(),
                    default=[2022,2020],
                    max_selections=5)

                st.write('')
                
        with rainfall_evolucion_col1:
            data_to_plot_rf_evolucion = weather_eeuu[weather_eeuu.state == rainfall_evolucion_select_state]
            data_to_plot_rf_evolucion = data_to_plot_rf_evolucion[data_to_plot_rf_evolucion['year'].isin(rainfall_evolucion_select_year)]
            
            data_rf_2022 = data_to_plot_rf_evolucion[data_to_plot_rf_evolucion['year']==2022]
            data_rf_2021 = data_to_plot_rf_evolucion[data_to_plot_rf_evolucion['year']==2021]
            data_rf_2020 = data_to_plot_rf_evolucion[data_to_plot_rf_evolucion['year']==2020]
            data_rf_2019 = data_to_plot_rf_evolucion[data_to_plot_rf_evolucion['year']==2019]
            data_rf_2018 = data_to_plot_rf_evolucion[data_to_plot_rf_evolucion['year']==2018]

            fig_rf_evolucion = go.Figure()   
            
            fig_rf_evolucion.add_trace(go.Scatter(
                name='2022',
                x=data_rf_2022.false_date, 
                y=data_rf_2022.precipitation, 
                line=dict(color=COLOR_2022)))
            
            fig_rf_evolucion.add_trace(go.Scatter(
                name='2021',
                x=data_rf_2021.false_date, 
                y=data_rf_2021.precipitation, 
                line=dict(color=COLOR_2021)))
            
            fig_rf_evolucion.add_trace(go.Scatter(
                name='2020',
                x=data_rf_2020.false_date, 
                y=data_rf_2020.precipitation, 
                line=dict(color=COLOR_2020)))
            
            fig_rf_evolucion.add_trace(go.Scatter(
                name='2019',
                x=data_rf_2019.false_date, 
                y=data_rf_2019.precipitation, 
                line=dict(color=COLOR_2019)))
            
            fig_rf_evolucion.add_trace(go.Scatter(
                name='2018',
                x=data_rf_2018.false_date, 
                y=data_rf_2018.precipitation, 
                line=dict(color=COLOR_2018)))
            
            title_fig_rf_evolucion = 'Evolución de las precipitaciones de la ciudad de ' + \
                    return_capital_state(rainfall_evolucion_select_state) + \
                        ' (' + rainfall_evolucion_select_state + ')'
            
            fig_rf_evolucion.update_layout(
                title=title_fig_rf_evolucion,
                yaxis_title='Precipitaciones (mm/h)',
                hovermode='x',
                xaxis=dict(
                    tickformat='%-d %b',
                    rangeselector=dict(
                        buttons=list([
                            dict(count=7,
                                 label='Semanal',
                                 step='day',
                                 stepmode='backward'),
                            dict(count=1,
                                 label='Mensual',
                                 step='month',
                                 stepmode='backward'),
                            dict(count=6,
                                 label='Semestral',
                                 step='month',
                                 stepmode='backward'),
                            dict(step='all',
                                 label='Todo')
                            ])
                        ),
                    rangeslider=dict(
                        visible=True
                        ),
                    type='date',
                    range=['2018-12-01', '2018-12-31']
                    ))

            st.plotly_chart(fig_rf_evolucion, use_container_width=True)
            
            with st.expander('Ver datos mensuales'):
                
                evolucion_rf_radio_mensual = st.radio(label='**Precipitaciones mensuales (mm/h)**',
                                                       options=['mean','max'],
                                                       key='rb_rf_evolucion',
                                                       format_func=functions_2.get,
                                                       horizontal=True,
                                                       index=0)
                
                data_table_rf_evolucion = data_to_plot_rf_evolucion.groupby(['year','month'])
                data_table_rf_evolucion = data_table_rf_evolucion.agg(evolucion_rf_radio_mensual)['precipitation'].reset_index()

                wide_table_rf_evolucion = data_table_rf_evolucion.pivot(index='month', 
                                                                        columns='year', 
                                                                        values='precipitation')
                wide_table_rf_evolucion.index = wide_table_rf_evolucion.index.map(lambda x: calendar.month_name[x])

                st.table(wide_table_rf_evolucion.style.format('{:.2f}'))          
    
    elif selected_rainfall == 'Comparación':
        rainfall_comparacion_col1, rainfall_comparacion_col2 = st.columns([5, 2], gap='medium')
        with rainfall_comparacion_col2:
            rainfall_container_comparacion = st.container()
            with rainfall_container_comparacion:
                st.text('')
                st.text('')
                
                with st.expander('**Estados**'):
                    rf_comparacion_select_state = st.multiselect(
                        label='**Estados**', 
                        options=weather_eeuu.state.unique(),
                        max_selections=4,
                        label_visibility='collapsed',
                        default=['Alaska', 'Nevada'])
                
                with st.expander('**Años**'):
                    rf_comparacion_select_year = st.multiselect(
                        label='**Años**', 
                        options=weather_eeuu.year.unique(),
                        label_visibility='collapsed',
                        default=[2022,2021],
                        max_selections=5)

                with st.expander('**Meses**'):
                    rf_comparacion_select_month = st.multiselect(
                        label='', 
                        options=weather_eeuu.month.unique(),
                        format_func = months.get,
                        label_visibility='collapsed',
                        default=[1,2,3,4,5,6,7,8,9,10,11,12])
                
                
                rf_comparacion_radio_mensual = st.radio(label='**Precipitaciones mensuales**',
                                                       options=['mean', 'max'],
                                                       key='rb_rf',
                                                       format_func=functions_2.get,
                                                       horizontal=True,
                                                       index=0)
        
        with rainfall_comparacion_col1:
            data_to_plot_rf_comparacion = weather_eeuu[weather_eeuu['state'].isin(rf_comparacion_select_state)]
            data_to_plot_rf_comparacion = data_to_plot_rf_comparacion[data_to_plot_rf_comparacion['year'].isin(rf_comparacion_select_year)]
            data_to_plot_rf_comparacion = data_to_plot_rf_comparacion[data_to_plot_rf_comparacion['month'].isin(rf_comparacion_select_month)]
            data_to_plot_rf_comparacion = data_to_plot_rf_comparacion.groupby(['state','year','month'])
            data_to_plot_rf_comparacion = data_to_plot_rf_comparacion.agg(rf_comparacion_radio_mensual).reset_index().round(2)
            
            figure_rf_comparacion = go.Figure()
            
            for state in rf_comparacion_select_state:
                plot_rf_df = data_to_plot_rf_comparacion[data_to_plot_rf_comparacion.state == state]
                figure_rf_comparacion.add_trace(
                    go.Bar(x=[plot_rf_df.year, plot_rf_df.month], y=plot_rf_df.precipitation, name=state),
                    )
            
            figure_rf_comparacion.update_layout(
                title='Comparación precipitaciones mensuales',
                yaxis_title='Precipitaciones (mm/h)',            
                hovermode='x',
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1))
            
            st.plotly_chart(figure_rf_comparacion, use_container_width=True)
    
elif selected == 'Mapas':
    
    selected_map = option_menu(None, ['Mapa del mundo', 'Mapa de calor'],
                                       icons=['globe', 'grid-3x3'],
                                       menu_icon='cast', default_index=0, orientation='horizontal')
    
    if selected_map == 'Mapa del mundo':
    
        with open('visualization/data/us-states.json', 'r', encoding = 'utf-8') as file:
            geojson_eeuu = json.load(file)
    
        with st.container():
            map_col0, map_col1, map_col2, map_col3, map_col4, map_col5 = st.columns([1, 3, 2, 3, 2, 1], gap='medium')
        
            with map_col1:
                map_variable_select = st.selectbox('**Información**',
                                                   options=['temperature',
                                                            'precipitation'],
                                                   format_func={'temperature': 'Temperatura',
                                                                'precipitation': 'Precipitaciones'}.get,
                                                   index=0)
                        
                if map_variable_select == 'temperature':
                    variable_to_plot = st.selectbox('**Información**',
                                                    options=['temperature_min',
                                                    'temperature_avg',
                                                    'temperature_max'],
                                                index=0,
                                                format_func=variables_temperatura.get,
                                                label_visibility='collapsed')
                    title_legend = variables_temperatura[variable_to_plot] + ' (ºC)'
                else:
                    variable_to_plot = 'precipitation'
                    title_legend = 'Precipitaciones (mm/h)'
        
            with map_col2:
                map_freq_radio = st.radio('**Período**', 
                                          options=['Día', 
                                                   'Mes', 
                                                   'Año', 
                                                   'Personalizado'],
                                          index=1)
                

        
            with map_col3:
                if map_freq_radio == 'Día':
                    map_date_input = st.date_input('**Día**',
                                                   value=weather_eeuu.date[0],
                                                   min_value=min(weather_eeuu.date),
                                                   max_value=max(weather_eeuu.date))
                
                    map_data_to_plot = weather_eeuu[weather_eeuu['date']==map_date_input][['abbreviation', variable_to_plot]]
                
                elif map_freq_radio == 'Mes':
                    map_year_select = st.selectbox('**Año y mes**',
                                                   options=weather_eeuu.year.unique(),
                                                   index=0)
                    map_month_select = st.selectbox('**Mes**',
                                                    options=weather_eeuu.month.unique(),
                                                    format_func=months.get,
                                                    index=0,
                                                    label_visibility='collapsed')
                
                    map_data_to_plot = weather_eeuu[(weather_eeuu['year']==map_year_select) 
                                                    & (weather_eeuu['month']==map_month_select)].groupby(['month', 
                                                                                                          'year', 
                                                                                                          'abbreviation'])
                
                elif map_freq_radio == 'Año':
                    map_year_select = st.selectbox('**Año**',
                                                   options=weather_eeuu.year.unique(),
                                                   index=0)
                
                    map_data_to_plot = weather_eeuu[weather_eeuu['year']==map_year_select].groupby(['year','abbreviation'])
                
                else:
                    map_date_input = st.date_input('**Rango de fechas**',
                                                   value=[weather_eeuu.date[0],
                                                          weather_eeuu.date[2]],
                                                   min_value=min(weather_eeuu.date),
                                                   max_value=max(weather_eeuu.date))
                
                    map_data_to_plot = weather_eeuu[(weather_eeuu['date']>=map_date_input[0]) 
                                                    & (weather_eeuu['date']<=map_date_input[0])].groupby('abbreviation')

                
            
            with map_col4:
                if map_variable_select == 'temperature':
                    if map_freq_radio != 'Día':
                        map_measure_radio = st.radio('**Medida**',
                                                     options=['min',
                                                              'mean',
                                                              'max'],
                                                     format_func=functions.get
                                                     )
                
                else:
                    if map_freq_radio != 'Día':
                        map_measure_radio = st.radio('**Medida**',
                                                     options=['mean',
                                                              'max',
                                                              'sum'],
                                                     format_func=functions_3.get
                                                     )
        
        with st.container():
            location_initial = [55.737652, -99.117088]
            if map_freq_radio != 'Día':
                map_data_to_plot = map_data_to_plot.agg(map_measure_radio).reset_index()
                map_data_to_plot = map_data_to_plot[['abbreviation', variable_to_plot]].round(2)
            
            state_variable_to_plot = dict(zip(map_data_to_plot['abbreviation'],
                                              map_data_to_plot[variable_to_plot]))
        
            for location_info in geojson_eeuu['features']:
                    location_info['properties']['variable'] = state_variable_to_plot[location_info['id']]        


            colors = cmp.LinearColormap(
                colors=variables_mapa[variable_to_plot]['color'],
                vmin=min(map_data_to_plot[variable_to_plot]), 
                vmax=max(map_data_to_plot[variable_to_plot]),
                caption=title_legend)

            def style_states (feature):

                return{'radius': 7,
                       'fillColor': colors(feature['properties']['variable']), 
                       'color': 'black', 
                       'weight': 1,
                       'opacity' : 1,
                       'fillOpacity' : 0.8}
        
            map_weather = folium.Map(location=location_initial, zoom_start = 3.25)

            folium.GeoJson(geojson_eeuu, style_function = style_states,
                       tooltip = folium.GeoJsonTooltip(fields = ['name','variable'],
                                                       aliases=['Estado: ', variables_mapa[variable_to_plot]['text']],
                                                       style = ("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
                                                       sticky = True
                                                       )).add_to(map_weather)
        
            folium.TileLayer('cartodbpositron').add_to(map_weather)
            colors.add_to(map_weather)
        
            map_weather
    
    elif selected_map == 'Mapa de calor':
        hmap_col1, hmap_col2 = st.columns([5, 2], gap='medium')
        
        with hmap_col2:
            hmap_state_select = st.selectbox('**Estado**',
                                                options=weather_eeuu.state.unique(),
                                                index=0)
            
            hmap_variable_select = st.selectbox('**Información**',
                                                options=['temperature',
                                                         'precipitation'],
                                                format_func={'temperature': 'Temperatura',
                                                             'precipitation': 'Precipitaciones'}.get,
                                                index=0)
                        
            if hmap_variable_select == 'temperature':
                hmap_variable_to_plot = st.selectbox('**Información**',
                                                     options=['temperature_min',
                                                              'temperature_avg',
                                                              'temperature_max'],
                                                     index=1,
                                                     format_func=variables_temperatura.get,
                                                     label_visibility='collapsed')
                title_hmap = variables_temperatura[hmap_variable_to_plot] + ' por semana de la ciudad de ' + return_capital_state(hmap_state_select) + ' (' + hmap_state_select + ')'
                variable_text_hover = variables_temperatura[hmap_variable_to_plot]
            else:
                hmap_variable_to_plot = 'precipitation'
                
                title_hmap= 'Precipitaciones por semana de la ciudad de ' +  return_capital_state(hmap_state_select) + ' (' + hmap_state_select + ')'
                variable_text_hover = 'Precipitaciones'
        
            hmap_year_select = st.selectbox('**Año**',
                                            options=weather_eeuu.year.unique(),
                                            index=0)
                
            hmap_data_to_plot = weather_eeuu[(weather_eeuu['year']==hmap_year_select) & 
                                             (weather_eeuu['state']==hmap_state_select)]
            
            hmap_data_to_plot = hmap_data_to_plot[['week_of_year',
                                                   'day_of_week',
                                                   hmap_variable_to_plot]].pivot_table(
                                                       index='day_of_week', 
                                                       columns='week_of_year',
                                                       values=hmap_variable_to_plot)
                                                       
        with hmap_col1:
            fig_hmap = px.imshow(hmap_data_to_plot, 
                                 aspect='auto', 
                                 color_continuous_scale='viridis',
                                 labels=dict(x='Semana', 
                                             y='Día', 
                                             color=variable_text_hover))
            
            fig_hmap.update_layout(
                title=title_hmap,
                xaxis_title='Semana del año',
                yaxis_title='Día de la semana',
                xaxis = dict(
                tickmode = 'array',
                tickvals = list(range(1,54,2)),
                ticktext = list(range(1,54,2))),
                yaxis = dict(
                tickmode = 'array',
                tickvals = list(range(7)),
                ticktext = list(calendar.day_name)))
            
            st.plotly_chart(fig_hmap, use_container_width=True)


                
                
        
        
                    
            
    
    