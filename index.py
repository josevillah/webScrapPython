from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class Index:
    def __init__(self):
        # URL base de las páginas de productos
        self.ruta = 'https://www.wrangler.cl/mujer?layout=option_4_items&order=OrderByReleaseDateDESC&page='
        # Configuración de Selenium WebDriver
        self.driver = webdriver.Chrome()  # Asegúrate de tener el ChromeDriver instalado

    def get_data(self, soup):
        # Buscar los contenedores de productos
        products = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')
        print(f"Se encontraron {len(products)} productos.")
        # Imprimir los productos encontrados (puedes extraer más información si lo deseas)
        for product in products:
            link = product.find('a', class_='vtex-product-summary-2-x-clearLink')['href']
            finishLink = f'https://www.wrangler.cl{link}'
            print(finishLink)

    def numberPages(self):
        for i in range(1, 20):  # Ajusta el rango de páginas que deseas cargar
            url = self.ruta + str(i)
            self.driver.get(url)
            
            try:
                # Esperar explícitamente a que los productos estén cargados en la página
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'vtex-search-result-3-x-galleryItem'))
                )

                # Obtener el HTML de la página cargada
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                self.get_data(soup)
            except Exception as e:
                print(f"Error al cargar la página {i}: {e}")
                break

    def close_driver(self):
        # Cerrar el navegador después de terminar
        self.driver.quit()

# Crear instancia y ejecutar
index = Index()
index.numberPages()
index.close_driver()