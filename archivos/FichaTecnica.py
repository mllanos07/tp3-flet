import flet as ft
import pymysql

def abrir_carpeta_fichas():
    llave = None
    try:
        llave = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="taller_mecanico",
            ssl_disabled=True
        )
        print("Conexion lista")
    except Exception as error:
        print("Error al conectar:", error)
    return llave

class VentanaFichas:
    def __init__(self, ventana, volver_menu):
        self.pantalla = ventana
        self.volver_al_inicio = volver_menu
        self.bd = abrir_carpeta_fichas()
        if self.bd:
            self.cursor = self.bd.cursor()
        else:
            self.cursor = None
        self.mostrar_fichas()

    def volver_a_menu(self, evento=None):
        self.pantalla.clean()
        self.volver_al_inicio(self.pantalla)

    def imprimir_fichas(self, evento=None):
        self.pantalla.snack_bar = ft.SnackBar(ft.Text("Impresion no disponible"))
        self.pantalla.snack_bar.open = True
        self.pantalla.update()

    def consulta_fichas(self, evento=None):
        self.pantalla.clean()
        self.pantalla.add(ft.Text("Consulta de Fichas", size=20, weight="bold"))
        self.pantalla.add(self.tabla_fichas())
        self.pantalla.add(ft.ElevatedButton("Volver", on_click=self.mostrar_fichas))
        self.pantalla.update()

    def guardar_cambios_ficha(self, evento=None, ficha=None):
        try:
            self.cursor.execute(
                "UPDATE ficha_tecnica SET cod_cliente=%s, vehiculo=%s, subtotal=%s, mano_obra=%s, total_general=%s WHERE nro_ficha=%s",
                (self.cod_cliente.value, self.vehiculo.value, self.subtotal.value, self.mano_obra.value, self.total_general.value, self.nro_ficha.value)
            )
            self.bd.commit()
            self.pantalla.snack_bar = ft.SnackBar(ft.Text("Ficha actualizada correctamente"))
            self.pantalla.snack_bar.open = True
            self.mostrar_fichas()
        except Exception as error:
            self.pantalla.snack_bar = ft.SnackBar(ft.Text("Error al actualizar: {}".format(error)))
            self.pantalla.snack_bar.open = True
            self.pantalla.update()

    def actualizar_ficha(self, evento=None, ficha=None):
        self.pantalla.clean()
        self.nro_ficha = ft.TextField(label="Nro Ficha", value=str(ficha[0]), width=250, disabled=True)
        self.cod_cliente = ft.TextField(label="Codigo Cliente", value=str(ficha[1]), width=250)
        self.vehiculo = ft.TextField(label="Vehiculo", value=ficha[2], width=250)
        self.subtotal = ft.TextField(label="Subtotal", value=str(ficha[3]), width=250)
        self.mano_obra = ft.TextField(label="Mano de Obra", value=str(ficha[4]), width=250)
        self.total_general = ft.TextField(label="Total General", value=str(ficha[5]), width=250)

        btn_guardar = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_cambios_ficha(e, ficha))
        btn_volver = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_fichas)

        self.pantalla.add(
            ft.Column([
                ft.Text("Editar Ficha", size=20, weight="bold"),
                self.nro_ficha,
                self.cod_cliente,
                self.vehiculo,
                self.subtotal,
                self.mano_obra,
                self.total_general,
                ft.Row([btn_guardar, btn_volver], spacing=8),
            ], spacing=8)
        )
        self.pantalla.update()

    def eliminar_ficha(self, evento=None, ficha=None):
        try:
            nro_ficha = ficha[0]
            self.cursor.execute("DELETE FROM ficha_tecnica WHERE nro_ficha = %s", (nro_ficha,))
            self.bd.commit()
            self.pantalla.snack_bar = ft.SnackBar(ft.Text("Ficha eliminada correctamente"))
            self.pantalla.snack_bar.open = True
            self.mostrar_fichas()
        except Exception as error:
            self.pantalla.snack_bar = ft.SnackBar(ft.Text("Error al eliminar: {}".format(error)))
            self.pantalla.snack_bar.open = True
            self.pantalla.update()

    def guardar_nueva_ficha(self, evento=None):
        try:
            if not self.nro_ficha.value or not self.vehiculo.value:
                self.pantalla.snack_bar = ft.SnackBar(ft.Text("Nro Ficha y Vehiculo son obligatorios"))
                self.pantalla.snack_bar.open = True
                self.pantalla.update()
                return

            try:
                nro_ficha = int(self.nro_ficha.value)
            except ValueError:
                self.pantalla.snack_bar = ft.SnackBar(ft.Text("Nro Ficha debe ser un numero entero"))
                self.pantalla.snack_bar.open = True
                self.pantalla.update()
                return

            cod_cliente = self.cod_cliente.value if self.cod_cliente.value else None
            if cod_cliente:
                self.cursor.execute("SELECT cod_cliente FROM cliente WHERE cod_cliente=%s", (cod_cliente,))
                if not self.cursor.fetchone():
                    self.pantalla.snack_bar = ft.SnackBar(ft.Text("El codigo de cliente no existe"))
                    self.pantalla.snack_bar.open = True
                    self.pantalla.update()
                    return

            try:
                subtotal = float(self.subtotal.value) if self.subtotal.value else None
            except ValueError:
                self.pantalla.snack_bar = ft.SnackBar(ft.Text("Subtotal debe ser un numero"))
                self.pantalla.snack_bar.open = True
                self.pantalla.update()
                return
            try:
                mano_obra = float(self.mano_obra.value) if self.mano_obra.value else None
            except ValueError:
                self.pantalla.snack_bar = ft.SnackBar(ft.Text("Mano de Obra debe ser un numero"))
                self.pantalla.snack_bar.open = True
                self.pantalla.update()
                return
            try:
                total_general = float(self.total_general.value) if self.total_general.value else None
            except ValueError:
                self.pantalla.snack_bar = ft.SnackBar(ft.Text("Total General debe ser un numero"))
                self.pantalla.snack_bar.open = True
                self.pantalla.update()
                return

            self.cursor.execute(
                "INSERT INTO ficha_tecnica (nro_ficha, cod_cliente, vehiculo, subtotal, mano_obra, total_general) VALUES (%s, %s, %s, %s, %s, %s)",
                (nro_ficha, cod_cliente, self.vehiculo.value, subtotal, mano_obra, total_general)
            )
            self.bd.commit()
            self.pantalla.snack_bar = ft.SnackBar(ft.Text("Ficha guardada correctamente"))
            self.pantalla.snack_bar.open = True
            self.mostrar_fichas()
        except Exception as error:
            self.pantalla.snack_bar = ft.SnackBar(ft.Text("Error al guardar: {}".format(error)))
            self.pantalla.snack_bar.open = True
            self.pantalla.update()

    def alta_ficha(self, evento=None):
        self.pantalla.clean()
        self.nro_ficha = ft.TextField(label="Nro Ficha", width=250)
        self.cod_cliente = ft.TextField(label="Codigo Cliente", width=250)
        self.vehiculo = ft.TextField(label="Vehiculo", width=250)
        self.subtotal = ft.TextField(label="Subtotal", width=250)
        self.mano_obra = ft.TextField(label="Mano de Obra", width=250)
        self.total_general = ft.TextField(label="Total General", width=250)

        btn_guardar = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_nueva_ficha)
        btn_volver = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_fichas)

        self.pantalla.add(
            ft.Column([
                ft.Text("Alta de Ficha", size=20, weight="bold"),
                self.nro_ficha,
                self.cod_cliente,
                self.vehiculo,
                self.subtotal,
                self.mano_obra,
                self.total_general,
                ft.Row([btn_guardar, btn_volver], spacing=8),
            ], spacing=8)
        )
        self.pantalla.update()

    def tabla_fichas(self):
        if not self.cursor:
            print("No hay conexion a la base de datos")
            return ft.Text("No hay conexion a la base de datos")

        consulta = """
            SELECT nro_ficha, cod_cliente, vehiculo, subtotal, mano_obra, total_general
            FROM ficha_tecnica
            ORDER BY nro_ficha
        """
        self.cursor.execute(consulta)
        datos = self.cursor.fetchall()
        filas = []

        for ficha in datos:
            btn_borrar = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, f=ficha: self.eliminar_ficha(e, f),
            )
            btn_editar = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, f=ficha: self.actualizar_ficha(e, f),
            )
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(ficha[0]))),
                        ft.DataCell(ft.Text(str(ficha[1]))),
                        ft.DataCell(ft.Text(ficha[2])),
                        ft.DataCell(ft.Text(str(ficha[3]))),
                        ft.DataCell(ft.Text(str(ficha[4]))),
                        ft.DataCell(ft.Text(str(ficha[5]))),
                        ft.DataCell(ft.Row(controls=[btn_borrar, btn_editar])),
                    ],
                ),
            )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nro Ficha")),
                ft.DataColumn(ft.Text("Codigo Cliente")),
                ft.DataColumn(ft.Text("Vehiculo")),
                ft.DataColumn(ft.Text("Subtotal")),
                ft.DataColumn(ft.Text("Mano de Obra")),
                ft.DataColumn(ft.Text("Total General")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=filas,
        )
        return tabla

    def mostrar_fichas(self, evento=None):
        self.pantalla.clean()
        fila_botones = ft.Row([
            ft.Text("Gestion de Fichas", size=18, weight="bold"),
            ft.ElevatedButton(text="Alta", on_click=self.alta_ficha),
            ft.ElevatedButton(text="Consulta", on_click=self.consulta_fichas),
            ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_fichas),
            ft.ElevatedButton(text="Volver", on_click=self.volver_a_menu),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        tabla = self.tabla_fichas()
        self.pantalla.add(
            ft.Column([
                fila_botones,
                tabla
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
