from etl import etl_funcao
from analise import  date_filter_func, traffic_options_func
from analise_restaurantes import qnt_entregadores_func, dist_media_func, desv_pad_fest_func, tempo_med_cidades_func, dist_tempo_cidade_func, temp_desv_ent_cidade_func, dist_tipo_alim_func
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
import locale

diretorio_dados = 'dados/train.csv'
df1 = etl_funcao(diretorio_dados)

st.set_page_config(page_title='Restaurantes', initial_sidebar_state='expanded', page_icon='<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36"><rect x="0" y="0" width="36" height="36" fill="none" stroke="none" /><path fill="#CCD6DD" d="M31 2H5a3 3 0 0 0-3 3v26a3 3 0 0 0 3 3h26a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3"/><path fill="#E1E8ED" d="M31 1H5a4 4 0 0 0-4 4v26a4 4 0 0 0 4 4h26a4 4 0 0 0 4-4V5a4 4 0 0 0-4-4m0 2c1.103 0 2 .897 2 2v4h-6V3zm-4 16h6v6h-6zm0-2v-6h6v6zM25 3v6h-6V3zm-6 8h6v6h-6zm0 8h6v6h-6zM17 3v6h-6V3zm-6 8h6v6h-6zm0 8h6v6h-6zM3 5c0-1.103.897-2 2-2h4v6H3zm0 6h6v6H3zm0 8h6v6H3zm2 14c-1.103 0-2-.897-2-2v-4h6v6zm6 0v-6h6v6zm8 0v-6h6v6zm12 0h-4v-6h6v4c0 1.103-.897 2-2 2"/><path fill="#5C913B" d="M13 33H7V16a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/><path fill="#3B94D9" d="M29 33h-6V9a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/><path fill="#DD2E44" d="M21 33h-6V23a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/></svg>')
with open("styles.css") as f:
    css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.title('Marketplace - Restaurantes')



# =============================
# Sidebar
# =============================

st.sidebar.title('Caio Fernando Brito Soares')
st.sidebar.title('Entregadores')
st.sidebar.write('---')
st.sidebar.header('Filtros')

date_slicer = st.sidebar.slider(label='Escolha o intervalo das datas',
    min_value=df1['Order_Date'].min().date(),
    max_value=df1['Order_Date'].max().date(),
    format='DD/MM/YYYY', value=df1['Order_Date'].max().date()
    )
date_slicer = datetime.combine(date_slicer, datetime.min.time())

unique_road_density = df1['Road_traffic_density'].unique().tolist()
traffic_options = st.sidebar.multiselect(
    'Condições de trânsito',
    unique_road_density,
    default=unique_road_density, placeholder='Escolha',
)

df1 = traffic_options_func(df1, traffic_options)
df1 = date_filter_func(df1, date_slicer)

st.sidebar.write('---')

# ==============================
# Sidebar Final 
# ==============================



tab1, tab2 = st.tabs(['Visão Gerencial', ' '])

with tab1:
    with st.container():
        st.markdown('# Totais')

        col1, col2, col3 = st.columns(3)
        with col1:
            qnt_entregadores = qnt_entregadores_func(df1)
            col1.metric('Qnt Entregadores', qnt_entregadores)

        with col2:
            temp_med_ent = desv_pad_fest_func(df1, 'Tempo Medio', 'No')
            col2.metric('Tempo Médio de Entregas', temp_med_ent)

        with col3:
            desv_pad_ent = desv_pad_fest_func(df1, 'Desv Padrao', 'No')
            col3.metric('Desvio Padrão de Entrega', desv_pad_ent)
 
    with st.container():       
        col1, col2, col3 = st.columns(3)
        with col1:
            dist_media = dist_media_func(df1)
            col1.metric('Distância Média', dist_media)

        with col2:
            temp_med_fest = desv_pad_fest_func(df1, 'Tempo Medio', 'Yes')
            col2.metric('Tempo Médio de Entregas - Eventos', temp_med_fest)

        with col3:
            desv_pad_fest = desv_pad_fest_func(df1, 'Desv Padrao', 'Yes')
            col3.metric('Desvio Padrão de Entrega - Eventos', desv_pad_fest)

    st.write('---')
        
    with st.container():
        st.markdown('# Tempo Médio de entrega por cidade')
        tempo_med_cidades = tempo_med_cidades_func(df1)
        fig = go.Figure(data=[go.Pie(labels=tempo_med_cidades['City'], values=tempo_med_cidades['distance'], pull=[0, 0.1, 0])])
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with st.container():
        st.markdown('# Distribuição do Tempo')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('#### Distribuiçao do Tempo por cidade')
            dist_tempo_cidade = dist_tempo_cidade_func(df1)
            st.plotly_chart(dist_tempo_cidade, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False, 'modeBarButtonsToAdd': []})
            
        with col2:
            st.markdown('#### Tempo Médio e Desvio Padrão por cidade')
            temp_desv_ent_cidade = temp_desv_ent_cidade_func(df1)
            st.plotly_chart(temp_desv_ent_cidade, config={'displayModeBar': False})

    with st.container():
        st.markdown('# Distribuição da Distancia')
        dist_tipo_alim = dist_tipo_alim_func(df1)
        st.dataframe(dist_tipo_alim, use_container_width=True, hide_index=True)
