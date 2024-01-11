import smtplib
import email.message

def contact_func(msg_name, msg_email, msg_body):
     msg = email.message.Message()
     msg['Subject'] = 'Contato - Dashboard Restaurante'
     msg['From'] = 'caiofernandobs@gmail.com'
     msg['To'] = 'caiofernandobs@gmail.com'
     password = 'sumwqqhepozgpgir'
     msg.add_header('Content-Type', 'text/html')
     msg.set_payload(f"""
                     Nome: {msg_name} - 
                     E-mail: {msg_email} - 
                     Mensagem: {msg_body}
                    """)

     s = smtplib.SMTP('smtp.gmail.com: 587')
     s.starttls()
     
     s.login(msg['From'], password)
     s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
