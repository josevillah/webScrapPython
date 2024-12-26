import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class ScrapData:
    def __init__(self, url='https://www.wrangler.cl/jeans-hombre-texas-regular-fit-stonewash/p', driver=None, categoria=''):
        self.url = url
        self.driver = driver
        self.categoria = categoria
        self.base_url = self.url.split("/")[0] + "//" + self.url.split("/")[2]

    def descargar_imagen(self, link_img, nombre_archivo):
        """
        Descarga una imagen desde un enlace asegurándose de que sea de tamaño original.
        """
        # Ruta de la carpeta Descargas/categoria
        carpeta_descargas = "Descargas"
        carpeta_categoria = os.path.join(carpeta_descargas, self.categoria)

        # Verificar si la carpeta "Descargas" existe, si no, crearla
        if not os.path.exists(carpeta_descargas):
            os.makedirs(carpeta_descargas)
            print(f'Carpeta "{carpeta_descargas}" creada.')

        # Verificar si la carpeta "Descargas/categoria" existe, si no, crearla
        if not os.path.exists(carpeta_categoria):
            os.makedirs(carpeta_categoria)
            print(f'Carpeta "{carpeta_categoria}" creada.')

        # Ruta completa del archivo
        ruta_archivo = os.path.join(carpeta_categoria, nombre_archivo)

        try:
            # Hacer la solicitud GET para obtener la imagen
            response = requests.get(link_img, stream=True)
            if response.status_code == 200:
                # Verificar si el tamaño original está disponible en los headers
                content_type = response.headers.get('Content-Type', '')
                if 'image' in content_type:
                    # Guardar la imagen
                    with open(ruta_archivo, 'wb') as file:
                        for chunk in response.iter_content(1024):  # Leer en bloques de 1 KB
                            file.write(chunk)
                    print(f'Imagen descargada correctamente en {ruta_archivo}')
                else:
                    print('El enlace proporcionado no parece ser una imagen.')
            else:
                print(f'Error al descargar la imagen. Estado: {response.status_code}')
        except Exception as e:
            print(f'Ocurrió un error al descargar la imagen: {e}')

    def get_data(self):
        try:
            self.driver.get(self.url)

            if self.base_url == 'https://www.wrangler.cl':
                # Extraer el nombre del producto
                nombre_modificado = 'Nombre no encontrado'
                nombre_element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//h3[contains(@class, "wranglercl-complement-name-0-x-productName--pdp-product-name")]'))
                )
                if nombre_element:
                    nombre = nombre_element.text
                    nombre_modificado = nombre.split(' ')[0] + ' ' + ' '.join(
                        [palabra.lower() for palabra in nombre.split(' ')[1:]]
                    )

                # Extraer el código del producto
                codigo_extraido = 'Código no encontrado'
                codigo_element = self.driver.find_element(
                    By.XPATH, '//div[contains(@class, "wranglercl-complement-name-0-x-container_identifier")]/p[contains(@class, "wranglercl-complement-name-0-x-identifier--pdp-product-identifier")]'
                )
                if codigo_element:
                    codigo = codigo_element.text.strip()
                    codigo_extraido = codigo.split(" / ")[-1]

                # Descargar la imagen
                link_img = 'Imagen no encontrada'
                img_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//img[contains(@class, "vtex-store-components-3-x-productImageTag")]'))
                )
                if img_element:
                    link_img = img_element.get_attribute('src')
                    print(link_img)
                    self.descargar_imagen(link_img, f'{codigo_extraido}.jpg')


            if self.base_url == 'https://www.leejeans.cl':

                # Extraer el nombre del producto
                nombre_modificado = 'Nombre no encontrado'
                nombre_element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//h3[contains(@class, "leejeanscl-complement-name-0-x-productName leejeanscl-complement-name-0-x-productName--pdp-product-name")]'))
                )
                if nombre_element:
                    nombre = nombre_element.text
                    nombre_modificado = nombre.split(' ')[0] + ' ' + ' '.join(
                        [palabra.lower() for palabra in nombre.split(' ')[1:]]
                    )

                # Extraer el código del producto
                codigo_extraido = 'Código no encontrado'
                codigo_element = self.driver.find_element(
                    By.XPATH, '//p[contains(@class, "leejeanscl-complement-name-0-x-identifier--pdp-product-identifier")]'
                )
                if codigo_element:
                    codigo = codigo_element.text.strip()
                    codigo_extraido = codigo.split(" / ")[-1]

                
                # Descargar la imagen
                link_img = 'Imagen no encontrada'
                img_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//img[contains(@class, "vtex-store-components-3-x-thumbImg vtex-store-components-3-x-thumbImg--pdp-dektop-product-images w-100 h-auto db")]'))
                )
                if img_element:
                    link_img = img_element.get_attribute('src')
                    self.descargar_imagen(link_img, f'{codigo_extraido}.jpg')


            return [codigo_extraido, nombre_modificado]


        except Exception as e:
            print(f"Error en el método get_data: {e}")
            return ['Código no encontrado', 'Nombre no encontrado']
