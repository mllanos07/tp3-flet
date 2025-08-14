import flet as ft
import pymysql
from Usuario import ModuloPersonaClave
from Cliente import VentanaPersonas
from Repuestos import VentanaRepuesto
from Empleado import VentanaPersonal
from Proveedor import VentanaSocios
from FichaTecnica import VentanaFichas
from Presupuesto import VentanaCuentas

def conexion():
    puerta = None
    try:
        puerta = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="taller_mecanico",
            ssl_disabled=True
        )
        print("Conexion lista")
    except Exception as err:
        print("Problema al conectar:", err)
    return puerta

puerta = conexion()

def abrir_personas(e, p):
    VentanaPersonas(p, tablero_inicio)

def abrir_repuesto(e, p):
    VentanaRepuesto(p, tablero_inicio)

def abrir_socios(e, p):
    VentanaSocios(p, tablero_inicio)

def abrir_fichas(e, p):
    VentanaFichas(p, tablero_inicio)

def abrir_clave(e, p):
    ModuloPersonaClave(p, tablero_inicio)

def abrir_cuentas(e, p):
    VentanaCuentas(p, tablero_inicio)

def abrir_personal(e, p):
    VentanaPersonal(p, tablero_inicio)

def menu_principal(p):
    p.clean()
    p.window.maximized = True
    p.title = "Panel Taller Amigo"

    fila_a = ft.Row([ft.Icon(ft.Icons.PERSON, size=26), ft.Text("Personas")], alignment=ft.MainAxisAlignment.START, spacing=6)
    fila_b = ft.Row([ft.Icon(ft.Icons.BUSINESS, size=26), ft.Text("Socios")], alignment=ft.MainAxisAlignment.START, spacing=6)
    fila_c = ft.Row([ft.Icon(ft.Icons.BUILD, size=26), ft.Text("Repuesto")], alignment=ft.MainAxisAlignment.START, spacing=6)
    fila_d = ft.Row([ft.Icon(ft.Icons.PEOPLE, size=26), ft.Text("Personal")], alignment=ft.MainAxisAlignment.START, spacing=6)
    fila_e = ft.Row([ft.Icon(ft.Icons.PERSON_OUTLINE, size=26), ft.Text("Clave")], alignment=ft.MainAxisAlignment.START, spacing=6)
    fila_f = ft.Row([ft.Icon(ft.Icons.DIRECTIONS_CAR, size=26), ft.Text("Ficha Tecnica")], alignment=ft.MainAxisAlignment.START, spacing=6)
    fila_g = ft.Row([ft.Icon(ft.Icons.ATTACH_MONEY, size=26), ft.Text("Cuentas")])

    boton_archivo = ft.PopupMenuButton(
        items=[ft.PopupMenuItem(text="Copiar", icon=ft.Icons.COPY, tooltip="Copiar"),
            ft.PopupMenuItem(text="Salir", icon=ft.Icons.EXIT_TO_APP, tooltip="Salir"),],
        content=ft.Text("Archivo"),
        tooltip="Archivo"
    )
    boton_herramientas = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=fila_a, on_click=lambda e: VentanaPersonas(p, tablero_inicio)),
            ft.PopupMenuItem(content=fila_b, on_click=lambda e: VentanaSocios(p, tablero_inicio)),
            ft.PopupMenuItem(content=fila_c, on_click=lambda e: VentanaRepuesto(p, tablero_inicio)),
            ft.PopupMenuItem(content=fila_d, on_click=lambda e: VentanaPersonal(p, tablero_inicio)),
            ft.PopupMenuItem(content=fila_e, on_click=lambda e: ModuloPersonaClave(p, tablero_inicio)),
        ],
        content=ft.Text("Herramientas"),
        tooltip="Herramientas"
    )
    boton_admin = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=fila_f, on_click=lambda e: abrir_fichas(e, p)),
            ft.PopupMenuItem(content=fila_g, on_click=lambda e: abrir_cuentas(e, p)),
        ],
        content=ft.Text("Admin"),
        tooltip="Admin"
    )

    # accesos directos
    boton_clave = ft.IconButton(icon=ft.Icons.PERSON_OUTLINE, tooltip="Clave", on_click=lambda e: ModuloPersonaClave(p, tablero_inicio))
    boton_personas = ft.IconButton(icon=ft.Icons.PERSON, tooltip="Personas", on_click=lambda e: VentanaPersonas(p, tablero_inicio))
    boton_ficha = ft.IconButton(icon=ft.Icons.DIRECTIONS_CAR, tooltip="Ficha Tecnica", on_click=lambda e: VentanaFichas(p, tablero_inicio))
    boton_cuentas = ft.IconButton(icon=ft.Icons.ATTACH_MONEY, tooltip="Cuentas", on_click=lambda e: VentanaCuentas(p, tablero_inicio))
    boton_repuesto = ft.IconButton(icon=ft.Icons.BUILD, tooltip="Repuesto", on_click=lambda e: VentanaRepuesto(p, tablero_inicio))

    p.add(
        ft.Row([boton_archivo, boton_admin, boton_herramientas], spacing=8), # menu
        ft.Row([boton_clave, boton_personas, boton_ficha, boton_cuentas, boton_repuesto]) # botones
    )

def tablero_inicio(p):
    menu_principal(p)

def inicio_general(p):
    p.window.maximized = True
    menu_principal(p)

if __name__ == "__main__":
    ft.app(target=inicio_general)
