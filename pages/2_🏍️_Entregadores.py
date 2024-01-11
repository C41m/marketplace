from etl import etl_funcao
from analise import  date_filter_func, traffic_options_func
from analise_entregadores import idade_func, condicao_veiculo_func, med_ent_func, med_desv_tra_func, med_desv_cli_func, ent_mais_rap_func, df_ent_mais_len_func
from datetime import datetime
from streamlit_folium import folium_static
import folium
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
diretorio_dados = 'dados/train.csv'
df1 = etl_funcao(diretorio_dados)

st.set_page_config(page_title='Entregadores', initial_sidebar_state='expanded' ,page_icon='<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36"><rect x="0" y="0" width="36" height="36" fill="none" stroke="none" /><path fill="#CCD6DD" d="M31 2H5a3 3 0 0 0-3 3v26a3 3 0 0 0 3 3h26a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3"/><path fill="#E1E8ED" d="M31 1H5a4 4 0 0 0-4 4v26a4 4 0 0 0 4 4h26a4 4 0 0 0 4-4V5a4 4 0 0 0-4-4m0 2c1.103 0 2 .897 2 2v4h-6V3zm-4 16h6v6h-6zm0-2v-6h6v6zM25 3v6h-6V3zm-6 8h6v6h-6zm0 8h6v6h-6zM17 3v6h-6V3zm-6 8h6v6h-6zm0 8h6v6h-6zM3 5c0-1.103.897-2 2-2h4v6H3zm0 6h6v6H3zm0 8h6v6H3zm2 14c-1.103 0-2-.897-2-2v-4h6v6zm6 0v-6h6v6zm8 0v-6h6v6zm12 0h-4v-6h6v4c0 1.103-.897 2-2 2"/><path fill="#5C913B" d="M13 33H7V16a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/><path fill="#3B94D9" d="M29 33h-6V9a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/><path fill="#DD2E44" d="M21 33h-6V23a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/></svg>')
with open("styles.css") as f:
    css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.title('Marketplace')

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
        st.title('Overall Metrics')

        col1, col2, col3, col4 = st.columns(4, gap='Small')
        idade_min, idade_max = idade_func(df1)
        cond_veic_min, cond_veic_max = condicao_veiculo_func(df1)

        with col1:
            # Maior idade dos entregadores
            st.markdown('##### Maior Idade')
            st.markdown(f'## {idade_max}')

        with col2:
            # Menor idade dos entregadores
            st.markdown('##### Menor Idade')
            st.markdown(f'## {idade_min}')
      
        with col3:
            # Melhor situação de veículo
            st.markdown('##### Melhor Condição de Veiculos')
            st.markdown(f'## {cond_veic_max}')
        with col4:
            st.markdown('##### Pior Condição de Veiculos')
            st.markdown(f'## {cond_veic_min}')


    with st.container():
        st.markdown('---')
        st.markdown('# Avaliações')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliações Médias por Entregador')
            df_aux_med_ent = med_ent_func(df1)
            st.dataframe(df_aux_med_ent, use_container_width=True, hide_index=True)
            
        with col2:
            st.markdown('##### Avaliação Média por Trânsito')
            df_aux_med_desv_tra = med_desv_tra_func(df1)
            st.dataframe(df_aux_med_desv_tra, use_container_width=True, hide_index=True)

            st.markdown('##### Avaliação Média por Clima')
            df_aux_med_desv_cli = med_desv_cli_func(df1)
            st.dataframe(df_aux_med_desv_cli, use_container_width=True, hide_index=True)

    with st.container():
        st.markdown('---')
        st.markdown('# Velocidade de Entrega')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('### Entregadores Mais Rápidos')
            ent_mais_rap = ent_mais_rap_func(df1)
            st.dataframe(ent_mais_rap, use_container_width=True, hide_index=True)

        with col2:
            st.markdown('### Entregadores Mais Lentos')
            df_ent_mais_len = df_ent_mais_len_func(df1)
            st.dataframe(df_ent_mais_len, use_container_width=True, hide_index=True)
