#Webscraping
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import openpyxl
###Envio  automatico de email
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


time.sleep(5)


contenido_pagina=requests.get(
    'https://www.cronista.com/MercadosOnline/dolar.html',
    headers={
'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36'
        }
    )


procesar_paginaweb=BeautifulSoup(contenido_pagina.text,'lxml')


dolares=procesar_paginaweb.find_all('td',class_="name")

precios=procesar_paginaweb.find_all('div',class_="sell-value")


tipos_dolar=[]
precios_dolar=[]
     
#usamos un loop para recorrer la coleccion de elementos
#agregando a la lista el texto ,que es el dato que queremos,de cada uno
for nombre in dolares:
    tipos_dolar.append(nombre.text)


for precio in precios: 
    precios_dolar.append(precio.text)


dolar_df=pd.DataFrame(
    {
      'Tipo Dolar':tipos_dolar,
      'Precio':precios_dolar
      }
    )

dolar_df.to_excel("C:\\Users\\PC\\Desktop\\mail\\CotizaciónDolar.xlsx")
cotizaciondolar=pd.read_excel("C:\\Users\\PC\\Desktop\\mail\\CotizaciónDolar.xlsx", engine='openpyxl')





subject = "Dolar al día"
body = "Cotización de venta"
sender_email = "Su mail emisor"
receiver_email = "Su mail receptor"


password = "Su contraseña"

# Crear mail
#MIME standard 

mi_mail = MIMEMultipart()
mi_mail["From"] = sender_email
mi_mail["To"] = receiver_email
mi_mail["Subject"] = subject

# agregar el cuerpo del mail al mail en si
mi_mail.attach(MIMEText(body, "plain"))


reporte = "C:\\Users\\PC\\Desktop\\mail\\CotizaciónDolar.xlsx"  


#abriendo el archivo reporte
#y poniendolo en la variable part con una codificacion necesaria
#para que sea aceptado como attachment en un mails
with open(reporte, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
 
encoders.encode_base64(part)


# encabezados que describen su contenido
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {reporte}",
)

# agregar el attachment a la variable creada para representar el mail

mi_mail.attach(part)
text = mi_mail.as_string()

# Crear una conexion segura con protocolo SSL
# al servidor de Gmail
#usar las credenciales que pusimos arriba para loguearnos remoto
# una vez ves logueados enviar el mail usando sendmail()
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
   