import streamlit as st
import re
from config import contact_func

def is_email_valid(email):
     return bool(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email))

def is_text_valid(msg_body):
     if msg_body == '':
          return False
     return True

def is_name_valid(msg_name):
     if msg_name == '':
          return False
     return True


st.set_page_config(page_title='Contato', initial_sidebar_state='expanded', page_icon='<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36"><rect x="0" y="0" width="36" height="36" fill="none" stroke="none" /><path fill="#CCD6DD" d="M31 2H5a3 3 0 0 0-3 3v26a3 3 0 0 0 3 3h26a3 3 0 0 0 3-3V5a3 3 0 0 0-3-3"/><path fill="#E1E8ED" d="M31 1H5a4 4 0 0 0-4 4v26a4 4 0 0 0 4 4h26a4 4 0 0 0 4-4V5a4 4 0 0 0-4-4m0 2c1.103 0 2 .897 2 2v4h-6V3zm-4 16h6v6h-6zm0-2v-6h6v6zM25 3v6h-6V3zm-6 8h6v6h-6zm0 8h6v6h-6zM17 3v6h-6V3zm-6 8h6v6h-6zm0 8h6v6h-6zM3 5c0-1.103.897-2 2-2h4v6H3zm0 6h6v6H3zm0 8h6v6H3zm2 14c-1.103 0-2-.897-2-2v-4h6v6zm6 0v-6h6v6zm8 0v-6h6v6zm12 0h-4v-6h6v4c0 1.103-.897 2-2 2"/><path fill="#5C913B" d="M13 33H7V16a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/><path fill="#3B94D9" d="M29 33h-6V9a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/><path fill="#DD2E44" d="M21 33h-6V23a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2z"/></svg>')
with open("styles.css") as f:
    css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.markdown('# Contato')


with st.form('Contato', clear_on_submit=True):
     st.markdown("## Fale comigo!")

     # Campo para inserir um e-mail
     msg_name = st.text_input('', placeholder='Nome')

     msg_email = st.text_input('', placeholder='Digite seu e-mail')

     msg_body = st.text_area('', placeholder='Digite sua mensagem')


     # Botão para enviar o formulário
     if st.form_submit_button("Enviar"):
          if is_email_valid(msg_email) and is_text_valid(msg_body) and is_name_valid(msg_name):
               with st.spinner('Enviando...'):
                    contact = contact_func(msg_name, msg_email, msg_body)
               st.success("Mensagem enviada com sucesso!")               
          elif is_email_valid(msg_email) == False:
               st.error("E-mail inválido. Por favor, insira um e-mail válido.")
          elif is_text_valid(msg_body) == False:
               st.error("Digite sua mensagem.")
          elif is_name_valid(msg_name) == False:
               st.error("Digite seu nome.")


