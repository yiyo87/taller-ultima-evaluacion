"""webtaller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from elcedroapp.views import index,crear_pedido,listar_pedidos,eliminar_pedido,actualizar_pedido,productos,certificados,galeria,sobreNosotros

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('productos/',productos, name='productos'),
    path('certificados/',certificados, name='certificados'),
    path('galeria/',galeria, name='galeria'),
    path('sobrenosotros/',sobreNosotros, name='sobrenosotros'),
    path('registrar-pedido',crear_pedido,name='registrar-pedido'),
    path('listar-pedidos/', listar_pedidos, name='listar-pedidos'),
    path('actualizar/<int:pedido_id>/', actualizar_pedido, name='actualizar-pedido'),
    path('eliminar/<int:pedido_id>/', eliminar_pedido, name='eliminar-pedido'),
    
]
