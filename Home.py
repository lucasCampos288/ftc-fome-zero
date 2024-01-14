"""
IMPORTS
"""
import streamlit as st
import altair as alt
import pandas as pd
import inflection

#
# HELPER FUNCTIONS
#
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

def country_name(country_id):
    return COUNTRIES[country_id]


def color_name(color_code):
    return COLORS[color_code]

def exchange_rates_amount(color_code):
    return exchange_rates[color_code]

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    
    return df

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America"
}

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred"
}

exchange_rates = {
    'Botswana Pula(P)': 0.5,  
    'Brazilian Real(R$)': 1.0,  
    'Dollar($)': 5.0,  
    'Emirati Diram(AED)': 1.4,  
    'Indian Rupees(Rs.)': 0.07, 
    'Indonesian Rupiah(IDR)': 0.00035,
    'NewZealand($)': 3.4,  
    'Pounds(Â£)': 6.5,  
    'Qatari Rial(QR)': 1.37, 
    'Rand(R)': 0.34, 
    'Sri Lankan Rupee(LKR)': 0.025, 
    'Turkish Lira(TL)': 0.65  
}

#
#LOADING DATA
#
df_raw = pd.read_csv('data/zomato (1).csv', encoding='ISO-8859-1')
df_raw["Cuisines"] = df_raw.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0] if isinstance(x, str) else x)
df_raw.drop_duplicates(inplace=True)
#
# LIMPEZA DE DADOS
#
df1 = df_raw.copy()

# Rename Columns
df1 = rename_columns(df1)
# country name
df1['country_name'] = df1['country_code'].map(country_name)

# price range
df1['price_range'] = df1['price_range'].map(create_price_tye)

# rating colors
df1['rating_color'] = df1['rating_color'].map(color_name)

# exchange_rates
df1['exchange_rates'] = df1['currency'].map(exchange_rates_amount)
df1['average_cost_for_two_for_real'] = df1['average_cost_for_two'] * df1['exchange_rates']

# dropna
df1 = df1.dropna()

#
# DASHBOARD STREAMLIT
#

# define mode wide screen
st.set_page_config(layout="wide")

# headline
st.header('DASHBOARD GERAL', divider='gray')

with st.sidebar:
    st.header('🍽️ - Fome Zero')
    st.write('Dashboard Fome Zero')

with st.container():
    # definindo o numero de colunas
    st.markdown("""
        Esse dashboard é composto de três pagínas, sendo elas:

        Países e Cidades: Mostrar métricas e gráficos dos países e cidades
        Tipos de culinária: mostra as visões de tipo de culinária
        Restaurantes: mostra as visões de restaurantes
        
        Qualquer dúvida, favor entrar em contato pelo seguinte e-mail:
        lucascampos288@gmail.com
    """)