import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class ScrapData:
    def __init__(self, url='https://www.wrangler.cl/jeans-hombre-texas-regular-fit-stonewash/p'):
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


    def descargar_imagen(self, link_img, nombre_archivo):
        # Verificar si la carpeta "Descargas" existe, si no, crearla
        carpeta_descargas = "Descargas"
        if not os.path.exists(carpeta_descargas):
            os.makedirs(carpeta_descargas)
            print(f'Carpeta "{carpeta_descargas}" creada.')

        # Crear la ruta completa del archivo
        ruta_archivo = os.path.join(carpeta_descargas, nombre_archivo)

        try:
            # Realizar la solicitud para obtener el contenido de la imagen
            response = requests.get(link_img)
            
            # Verificar si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Guardar la imagen en el directorio "Descargas"
                with open(ruta_archivo, 'wb') as file:
                    file.write(response.content)
                print(f'Imagen descargada correctamente en {ruta_archivo}')
            else:
                print(f'Error al descargar la imagen. Estado: {response.status_code}')
        
        except Exception as e:
            print(f'Ocurrió un error al descargar la imagen: {e}')


    def get_data(self):
        self.driver.get(self.url)

        try:
            # Esperar a que el nombre del producto esté visible (usando XPath)
            nombre_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//h3[contains(@class, "wranglercl-complement-name-0-x-productName--pdp-product-name")]'))
            )
            
            # Extraer el nombre del producto
            nombre = nombre_element.text
            nombre_modificado = nombre.split(' ')[0] + ' ' + ' '.join([palabra.lower() for palabra in nombre.split(' ')[1:]])

            # Extraer el código del producto usando el XPath correcto
            codigo_element = self.driver.find_element(By.XPATH, '//div[contains(@class, "wranglercl-complement-name-0-x-container_identifier")]/p[contains(@class, "wranglercl-complement-name-0-x-identifier--pdp-product-identifier")]')
            codigo = codigo_element.text.strip() if codigo_element else 'Código no encontrado'
            codigo_extraido = codigo.split(" / ")[-1]  # Dividimos la cadena por " / " y tomamos la segunda parte
            
            
            # Esperar a que la imagen esté presente en el DOM
            img_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//img[contains(@class, "vtex-store-components-3-x-productImageTag")]'))
            )
            link_img = img_element.get_attribute('src') if img_element else 'Imagen no encontrada'
            
            # Descargar la imagen
            self.descargar_imagen(link_img, f'{codigo_extraido}.jpg')
            
            return [codigo_extraido, nombre_modificado]

            

        except Exception as e:
            print(f'Error al extraer datos: {e}')
        finally:
            self.driver.quit()