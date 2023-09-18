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

def get_product(url,workbook):
    
    firefox_options = Options()
    #firefox_options.add_argument("--headless")
    firefox_options.add_argument("--window-size=1920,1080")
    firefox_options.add_argument('--start-maximized')
    firefox_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.set_preference("javascript.enabled", False)
    driver = webdriver.Chrome(options=firefox_options)
    driver.minimize_window()
    driver.get(url)
# Configura un tiempo de espera máximo de 30 segundos
    wait = WebDriverWait(driver, 30)
    try:
        # Espera hasta que el elemento esté presente y visible
        button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'productOffers-listLoadMore')))
        button.click()
    except Exception as e:
        # Captura cualquier excepción que pueda ocurrir durante la espera o el clic
        print(f"Error: {e}")

    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    # Obtener el nombre de la tienda
    sellers = soup.find_all('a', class_='productOffers-listItemOfferShopV2LogoLink')
    driver.quit()
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
            if float(cheapest[1])*1.35<price and price-cheapest[1]>20:
                amz.append(name)
                amz.append(price)
                amz.append(seller['href']) #Aqui esta el problema, la url no es la url real de amazon sino lo que te he mostrado en el ejemplo
            else:
                print('Not enough profit')
                return
            break
    if not len(amz)!=0:
        print('Amazon not found')
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
    data=[product_name, cheapest[1], amz[1], porcentaje, beneficio, url]
    # Crear un libro de trabajo y una hoja de trabajo
    sheet = workbook.active
    sheet.append(data)

    # Especifica el nombre del archivo de Excel en el que deseas guardar los datos
    nombre_archivo = "./products.xlsx"

    # Guardar el libro de trabajo en el archivo de Excel
    workbook.save(nombre_archivo)
    workbook.close()
    bs.frena()


nombre_archivo = "./products.xlsx"
# Crear un libro de trabajo y una hoja de trabajo
workbook = Workbook()
sheet = workbook.active
# Especifica el nombre del archivo de Excel en el que deseas guardar los datos
# Agregar los datos a la hoja de trabajo
sheet.append(["Name", "Cheapest Price", "Amazon Price", "Profit %", "Profit €", "Product URL"])
# Guardar el libro de trabajo en el archivo de Excel
workbook.save(nombre_archivo)

products = bs.lines('products.txt')


    
num_workers=3
with ThreadPoolExecutor(max_workers=num_workers) as executor:
    for product in products:
        executor.submit(get_product,product[0],workbook)
        
