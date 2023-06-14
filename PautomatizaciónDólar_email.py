import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import schedule
import datetime

def obtener_cotizacion_dolar():
    contenido_pagina = requests.get(
        'https://www.cronista.com/MercadosOnline/dolar.html',
        headers={
            'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36'
        }
    )

    procesar_paginaweb = BeautifulSoup(contenido_pagina.text, 'lxml')

    dolares = procesar_paginaweb.find_all('td', class_="name")
    precios = procesar_paginaweb.find_all('div', class_="sell-value")

    tipos_dolar = []
    precios_dolar = []

    for nombre in dolares:
        tipos_dolar.append(nombre.text)

    for precio in precios:
        precios_dolar.append(precio.text)

    dolar_df = pd.DataFrame({
        'Dólar': tipos_dolar,
        'Venta': precios_dolar
    })

    # Guardar el archivo Excel
    CotizaciónDólar = "C:\\Users\\PC\\Desktop\\mail\\CotizaciónDólar.xlsx"
    dolar_df.to_excel(CotizaciónDólar, index=False)

    return CotizaciónDólar

def enviar_correo():
    CotizaciónDólar = obtener_cotizacion_dolar()

    subject = "Dólar al día"
    body = "Buen día, esta es la cotización de venta por el momento."
    sender_email = ""
    receiver_email = ""
    password = ""

    # Crear mail
    mi_mail = MIMEMultipart()
    mi_mail["From"] = sender_email
    mi_mail["To"] = receiver_email
    mi_mail["Subject"] = subject

    # Agregar el cuerpo del mail al mail en sí
    mi_mail.attach(MIMEText(body, "plain"))

    # Adjuntar el archivo
    with open(CotizaciónDólar, "rb") as attachment:
        part = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{CotizaciónDólar}"')
        mi_mail.attach(part)

    text = mi_mail.as_string()

    # Crear una conexión segura con protocolo SSL al servidor de Gmail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    print("El correo electrónico fue enviado correctamente.")

def programar_tarea():
    ahora = datetime.datetime.now()
    dia_semana = ahora.weekday()
    hora_actual = ahora.time()

    if (dia_semana == 0 and hora_actual >= datetime.time(9, 0)) or (dia_semana == 1 and hora_actual >= datetime.time(9, 0)):
        enviar_correo()

# Programar la tarea para que se ejecute cada minuto
schedule.every().monday.at("09:00").do(programar_tarea)
schedule.every().tuesday.at("09:00").do(programar_tarea)

while True:
    schedule.run_pending()
    time.sleep(1)