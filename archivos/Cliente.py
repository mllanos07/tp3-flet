import flet as ft
import pymysql

def conexion_amistosa():
    db = None
    try:
        db = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="taller_mecanico",
            ssl_disabled=True
        )
        print("Conexion exitosa")
    except Exception as error:
        print("Error al conectar con la base de datos:", error)
    return db

class VentanaPersonas:
    def __init__(self, pantalla, volver_a_inicio):
        self.vista = pantalla
        self.volver_menu_principal = volver_a_inicio
        self.db = conexion_amistosa()
        if self.db:
            self.cur = self.db.cursor()
        else:
            self.cur = None
        self.mostrar_personas()

    def volver_a_menu(self, evento):
        self.vista.clean()
        self.volver_menu_principal(self.vista)

    def imprimir_lista_personas(self, evento):
        self.vista.snack_bar = ft.SnackBar(ft.Text("No se puede imprimir todavia"))
        self.vista.snack_bar.open = True
        self.vista.update()

    def consulta_personas(self, evento):
        self.vista.clean()
        self.vista.add(ft.Text("Consulta de Personas", size=20, weight="bold"))
        self.vista.add(self.tabla_personas())
        self.vista.add(ft.ElevatedButton("Volver", on_click=self.mostrar_personas))
        self.vista.update()

    def guardar_edicion_persona(self, evento, persona):
        try:
            self.cur.execute(
                "UPDATE persona SET apellido=%s, nombre=%s, direccion=%s, tele_contac=%s WHERE dni=%s",
                (self.apellido.value, self.nombre.value, self.direccion.value, self.telefono.value, self.dni.value)
            )
            self.db.commit()
            self.vista.snack_bar = ft.SnackBar(ft.Text("Persona actualizada correctamente"))
            self.vista.snack_bar.open = True
            self.mostrar_personas()
        except Exception as error:
            self.vista.snack_bar = ft.SnackBar(ft.Text("Error al actualizar: {}".format(error)))
            self.vista.snack_bar.open = True
            self.vista.update()

    def actualizar_persona(self, evento, persona):
        self.vista.clean()
        self.dni = ft.TextField(label="DNI", value=str(persona[2]), width=250, disabled=True)
        self.apellido = ft.TextField(label="Apellido", value=persona[0], width=250)
        self.nombre = ft.TextField(label="Nombre", value=persona[1], width=250)
        self.direccion = ft.TextField(label="Direccion", value=persona[3], width=250)
        self.telefono = ft.TextField(label="Telefono", value=persona[4], width=250)
        self.cod_cliente = ft.TextField(label="Codigo Persona", value=str(persona[5]), width=250, disabled=True)

        btn_guardar = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_edicion_persona(e, persona))
        btn_volver = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_personas)

        self.vista.add(
            ft.Column([
                ft.Text("Editar Persona", size=20, weight="bold"),
                self.dni,
                self.apellido,
                self.nombre,
                self.direccion,
                self.telefono,
                self.cod_cliente,
                ft.Row([btn_guardar, btn_volver], spacing=8),
            ], spacing=8)
        )
        self.vista.update()

    def eliminar_persona(self, evento, persona):
        try:
            dni = persona[2]
            cod_cliente = persona[5]
            self.cur.execute("DELETE FROM cliente WHERE cod_cliente = %s", (cod_cliente,))
            self.cur.execute("DELETE FROM persona WHERE dni = %s", (dni,))
            self.db.commit()
            self.vista.snack_bar = ft.SnackBar(ft.Text("Persona eliminada correctamente"))
            self.vista.snack_bar.open = True
            self.mostrar_personas()
        except Exception as error:
            self.vista.snack_bar = ft.SnackBar(ft.Text("Error al eliminar: {}".format(error)))
            self.vista.snack_bar.open = True
            self.vista.update()

    def guardar_nueva_persona(self, evento):
        try:
            self.cur.execute(
                "INSERT INTO persona (dni, apellido, nombre, direccion, tele_contac) VALUES (%s, %s, %s, %s, %s)",
                (self.dni.value, self.apellido.value, self.nombre.value, self.direccion.value, self.telefono.value)
            )
            self.cur.execute(
                "INSERT INTO cliente (cod_cliente, dni) VALUES (%s, %s)",
                (self.cod_cliente.value, self.dni.value)
            )
            self.db.commit()
            self.vista.snack_bar = ft.SnackBar(ft.Text("Persona guardada correctamente"))
            self.vista.snack_bar.open = True
            self.mostrar_personas()
        except Exception as error:
            self.vista.snack_bar = ft.SnackBar(ft.Text("Error al guardar: {}".format(error)))
            self.vista.snack_bar.open = True
            self.vista.update()

    def alta_persona(self, evento):
        self.vista.clean()
        self.dni = ft.TextField(label="DNI", width=250)
        self.apellido = ft.TextField(label="Apellido", width=250)
        self.nombre = ft.TextField(label="Nombre", width=250)
        self.direccion = ft.TextField(label="Direccion", width=250)
        self.telefono = ft.TextField(label="Telefono", width=250)
        self.cod_cliente = ft.TextField(label="Codigo Persona", width=250)

        btn_guardar = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_nueva_persona)
        btn_volver = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_personas)

        self.vista.add(
            ft.Column([
                ft.Text("Alta de Persona", size=20, weight="bold"),
                self.dni,
                self.apellido,
                self.nombre,
                self.direccion,
                self.telefono,
                self.cod_cliente,
                ft.Row([btn_guardar, btn_volver], spacing=8),
            ], spacing=8)
        )
        self.vista.update()

    def tabla_personas(self):
        if not self.cur:
            print("No hay conexion a la base de datos")
            return ft.Text("No hay conexion a la base de datos")

        consulta = """
            SELECT per.apellido, per.nombre, per.dni,
                   per.direccion, per.tele_contac, c.cod_cliente
            FROM persona per INNER JOIN cliente c ON per.dni = c.dni
            ORDER BY per.apellido
        """
        self.cur.execute(consulta)
        datos = self.cur.fetchall()
        filas = []

        for cli in datos:
            btn_borrar = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, c=cli: self.eliminar_persona(e, c),
            )
            btn_editar = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, c=cli: self.actualizar_persona(e, c),
            )
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(cli[0])),
                        ft.DataCell(ft.Text(cli[1])),
                        ft.DataCell(ft.Text(str(cli[2]))),
                        ft.DataCell(ft.Text(cli[3])),
                        ft.DataCell(ft.Text(cli[4])),
                        ft.DataCell(ft.Text(str(cli[5]))),
                        ft.DataCell(ft.Row(controls=[btn_borrar, btn_editar])),
                    ],
                ),
            )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("DNI")),
                ft.DataColumn(ft.Text("Direccion")),
                ft.DataColumn(ft.Text("Telefono")),
                ft.DataColumn(ft.Text("Codigo Persona")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=filas,
        )
        return tabla

    def mostrar_personas(self):
        self.vista.clean()
        fila_botones = ft.Row([
            ft.Text("Gestion de Personas", size=18, weight="bold"),
            ft.ElevatedButton(text="Alta", on_click=self.alta_persona),
            ft.ElevatedButton(text="Consulta", on_click=self.consulta_personas),
            ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_lista_personas),
            ft.ElevatedButton(text="Volver", on_click=self.volver_a_menu),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        tabla = self.tabla_personas()
        self.vista.add(
            ft.Column([
                fila_botones,
                tabla
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        self.vista.update()

def menu_hogar(p):
    p.clean()
    p.add(ft.Text("Menu Principal"))

def principal(p):
    app = VentanaPersonas(p, menu_hogar)
