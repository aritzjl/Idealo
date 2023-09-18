from selenium import webdriver
import time
from bs4 import BeautifulSoup
import beltzscrap as bs
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox  # Importar el módulo messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle  # Importar el módulo ThemedStyle
import threading
from selenium.webdriver.common.by import By  # Importa la clase By
# Configura el controlador de Selenium (asegúrate de tener el controlador adecuado instalado)
global progress
progress=0
# Define una excepción personalizada
class MiErrorPersonalizado(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
def get_page(var,driver,url):
    # Abre la página we
    #print(var)
    newurl = f'{url}{var}.html'
    originalurl=url.replace('I16-','')+'.html'
    #print(newurl)
    driver.get(newurl)
    time.sleep(10)
    if driver.current_url==originalurl and var !=15:
        raise MiErrorPersonalizado("No hay mas paginas")
    
    while True:
        try:
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            important = soup.find('div', class_='sr-searchResult__resultPanel')
            titles = important.find_all('a')
            titles = titles[:-5]
            prices = important.find_all('div', class_='sr-detailedPriceInfo__price')
            contador = 0
            #print(len(titles), len(prices))
            
            for t in titles:
                try:
                    price = prices[contador].text.replace('ab', '').replace(' €', '')
                    contador += 1
                    price = price[:-3].replace('.','')
                    min_price=float(min_product_price_entry.get())
                    if not int(price) < min_price:
                        with open('products.txt', 'a') as f:
                            f.write(t['href'] + '\n')
                            f.close()
                except Exception as e:
                    #print(f"Se ha producido un error: {str(e)}")
                    pass
            #print('Page scraped')
            #break
               
        except Exception as e:
            #print(f"Se ha producido un error: {str(e)}")
            time.sleep(3)
            continue  # Continuará ejecutando el bucle incluso después de un error
            
        
def get_all_pages(category,total_categorias):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    #chrome_options.add_argument("--start-minimized")
    chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})
    driver = webdriver.Chrome(options=chrome_options)
    driver.minimize_window()
    var=15
    while True:
        try:
            get_page(var,driver,category)
        except:
            progress+=1
            progress_bar['value'] = progress
            break
        var+=15
        
def start_scraping():  
    print('hi')
    progress_var = tk.IntVar()
    progress_var.set(0)
    
    categorias = bs.lines('categorias-links.txt')
    newcats=[]
    for categoria in categorias:
        for c in categoria:
            c=c.split('/')
            catid=c[5].split('.')[0]
            newcat=c[0] + '/' + c[1]+ '/' + c[2] + '/' + c[3]+ '/' + c[4] + '/' + catid + 'I16-'
            newcats.append(newcat)
    progress_bar.config(maximum=len(newcats), variable=progress_var)
    total_categorias=len(newcats)
    num_workers=8
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for category in newcats:
            executor.submit(get_all_pages,category,total_categorias)
    num_workers_entry.config(state='normal')
    start_button.config(state='normal')
        
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
# Create the main window
root = tk.Tk()
root.title("Idealo Scraping")
root.option_add("*tearOff", False) # This is always a good idea
root.geometry('300x400')  # Window size
# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", "forest-light.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-light")
# Title and description
title_label = tk.Label(root, text="Products URLS", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

description_label = tk.Label(root, text="Execute this program to update all the products url from Idealo.", wraplength=250)
description_label.pack()


num_workers_frame = tk.Frame(root)
num_workers_frame.pack(pady=5)

num_workers_label = tk.Label(num_workers_frame, text="Number of Workers:")
num_workers_label.pack(side=tk.LEFT)

workers_info_button = ttk.Button(num_workers_frame, text="?", style="Accent.TButton",command=show_workers_info, width=2)
workers_info_button.pack(side=tk.LEFT)

num_workers_entry = ttk.Entry(root, width=5)
num_workers_entry.pack()
# Etiqueta y entrada para Min Product Price
min_product_price_label = ttk.Label(root, text="Min Product Price:")
min_product_price_label.pack(pady=10)
min_product_price_entry = ttk.Entry(root, width=5)
min_product_price_entry.insert(0,'10')
min_product_price_entry.pack()
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

# Start the main interface loop
root.mainloop()