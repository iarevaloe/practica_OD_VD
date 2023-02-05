
import re
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_capital_states_eeuu():
    url_expansion = 'https://es.wikipedia.org/wiki/Anexo:Capitales_en_los_Estados_Unidos'
    eeuu_table_columns = [
        'state', 
        'abbreviation', 
        'incorporation_date', 
        'capital', 
        'since', 
        'area', 
        'ranked_city_population', 
        'municipal_population', 
        'metropolitan_population', 
        'note' ]

    expansion_request = requests.get(url_expansion)

    if expansion_request.status_code != 200: 
        return pd.DataFrame([], columns = eeuu_table_columns)

    expansion_web = BeautifulSoup(expansion_request.text, 'html.parser')
    table_eeuu = expansion_web.find('table',{'class':'wikitable'})

    df_table_eeuu = pd.read_html(str(table_eeuu))
    df_table_eeuu = pd.DataFrame(df_table_eeuu[0])
    df_table_eeuu.columns = eeuu_table_columns
    return(df_table_eeuu)

eeuu_data = get_capital_states_eeuu()
eeuu_data = eeuu_data[['state', 'abbreviation', 'capital']]

eeuu_data.to_csv('data\\capital_eeuu\\eeuu_states_capital.csv', index = False)