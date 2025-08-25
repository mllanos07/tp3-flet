import flet as ft

class ModuloPersonaClave:
    def __init__(self, ventana, regresar_menu):
        self.pantalla = ventana
        self.volver_al_inicio = regresar_menu
        self.mostrar_formulario_login()

    def mostrar_formulario_login(self):
        self.pantalla.clean()
        self.campo_usuario = ft.TextField(label="Usuario", width=250)
        self.campo_clave = ft.TextField(label="Clave", password=True, width=250)
        # boton_ingresar = ft.ElevatedButton("Entrar")
        boton_regresar = ft.ElevatedButton("Entrar", on_click=lambda e: self.volver_al_inicio(self.pantalla))

        self.pantalla.add(
            ft.Column([
                ft.Text("Ingreso al Sistema", size=20, weight="bold"),
                self.campo_usuario,
                self.campo_clave,
                ft.Row([boton_regresar], spacing=8),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        self.pantalla.update()
