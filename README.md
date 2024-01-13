![image](https://github.com/iBeltz-py/Idealo/assets/129123101/fc3a2892-c187-4f9e-9aa4-5bc6030fd51e)


# Description

## General Description

This project is an advanced tool specifically designed for Amazon traders aiming to optimize their process of searching and comparing products on the platform. The tool employs web scraping techniques to gather detailed product information from Idealo, a reference platform for finding deals and competitive prices on various products.

## **Graphical Interface for URL Collection**:

It provides an intuitive graphical interface that enables users to collect product URLs from Idealo. This is accomplished by selecting the number of "workers," streamlining the link retrieval process, and maximizing the efficiency of scraping.

## **Product Extractor**:

The product extractor is the central part of the tool. Once the product URLs are collected from Idealo, it uses advanced scraping techniques (Selenium and BeautifulSoup) to compare prices and details of products on Amazon. Users can configure specific filters, such as a minimum profit percentage and a minimum euro profit value. The extractor filters products that meet these criteria and stores relevant details, such as product name, prices, profit percentage, and links, in an Excel file. This function enables traders to identify efficiently and organizedly products that could offer more profitable business opportunities on Amazon.

# Running the Program

1. **Create a virtual environment:**
    - Linux/Mac: **`python3 -m venv venv`**
    - Windows: **`python -m venv venv`**
2. **Activate the virtual environment:**
    - Linux/Mac: **`source venv/bin/activate`**
    - Windows: **`venv\Scripts\activate`**
3. **Install the libraries:**
    - Run **`pip install -r requirements.txt`**
4. **Execute `index.py` to update the list of URLs with all products (`products.txt`):**
    - **`python index.py`**
5. **Once the list of products is obtained, run `get_products.py` to start analyzing all products:**
    - **`python get_products.py`**
6. **Let the magic happen; you can observe the Excel file `products.xlsx` updating in real-time.**
