from django.test import TestCase
from django.urls import reverse
from django.db import connection
from elcedroapp.models import Pedido
from django.core.management import call_command
from django.shortcuts import redirect, render
from django.test import TestCase
from elcedroapp.models import Pedido
class PedidoTestCase(TestCase):
    def setUp(self):
        # Crea un pedido inicial para pruebas usando el modelo Django
        Pedido.objects.create(
            nombre="ignacio diocare",
            direccion="nuevo mundo 1771",
            numero="123456789",
            cantidad_bidones=2,
        )
    def test_pedido_creation(self):
        # Verifica que el pedido fue creado correctamente
        pedido = Pedido.objects.get(nombre="ignacio diocare")
        print("Resultado test creado")
        print("Nombre:", pedido.nombre)
        print("Direccion:", pedido.direccion)
        print("Numero:", pedido.numero)
        print("Cantidad de Bidones:", pedido.cantidad_bidones)
        self.assertEqual(pedido.nombre, "ignacio diocare")
    def test_pedido_retrieve(self):
        # Recupera y verifica la información de un pedido existente
        pedido = Pedido.objects.get(nombre="ignacio diocare")
        print("Resultado test mostrar")
        print("Nombre:", pedido.nombre)
        print("Direccion:", pedido.direccion)
        print("Numero:", pedido.numero)
        print("Cantidad de Bidones:", pedido.cantidad_bidones)
        self.assertEqual(pedido.nombre, "ignacio diocare")
        self.assertEqual(pedido.direccion, "nuevo mundo 1771")
        self.assertEqual(pedido.numero, "123456789")
        self.assertEqual(pedido.cantidad_bidones, 2)
    def test_pedido_update(self):
        # Actualiza un pedido existente
        pedido = Pedido.objects.get(nombre="ignacio diocare")
        pedido.direccion = "calle renovada 2024"
        pedido.cantidad_bidones = 5
        pedido.save()

        # Recupera el pedido actualizado y verifica los cambios
        pedido_actualizado = Pedido.objects.get(nombre="ignacio diocare")
        print("Resultado test actualizar")
        print("Direccion actualizada:", pedido_actualizado.direccion)
        print("Cantidad de Bidones actualizada:", pedido_actualizado.cantidad_bidones)
        self.assertEqual(pedido_actualizado.direccion, "calle renovada 2024")
        self.assertEqual(pedido_actualizado.cantidad_bidones, 5)
    def test_pedido_delete(self):
        # Elimina un pedido existente
        pedido = Pedido.objects.get(nombre="ignacio diocare")
        pedido.delete()

        # Verifica que el pedido ya no existe
        pedidos = Pedido.objects.filter(nombre="ignacio diocare")
        print("Resultado test eliminar")
        print("Pedidos restantes con ese nombre:", pedidos.count())
        self.assertEqual(pedidos.count(), 0)
    
    
    #verifica que se envian registro a la base de datos a traves de un formulario con los datos de clauss 
    #tambien se considera como prueba del sistema ya que se esta intereactuando o mejor dicho validando un pedido ingresado a traves de uin formulario esto verifica la integracion entre varias partes del sistema
    def test_form_submission_success(self):
        form_data = {
            'nombre': 'clauss morgendofer',
            'direccion': 'padre avelino 8888',
            'numero': '123456789',
            'cantidad_bidones': 2,
        }
        self.client.post(reverse('registrar-pedido'), data=form_data)
        pedido = Pedido.objects.filter(nombre='clauss morgendofer').first()
        self.assertIsNotNone(pedido)
        self.assertEqual(pedido.direccion, 'padre avelino 8888')
        self.assertEqual(pedido.cantidad_bidones, 2)
    
    #funcion para poder crear tambien un registro dentro de la base de datos pero con datos distintos y verificar que se pueden ingresar usuarios distintos
    def test_verificar_registro(self):
        form_data = {
            'nombre': 'Juan Pérez',
            'direccion': 'Calle Falsa 123',
            'numero': '987654321',
            'cantidad_bidones': 3,
        }
        self.client.post(reverse('registrar-pedido'), data=form_data)
        pedido = Pedido.objects.filter(nombre='Juan Pérez').first()
        self.assertIsNotNone(pedido)  # Verifica que no sea None
        self.assertEqual(pedido.direccion, 'Calle Falsa 123')
        self.assertEqual(pedido.cantidad_bidones, 3)
        print(f"Registro creado: Nombre={pedido.nombre}, Dirección={pedido.direccion}")