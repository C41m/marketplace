from etl import etl_funcao
from analise import qnt_entregas_fun, qnt_pedidos_dia_func, qnt_pedidos_trafego_func, qnt_pedidos_cidade_trafego_func, map_func, date_filter_func, traffic_options_func, pedidos_semana_func, pedidos_semana_entregador_func
from datetime import datetime
from streamlit_folium import folium_static
import folium
import streamlit as st
import locale


diretorio_dados = 'dados/train.csv'
df1 = etl_funcao(diretorio_dados)

map = map_func(df1)

st.set_page_config(page_title='Empresa', initial_sidebar_state='expanded' ,page_icon='<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36"><rect x="0" y="0" width="36" height="36" fill="none" stroke="none" /><path fill="#CCD6DD" d="M31 2H5a3 3 0 0 0-3 3v26a3 3 0 0 0 3 3h26a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3"/><path fill="#E1E8ED" d="M31 1H5a4 4 0 0 0-4 4v26a4 4 0 0 0 4 4h26a4 4 0 0 0 4-4V5a4 4 0 0 0-4-4m0 2c1.103 0 2 .897 2 2v4h-6V3zm-4 16h6v6h-6zm0-2v-6h6v6zM25 3v6h-6V3zm-6 8h6v6h-6zm0 8h6v6h-6zM17 3v6h-6V3zm-6 8h6v6h-6zm0 8h6v6h-6zM3 5c0-1.103.897-2 2-2h4v6H3zm0 6h6v6H3zm0 8h6v6H3zm2 14c-1.103 0-2-.897-2-2v-4h6v6zm6 0v-6h6v6zm8 0v-6h6v6zm12 0h-4v-6h6v4c0 1.103-.897 2-2 2"/><path fill="#5C913B" d="M13 33H7V16a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/><path fill="#3B94D9" d="M29 33h-6V9a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/><path fill="#DD2E44" d="M21 33h-6V23a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/></svg>')
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

with st.container():
    tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Demográfica'])

with tab1:
    with st.container():
        st.markdown('## Total de Entregas')
        qnt_entregas = qnt_entregas_fun(df1)
        st.metric('', qnt_entregas)
        st.markdown('---')

    with st.container():
        st.markdown('## Pedidos por Dia')
        qnt_pedidos_dia = qnt_pedidos_dia_func(df1)
        st.plotly_chart(qnt_pedidos_dia, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False, 'modeBarButtonsToAdd': []})
    

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('## Pedidos por tráfego')
            qnt_pedidos_trafego = qnt_pedidos_trafego_func(df1)
            st.plotly_chart(qnt_pedidos_trafego, use_container_width=True, config={'displayModeBar': False})

        with col2:
            st.markdown('## Pedidos por tipo de tráfego')
            qnt_pedidos_cidade_trafego = qnt_pedidos_cidade_trafego_func(df1)
            st.plotly_chart(qnt_pedidos_cidade_trafego, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False, 'modeBarButtonsToAdd': []})


with tab2:
    with st.container():
        st.markdown('# Entregas por Semana')
        pedidos_semana = pedidos_semana_func(df1)
        st.plotly_chart(pedidos_semana, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False, 'modeBarButtonsToAdd': []})
    
    with st.container():
        st.markdown('# Entregas por Entregador por Semana')
        pedidos_semana_entregador = pedidos_semana_entregador_func(df1)
        st.plotly_chart(pedidos_semana_entregador, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False, 'modeBarButtonsToAdd': []})
        
with tab3:
    with st.container():
        st.markdown('# Mapa')
        df_aux =df1.loc[:,['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()
        map = folium.Map()

        for index, location_info in df_aux.iterrows():
            folium.Marker( [location_info['Delivery_location_latitude'],
                            location_info['Delivery_location_longitude']],
                            popup=location_info[['City', 'Road_traffic_density']]).add_to(map)
        
        folium_static(map, width=700, height=500)

    
