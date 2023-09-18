import time
import random
from datetime import datetime
from email.message import EmailMessage
import ssl
import smtplib
import re
from selenium.webdriver.common.keys import Keys

EMAIL_SENDER = "beltz.auto@gmail.com"
EMAIL_PASS = "shxcsgrnsbnsgrgx"
def espera():
    """
    Esta función hace un time.sleep de una cantidad aleatoria de tiempo entre 2 y 5 segundos.
    """
    tiempo = random.uniform(2, 5)
    time.sleep(tiempo)

def esperamas():
    """
    Esta función hace un time.sleep de una cantidad aleatoria de tiempo entre 10 y 15 segundos.
    """
    tiempo = random.uniform(10, 15)
    time.sleep(tiempo)
    
def wait(min_seconds, max_seconds):
    """
    Esta función hace un time.sleep de una cantidad aleatoria de tiempo entre los valores
    especificados como mínimo y máximo en segundos.
    
    :param min_seconds: Tiempo mínimo de espera en segundos.
    :param max_seconds: Tiempo máximo de espera en segundos.
    """
    tiempo = random.uniform(min_seconds, max_seconds)
    time.sleep(tiempo)

def log(title, description, variables, importance=1):
    """
    Esta función guarda logs en el archivo 'logs.html', incluyendo la hora exacta.
    
    :param title: Título del log.
    :param description: Descripción detallada del log.
    :param variables: Variables relevantes para el log.
    :param importance: Importancia del log (1 al 3, siendo 3 el más alto).
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    importance_styles = ["", "font-weight: bold;", "font-size: larger; font-weight: bold;", "font-size: larger; font-weight: bold; color: red;"]
    
    log_entry = f"""
    <div style="border: 1px solid black; padding: 10px; margin: 10px;">
        <p><strong>Timestamp:</strong> {timestamp}</p>
        <p style="{importance_styles[importance]}"><strong>Title:</strong> {title}</p>
        <p><strong>Description:</strong> {description}</p>
        <p><strong>Variables:</strong></p>
    """
    if variables:
        for var in variables:
            log_entry += f"<p>{var}</p>"
    log_entry += "</div>\n"
        
    with open("logs.html", "a") as log_file:
        log_file.write(log_entry)

def log_fake(title, description, variables, importance=1):
    """
    Esta función guarda logs en el archivo 'logs.html', incluyendo la hora exacta.
    
    :param title: Título del log.
    :param description: Descripción detallada del log.
    :param variables: Variables relevantes para el log.
    :param importance: Importancia del log (1 al 3, siendo 3 el más alto).
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    importance_styles = ["", "font-weight: bold;", "font-size: larger; font-weight: bold;", "font-size: larger; font-weight: bold; color: red;"]
    
    log_entry = f"""
    <div style="border: 1px solid black; padding: 10px; margin: 10px;">
        <p><strong>Timestamp:</strong> {timestamp}</p>
        <p style="{importance_styles[importance]}"><strong>Title:</strong> {title}</p>
        <p><strong>Description:</strong> {description}</p>
        <p><strong>Variables:</strong></p>
    """
    if variables:
        for var in variables:
            log_entry += f"<p>{var}</p>"
    log_entry += "</div>\n"
        
    with open("log_fake.html", "a") as log_file:
        log_file.write(log_entry)



def frena():
    """
    Esta función paraliza el script.
    
    """
    while True:
        time.sleep(1)
    
def notify(titulo, descripcion):
    """
    Esta función envia un email a tu cuenta.
    
    :param titulo: Asunto del email.
    :param descripcion: Texto del email.
    """
    try:
        email_receptor = 'aritzzjl@gmail.com'
        email_subject = titulo
        email_body = descripcion

        em = EmailMessage()
        em["From"] = EMAIL_SENDER
        em["To"] = email_receptor
        em["Subject"] = email_subject
        em.set_content(email_body)

        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as mensaje:
            mensaje.login(EMAIL_SENDER, EMAIL_PASS)
            mensaje.sendmail(EMAIL_SENDER, email_receptor, em.as_string())

        log('Email Sent',descripcion,[titulo,descripcion])

    except Exception as e:
        print("An error occurred while sending the notification:", e)


def type(str,input):
    i=0
    while i<len(str):
        input.send_keys(str[i:i+1])
        i+=1
        wait(0,1)
        
        
def save(txt,data):
    text=''
    for d in data:
        text=text+str(d)+','
    with open(txt+'.txt','a') as file:
        file.write(f'{text}\n')


def lines(file):
    categorias_array = []
    with open(file, 'r') as file:
        for line in file:
            categorias_array.append(line.strip().split(','))  # Divide la línea y agrega el resultado
    
    return categorias_array
        
        
def acentos(str):
    r=['á','é','í','ó','ú']
    a=['a','e','i','o','u']

    c=0
    while c < 5:
        str=str.replace(r[c],a[c])
        c+=1
    return str


def scroll_load(driver,sleep):
    """
    Esta función hace que Selenium driver haga scroll hasta abajo hasta que temrine de cargar todo el contenido.
    
    :param driver: Driver.
    :param sleep: Cuantos segundos quieres que espere antes de volver a hacer scroll.
    """
    # Scroll down until all images have loaded
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep)  # Adjust the sleep time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
