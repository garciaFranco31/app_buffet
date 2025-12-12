import json

total = 0

with open('json/comidas.json', 'r') as file:
    data = json.load(file)
    i = 1
    for line in data:
        print(f"{i} {line['name']}")
        i += 1
        #total += int(line['price'])
ok = False
print("Presione 0 para salir")
print(len(data))
while (not ok):    
    prod_selec = int(input("seleccione un producto de la lista:"))    
    #print(total)
    print(prod_selec)
    for prod in data:
        if prod_selec > 6:
            print("Producto invalido, seleccione uno nuevo")
            prod_selec = int(input("seleccione un producto de la lista:"))
        elif prod["id"] == prod_selec:
            #
            print(prod["price"])
            total += int(prod["price"])

    if prod_selec == 0:
        ok = True
print(total)
print("Seleccione el método de pago:")
print("1. Transferencia" \
"2.Efectivo")
metodo_pago = int(input())

if (metodo_pago == 1):
    opc_seleccionada = "Transferencia"
elif (metodo_pago == 2):
    opc_seleccionada = "Efectivo"


# ingreso los datos del nuevo producto
#producto = input("ingrese producto: ")
#precio = input("ingrese precio: ")
#nuevo = {
#    "name": producto,
#    "price": precio
#}
#
##agrego el nuevo producto a la lista
#data.append(nuevo)
#
##Escribo el archivo
#with open('json/comidas.json', 'w') as file:
#    json.dump(data, file, indent=4)