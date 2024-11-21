import PySimpleGUI as sg
import os

# Función para leer usuarios desde un archivo
def leer_usuarios():
    if os.path.exists("usuarios.txt"):
        print("Archivo 'usuarios.txt' encontrado.")  # Mensaje de depuración
        with open("usuarios.txt", "r") as f:
            usuarios = [line.strip().split(",") for line in f.readlines()]
            # Eliminar espacios en blanco alrededor de usuario y contraseña
            usuarios_dict = {user[0].strip(): user[1].strip() for user in usuarios if len(user) == 2}
            print("Usuarios leídos:", usuarios_dict)  # Mostrar usuarios leídos
            return usuarios_dict
    else:
        print("Archivo 'usuarios.txt' no encontrado.")  # Mensaje de depuración
    return {}

# Ventana de login
def ventana_login():
    layout = [
        [sg.Text('Usuario'), sg.InputText(key='-USUARIO-')],
        [sg.Text('Contraseña'), sg.InputText(key='-PASSWORD-', password_char='*')],
        [sg.Button('Iniciar Sesión'), sg.Button('Salir')]
    ]
    return sg.Window('Login', layout, finalize=True)

# Ventana principal (puedes modificarla según tus necesidades)
def ventana_principal():
    layout = [
        [sg.Text('Bienvenido a la aplicación')],
        [sg.Button('Cerrar')]
    ]
    return sg.Window('Ventana Principal', layout, finalize=True)

# Inicializar datos
usuarios = leer_usuarios()

# Ventana de login
window_login = ventana_login()
window_principal = None

while True:
    window, event, values = sg.read_all_windows()

    if event == sg.WINDOW_CLOSED or event == 'Salir':
        window.close()
        break

    if event == 'Iniciar Sesión':
        usuario = values['-USUARIO-'].strip()  # Eliminar espacios en el input
        password = values['-PASSWORD-'].strip()  # Eliminar espacios en el input
        print(f"Intentando iniciar sesión con: '{usuario}', '{password}'")  # Mensaje de depuración
        if usuario in usuarios:
            print(f"Contraseña almacenada para '{usuario}': '{usuarios[usuario]}'")  # Mostrar la contraseña almacenada
            if usuarios[usuario] == password:
                sg.popup('Login exitoso')
                window_login.close()  # Cerrar ventana de login
                window_principal = ventana_principal()  # Abrir ventana principal
            else:
                sg.popup_error('Contraseña incorrecta')
        else:
            sg.popup_error('Usuario no encontrado')

    # Manejo de eventos en la ventana principal
    if window == window_principal and event == 'Cerrar':
        window.close()