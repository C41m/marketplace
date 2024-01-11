import plotly.express as px
import folium
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from haversine import haversine
from datetime import timedelta


def qnt_entregadores_func(df1):
    qnt_entregadores = len(df1.loc[:, 'Delivery_person_ID'].unique())
    return qnt_entregadores

def dist_media_func(df1):
    cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
    df1['distance'] = df1.apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)

    dist_media = np.round(df1['distance'].mean(), 2)

    return dist_media

def desv_pad_fest_func(df1, col_med_desv, festival):
    cols = ['Time_taken(min)', 'Festival']
    temp_med_fest = df1.loc[:, cols].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']})
    temp_med_fest.columns = ['Tempo Medio', 'Desv Padrao']
    temp_med_fest = temp_med_fest.reset_index()

    temp_med_fest = np.round(temp_med_fest.loc[temp_med_fest['Festival'] == festival, col_med_desv], 2)


    # Função para formatar minutos e segundos
    def formatar_tempo(media_em_minutos):
        minutos = int(media_em_minutos)
        segundos = round((media_em_minutos - minutos) * 60)
        return timedelta(minutes=minutos, seconds=segundos)

    # Certifique-se de que a Série está convertida para o tipo correto
    temp_med_fest = temp_med_fest.astype(float)

    # Usando a função map para aplicar a formatação
    temp_med_fest_formatada = temp_med_fest.map(formatar_tempo)

    # Converter a Série para uma lista de strings formatadas
    temp_med_fest_lista = temp_med_fest_formatada.apply(lambda x: f"{(x.seconds // 60) % 60:02d}:{x.seconds % 60:02d}")

    # Selecione o primeiro valor da lista para usar no método metric
    valor_metric = temp_med_fest_lista.iloc[0]

    return valor_metric

def tempo_med_cidades_func(df1):
    cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
    df1['distance'] = df1.apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
    
    tempo_medio_cidades = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()

    return tempo_medio_cidades

def dist_tempo_cidade_func(df1):
    df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)':['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = go.Figure()

    # Utilize hovertemplate para personalizar o texto que aparece quando você passa o mouse sobre as barras
    hover_template = '%{x}: %{y:.6f} ± %{customdata:.2f}'
    fig.add_trace(go.Bar(
        name='',
        x=df_aux['City'],
        y=df_aux['avg_time'],
        error_y=dict(type='data', array=df_aux['std_time']),
        customdata=df_aux['std_time'],
        hovertemplate=hover_template
    ))

    # Desativar completamente a interatividade de seleção
    fig.update_layout(
        dragmode=False
    )

    fig.update_layout(barmode='group')


    return fig

def temp_desv_ent_cidade_func(df1):
    cols =['City', 'Time_taken(min)', 'Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)' : ['mean', 'std']})

    df_aux.columns = ['avg_time', 'std_time']

    df_aux = df_aux.reset_index()

    fig = px.sunburst(df_aux, 
                    path=['City', 'Road_traffic_density'], 
                    values='avg_time',
                    color='std_time',
                    color_continuous_scale='RdBu',
                    color_continuous_midpoint=np.average(df_aux['std_time']))

    # Personalizando o layout da dica de ferramenta
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Tempo Médio: %{value:.2f} minutos<br>Std Time: %{customdata[0]:.2f} minutos'
    )

    # Ajustando o título da barra de cores
    fig.update_layout(coloraxis_colorbar_title='Desvio Padrão de Tempo (minutos)')

    return fig

def dist_tipo_alim_func(df1):
    cols = ['City', 'Time_taken(min)', 'Type_of_order']
    df_aux = df1.loc[:, cols].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})

    df_aux.columns = ['Tempo Medio (min)', 'Desvio Padrão (min)']

    df_aux = df_aux.reset_index()

    df_aux = df_aux.rename(columns={'City': 'Cidade', 'Type_of_order': 'Tipo de Pedido'})
    return df_aux



# def tempo_mwe
#     cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
#     df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
#     df_aux.columns = ['Tempo Medio', 'Desv Padrao']
#     df_aux = df_aux.reset_index()