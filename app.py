import json

total = 0

with open('json/productos.json', 'r') as file:
    data = json.load(file)
    i = 1
    for line in data:
        print(f"{i} {line['name']}")
        i += 1
        #total += int(line['price'])
    prod_selec = int(input("seleccione un producto de la lista:"))    
    #print(total)

    if prod_selec in data:
        print(prod_selec['price'])

# ingreso los datos del nuevo producto
producto = input("ingrese producto: ")
precio = input("ingrese precio: ")
nuevo = {
    "name": producto,
    "price": precio
}

#agrego el nuevo producto a la lista
data.append(nuevo)

#Escribo el archivo
with open('json/productos.json', 'w') as file:
    json.dump(data, file, indent=4)