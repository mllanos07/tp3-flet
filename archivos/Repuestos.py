import flet as ft
import pymysql

def llave_deposito():
    puerta = None
    try:
        puerta = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="taller_mecanico",
            ssl_disabled=True,
        )
        print("Conexion lista")
    except Exception as error:
        print("Error al abrir la base:", error)
    return puerta

class VentanaRepuesto:
    def __init__(self, ventana, volver_menu):
        self.pantalla = ventana
        self.volver_al_inicio = volver_menu
        self.bd = llave_deposito()
        self.cursor = self.bd.cursor() if self.bd else None
        self.mostrar_lista_repuestos()

    def volver_a_menu(self, evento):
        self.pantalla.clean()
        self.volver_al_inicio(self.pantalla)

    def imprimir_repuestos(self, evento):
        self.pantalla.snack_bar = ft.SnackBar(ft.Text("Impresion no implementada"))
        self.pantalla.snack_bar.open = True
        self.pantalla.update()

    def consulta_repuestos(self, evento):
        self.pantalla.clean()
        self.pantalla.add(ft.Text("Consulta de Repuestos", size=24, weight="bold"))
        self.pantalla.add(self.tabla_de_repuestos())
        self.pantalla.add(ft.ElevatedButton("Volver", on_click=self.mostrar_lista_repuestos))
        self.pantalla.update()

    def guardar_edicion(self, evento, pieza):
        try:
            self.cursor.execute(
                "UPDATE repuestos SET descripcion=%s, pcio_unit=%s WHERE cod_repuesto=%s",
                (self.descripcion.value, self.precio.value, self.cod_repuesto.value),
            )
            self.bd.commit()
            self.pantalla.snack_bar = ft.SnackBar(ft.Text("Repuesto actualizado correctamente"))
            self.pantalla.snack_bar.open = True
            self.mostrar_lista_repuestos()
        except Exception as error:
            self.pantalla.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {error}"))
            self.pantalla.snack_bar.open = True
            self.pantalla.update()

    def actualizar_repuesto(self, evento, pieza):
        self.pantalla.clean()
        self.cod_repuesto = ft.TextField(label="Codigo Repuesto", value=str(pieza[0]), width=300, disabled=True)
        self.descripcion = ft.TextField(label="Descripcion", value=pieza[1], width=300)
        self.precio = ft.TextField(label="Precio Unitario", value=str(pieza[2]), width=300)

        btn_guardar = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_edicion(e, pieza))
        btn_volver = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_lista_repuestos)

        self.pantalla.add(
            ft.Column(
                [
                    ft.Text("Editar Repuesto", size=24, weight="bold"),
                    self.cod_repuesto,
                    self.descripcion,
                    self.precio,
                    ft.Row([btn_guardar, btn_volver], spacing=10),
                ],
                spacing=10,
            )
        )
        self.pantalla.update()

    def eliminar_repuesto(self, evento, pieza):
        try:
            cod_repuesto = pieza[0]
            self.cursor.execute("DELETE FROM repuestos WHERE cod_repuesto = %s", (cod_repuesto,))
            self.bd.commit()
            self.pantalla.snack_bar = ft.SnackBar(ft.Text("Repuesto eliminado correctamente"))
            self.pantalla.snack_bar.open = True
            self.mostrar_lista_repuestos()
        except Exception as error:
            self.pantalla.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {error}"))
            self.pantalla.snack_bar.open = True
            self.pantalla.update()

    def guardar_nuevo_repuesto(self, evento):
        try:
            if not self.cod_repuesto.value or not self.descripcion.value or not self.precio.value:
                self.pantalla.snack_bar = ft.SnackBar(ft.Text("Todos los campos son obligatorios"))
                self.pantalla.snack_bar.open = True
                self.pantalla.update()
                return

            self.cursor.execute("SELECT cod_repuesto FROM repuestos WHERE cod_repuesto=%s", (self.cod_repuesto.value,))
            if self.cursor.fetchone():
                self.pantalla.snack_bar = ft.SnackBar(ft.Text("El codigo ya existe"))
                self.pantalla.snack_bar.open = True
                self.pantalla.update()
                return

            try:
                precio = float(self.precio.value)
            except ValueError:
                self.pantalla.snack_bar = ft.SnackBar(ft.Text("El precio debe ser un numero"))
                self.pantalla.snack_bar.open = True
                self.pantalla.update()
                return

            self.cursor.execute(
                "INSERT INTO repuestos (cod_repuesto, descripcion, pcio_unit) VALUES (%s, %s, %s)",
                (self.cod_repuesto.value, self.descripcion.value, precio),
            )
            self.bd.commit()
            self.pantalla.snack_bar = ft.SnackBar(ft.Text("Repuesto guardado correctamente"))
            self.pantalla.snack_bar.open = True
            self.mostrar_lista_repuestos()
        except Exception as error:
            self.pantalla.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {error}"))
            self.pantalla.snack_bar.open = True
            self.pantalla.update()

    def alta_repuesto(self, evento):
        self.pantalla.clean()
        self.cod_repuesto = ft.TextField(label="Codigo Repuesto", width=300)
        self.descripcion = ft.TextField(label="Descripcion", width=300)
        self.precio = ft.TextField(label="Precio Unitario", width=300)

        btn_guardar = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_nuevo_repuesto)
        btn_volver = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_lista_repuestos)

        self.pantalla.add(
            ft.Column(
                [
                    ft.Text("Alta de Repuesto", size=24, weight="bold"),
                    self.cod_repuesto,
                    self.descripcion,
                    self.precio,
                    ft.Row([btn_guardar, btn_volver], spacing=10),
                ],
                spacing=10,
            )
        )
        self.pantalla.update()

    def tabla_de_repuestos(self):
        if not self.cursor:
            print("No hay conexion a la base de datos")
            return ft.Text("No hay conexion a la base de datos")

        consulta = """
            SELECT cod_repuesto, descripcion, pcio_unit
            FROM repuestos
            ORDER BY cod_repuesto
        """
        self.cursor.execute(consulta)
        datos = self.cursor.fetchall()
        filas = []

        for pieza in datos:
            btn_borrar = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, p=pieza: self.eliminar_repuesto(e, p),
            )
            btn_editar = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, p=pieza: self.actualizar_repuesto(e, p),
            )
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(pieza[0]))),
                        ft.DataCell(ft.Text(pieza[1])),
                        ft.DataCell(ft.Text(str(pieza[2]))),
                        ft.DataCell(ft.Row(controls=[btn_borrar, btn_editar])),
                    ],
                ),
            )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Codigo Repuesto")),
                ft.DataColumn(ft.Text("Descripcion")),
                ft.DataColumn(ft.Text("Precio Unitario")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=filas,
        )
        return tabla

    def mostrar_lista_repuestos(self):
        self.pantalla.clean()
        cabecera = ft.Row(
            controls=[
                ft.Text("Gestion de Repuestos", size=20, weight="bold"),
                ft.ElevatedButton(text="Alta", on_click=self.alta_repuesto),
                ft.ElevatedButton(text="Consulta", on_click=self.consulta_repuestos),
                ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_repuestos),
                ft.ElevatedButton(text="Volver al Menu", on_click=self.volver_a_menu),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        tabla = self.tabla_de_repuestos()
        self.pantalla.add(
            ft.Container(
                content=ft.Column(
                    controls=[cabecera, tabla],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        )
