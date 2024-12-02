from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from django.contrib import messages
from datetime import datetime
import re

def index(request):
    """
    Renderiza la página de inicio.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Respuesta con la plantilla de la página de inicio.
    """
    return render(request, 'elcedroapp/index.html')

def productos(request):
    """
    Renderiza la página de productos.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Respuesta con la plantilla de la página de productos.
    """
    return render(request, 'elcedroapp/productos.html')

def certificados(request):
    """
    Renderiza la página de certificados.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Respuesta con la plantilla de la página de certificados.
    """
    return render(request, 'elcedroapp/certificados.html')

def galeria(request):
    """
    Renderiza la página de galería.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Respuesta con la plantilla de la página de galería.
    """
    return render(request, 'elcedroapp/galeria.html')

def sobreNosotros(request):
    """
    Renderiza la página de información "Sobre Nosotros".

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Respuesta con la plantilla de la página "Sobre Nosotros".
    """
    return render(request, 'elcedroapp/sobrenosotros.html')

def crear_pedido(request):
    """
    Crea un nuevo pedido a partir de los datos enviados por el usuario.

    Valida los datos del formulario y los inserta en la base de datos.
    Si hay errores de validación, muestra mensajes al usuario.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la página del formulario en caso de error o redirige a la lista de pedidos.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        numero = request.POST.get('numero', '').strip()
        cantidad = request.POST.get('cantidad_bidones', '').strip()
        fecha = request.POST.get('fecha', '').strip()

        errores = []

        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            errores.append("El nombre no puede contener números ni caracteres especiales.")

        if not numero.isdigit() or len(numero) != 9:
            errores.append("El número debe contener exactamente 9 dígitos.")

        try:
            fecha_ingresada = datetime.strptime(fecha, "%Y-%m-%d")
            if fecha_ingresada.date() < datetime.now().date():
                errores.append("La fecha no puede ser anterior al día actual.")
        except ValueError:
            errores.append("El formato de la fecha es inválido.")

        if not cantidad.isdigit() or int(cantidad) <= 0:
            errores.append("La cantidad debe ser un número entero positivo.")

        if errores:
            for error in errores:
                messages.error(request, error)
            return render(request, 'elcedroapp/registrar.html', {
                'nombre': nombre,
                'direccion': direccion,
                'numero': numero,
                'cantidad_bidones': cantidad,
                'fecha': fecha,
            })

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Pedido (nombre, direccion, numero, cantidad_bidones, fecha) VALUES (%s, %s, %s, %s, %s)",
                [nombre, direccion, numero, cantidad, fecha]
            )
        messages.success(request, "Pedido registrado exitosamente.")
        return redirect(to='listar-pedidos')

    return render(request, 'elcedroapp/registrar.html')

def listar_pedidos(request):
    """
    Recupera y muestra todos los pedidos almacenados en la base de datos.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Respuesta con la plantilla de la lista de pedidos y los datos correspondientes.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Pedido")
        pedidos = cursor.fetchall()
    return render(request, 'elcedroapp/listar_pedidos.html', {'pedidos': pedidos})

def actualizar_pedido(request, pedido_id):
    """
    Actualiza un pedido existente en la base de datos.

    Muestra los datos actuales en un formulario, y guarda los cambios realizados por el usuario.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        pedido_id (int): ID del pedido a actualizar.

    Returns:
        HttpResponse: Renderiza el formulario con los datos existentes o redirige a la lista de pedidos tras actualizar.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Pedido WHERE id_pedido = %s", [pedido_id])
        pedido = cursor.fetchone()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        numero = request.POST.get('numero')
        cantidad = request.POST.get('cantidad_bidones')
        fecha = request.POST.get('fecha')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Pedido 
                SET nombre = %s, direccion = %s, numero = %s, cantidad_bidones = %s, fecha = %s
                WHERE id_pedido = %s
            """, [nombre, direccion, numero, cantidad, fecha, pedido_id])

        return redirect(to='listar-pedidos')

    return render(request, 'elcedroapp/actualizar_pedido.html', {'pedido': pedido})

def eliminar_pedido(request, pedido_id):
    """
    Elimina un pedido de la base de datos.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        pedido_id (int): ID del pedido a eliminar.

    Returns:
        HttpResponse: Redirige a la lista de pedidos tras eliminar el registro.
    """
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Pedido WHERE id_pedido = %s", [pedido_id])
    return redirect(to='listar-pedidos')
