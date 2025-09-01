# correr codigo:Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force; .\.venv\Scripts\Activate.ps1
# python archivos\App.py
import flet as ft
import pymysql
from Usuario import Herramienta_Usuario
from Cliente import Herramienta_Cliente
from Repuestos import Herramienta_Repuesto
from Empleado import Herramienta_Empleado
from Proveedor import Herramienta_Proveedor
from FichaTecnica import Herramienta_FichaTecnica
from Presupuesto import Herramienta_Presupuesto


def connect_to_db():
    try:
        connection = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="taller_mecanico",
            ssl_disabled=True,
        )
        # pymysql.connect() raises an exception on failure. If we reach here,
        # the connection was successful — return the connection object.
        print("Conexión exitosa")
        return connection
    except Exception as ex:
        print("Conexión errónea")
        print(ex)
        return None


connection = connect_to_db()


# Navegacion
def cliente(e, page: ft.Page):
    Herramienta_Cliente(page, menu_principal)


def mostrar_cliente(e, page: ft.Page):
    Herramienta_Cliente(page, menu_principal)


def repuesto(e, page: ft.Page):
    Herramienta_Repuesto(page, menu_principal)


def mostrar_repuesto(e, page: ft.Page):
    Herramienta_Repuesto(page, menu_principal)


def proveedor(e, page: ft.Page):
    Herramienta_Proveedor(page, menu_principal)


def producto(e, page: ft.Page):
    pass


def empleado(e, page: ft.Page):
    Herramienta_Empleado(page, menu_principal)


def usuario(e, page: ft.Page):
    Herramienta_Usuario(page, menu_principal)


def ficha_tecnica(e, page: ft.Page):
    Herramienta_FichaTecnica(page, menu_principal)


def presupuesto(e, page: ft.Page):
    Herramienta_Presupuesto(page, menu_principal)


# Menu
def menu_principal(page: ft.Page):
    page.clean()
    page.window.maximized = True
    page.title = "Administración de Taller Mecánico"

    cliente_icono = ft.Icon(ft.Icons.PERSON, size=28)
    cliente_item = ft.Row(
        controls=[cliente_icono, ft.Text("Cliente")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8,
    )

    proveedor_icono = ft.Icon(ft.Icons.BUSINESS, size=28)
    proveedor_item = ft.Row(
        controls=[proveedor_icono, ft.Text("Proveedor")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8,
    )

    repuesto_icono = ft.Icon(ft.Icons.BUILD, size=28)
    repuesto_item = ft.Row(
        controls=[repuesto_icono, ft.Text("Repuesto")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8,
    )

    empleado_icono = ft.Icon(ft.Icons.PEOPLE, size=28)
    empleado_item = ft.Row(
        controls=[empleado_icono, ft.Text("Empleado")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8,
    )

    usuario_icono = ft.Icon(ft.Icons.PERSON_OUTLINE, size=28)
    usuario_item = ft.Row(
        controls=[usuario_icono, ft.Text("Usuario")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8,
    )

    ficha_tecnica_icono = ft.Icon(ft.Icons.DIRECTIONS_CAR, size=28)
    ficha_tecnica_item = ft.Row(
        controls=[ficha_tecnica_icono, ft.Text("Ficha Técnica")],
        alignment=ft.MainAxisAlignment.START,
        spacing=8,
    )

    presupuesto_icono = ft.Icon(ft.Icons.ATTACH_MONEY, size=28)
    presupuesto_icono_item = ft.Row(
        controls=[presupuesto_icono, ft.Text("Presupuesto")]
    )

    # Botones secundarios
    archivo_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Copiar", icon=ft.Icons.COPY, tooltip="Copiar"),
            ft.PopupMenuItem(text="Salir", icon=ft.Icons.EXIT_TO_APP, tooltip="Salir"),
        ],
        content=ft.Text("Archivo"),
        tooltip="Archivo",
    )

    herramientas_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=cliente_item, on_click=lambda e: cliente(e, page)),
            ft.PopupMenuItem(
                content=proveedor_item, on_click=lambda e: proveedor(e, page)
            ),
            ft.PopupMenuItem(
                content=repuesto_item, on_click=lambda e: repuesto(e, page)
            ),
            ft.PopupMenuItem(
                content=empleado_item, on_click=lambda e: empleado(e, page)
            ),
            ft.PopupMenuItem(content=usuario_item, on_click=lambda e: usuario(e, page)),
        ],
        content=ft.Text("Herramientas"),
        tooltip="Administrador de archivos maestros",
    )

    administracion = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ficha_tecnica_item, on_click=lambda e: ficha_tecnica(e, page)),
            ft.PopupMenuItem(content=presupuesto_icono_item, on_click=lambda e: presupuesto(e, page)),
        ],
        content=ft.Text("Administración"),
        tooltip="Administración de presupuesto y ficha técnica",
    )

    # Botones principales
    boton_cliente = ft.IconButton(
        icon=ft.Icons.PERSON,
        tooltip="Cliente",
        on_click=lambda e: mostrar_cliente(e, page),
    )

    boton_usuario = ft.IconButton(
        icon=ft.Icons.PERSON_OUTLINE,
        tooltip="Usuario",
        on_click=lambda e: usuario(e, page),
    )

    boton_repuestos = ft.IconButton(
        icon=ft.Icons.BUILD,
        tooltip="Repuesto",
        on_click=lambda e: mostrar_repuesto(e, page),
    )
    boton_ficha_tecnica = ft.IconButton(
        icon=ft.Icons.DIRECTIONS_CAR,
        tooltip="Ficha Técnica",
        on_click=lambda e: ficha_tecnica(e, page),
    )
    boton_presupuesto = ft.IconButton(
        icon=ft.Icons.ATTACH_MONEY,
        tooltip="Presupuesto",
        on_click=lambda e: presupuesto(e, page),
    )

    page.add(
        ft.Row(
            controls=[archivo_menu, administracion, herramientas_menu],
            spacing=10,
        ),
        ft.Row(
            controls=[
                boton_cliente,
                boton_repuestos,
                boton_ficha_tecnica,
                boton_presupuesto,
                boton_usuario,
            ]
        ),
    )


def main(page: ft.Page):
    page.window.maximized = True
    menu_principal(page)


ft.app(target=main)
