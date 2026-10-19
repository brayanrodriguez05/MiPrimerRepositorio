# Módulo del sistema hotelero
from datetime import datetime, date
from comun import datos, guardar, texto, entero, decimal, fecha, confirmar, buscar, nueva_id


def obtener_huesped():
    identificacion = texto('Documento del huésped: ')
    huesped = buscar(datos['huespedes'], 'documento', identificacion)
    if huesped is None:
        print('Huésped no registrado.')
    return huesped


def registrar_huesped():
    print('\n--- REGISTRAR HUÉSPED ---')
    documento = texto('Documento de identificación: ')
    if buscar(datos['huespedes'], 'documento', documento):
        print('Ya existe un huésped con ese documento.')
        return
    nombre = texto('Nombre completo: ')
    telefono = texto('Teléfono: ')
    correo = texto('Correo electrónico: ')
    if '@' not in correo or '.' not in correo.split('@')[-1] or ' ' in correo:
        print('Correo inválido. No se registró el huésped.')
        return
    datos['huespedes'].append({'documento': documento, 'nombre': nombre,
                               'telefono': telefono, 'correo': correo})
    if guardar():
        print('Huésped registrado correctamente.')


def historial():
    from pagos import mostrar_costo
    print('\n--- HISTORIAL DEL CLIENTE ---')
    huesped = obtener_huesped()
    if huesped is None:
        return
    print('Cliente:', huesped['nombre'], '| Documento:', huesped['documento'])
    cantidad = 0
    for reserva in datos['reservas']:
        if reserva['documento'] == huesped['documento']:
            print('\nID:', reserva['id'], '| Habitación:', reserva['habitacion'],
                  '| Entrada:', reserva['entrada'], '| Salida:', reserva['salida'])
            mostrar_costo(reserva)
            cantidad += 1
    if cantidad == 0:
        print('Este cliente todavía no tiene reservaciones.')
