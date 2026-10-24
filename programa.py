# Módulo del sistema hotelero
from datetime import datetime, date
from comun import datos, guardar, texto, entero, decimal, fecha, confirmar, buscar, nueva_id


def obtener_reserva():
    numero = entero('ID de reservación: ')
    reserva = buscar(datos['reservas'], 'id', numero)
    if reserva is None:
        print('Reservación no encontrada.')
    return reserva


def crear_reserva():
    from clientes import obtener_huesped
    from habitaciones import disponible, obtener_habitacion, pedir_periodo
    from pagos import mostrar_costo
    print('\n--- CREAR RESERVACIÓN ---')
    huesped = obtener_huesped()
    if huesped is None:
        return
    inicio, fin = pedir_periodo()
    personas = entero('Cantidad de personas: ')
    habitacion = obtener_habitacion()
    if habitacion is None:
        return
    if personas > habitacion['capacidad']:
        print('La cantidad de personas supera la capacidad.')
        return
    if not disponible(habitacion['numero'], inicio, fin):
        print('La habitación ya está reservada u ocupada en ese período.')
        return
    descuento = decimal('Descuento (%) entre 0 y 100: ')
    if descuento > 100:
        print('Descuento inválido.')
        return
    reserva = {'id': nueva_id(datos['reservas']), 'documento': huesped['documento'],
               'habitacion': habitacion['numero'], 'entrada': inicio.isoformat(),
               'salida': fin.isoformat(), 'personas': personas,
               'precio_noche': habitacion['precio'], 'descuento': descuento,
               'cargos': [], 'pagos': [], 'estado': 'Reservada'}
    datos['reservas'].append(reserva)
    if guardar():
        print('Reservación creada con ID:', reserva['id'])
        mostrar_costo(reserva)


def modificar_reserva():
    from habitaciones import disponible, obtener_habitacion, pedir_periodo
    from pagos import mostrar_costo
    print('\n--- MODIFICAR RESERVACIÓN ---')
    reserva = obtener_reserva()
    if reserva is None:
        return
    if reserva['estado'] != 'Reservada':
        print('Solo se pueden modificar reservaciones en estado Reservada.')
        return
    if reserva['pagos']:
        print('No se pueden modificar fechas o habitación cuando existen pagos registrados.')
        return
    inicio, fin = pedir_periodo()
    personas = entero('Nueva cantidad de personas: ')
    habitacion = obtener_habitacion()
    if habitacion is None:
        return
    if personas > habitacion['capacidad']:
        print('La capacidad es insuficiente.')
        return
    if not disponible(habitacion['numero'], inicio, fin, reserva['id']):
        print('La habitación no está disponible.')
        return
    reserva['entrada'] = inicio.isoformat()
    reserva['salida'] = fin.isoformat()
    reserva['personas'] = personas
    reserva['habitacion'] = habitacion['numero']
    reserva['precio_noche'] = habitacion['precio']
    if guardar():
        print('Reservación modificada.')
        mostrar_costo(reserva)


def cancelar_reserva():
    print('\n--- CANCELAR RESERVACIÓN ---')
    reserva = obtener_reserva()
    if reserva is None:
        return
    if reserva['estado'] != 'Reservada':
        print('Solo se pueden cancelar reservaciones pendientes.')
        return
    if reserva['pagos']:
        print('La reservación tiene pagos. Resuelva el reembolso antes de cancelarla.')
        return
    if confirmar('¿Confirma la cancelación?'):
        reserva['estado'] = 'Cancelada'
        if guardar():
            print('Reservación cancelada.')


def registrar_entrada():
    print('\n--- REGISTRAR ENTRADA ---')
    reserva = obtener_reserva()
    if reserva is None:
        return
    if reserva['estado'] != 'Reservada':
        print('La reservación no está pendiente de entrada.')
    elif date.today() < date.fromisoformat(reserva['entrada']):
        print('Todavía no ha llegado la fecha de entrada.')
    elif date.today() >= date.fromisoformat(reserva['salida']):
        print('La fecha de salida ya pasó. Modifique la reservación.')
    else:
        reserva['estado'] = 'Ocupada'
        if guardar():
            print('Entrada registrada.')


def registrar_salida():
    from pagos import costo, mostrar_costo
    print('\n--- REGISTRAR SALIDA ---')
    reserva = obtener_reserva()
    if reserva is None:
        return
    if reserva['estado'] != 'Ocupada':
        print('La reservación no está ocupada.')
        return
    mostrar_costo(reserva)
    if round(costo(reserva)[4] - costo(reserva)[5], 2) > 0:
        print('No puede finalizar: existe saldo pendiente.')
        return
    if confirmar('¿Registrar salida y finalizar reservación?'):
        reserva['estado'] = 'Finalizada'
        if guardar():
            print('Salida registrada.')