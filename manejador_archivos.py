import json

def abrir_archivo():
    """Funcion utilizada para abrir el archivo de comidas"""
    with open('json/comidas.json', 'r') as file:
        data = json.load(file)
    return data

def cargar_datos(data, producto_nuevo):
    """Permite agregar nuevos datos al archivo de comidas"""
    data.append(producto_nuevo)

    with open('json/comidas.json', 'w') as file:
        json.dump(data, file, indent=4)



#datos = abrir_archivo()
#
#print(datos)
#
#nuevo = {
#    "name": "Cokita",
#    "price": 200
#}
#
#
#cargar_datos(datos, nuevo)
#print(datos)
