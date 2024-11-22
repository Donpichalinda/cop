import PySimpleGUI as sg
import json
import os

# Función para leer usuarios desde un archivo
def leer_usuarios():
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r") as f:
            usuarios = [line.strip().split(",") for line in f.readlines()]
            usuarios_dict = {user[0].strip(): user[1].strip() for user in usuarios if len(user) == 2}
            return usuarios_dict
    return {}

# Función para agregar un nuevo usuario
def agregar_usuario(usuario, password):
    with open("usuarios.txt", "a") as f:
        f.write(f"{usuario},{password}\n")

# Ventana de login
def ventana_login():
    layout = [
        [sg.Text('Usuario'), sg.InputText(key='-USUARIO-')],
        [sg.Text('Contraseña'), sg.InputText(key='-PASSWORD-', password_char='*')],
        [sg.Button('Iniciar Sesión'), sg.Button('Agregar Usuario'), sg.Button('Salir')]
    ]
    return sg.Window('Login', layout, finalize=True)

# Ventana para agregar usuario
def ventana_agregar_usuario():
    layout = [
        [sg.Text('Nuevo Usuario'), sg.InputText(key='-NUEVO_USUARIO-')],
        [sg.Text('Nueva Contraseña'), sg.InputText(key='-NUEVA_CONTRASENA-', password_char='*')],
        [sg.Button('Guardar'), sg.Button('Cancelar')]
    ]
    return sg.Window('Agregar Usuario', layout, finalize=True)

# Ventana principal
def ventana_principal():
    layout = [
        [sg.TabGroup([
            [sg.Tab('Eventos', [
                [sg.Text('Nombre Evento'), sg.InputText(key='-NOMBRE-')],
                [sg.Text('Fecha'), sg.InputText(key='-FECHA-')],
                [sg.Text('Cupo'), sg.InputText(key='-CUPO-')],
                [sg.Text('Lugar'), sg.InputText(key='-LUGAR-')],
                [sg.Text('Hora'), sg.InputText(key='-HORA-')],
                [sg.Text('Imagen'), sg.InputText(key='-IMAGEN-'), sg.FileBrowse('Buscar')],
                [sg.Button('Agregar'), sg.Button('Modificar'), sg.Button('Eliminar')],
                [sg.Table(
                    headings=['Nombre', 'Fecha', 'Cupo', 'Lugar', 'Hora', 'Imagen'],
                    values=[], size=(80, 10), key='-TABLE-', enable_events=True
                )],
                [sg.Image(key='-IMAGE-', size=(100, 100))]
            ])],
            [sg.Tab('Participantes', [
                [sg.Text('Nombre'), sg.InputText(key='-NOMBRE_PARTICIPANTE-')],
                [sg.Text('Tipo Documento'), sg.InputText(key='-TIPO_DOCUMENTO-')],
                [sg.Text('Número Documento'), sg.InputText(key='-NUMERO_DOCUMENTO-')],
                [sg.Text('Teléfono'), sg.InputText(key='-TELEFONO-')],
                [sg.Text('Dirección'), sg.InputText(key='-DIRECCION-')],
                [sg.Text('Tipo Participante'), sg.Combo(['Estudiante', 'Otro'], key='-TIPO_PARTICIPANTE-')],
                [sg.Button('Agregar Participante'), sg.Button('Modificar Participante'), sg.Button('Eliminar Participante')],
                [sg.Table(
                    headings=['Nombre', 'Tipo Documento', 'Número Documento', 'Teléfono', 'Dirección', 'Tipo Participante'],
                    values=[], size=(80, 10), key='-TABLE_PARTICIPANTES-', enable_events=True
                )],
            ])],
        ])]
    ]
    return sg.Window('Gestión de Eventos', layout, finalize=True)

# Guardar datos en archivo JSON
def guardar_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Cargar datos desde archivo JSON
def cargar_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

# Inicializar datos
usuarios = leer_usuarios()
eventos = cargar_json("eventos.json")
participantes = cargar_json("participantes.json")
configuracion = cargar_json("configuracion.json")

# Ventana de login
window_login = ventana_login()
window_principal = None
window_agregar_usuario = None

while True:
    window, event, values = sg.read_all_windows()

 # Cerrar aplicación
    if event == sg.WINDOW_CLOSED or event == 'Salir':
        window.close()
        if window == window_principal:
            guardar_json("eventos.json", eventos)
            guardar_json("participantes.json", participantes)
            guardar_json("configuracion.json", configuracion)
            break

    # Login
    if event == 'Iniciar Sesión':
        usuario = values['-USUARIO-'].strip()
        password = values['-PASSWORD-'].strip()
        if usuario in usuarios and usuarios[usuario] == password:
            sg.popup('Login exitoso')
            window_login.close()
            window_principal = ventana_principal()
        else:
            sg.popup_error('Usuario o contraseña incorrectos')

    # Agregar usuario
    if event == 'Agregar Usuario':
        window_agregar_usuario = ventana_agregar_usuario()

    # Guardar nuevo usuario
    if window == window_agregar_usuario:
        if event == 'Guardar':
            nuevo_usuario = values['-NUEVO_USUARIO-'].strip()
            nueva_contrasena = values['-NUEVA_CONTRASENA-'].strip()
            if nuevo_usuario and nueva_contrasena:
                agregar_usuario(nuevo_usuario, nueva_contrasena)
                usuarios[nuevo_usuario] = nueva_contrasena  # Actualizar la lista de usuarios
                sg.popup('Usuario agregado exitosamente')
                window_agregar_usuario.close()
            else:
                sg.popup_error('Complete todos los campos para agregar un usuario')
        
        if event == 'Cancelar':
            window_agregar_usuario.close()

    # Ventana principal: Eventos
    if window == window_principal:
        if event == 'Agregar':
            nombre = values['-NOMBRE-']
            fecha = values['-FECHA-']
            cupo = values['-CUPO-']
            lugar = values['-LUGAR-']
            hora = values['-HORA-']
            imagen = values['-IMAGEN-']
            if nombre and fecha and cupo and lugar and hora:
                try:
                    if not cupo.isdigit():
                        raise ValueError("El cupo debe ser un número")
                    if any(e[0] == nombre for e in eventos):
                        raise ValueError("Ya existe un evento con este nombre")
                    eventos.append([nombre, fecha, int(cupo), lugar, hora, imagen])
                    window['-TABLE-'].update(eventos)
                except Exception as e:
                    sg.popup_error(f"Error: {e}")
            else:
                sg.popup_error("Complete todos los campos para agregar un evento")

        # Modificar evento
        if event == 'Modificar':
            selected_row = values['-TABLE-'][0] if values['-TABLE-'] else None
            if selected_row is not None:
                eventos[selected_row] = [values['-NOMBRE-'], values['-FECHA-'], values['-CUPO-'], values['-LUGAR-'], values['-HORA-'], values['-IMAGEN-']]
                window['-TABLE-'].update(eventos)
            else:
                sg.popup_error("Seleccione un evento para modificar")

        # Eliminar evento
        if event == 'Eliminar':
            selected_row = values['-TABLE-'][0] if values['-TABLE-'] else None
            if selected_row is not None:
                eventos.pop(selected_row)
                window['-TABLE-'].update(eventos)
            else:
                sg.popup_error("Seleccione un evento para eliminar")

        # Participantes
        if event == 'Agregar Participante':
            nombre = values['-NOMBRE_PARTICIPANTE-']
            tipo_documento = values['-TIPO_DOCUMENTO-']
            numero_documento = values['-NUMERO_DOCUMENTO-']
            telefono = values['-TELEFONO-']
            direccion = values['-DIRECCION-']
            tipo_participante = values['-TIPO_PARTICIPANTE-']
            if nombre and tipo_documento and numero_documento and telefono and direccion and tipo_participante:
                try:
                    if not numero_documento.isdigit():
                        raise ValueError("El número de documento debe ser numérico")
                    if any(p[2] == numero_documento for p in participantes):
                        raise ValueError("Ya existe un participante con este número de documento")
                    participantes.append([nombre, tipo_documento, numero_documento, telefono, direccion, tipo_participante])
                    window['-TABLE_PARTICIPANTES-'].update(participantes)
                except Exception as e:
                    sg.popup_error(f"Error: {e}")
            else:
                sg.popup_error("Complete todos los campos para agregar un participante")

        # Modificar participante
        if event == 'Modificar Participante':
            selected_row = values['-TABLE_PART ```pythonICIPANTES-'][0] if values['-TABLE_PARTICIPANTES-'] else None
            if selected_row is not None:
                participantes[selected_row] = [
                    values['-NOMBRE_PARTICIPANTE-'],
                    values['-TIPO_DOCUMENTO-'],
                    values['-NUMERO_DOCUMENTO-'],
                    values['-TELEFONO-'],
                    values['-DIRECCION-'],
                    values['-TIPO_PARTICIPANTE-']
                ]
                window['-TABLE_PARTICIPANTES-'].update(participantes)
            else:
                sg.popup_error("Seleccione un participante para modificar")

        # Eliminar participante
        if event == 'Eliminar Participante':
            selected_row = values['-TABLE_PARTICIPANTES-'][0] if values['-TABLE_PARTICIPANTES-'] else None
            if selected_row is not None:
                participantes.pop(selected_row)
                window['-TABLE_PARTICIPANTES-'].update(participantes)
            else:
                sg.popup_error("Seleccione un participante para eliminar")

window.close()