import flet as ft
import pymysql

def puerta_contactos():
    conexion = None
    try:
        conexion = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="taller_mecanico",
            ssl_disabled=True
        )
        print("Conexion lista")
    except Exception as error:
        print("Error de conexion:", error)
    return conexion

class VentanaSocios:
    def __init__(self, pantalla, volver_a_inicio):
        self.vista = pantalla
        self.volver_menu_principal = volver_a_inicio
        self.db = puerta_contactos()
        if self.db:
            self.cur = self.db.cursor()
        else:
            self.cur = None
        self.mostrar_socios()

    def volver_a_menu(self, evento):
        self.vista.clean()
        self.volver_menu_principal(self.vista)

    def imprimir_lista_socios(self, evento):
        self.vista.snack_bar = ft.SnackBar(ft.Text("No se puede imprimir todavia"))
        self.vista.snack_bar.open = True
        self.vista.update()

    def consulta_socios(self, evento):
        self.vista.clean()
        self.vista.add(ft.Text("Consulta de Socios", size=20, weight="bold"))
        self.vista.add(self.tabla_socios())
        self.vista.add(ft.ElevatedButton("Volver", on_click=self.mostrar_socios))
        self.vista.update()

    def guardar_edicion(self, evento, socio):
        try:
            self.cur.execute(
                "UPDATE proveedor SET nombre=%s, direccion=%s, telefono=%s, email=%s WHERE cod_proveedor=%s",
                (self.nombre.value, self.direccion.value, self.telefono.value, self.email.value, self.cod_proveedor.value)
            )
            self.db.commit()
            self.vista.snack_bar = ft.SnackBar(ft.Text("Socio actualizado correctamente"))
            self.vista.snack_bar.open = True
            self.mostrar_socios()
        except Exception as error:
            self.vista.snack_bar = ft.SnackBar(ft.Text("Error al actualizar: {}".format(error)))
            self.vista.snack_bar.open = True
            self.vista.update()

    def actualizar_socio(self, evento, socio):
        self.vista.clean()
        self.cod_proveedor = ft.TextField(label="Codigo Socio", value=str(socio[0]), width=250, disabled=True)
        self.nombre = ft.TextField(label="Nombre", value=socio[1], width=250)
        self.direccion = ft.TextField(label="Direccion", value=socio[2], width=250)
        self.telefono = ft.TextField(label="Telefono", value=socio[3], width=250)
        self.email = ft.TextField(label="Email", value=socio[4], width=250)

        btn_guardar = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_edicion(e, socio))
        btn_volver = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_socios)

        self.vista.add(
            ft.Column([
                ft.Text("Editar Socio", size=20, weight="bold"),
                self.cod_proveedor,
                self.nombre,
                self.direccion,
                self.telefono,
                self.email,
                ft.Row([btn_guardar, btn_volver], spacing=8),
            ], spacing=8)
        )
        self.vista.update()

    def eliminar_socio(self, evento, socio):
        try:
            cod_proveedor = socio[0]
            self.cur.execute("DELETE FROM proveedor WHERE cod_proveedor = %s", (cod_proveedor,))
            self.db.commit()
            self.vista.snack_bar = ft.SnackBar(ft.Text("Socio eliminado correctamente"))
            self.vista.snack_bar.open = True
            self.mostrar_socios()
        except Exception as error:
            self.vista.snack_bar = ft.SnackBar(ft.Text("Error al eliminar: {}".format(error)))
            self.vista.snack_bar.open = True
            self.vista.update()

    def guardar_nuevo(self, evento):
        try:
            self.cur.execute(
                "INSERT INTO proveedor (cod_proveedor, nombre, direccion, telefono, email) VALUES (%s, %s, %s, %s, %s)",
                (self.cod_proveedor.value, self.nombre.value, self.direccion.value, self.telefono.value, self.email.value)
            )
            self.db.commit()
            self.vista.snack_bar = ft.SnackBar(ft.Text("Socio guardado correctamente"))
            self.vista.snack_bar.open = True
            self.mostrar_socios()
        except Exception as error:
            self.vista.snack_bar = ft.SnackBar(ft.Text("Error al guardar: {}".format(error)))
            self.vista.snack_bar.open = True
            self.vista.update()

    def alta_socio(self, evento):
        self.vista.clean()
        self.cod_proveedor = ft.TextField(label="Codigo Socio", width=250)
        self.nombre = ft.TextField(label="Nombre", width=250)
        self.direccion = ft.TextField(label="Direccion", width=250)
        self.telefono = ft.TextField(label="Telefono", width=250)
        self.email = ft.TextField(label="Email", width=250)

        btn_guardar = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_nuevo)
        btn_volver = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_socios)

        self.vista.add(
            ft.Column([
                ft.Text("Alta de Socio", size=20, weight="bold"),
                self.cod_proveedor,
                self.nombre,
                self.direccion,
                self.telefono,
                self.email,
                ft.Row([btn_guardar, btn_volver], spacing=8),
            ], spacing=8)
        )
        self.vista.update()

    def tabla_socios(self):
        if not self.cur:
            print("No hay conexion a la base de datos")
            return ft.Text("No hay conexion a la base de datos")

        consulta = """
            SELECT cod_proveedor, nombre, direccion, telefono, email
            FROM proveedor
            ORDER BY nombre
        """
        self.cur.execute(consulta)
        datos = self.cur.fetchall()
        filas = []

        for socio in datos:
            btn_borrar = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, s=socio: self.eliminar_socio(e, s),
            )
            btn_editar = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, s=socio: self.actualizar_socio(e, s),
            )
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(socio[0]))),
                        ft.DataCell(ft.Text(socio[1])),
                        ft.DataCell(ft.Text(socio[2])),
                        ft.DataCell(ft.Text(socio[3])),
                        ft.DataCell(ft.Text(socio[4])),
                        ft.DataCell(ft.Row(controls=[btn_borrar, btn_editar])),
                    ],
                ),
            )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Codigo Socio")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Direccion")),
                ft.DataColumn(ft.Text("Telefono")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=filas,
        )
        return tabla

    def mostrar_socios(self):
        self.vista.clean()
        fila_botones = ft.Row([
            ft.Text("Gestion de Socios", size=18, weight="bold"),
            ft.ElevatedButton(text="Alta", on_click=self.alta_socio),
            ft.ElevatedButton(text="Consulta", on_click=self.consulta_socios),
            ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_lista_socios),
            ft.ElevatedButton(text="Volver", on_click=self.volver_a_menu),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        tabla = self.tabla_socios()
        self.vista.add(
            ft.Column([
                fila_botones,
                tabla
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
