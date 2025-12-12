class Venta:
    
    def __init__(self, titulo):
        self.titulo = titulo
        self.productos = []
        self.total = 0
        self.tipo_pago = ""


    def registrar_venta(self,producto):
        self.productos.extend(producto)

    def total_venta(self):
        for prod in self.productos:
            print(prod['precio'])
            self.total += prod["precio"]
        print(self.total)
    
    def pago_venta(self, tipo_pago):
        self.tipo_pago = tipo_pago


venta1 = Venta("venta1")
print(venta1.productos)

prods = [
    {
        "nombre": "cono de papas",
        "precio": 200
    },
    {
        "nombre": "pancho",
        "precio": 100
    }
]

venta1.registrar_venta(prods)
print(venta1.productos)

venta1.total_venta()