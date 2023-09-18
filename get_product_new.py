from selenium import webdriver
import time
from bs4 import BeautifulSoup
import beltzscrap as bs
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox  # Importar el módulo messagebox
from selenium.webdriver.firefox.options import Options
from tkinter import ttk
from ttkthemes import ThemedStyle  # Importar el módulo ThemedStyle
import threading
from selenium.webdriver.common.by import By  # Importa la clase By
import beltzscrap as bs
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook
from selenium.webdriver.firefox.options import Options
from concurrent.futures import ThreadPoolExecutor
global progress
progress=0
def get_product(url,workbook,total):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 1})
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(30)

    time.sleep(5)
    iframes=driver.find_elements(By.TAG_NAME,'iFrame')

    iframe = driver.find_element(By.ID, "sp_message_iframe_818331")
    driver.switch_to.frame(iframe)

    # Encuentra y hace clic en el botón dentro del iframe
    button=driver.find_element(By.CLASS_NAME,'btn-accept-all')
    button.click()

    # Cuando hayas terminado de interactuar con el iframe, asegúrate de volver al contexto principal
    driver.switch_to.default_content()
    time.sleep(1)
    try:
        button=driver.find_element(By.CLASS_NAME,'productOffers-listLoadMore')
        button.click()
    except:
        pass
    time.sleep(1)
    try:
        button=driver.find_element(By.CLASS_NAME,'productOffers-listLoadMore')
        button.click()
    except:
        pass
    time.sleep(1)
    try:
        html=driver.page_source

        soup=BeautifulSoup(html,'html.parser')
        # Obtener el nombre de la tienda
        sellers = soup.find_all('a', class_='productOffers-listItemOfferShopV2LogoLink')
        driver.quit()
        global progress
        progress+=1
        progress_label.config(text=f'{progress}/{total}')
        with open('./checked_products.txt','a') as f:
            f.write(f'{url}\n')
            f.close()
        cheapest=[sellers[0]['data-shop-name'].replace(' ','').replace('\n',''),float(sellers[0]['data-gtm-payload'].split('"product_price": "')[1].split('"')[0]),sellers[0]['href']]
        if cheapest[0]=='eBay':
            print('eBay')
            return
        if 'amazon' in cheapest[0].lower():
            print('Amazon is the cheapest')
            return
        amz=[]
        for seller in sellers:
            name=seller['data-shop-name']
            price=float(seller['data-gtm-payload'].split('"product_price": "')[1].split('"')[0])
            if 'amazon' in name.lower():
                porcentaje_min=float(min_percent_benefit_entry.get())
                beneficio_min=float(min_euro_benefit_entry.get())
                if float(cheapest[1])*porcentaje_min<price and price-cheapest[1]>beneficio_min:
                    amz.append(name)
                    amz.append(price)
                    amz.append(seller['href']) #Aqui esta el problema, la url no es la url real de amazon sino lo que te he mostrado en el ejemplo
                else:
                    info_label.config(text=f'Not enough profit')
                    return
                break
        if not len(amz)!=0:
            print('Amazon not found')
            info_label.config(text=f'Amazon not found')
            return
        porcentaje=(amz[1]-cheapest[1])/cheapest[1]*100
        beneficio=amz[1]-cheapest[1]
        product_name=soup.find('h1',class_='oopStage-title').find('span').text
        """
        Descartado para aumentar la eficiencia
        xpath=f'//img[contains(@alt, "{amz[0]}") and contains(@class, "productOffers-listItemOfferShopV2LogoImage")]'
        imagen = driver.find_element(By.XPATH,xpath)
        imagen.click()
        """
        #Data: Name, Cheapest Price, Amazon Price, Profit %, Profit €, Cheap Seller URL, Amz URL
        print(product_name)
        info_label.config(text=f'Saved {product_name}')
        data=[product_name, cheapest[1], amz[1], porcentaje, beneficio, url]
        # Crear un libro de trabajo y una hoja de trabajo
        try:
            sheet = workbook.active
            sheet.append(data)

            # Especifica el nombre del archivo de Excel en el que deseas guardar los datos
            nombre_archivo = "./products.xlsx"

            # Guardar el libro de trabajo en el archivo de Excel
            workbook.save(nombre_archivo)
        except Exception as e:
            print(f'Error al guardar el archivo: {str(e)}')
    except Exception as e:
        # Captura cualquier excepción que pueda ocurrir durante la espera o el clic
        print(f"Error: {e}")

def start_scraping():
    start_button.config(state='disabled')
    nombre_archivo = "./products.xlsx"
    # Crear un libro de trabajo y una hoja de trabajo
    workbook = Workbook()
    sheet = workbook.active
    # Especifica el nombre del archivo de Excel en el que deseas guardar los datos
    # Agregar los datos a la hoja de trabajo
    sheet.append(["Name", "Cheapest Price", "Amazon Price", "Profit %", "Profit €", "Product URL"])
    # Guardar el libro de trabajo en el archivo de Excel
    workbook.save(nombre_archivo)
    num_workers = int(num_workers_entry.get())
    products = bs.lines('./products.txt')
    total_products=len(products)
    progress_label.config(text=f'/{total_products}')
    num_workers=5
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for product in products:
            executor.submit(get_product,product[0],workbook,total_products)
            



def show_workers_info():
    workers_info = (
        "The number of workers determines how many 'bots' will be used for scraping.\n"
        "Using more workers can speed up the process, but keep in mind that an excessive number\n"
        "can lead to higher resource consumption and performance issues.\n"
        'Should not use more than 20.'
    )
    messagebox.showinfo("Workers Information", workers_info)
def start_scraping_thread():
    thread = threading.Thread(target=start_scraping)
    thread.start()   
# Crear una nueva ventana para la configuración
root = tk.Tk()
root.title("Configuration")
root.geometry('300x550')
# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", "forest-light.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-light")

# Set the theme with the theme_use method
style.theme_use("forest-light")

# Título de la ventana de configuración
title_label = ttk.Label(root, text="Idealo Products Scraper", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Descripción
description_label = ttk.Label(root, text="Execute this in order to make your bots search all the saved products urls, and storage the products that meet your requirements.", wraplength=250)
description_label.pack()

num_workers_frame = tk.Frame(root)
num_workers_frame.pack(pady=5)

num_workers_label = tk.Label(num_workers_frame, text="Number of Workers:")
num_workers_label.pack(side=tk.LEFT)

workers_info_button = ttk.Button(num_workers_frame, text="?", style="Accent.TButton",command=show_workers_info, width=2)
workers_info_button.pack(side=tk.LEFT)

num_workers_entry = ttk.Entry(root, width=5)
num_workers_entry.insert(0,'5')
num_workers_entry.pack()


# Etiqueta y entrada para Min % Benefit
min_percent_benefit_label = ttk.Label(root, text="Min % Benefit: (example 1.35 = 35%)")
min_percent_benefit_label.pack(pady=10)
min_percent_benefit_entry = ttk.Entry(root, width=5)
min_percent_benefit_entry.insert(0,'1.35')
min_percent_benefit_entry.pack()

# Etiqueta y entrada para Min € Benefit
min_euro_benefit_label = ttk.Label(root, text="Min € Benefit:")
min_euro_benefit_label.pack(pady=10)
min_euro_benefit_entry = ttk.Entry(root, width=5)
min_euro_benefit_entry.insert(0,'20')
min_euro_benefit_entry.pack()


# Progress bar and info label
progress_label = tk.Label(root, text="Progress:")
progress_label.pack(pady=10)

info_label = tk.Label(root, text="")
info_label.pack()

progress_bar = ttk.Progressbar(root, mode='determinate', length=250)
progress_bar.pack()

# "Start Scraping" button
start_button = ttk.Button(root, text="Start Scraping", style="Accent.TButton",command=start_scraping_thread)
start_button.pack(pady=10)

# Iniciar el bucle de la ventana de configuración
root.mainloop()