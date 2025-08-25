import flet as ft

class Herramienta_Usuario:
    def __init__(self, page: ft.Page, main_menu_callback):
        self.page = page
        self.main_menu_callback = main_menu_callback
        self.mostrar_login()

    def mostrar_login(self):
        self.page.clean()
        self.usuario = ft.TextField(label="Usuario", width=300)
        self.contrasena = ft.TextField(label="Contraseña", password=True, width=300)
        iniciar_btn = ft.ElevatedButton("Iniciar sesión")
        volver_btn = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.main_menu_callback(self.page))

        self.page.add(
            ft.Column(
                [
                    ft.Text("Inicio de Sesión", size=24, weight="bold"),
                    self.usuario,
                    self.contrasena,
                    ft.Row([iniciar_btn, volver_btn], spacing=10),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )