# Módulo del sistema hotelero
from datetime import datetime, date
from comun import datos, guardar, texto, entero, decimal, fecha, confirmar, buscar, nueva_id


def costo(reserva):
    noches = (date.fromisoformat(reserva['salida']) - date.fromisoformat(reserva['entrada'])).days
    subtotal = noches * reserva['precio_noche']
    extras = sum(cargo['monto'] for cargo in reserva['cargos'])
    descuento = subtotal * reserva['descuento'] / 100
    total = round(subtotal + extras - descuento, 2)
    pagado = round(sum(pago['monto'] for pago in reserva['pagos']), 2)
    return noches, round(subtotal, 2), round(extras, 2), round(descuento, 2), total, pagado


def mostrar_costo(reserva):
    noches, subtotal, extras, descuento, total, pagado = costo(reserva)
    print('\nReservación:', reserva['id'], '| Estado:', reserva['estado'])
    print('Noches:', noches, '| Hospedaje: Q', subtotal)
    print('Cargos adicionales: Q', extras, '| Descuento: Q', descuento)
    print('TOTAL: Q', total, '| Pagado: Q', pagado, '| Saldo: Q', round(total - pagado, 2))


def registrar_pago():
    from reservaciones import obtener_reserva
    print('\n--- REGISTRAR PAGO ---')
    reserva = obtener_reserva()
    if reserva is None:
        return
    if reserva['estado'] not in ('Reservada', 'Ocupada'):
        print('No se aceptan pagos para este estado.')
        return
    mostrar_costo(reserva)
    saldo = round(costo(reserva)[4] - costo(reserva)[5], 2)
    if saldo <= 0:
        print('No hay saldo pendiente.')
        return
    monto = decimal('Monto del pago (Q): ', 0.01)
    if monto > saldo:
        print('El pago no puede superar el saldo pendiente.')
        return
    metodo = texto('Método de pago (efectivo, tarjeta, transferencia): ')
    reserva['pagos'].append({'monto': monto, 'metodo': metodo,
                             'fecha': date.today().isoformat()})
    if guardar():
        print('Pago registrado. Saldo restante: Q', round(saldo - monto, 2))


def agregar_cargo():
    from reservaciones import obtener_reserva
    print('\n--- CARGO ADICIONAL ---')
    reserva = obtener_reserva()
    if reserva is None:
        return
    if reserva['estado'] not in ('Reservada', 'Ocupada'):
        print('No se pueden agregar cargos a esta reservación.')
        return
    concepto = texto('Servicio o concepto: ')
    monto = decimal('Monto del cargo (Q): ', 0.01)
    reserva['cargos'].append({'concepto': concepto, 'monto': monto})
    if guardar():
        print('Cargo registrado.')
        mostrar_costo(reserva)


def calcular_hospedaje():
    from reservaciones import obtener_reserva
    reserva = obtener_reserva()
    if reserva is not None:
        mostrar_costo(reserva)