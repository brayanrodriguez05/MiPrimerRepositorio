# Módulo del sistema hotelero
from datetime import datetime, date
from comun import datos, guardar, texto, entero, decimal, fecha, confirmar, buscar, nueva_id


def obtener_habitacion():
    numero = entero('Número de habitación: ')
    habitacion = buscar(datos['habitaciones'], 'numero', numero)
    if habitacion is None:
        print('Habitación no registrada.')
    return habitacion


def registrar_habitacion():
    print('\n--- REGISTRAR HABITACIÓN ---')
    numero = entero('Número: ')
    if buscar(datos['habitaciones'], 'numero', numero):
        print('Ya existe ese número de habitación.')
        return
    tipo = texto('Tipo (individual, doble, suite, etc.): ')
    capacidad = entero('Capacidad de personas: ')
    precio = decimal('Precio por noche (Q): ', 0.01)
    datos['habitaciones'].append({'numero': numero, 'tipo': tipo,
                                  'capacidad': capacidad, 'precio': precio})
    if guardar():
        print('Habitación registrada.')


def modificar_habitacion():
    print('\n--- MODIFICAR HABITACIÓN ---')
    habitacion = obtener_habitacion()
    if habitacion is None:
        return
    print('1. Tipo  2. Capacidad  3. Precio')
    opcion = entero('Seleccione: ')
    if opcion == 1:
        habitacion['tipo'] = texto('Nuevo tipo: ')
    elif opcion == 2:
        nueva = entero('Nueva capacidad: ')
        for reserva in datos['reservas']:
            if reserva['habitacion'] == habitacion['numero'] and reserva['estado'] in ('Reservada', 'Ocupada'):
                if reserva['personas'] > nueva:
                    print('No puede reducir la capacidad: hay una reserva con más personas.')
                    return
        habitacion['capacidad'] = nueva
    elif opcion == 3:
        habitacion['precio'] = decimal('Nuevo precio (Q): ', 0.01)
        print('El nuevo precio aplicará a futuras reservaciones.')
    else:
        print('Opción inválida.')
        return
    if guardar():
        print('Habitación modificada.')


def disponible(numero, inicio, fin, excluir_id=0):
    for reserva in datos['reservas']:
        if reserva['id'] == excluir_id or reserva['habitacion'] != numero:
            continue
        if reserva['estado'] not in ('Reservada', 'Ocupada'):
            continue
        inicio_existente = date.fromisoformat(reserva['entrada'])
        fin_existente = date.fromisoformat(reserva['salida'])
        if inicio < fin_existente and fin > inicio_existente:
            return False
    return True


def pedir_periodo():
    while True:
        inicio = fecha('Fecha de entrada (DD/MM/AAAA): ')
        fin = fecha('Fecha de salida (DD/MM/AAAA): ')
        if inicio < date.today():
            print('La entrada no puede ser anterior a hoy.')
        elif fin <= inicio:
            print('La salida debe ser posterior a la entrada.')
        else:
            return inicio, fin


def consultar_disponibilidad():
    print('\n--- DISPONIBILIDAD ---')
    inicio, fin = pedir_periodo()
    personas = entero('Cantidad de personas: ')
    encontrados = 0
    for habitacion in datos['habitaciones']:
        if habitacion['capacidad'] >= personas and disponible(habitacion['numero'], inicio, fin):
            print('Habitación:', habitacion['numero'], '| Tipo:', habitacion['tipo'],
                  '| Capacidad:', habitacion['capacidad'], '| Q', habitacion['precio'], 'por noche')
            encontrados += 1
    if encontrados == 0:
        print('No hay habitaciones disponibles para esas fechas y capacidad.')