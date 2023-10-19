from django.shortcuts import get_object_or_404, redirect, render
from .models import Evento, Usuario, RegistroEvento
from .forms import EventoForm, UsuarioForm, RegistroEventoForm
from datetime import datetime
from django.db.models import Count

def eventos_por_mes(request):
    if request.method == 'GET':
        selected_month = request.GET.get('mes')
        selected_year = request.GET.get('anio')
        if selected_month and selected_year:
            # Filtra los eventos por mes y año seleccionados
            eventos = Evento.objects.filter(fecha__month=selected_month, fecha__year=selected_year)
        else:
            # Si no se selecciona un mes y año, muestra todos los eventos
            eventos = Evento.objects.all()

        return render(request, 'template.html', {'eventos': eventos})
    


def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_eventos') 
    else:
        form = EventoForm()
    return render(request, 'crear_evento.html', {'form': form})

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})

def crear_registro_evento(request):
    if request.method == 'POST':
        form = RegistroEventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_registros_evento') 
    else:
        form = RegistroEventoForm()
    return render(request, 'crear_registro_evento.html', {'form': form})

def contar_usuarios_por_evento(evento_id):
    return RegistroEvento.objects.filter(evento__id=evento_id).count()




def lista_eventos(request):
    # Obtén los años únicos de tus eventos desde la base de datos
    years = Evento.objects.dates('fecha', 'year', order='DESC')

    selected_month = request.GET.get('mes')
    selected_year = request.GET.get('anio')

    if selected_month and selected_year:
        # Filtra eventos por mes y año seleccionados
        eventos = Evento.objects.filter(fecha__month=selected_month, fecha__year=selected_year).order_by('evento')[:6]
    else:
        # Si no se selecciona un mes y año, muestra los últimos 6 eventos sin filtrar
        eventos = Evento.objects.order_by('evento')[:6]

        # Si no se selecciona un año, establece el valor predeterminado como el primer año en la lista de años
        selected_year = years[0].year if years else None

    eventos_con_usuarios = []
    for evento in eventos:
        cantidad_usuarios = contar_usuarios_por_evento(evento.id)
        eventos_con_usuarios.append({'evento': evento, 'cantidad_usuarios': cantidad_usuarios})

    context = {
        'eventos': eventos,
        'eventos_con_usuarios': eventos_con_usuarios,
        'selected_month': selected_month,  # Esto es útil para mantener la opción seleccionada en el formulario
        'selected_year': int(selected_year) if selected_year else None,  # Esto es útil para mantener la opción seleccionada en el formulario
        'years': years  # Lista de años únicos para las opciones del campo de entrada del año
    }
    return render(request, 'lista_eventos.html', context)





def detalle_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    registros = RegistroEvento.objects.filter(evento=evento)
    return render(request, 'detalle_evento.html', {'evento': evento, 'registros': registros})




def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    # Realiza una consulta para contar los eventos registrados para cada usuario
    usuarios_con_eventos = Usuario.objects.annotate(num_eventos=Count('registroevento')).order_by('-num_eventos')
    # Recupera al usuario con más eventos registrados (el primero después de ordenar por num_eventos en orden descendente)
    usuario_con_mas_eventos = usuarios_con_eventos.first()

    # Renderiza el template para la lista de usuarios y pasa los datos
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios, 'usuario_con_mas_eventos': usuario_con_mas_eventos})



def lista_registros_evento(request):
    usuarios = Usuario.objects.all()
    usuario_id = request.GET.get('usuario_id')  # Obtén el ID del usuario seleccionado en el formulario
    selected_usuario = None
    registros_evento = RegistroEvento.objects.all()  # Obtén todos los registros de eventos por defecto

    if usuario_id:
        selected_usuario = Usuario.objects.get(id=usuario_id)
        registros_evento = RegistroEvento.objects.filter(usuario=selected_usuario)

    return render(request, 'lista_registros_evento.html', {'usuarios': usuarios, 'selected_usuario_id': int(usuario_id) 
                                                           if usuario_id else None, 'registros_evento': registros_evento})





def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('lista_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'editar_evento.html', {'form': form, 'evento': evento})

def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})

def editar_registro_evento(request, registro_id):
    registro = get_object_or_404(RegistroEvento, pk=registro_id)
    if request.method == 'POST':
        form = RegistroEventoForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('lista_registros_evento')
    else:
        form = RegistroEventoForm(instance=registro)
    return render(request, 'editar_registro_evento.html', {'form': form, 'registro': registro})

def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    evento.delete()
    return redirect('lista_eventos')

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    usuario.delete()
    return redirect('lista_usuarios')

def eliminar_registro_evento(request, registro_id):
    registro = get_object_or_404(RegistroEvento, pk=registro_id)
    registro.delete()
    return redirect('lista_registros_evento')

