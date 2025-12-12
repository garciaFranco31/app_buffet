class Venta:
    
    def __init__(self, titulo):
        self.titulo = titulo
        self.productos = []
        self.total = 0
        self.tipo_pago = ""


    def registrar_venta(self,producto):
        """Permite agregar productos a una venta"""
        self.productos.extend(producto)

    def total_venta(self):
        """Devuelve el total a pagar"""
        for prod in self.productos:
            print(prod)
            #self.total += prod["price"]
        #print(self.total)
    
    def pago_venta(self, tipo_pago):
        """Se guarda el método de pago de la venta"""
        self.tipo_pago = tipo_pago
        print(tipo_pago)


#venta1 = Venta("venta1")
#print(venta1.productos)
#
#prods = [
#    {
#        "id":1,
#        "nombre": "cono de papas",
#        "precio": 200
#    },
#    {
#        "nombre": "pancho",
#        "precio": 100
#    }
#]
#
#venta1.registrar_venta(prods)
#print(venta1.productos)
#
#venta1.total_venta()