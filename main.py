from bs4 import BeautifulSoup
from openpyxl import Workbook
from scrapdata import ScrapData

# Leer el archivo HTML local
with open('./wrangler.html', 'r', encoding='utf-8') as file:
    content = file.read()

# Crear un objeto BeautifulSoup para analizar el HTML
soup = BeautifulSoup(content, 'html.parser')

# Buscar los contenedores principales de los productos
productos = soup.find_all('div', class_='vtex-search-result-3-x-galleryItem')

arrayLinks = []
listaDatos = []

# Verificar si se encontraron productos
if not productos:
    print("No se encontraron productos.")
else:
    for prod in productos:
        # Extraer el enlace al producto
        link_a = prod.find('a', class_='vtex-product-summary-2-x-clearLink')
        link = link_a['href'] if link_a else "Enlace no disponible"
        
        # Ingresar los links en el array
        arrayLinks.append(link)

# Crear un archivo Excel
wb = Workbook()
ws = wb.active
ws.title = "Productos"

# Escribir los encabezados en la primera fila
ws.append(["Código", "Nombre"])

# Iterar sobre los enlaces y almacenar los datos en el archivo Excel
for i in range(0, len(arrayLinks)):  # Limitar a 2 iteraciones como ejemplo
    scrap = ScrapData(arrayLinks[i])  # Crear la instancia de ScrapData
    data = scrap.get_data()  # Llamar a get_data para obtener los datos
    
    # Agregar los datos del producto al archivo Excel
    if data:
        ws.append([data[0], data[1]])  # Agregar precio si disponible

# Guardar el archivo Excel
wb.save("productosMujeres.xlsx")
print("Datos guardados en 'productos.xlsx'")
