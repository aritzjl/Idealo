![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/6dca3253-0e96-4032-821c-b20545e84ed2/27f12c53-a847-44c0-afe3-76d34ca4d73a/Untitled.png)

# Descripción

## Descripción General

Este proyecto es una herramienta avanzada diseñada específicamente para traders de Amazon que desean optimizar su proceso de búsqueda y comparación de productos en la plataforma. La herramienta utiliza técnicas de web scraping para recopilar información detallada de productos en Idealo, una plataforma de referencia para encontrar ofertas y precios competitivos en múltiples productos.

## **Interfaz Gráfica para Recopilación de URLs**:

Ofrece una interfaz gráfica intuitiva que permite al usuario recopilar URLs de productos desde Idealo. Esto se realiza mediante la selección de la cantidad de "workers", lo que agiliza el proceso de obtención de enlaces y maximiza la eficiencia del scraping.

## **Extractor de Productos**:

El extractor de productos es la parte central de la herramienta. Una vez recopiladas las URLs de los productos desde Idealo, utiliza técnicas avanzadas de scraping (Selenium y BeautifulSoup) para comparar los precios y detalles de los productos en Amazon. Los usuarios pueden configurar filtros específicos, como un porcentaje mínimo de beneficio y un valor mínimo en euros de beneficio. El extractor filtra los productos que cumplen con estos criterios y almacena los detalles relevantes, como nombre del producto, precios, porcentaje de beneficio y enlaces, en un archivo Excel. Esta función permite a los traders identificar de manera eficiente y organizada los productos que podrían ofrecer oportunidades de negocios más rentables en Amazon
