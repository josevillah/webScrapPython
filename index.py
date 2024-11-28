from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime

from scrapdata import ScrapData

class Index:
    def __init__(self, ruta, ws):
        # URL base de las páginas de productos
        self.ruta = ruta
        # Hoja activa de Excel compartida
        self.ws = ws
        # Configuración de Selenium WebDriver
        self.driver = webdriver.Chrome()  # Asegúrate de tener el ChromeDriver instalado
        self.arrayLinks = []

    # Procesar los datos de los productos y agregar al archivo Excel
    def process_data(self):
        categoria = self.ruta.split('/')[3].split('?')[0]

        for i in range(0, len(self.arrayLinks)):  # Iterar sobre los enlaces recopilados
            scrapData = ScrapData(self.arrayLinks[i], self.driver, categoria)  # Crear la instancia de ScrapData
            data = scrapData.get_data()

            if data and len(data) >= 2 and data[0] and data[1]:
                # Agregar los datos a la hoja Excel compartida
                self.ws.append([data[0], data[1], categoria])
            else:
                print(f"Datos inválidos o incompletos para el enlace: {self.arrayLinks[i]}")

    # Obtener los datos de los productos de la página
    def get_data(self, soup):
        # Buscar los contenedores de productos
        products = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')

        for product in products:
            link = product.find('a', class_='vtex-product-summary-2-x-clearLink')['href']
            finishLink = f'https://www.wrangler.cl{link}'

            if finishLink not in self.arrayLinks:
                self.arrayLinks.append(finishLink)

    # Navegar por las páginas de productos
    def numberPages(self):
        for i in range(1, 100):  # Ajusta el rango de páginas que deseas cargar
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
        
        self.process_data()

    def close_driver(self):
        # Cerrar el navegador después de terminar
        self.driver.quit()

# Registrar el tiempo de inicio
horaStart = datetime.now()
print(f'Proceso Iniciado a las {horaStart}')

# Crear un archivo Excel único
wb = Workbook()
ws = wb.active
ws.title = "Productos"

# Escribir los encabezados en la primera fila
ws.append(["Código", "Nombre", "Categoría"])

# Lista de URLs a procesar
listRuta = [
    'https://www.wrangler.cl/hombre?layout=option_4_items&order=OrderByReleaseDateDESC&page=',
    'https://www.wrangler.cl/mujer?layout=option_4_items&order=OrderByReleaseDateDESC&page=',
]

# Iterar sobre cada URL en la lista y ejecutar el proceso
for ruta in listRuta:
    index = Index(ruta, ws)  # Pasar la hoja activa como parámetro
    index.numberPages()  # Cargar las páginas y procesar los datos
    index.arrayLinks = []  # Limpiar la lista de enlaces

index.close_driver()  # Cerrar el navegador después de procesar

# Guardar el archivo Excel único
fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
archivo_excel = f'Productos_combinados_{fecha_hora_actual}.xlsx'
wb.save(archivo_excel)

# Registrar el tiempo de finalización
horaEnd = datetime.now()
print(f'Proceso completado a las {horaEnd}')

# Calcular la duración del proceso
timeDifference = horaEnd - horaStart
hours = timeDifference.seconds // 3600
minutes = (timeDifference.seconds % 3600) // 60
seconds = timeDifference.seconds % 60

print(f'Duración del proceso: {hours} horas, {minutes} minutos, {seconds} segundos')
print(f'Datos guardados en el archivo: {archivo_excel}')