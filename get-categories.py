"""from bs4 import BeautifulSoup

with open('categorias.txt', 'r', encoding='utf-8') as archivo:
    # Lee el contenido del archivo
    contenido = archivo.read()

# Crea un objeto BeautifulSoup para analizar el contenido
soup = BeautifulSoup(contenido, 'html.parser')
categorias=soup.find_all('a',class_='mainCategories-itemLink')
for c in categorias:
    link=c['href']
    if not link.split('/')[4]=='SubProductCategory':
        with open('categorias-links.txt','a') as f:
            f.write(link+'\n')"""
     