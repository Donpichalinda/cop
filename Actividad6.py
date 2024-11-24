import PySimpleGUI as sg
import json
import os
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd

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

# Ventana principal con nueva funcionalidad de análisis
def ventana_principal(configuracion, eventos):
    layout = [
        [sg.TabGroup([
            [sg.Tab('Eventos', [
                [sg.Text('Nombre Evento'), sg.InputText(key='-NOMBRE-', size=(25, 1)), sg.Text('Fecha'), sg.InputText(key='-FECHA-', size=(25, 1))],
                [sg.Text('Cupo'), sg.InputText(key='-CUPO-', size=(25, 1)), sg.Text('Lugar'), sg.InputText(key='-LUGAR-', size=(25, 1))],
                [sg.Text('Hora'), sg.InputText(key='-HORA-', size=(25, 1)), sg.Text('Imagen'), sg.InputText(key='-IMAGEN-', size=(25, 1)), sg.FileBrowse('Buscar')],
                [sg.Button('Agregar'), sg.Button('Modificar', key='-MODIFICAR_EVENTO-', visible=True), sg.Button('Eliminar', key='-ELIMINAR_EVENTO-', visible=True)],
                [sg.Table(
                    headings=['Nombre', 'Fecha', 'Cupo', 'Lugar', 'Hora', 'Imagen'],
                    values=[], size=(80, 10), key='-TABLE-', enable_events=True
                )],
                [sg.Image(key='-IMAGE-', size=(100, 100))]
            ])],
            [sg.Tab('Participantes', [
                [sg.Text('Selecciona el evento'), sg.Combo([], key='-EVENTO-', size=(20, 1)), sg.Text('Nombre'), sg.InputText(key='-NOMBRE_PARTICIPANTE-', size=(25, 1))],
                [sg.Text('Tipo Documento'), sg.InputText(key='-TIPO_DOCUMENTO-', size=(25, 1)), sg.Text('Número Documento'), sg.InputText(key='-NUMERO_DOCUMENTO-', size=(25, 1))],
                [sg.Text('Teléfono'), sg.InputText(key='-TELEFONO-', size=(25, 1)), sg.Text('Dirección'), sg.InputText(key='-DIRECCION-', size=(25, 1))],
                [sg.Text('Tipo Participante'), sg.Combo(['Estudiante', 'Otro'], key='-TIPO_PARTICIPANTE-')],
                [sg.Button('Agregar Participante'), sg.Button('Modificar Participante', key='-MODIFICAR_PARTICIPANTE-', visible=True), sg.Button('Eliminar Participante', key='-ELIMINAR_PARTICIPANTE-', visible=True)],
                [sg.Table(
                    headings=['Nombre', 'Tipo Documento', 'Número Documento', 'Teléfono', 'Dirección', 'Tipo Participante', 'Evento'],
                    values=[], size=(80, 10), key='-TABLE_PARTICIPANTES-', enable_events=True
                )],
            ])],
            [sg.Tab('Análisis', [
                [sg.Text('Participantes que fueron a todos los eventos')],
                [sg.Multiline (size=(60, 5), key='-TODOS_EVENTOS-', disabled=True)],
                [sg.Text('Participantes que fueron al menos a un evento')],
                [sg.Multiline(size=(60, 5), key='-AL_MENOS_UNO-', disabled=True)],
                [sg.Text('Participantes que fueron solo al primer evento')],
                [sg.Multiline(size=(60, 5), key='-SOLO_PRIMERO-', disabled=True)],
                [sg.Button('Actualizar Análisis', key='-ACTUALIZAR_ANALISIS-')]
            ])],
            [sg.Tab('Gráficos', [
                [sg.Text('Seleccione tipo de gráfico')],
                [sg.Combo(['Barras', 'Pastel', 'Línea'], key='-TIPO_GRAFICO-', size=(30, 1))],
                [sg.Button('Generar Gráfico', key='-GENERAR_GRAFICO-')],
                [sg.Image(key='-GRAFICO-', size=(500, 500))]
            ])],
            [sg.Tab('Configuración', [
                [sg.Text('Configuración')],
                [sg.Checkbox('Validar Aforo al agregar participantes', key='-VALIDAR_AFORO-', default=configuracion.get('validar_aforo', True), enable_events=True)],
                [sg.Checkbox('Solicitar imágenes', key='-SOLICITAR_IMAGENES-', default=configuracion.get('solicitar_imagenes', True), enable_events=True)],
                [sg.Checkbox('Modificar registros', key='-MODIFICAR_REGISTROS-', default=configuracion.get('modificar_registros', True), enable_events=True)],
                [sg.Checkbox('Eliminar Registros', key='-ELIMINAR_REGISTROS-', default=configuracion.get('eliminar_registros', True), enable_events=True)],
                [sg.Button('Guardar Configuración', key='-GUARDAR_CONFIG-', visible=True)],
            ])],
        ])]
    ]
    return sg.Window('Gestión de Eventos', layout, finalize=True)

# Función para generar gráficos
def generar_grafico(eventos, participantes, tipo_grafico):
    fig, ax = plt.subplots(figsize=(6, 4))
    if tipo_grafico == 'Barras':
        df = pd.DataFrame(eventos, columns=['Nombre', 'Fecha', 'Cupo', 'Lugar', 'Hora', 'Imagen'])
        lugares = df['Lugar'].value_counts()
        lugares.plot(kind='bar', ax=ax, title='Eventos por Lugar', color='skyblue')
        ax.set_xlabel('Lugar')
        ax.set_ylabel('Número de Eventos')
    elif tipo_grafico == 'Pastel':
        df = pd.DataFrame(participantes, columns=['Nombre', 'Tipo Documento', 'Número Documento', 'Teléfono', 'Dirección', 'Tipo Participante', 'Evento'])
        eventos_participantes = df['Evento'].value_counts()
        eventos_participantes.plot(kind='pie', ax=ax, title='Participantes por Evento', autopct='%1.1f%%')
        ax.set_ylabel('')  # Eliminar la etiqueta del eje y
    elif tipo_grafico == 'Línea':
        df = pd.DataFrame(participantes, columns=['Nombre', 'Tipo Documento', 'Número Documento', 'Teléfono', 'Dirección', 'Tipo Participante', 'Evento'])
        eventos_participantes = df['Evento'].value_counts()
        eventos_participantes.plot(kind='line', ax=ax, title='Participantes por Evento', marker='o')
        ax.set_xlabel('Evento')
        ax.set_ylabel('Número de Participantes')
    else:
        plt.text(0.5, 0.5, 'Seleccione un gráfico válido', ha='center', va='center', fontsize=12)
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)  # Cerrar la figura para liberar memoria
    return buf

# Lógica para el análisis
def realizar_analisis(eventos, participantes):
    eventos_nombres = {evento[0] for evento in eventos}
    participantes_eventos = {}

    for participante in participantes:
        nombre = participante[0]
        evento = participante[6]
        if nombre not in participantes_eventos:
            participantes_eventos[nombre] = set()
        participantes_eventos[nombre].add(evento)

    todos_eventos = [nombre for nombre, eventos in participantes_eventos.items() if eventos == eventos_nombres]
    al_menos_uno = list(participantes_eventos.keys())
    primer_evento = next(iter(eventos_nombres), None)
    solo_primer_evento = [nombre for nombre, eventos in participantes_eventos.items() if eventos == {primer_evento}]

    return todos_eventos, al_menos_uno, solo_primer_evento

# Función para manejar la visibilidad de los botones
def manejar_visibilidad_boton(window, values):
    window['-MODIFICAR_EVENTO-'].update(visible=values['-MODIFICAR_REGISTROS-'])
    window['-ELIMINAR_EVENTO-'].update(visible=values['-ELIMINAR_REGISTROS-'])
    window['-MODIFICAR_PARTICIPANTE-'].update(visible=values['-MODIFICAR_REGISTROS-'])
    window['-ELIMINAR_PARTICIPANTE-'].update(visible=values['-ELIMINAR_REGISTROS-'])

# Guardar datos en archivo JSON
def guardar_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Cargar datos desde archivo JSON
def cargar_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Inicializar datos
usuarios = leer_usuarios()
eventos = cargar_json("eventos.json")
participantes = cargar_json("participantes.json")
configuracion = cargar_json("configuracion.json")

if not isinstance(configuracion, dict):
    configuracion = {}

window_login = ventana_login()
window_principal = None
window_agregar_usuario = None

while True:
    window, event, values = sg.read_all_windows()

    if event == sg.WINDOW_CLOSED or event == 'Salir':
        window.close()
        if window == window_principal:
            guardar_json("eventos.json", eventos)
            guardar_json("participantes.json", participantes)
            guardar_json("configuracion.json", configuracion)
        if window == window_login:
            break

    if event == 'Iniciar Sesión':
        usuario = values['-USUARIO-'].strip()
        password = values['-PASSWORD-'].strip()
        if usuario in usuarios and usuarios[usuario] == password:
            sg.popup('Login exitoso')
            window_login.close()
            window_principal = ventana_principal(configuracion, eventos)
        else:
            sg.popup_error('Usuario o contraseña incorrectos')

    if event == 'Agregar Usuario':
        window_agregar_usuario = ventana_agregar_usuario()

    if window == window_agregar_usuario:
        if event == 'Guardar':
            nuevo_usuario = values['-NUEVO_USUARIO-'].strip()
            nueva_contrasena = values['-NUEVA_CONTRASENA-'].strip()
            if nuevo_usuario and nueva_contrasena:
                agregar_usuario(nuevo_usuario, nueva_contrasena)
                usuarios[nuevo_usuario] = nueva_contrasena
                sg.popup('Usuario agregado exitosamente')
                window_agregar_usuario.close()
            else:
                sg.popup_error('Complete todos los campos para agregar un usuario')
        if event == 'Cancelar':
            window_agregar_usuario.close()

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
                    window['-EVENTO-'].update(values=[e[0] for e in eventos])
                except Exception as e:
                    sg.popup_error(f"Error: {e}")
            else:
                sg.popup_error("Complete todos los campos para agregar un evento")

        if event == '-ACTUALIZAR_ANALISIS-':
            todos_eventos, al_menos_uno, solo_primer_evento = realizar_analisis(eventos, participantes)
            window['-TODOS_EVENTOS-'].update('\n'.join(todos_eventos))
            window['-AL_MENOS_UNO-'].update('\n'.join(al_menos_uno))
            window['-SOLO_PRIMERO-'].update('\n'.join(solo_primer_evento))

        if event == '-GENERAR_GRAFICO-':
            tipo_grafico = values['-TIPO_GRAFICO-']
            if tipo_grafico:
                buf = generar_grafico(eventos, participantes, tipo_grafico)
                window['-GRAFICO-'].update(data=buf.getvalue())
            else:
                sg.popup_error('Seleccione un tipo de gráfico para generar')

        if event == '-MODIFICAR_EVENTO-':
            selected_row = values['-TABLE-'][0] if values['-TABLE-'] else None
            if selected_row is not None:
                eventos[selected_row] = [values['-NOMBRE-'], values['-FECHA-'], values['-CUPO-'], values['-LUGAR-'], values['-HORA-'], values['-IMAGEN-']]
                window['-TABLE-'].update(eventos)
                window['-EVENTO-'].update(values=[e[0] for e in eventos])
            else:
                sg.popup_error("Seleccione un evento para modificar")

        if event == '-ELIMINAR_EVENTO-':
            selected_row = values['-TABLE-'][0] if values['-TABLE-'] else None
            if selected_row is not None:
                eventos.pop(selected_row)
                window['-TABLE-'].update(eventos)
                window['-EVENTO-'].update(values=[e[0] for e in eventos])
            else:
                sg.popup_error("Seleccione un evento para eliminar")

        if event == 'Agregar Participante':
            nombre = values['-NOMBRE_PARTICIPANTE-']
            tipo_documento = values['-TIPO_DOCUMENTO-']
            numero_documento = values['-NUMERO_DOCUMENTO-']
            telefono = values['-TELEFONO-']
            direccion = values['-DIRECCION-']
            tipo_participante = values['-TIPO_PARTICIPANTE-']
            evento_seleccionado = values['-EVENTO-']
            if nombre and tipo_documento and numero_documento and telefono and direccion and tipo_participante and evento_seleccionado:
                try:
                    if not numero_documento.isdigit():
                        raise ValueError("El número de documento debe ser numérico")
                    if any(p[2] == numero_documento for p in participantes):
                        raise ValueError("Ya existe un participante con este número de documento")
                    participantes.append([nombre, tipo_documento, numero_documento, telefono, direccion, tipo_participante, evento_seleccionado])
                    window['-TABLE_PARTICIPANTES-'].update(participantes)
                except Exception as e:
                    sg.popup_error(f"Error: {e}")
            else:
                sg.popup_error("Complete todos los campos para agregar un participante")

        if event == '-MODIFICAR_PARTICIPANTE-':
            selected_row = values['-TABLE_PARTICIPANTES-'][0] if values['-TABLE_PARTICIPANTES-'] else None
            if selected_row is not None:
                participantes[selected_row] = [
                    values['-NOMBRE_PARTICIPANTE-'],
                    values['-TIPO_DOCUMENTO-'],
                    values['-NUMERO_DOCUMENTO-'],
                    values['-TELEFONO-'],
                    values['-DIRECCION-'],
                    values['-TIPO_PARTICIPANTE-'],
                    values['-EVENTO-']
                ]
                window['-TABLE_PARTICIPANTES-'].update(participantes)
            else:
                sg.popup_error("Seleccione un participante para modificar")

        if event == '-ELIMINAR_PARTICIPANTE-':
            selected_row = values['-TABLE_PARTICIPANTES-'][0] if values['-TABLE_PARTICIPANTES-'] else None
            if selected_row is not None:
                participantes.pop(selected_row)
                window['-TABLE_PARTICIPANTES-'].update(participantes)
            else:
                sg.popup_error("Seleccione un participante para eliminar")

        if event == 'Guardar Configuración':
            configuracion['validar_aforo'] = values['-VALIDAR_AFORO-']
            configuracion['solicitar_imagenes'] = values['-SOLICITAR_IMAGENES-']
            configuracion['modificar_registros'] = values['-MODIFICAR_REGISTROS-']
            configuracion['eliminar_registros'] = values['-ELIMINAR_REGISTROS-']
            guardar_json("configuracion.json", configuracion)
            sg.popup('Configuración guardada exitosamente')

        if event in ['-VALIDAR_AFORO-', '-SOLICITAR_IMAGENES-', '-MODIFICAR_REGISTROS-', '-ELIMINAR_REGISTROS-']:
            manejar_visibilidad_boton(window_principal, values)

window.close()