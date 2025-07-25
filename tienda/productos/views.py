from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required(login_url='usuarios:login')
def inicio_view(request):
    productos_destacados = Producto.objects.filter(destacado=True)
    categorias = Categoria.objects.all()
    return render(request, 'tienda/inicio.html', {
        'productos': productos_destacados,
        'categorias': categorias,
        'categoria_actual': None
    })

def productos_por_categoria(request, categoria_id):
    productos = Producto.objects.filter(categoria_id=categoria_id)
    categorias = Categoria.objects.all()
    categoria_actual = Categoria.objects.get(id=categoria_id).nombre

    return render(request, 'tienda/inicio.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_actual': categoria_actual,
    })


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)] += 1
    else:
        carrito[str(producto_id)] = 1

    request.session['carrito'] = carrito
    return redirect('tienda:inicio')


def ver_carrito(request):
    carrito =request.session.get('carrito', {})
    productos = []
    total = 0 
    
    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        producto.total = producto.precio * cantidad
        producto.cantidad = cantidad
        producto.append = (producto,)
        total += producto.total
        
        return render(request, 'tienda/carrito.html', {'productos': productos, 'total': total})
    
def eliminar_del_carrito(request, producto_id):
    carrito= request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        messages.warning(request, 'Producto eliminado del carrito.') 
    return redirect('tienda:ver_carrito')

def carrito_view(request):
    carrito = request.session.get('carrito', {})
    productos_en_carrito = []
    total = 0

    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id)
            subtotal = producto.precio * cantidad
            productos_en_carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal
        except Producto.DoesNotExist:
            pass  # Ignora si el producto ya no existe

    return render(request, 'tienda/carrito.html', {
        'productos_en_carrito': productos_en_carrito,
        'total': total
    })
    
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'tienda/detalle_producto.html', {'producto': producto})


def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito

    return redirect('tienda:ver_carrito')



def buscar_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(
        Q(nombre__icontains=query) | Q(descripcion__icontains=query)
    ) if query else Producto.objects.none()

    categorias = Categoria.objects.all()
    return render(request, 'tienda/busqueda.html', {
        'resultados': productos,
        'query': query,
        'categorias': categorias
    })

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if producto.stock > 0:

        carrito = request.session.get('carrito', {})
        carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
        request.session['carrito'] = carrito

        # Reducir el stock por si llego a comprar, o si lo agrego al carrito
        
        producto.save()

        messages.success(request, f"{producto.nombre} agregado al carrito.")
    else:
        messages.error(request, "Este producto está agotado.")

    return redirect('tienda:inicio')  

from .models import Pedido, DetallePedido

@login_required(login_url='usuarios:login')
def realizar_compra(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('tienda:inicio')

    total = 0
    detalles = []

    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        
        if producto.stock < cantidad:
            messages.error(request, f"No hay suficiente stock para {producto.nombre}.")
            return redirect('tienda:ver_carrito')

        subtotal = producto.precio * cantidad
        total += subtotal
        detalles.append((producto, cantidad, producto.precio))

    pedido = Pedido.objects.create(usuario=request.user, total=total)

    for producto, cantidad, precio in detalles:
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio
        )
        producto.stock -= cantidad
        producto.save()

    request.session['carrito'] = {}  # Vaciar carrito
    messages.success(request, f'Compra realizada correctamente. Pedido #{pedido.id}')
    return redirect('tienda:inicio')