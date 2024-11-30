from openpyxl import load_workbook

from connection import Connection

class ExcelReader:
    def __init__(self):
        self.workbook = None

    def load_file(self, file_name):
        """
        Carga el archivo Excel.
        """
        try:
            self.workbook = load_workbook(file_name)
            print(f"Archivo '{file_name}' cargado correctamente.")
        except FileNotFoundError:
            print(f"El archivo '{file_name}' no fue encontrado.")
        except Exception as e:
            print(f"Ocurrió un error al cargar el archivo: {e}")

    def read_sheet(self, sheet_name):
        """
        Lee los datos de una hoja específica.
        """
        if not self.workbook:
            print("El archivo no está cargado.")
            return None

        try:
            sheet = self.workbook[sheet_name]
            data = []
            for row in sheet.iter_rows(values_only=True):
                data.append(row)
            return data
        except KeyError:
            print(f"La hoja '{sheet_name}' no existe en el archivo.")
            return None
        except Exception as e:
            print(f"Error al leer la hoja: {e}")
            return None


    def insertData(self, data):
        connet = Connection()
        connet.connect()
        query = "SELECT id FROM productos order by id desc limit 1"
        id = connet.execute_query(query)[0][0]+1
        if(id):
            for row in data:
                print(row)
                query = f"INSERT INTO productos (id, codpro, nompro, prepro, idsubcat, oculto, fecharegistro, urlimagen, medida, cantidad, agregarCarrito) VALUES({id}, '{row[0]}', '{row[1]}', '{row[4]}', '{row[2]}', '{row[3]}', '{row[5]}')"
                print(query)
                break
                id += 1
                # connet.execute_query(query)
        connet.close()


# Instanciar el lector de Excel
reader = ExcelReader()

# Cargar el archivo de datos original
reader.load_file("./db.xlsx")
data = reader.read_sheet("Productos")

# Cargar el archivo de información combinada
reader.load_file("./Productos_combinados_2024-11-28_16-46-35.xlsx")
info = reader.read_sheet("Productos")

# Lista para guardar los resultados
arrayToInsert = []

if data:
    for row in data:
        if len(row) > 3 and (row[3] == 'ROPA HOMBRE' or row[3] == 'ROPA MUJER'):
            for row2 in info:
                if str(row[0]).strip() == str(row2[0]).strip():

                    if(row[3] == 'ROPA HOMBRE'):
                        idsubcat = 73
                    if(row[3] == 'ROPA MUJER'):
                        idsubcat = 74
                    
                    if(row[5] > 1):
                        stock = 1
                    else:
                        stock = 0

                    arrayToInsert.append(
                        [row[0], row2[1], row[4], idsubcat, stock]
                    )


excel = ExcelReader()

excel.insertData(arrayToInsert)