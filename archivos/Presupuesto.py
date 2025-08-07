import flet as ft
import pymysql

def conectar_billetera():
    caja = None
    try:
        caja = pymysql.connect(
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
    return caja

class VentanaCuentas:
    def __init__(self, pantalla, volver_a_inicio):
        self.vista = pantalla
        self.volver_menu_principal = volver_a_inicio
        self.db = conectar_billetera()
        if self.db:
            self.cur = self.db.cursor()
        else:
            self.cur = None
        self.mostrar_cuentas()

    def volver_a_menu(self, evento):
        self.vista.clean()
        self.volver_menu_principal(self.vista)

    def imprimir_cuentas(self, evento):
        self.vista.snack_bar = ft.SnackBar(ft.Text("No se puede imprimir todavia"))
        self.vista.snack_bar.open = True
        self.vista.update()

    def consulta_cuentas(self, evento):
        self.vista.clean()
        tabla, total_presu, total_gasto = self.tabla_cuentas()
        self.vista.add(ft.Text("Consulta de Cuentas", size=20, weight="bold"))
        self.vista.add(ft.Text(f"Total Presupuestado: ${total_presu}", size=16, weight="bold"))
        self.vista.add(ft.Text(f"Total Gastado: ${total_gasto}", size=16, weight="bold"))
        self.vista.add(tabla)
        self.vista.add(ft.ElevatedButton("Volver", on_click=self.mostrar_cuentas))
        self.vista.update()

    def guardar_edicion(self, evento, cuenta):
        try:
            self.cur.execute(
                "UPDATE presupuesto SET cod_cliente=%s, descripcion=%s, total_presupuesto=%s, total_gastado=%s WHERE nro_presupuesto=%s",
                (self.cod_cliente.value, self.descripcion.value, self.total_presupuesto.value, self.total_gastado.value, self.nro_presupuesto.value)
            )
            self.db.commit()
            self.vista.snack_bar = ft.SnackBar(ft.Text("Cuenta actualizada correctamente"))
            self.vista.snack_bar.open = True
            self.mostrar_cuentas()
        except Exception as error:
            self.vista.snack_bar = ft.SnackBar(ft.Text("Error al actualizar: {}".format(error)))
            self.vista.snack_bar.open = True
            self.vista.update()

    def actualizar_cuenta(self, evento, cuenta):
        self.vista.clean()
        self.nro_presupuesto = ft.TextField(label="Nro Cuenta", value=str(cuenta[0]), width=250, disabled=True)
        self.cod_cliente = ft.TextField(label="Codigo Cliente", value=str(cuenta[1]), width=250)
        self.descripcion = ft.TextField(label="Descripcion", value=cuenta[2], width=250)
        self.total_presupuesto = ft.TextField(label="Total Presupuestado", value=str(cuenta[3]), width=250)
        self.total_gastado = ft.TextField(label="Total Gastado", value=str(cuenta[4]), width=250)

        btn_guardar = ft.ElevatedButton("Guardar Cambios", icon=ft.Icons.SAVE, on_click=lambda e: self.guardar_edicion(e, cuenta))
        btn_volver = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_cuentas)

        self.vista.add(
            ft.Column([
                ft.Text("Editar Cuenta", size=20, weight="bold"),
                self.nro_presupuesto,
                self.cod_cliente,
                self.descripcion,
                self.total_presupuesto,
                self.total_gastado,
                ft.Row([btn_guardar, btn_volver], spacing=8),
            ], spacing=8)
        )
        self.vista.update()

    def eliminar_cuenta(self, evento, cuenta):
        try:
            nro_presupuesto = cuenta[0]
            self.cur.execute("DELETE FROM presupuesto WHERE nro_presupuesto = %s", (nro_presupuesto,))
            self.db.commit()
            self.vista.snack_bar = ft.SnackBar(ft.Text("Cuenta eliminada correctamente"))
            self.vista.snack_bar.open = True
            self.mostrar_cuentas()
        except Exception as error:
            self.vista.snack_bar = ft.SnackBar(ft.Text("Error al eliminar: {}".format(error)))
            self.vista.snack_bar.open = True
            self.vista.update()

    def guardar_nueva_cuenta(self, evento):
        try:
            self.cur.execute(
                "INSERT INTO presupuesto (nro_presupuesto, cod_cliente, descripcion, total_presupuesto, total_gastado) VALUES (%s, %s, %s, %s, %s)",
                (self.nro_presupuesto.value, self.cod_cliente.value, self.descripcion.value, self.total_presupuesto.value, self.total_gastado.value)
            )
            self.db.commit()
            self.vista.snack_bar = ft.SnackBar(ft.Text("Cuenta guardada correctamente"))
            self.vista.snack_bar.open = True
            self.mostrar_cuentas()
        except Exception as error:
            self.vista.snack_bar = ft.SnackBar(ft.Text("Error al guardar: {}".format(error)))
            self.vista.snack_bar.open = True
            self.vista.update()

    def alta_cuenta(self, evento):
        self.vista.clean()
        self.nro_presupuesto = ft.TextField(label="Nro Cuenta", width=250)
        self.cod_cliente = ft.TextField(label="Codigo Cliente", width=250)
        self.descripcion = ft.TextField(label="Descripcion", width=250)
        self.total_presupuesto = ft.TextField(label="Total Presupuestado", width=250)
        self.total_gastado = ft.TextField(label="Total Gastado", width=250)

        btn_guardar = ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=self.guardar_nueva_cuenta)
        btn_volver = ft.ElevatedButton("Volver", icon=ft.Icons.ARROW_BACK, on_click=self.mostrar_cuentas)

        self.vista.add(
            ft.Column([
                ft.Text("Alta de Cuenta", size=20, weight="bold"),
                self.nro_presupuesto,
                self.cod_cliente,
                self.descripcion,
                self.total_presupuesto,
                self.total_gastado,
                ft.Row([btn_guardar, btn_volver], spacing=8),
            ], spacing=8)
        )
        self.vista.update()

    def tabla_cuentas(self):
        if not self.cur:
            print("No hay conexion a la base de datos")
            return ft.Text("No hay conexion a la base de datos"), 0, 0

        consulta = """
            SELECT nro_presupuesto, cod_cliente, descripcion, total_presupuesto, total_gastado
            FROM presupuesto
            ORDER BY nro_presupuesto
        """
        self.cur.execute(consulta)
        datos = self.cur.fetchall()
        filas = []

        total_presu = 0
        total_gasto = 0

        for cuenta in datos:
            total_presu += float(cuenta[3] or 0)
            total_gasto += float(cuenta[4] or 0)
            btn_borrar = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Borrar",
                on_click=lambda e, c=cuenta: self.eliminar_cuenta(e, c),
            )
            btn_editar = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Modificar",
                on_click=lambda e, c=cuenta: self.actualizar_cuenta(e, c),
            )
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(cuenta[0]))),
                        ft.DataCell(ft.Text(str(cuenta[1]))),
                        ft.DataCell(ft.Text(cuenta[2])),
                        ft.DataCell(ft.Text(str(cuenta[3]))),
                        ft.DataCell(ft.Text(str(cuenta[4]))),
                        ft.DataCell(ft.Row(controls=[btn_borrar, btn_editar])),
                    ],
                ),
            )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nro Cuenta")),
                ft.DataColumn(ft.Text("Codigo Cliente")),
                ft.DataColumn(ft.Text("Descripcion")),
                ft.DataColumn(ft.Text("Total Presupuestado")),
                ft.DataColumn(ft.Text("Total Gastado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=filas,
        )
        return tabla, total_presu, total_gasto

    def mostrar_cuentas(self):
        self.vista.clean()
        fila_botones = ft.Row([
            ft.Text("Gestion de Cuentas", size=18, weight="bold"),
            ft.ElevatedButton(text="Alta", on_click=self.alta_cuenta),
            ft.ElevatedButton(text="Consulta", on_click=self.consulta_cuentas),
            ft.ElevatedButton(text="Imprimir", on_click=self.imprimir_cuentas),
            ft.ElevatedButton(text="Volver", on_click=self.volver_a_menu),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        tabla, total_presu, total_gasto = self.tabla_cuentas()
        self.vista.add(
            ft.Column([
                fila_botones,
                ft.Text(f"Total Presupuestado: ${total_presu}", size=16, weight="bold"),
                ft.Text(f"Total Gastado: ${total_gasto}", size=16, weight="bold"),
                tabla
            ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
