import json
from venta import Venta
from manejador_archivos import abrir_archivo, cargar_datos

total = 0
venta = Venta("venta2")

data = abrir_archivo()

# Lógica para cargar productos a una venta
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
            print(prod["price"])
            venta.registrar_venta(prod)
            #total += int(prod["price"])

    if prod_selec == 0:
        ok = True
#print(venta.total_venta())
venta.total_venta()


#Selecciona el método de pago y lo guarda en la variable del obj
print("Seleccione el método de pago:")
print("1. Transferencia")
print("2.Efectivo")
metodo_pago = int(input())

if (metodo_pago == 1):
    opc_seleccionada = "Transferencia"
elif (metodo_pago == 2):
    opc_seleccionada = "Efectivo"
    
venta.pago_venta(opc_seleccionada)

