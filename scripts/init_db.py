import pymysql
import os
import sys

CONFIG_DB = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "taller_mecanico",
}

SQL_CREAR_REPUESTOS = """
CREATE TABLE IF NOT EXISTS repuestos (
  cod_repuesto VARCHAR(30) NOT NULL PRIMARY KEY,
  descripcion VARCHAR(255) DEFAULT NULL,
  pcio_unit FLOAT DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

SQL_CREAR_PROVEEDOR = """
CREATE TABLE IF NOT EXISTS proveedor (
    cod_proveedor VARCHAR(30) NOT NULL PRIMARY KEY,
    nombre VARCHAR(255) DEFAULT NULL,
    direccion VARCHAR(255) DEFAULT NULL,
    telefono VARCHAR(50) DEFAULT NULL,
    email VARCHAR(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

if __name__ == "__main__":
    # ejecuta el archivo
    try:
        conexion = pymysql.connect(**CONFIG_DB, ssl_disabled=True)
        with conexion.cursor() as cursor:
            cursor.execute(SQL_CREAR_REPUESTOS)
            cursor.execute(SQL_CREAR_PROVEEDOR)
        conexion.commit()
        print("Tabla 'repuestos' creada o ya existente.")
        print("Tabla 'proveedor' creada o ya existente.")

        # busca archivo sql dentro del proyecto
        ruta_sql = os.path.join(os.path.dirname(os.path.dirname(__file__)), "archivos", "taller_mecanico.sql")
        if os.path.exists(ruta_sql):
            print(f"Encontrado SQL dump en: {ruta_sql} — intentando ejecutar...")
            # Abre el archivo en modo lectura
            with open(ruta_sql, "r", encoding="utf-8") as f:
                # lee y guarda contenidio
                texto_sql = f.read()

            sentencias = [] #guarda lineas
            partes = [] # gurda ordenes
            for linea in texto_sql.splitlines():
                linea_limpia = linea.strip() # Limpia la línea
                if not linea_limpia or linea_limpia.startswith("--") or linea_limpia.startswith("/*") or linea_limpia.startswith("*/"):
                    continue
                partes.append(linea)
                if linea_limpia.endswith(";"):
                    sentencia = "\n".join(partes).strip()
                    if sentencia.endswith(";"): # si termina en ; termino
                        sentencia = sentencia[:-1]
                    if sentencia:
                        sentencias.append(sentencia)
                    partes = []
                    
            # toma odenes sql y ejecuta una por una
            ejecutadas = 0
            with conexion.cursor() as cursor2: # escribe en DB
                try:
                    cursor2.execute("SET FOREIGN_KEY_CHECKS=0;") # apaga comprovaciones
                except Exception:
                    pass

                for sentencia in sentencias: # recorrer odenes
                    s = sentencia.strip() # limpia oden
                    if not s:
                        # si queda vacia la salta
                        continue
                    # Filtra cosas que no queremos ejecutar
                    mayus = s.upper()
                    if mayus.startswith("CREATE DATABASE") or mayus.startswith("USE ") or mayus.startswith("LOCK TABLES") or mayus.startswith("UNLOCK TABLES") or s.startswith("/*!"):
                        continue # evita duplicados
                    try:
                        cursor2.execute(s) # ejecuta orden valida
                        ejecutadas = ejecutadas + 1
                    except Exception as error_sentencia: # en caso de falla muetra error y sigue
                        print(f"Omitiendo statement por error: {error_sentencia}\n-- Statement start --\n{s}\n-- Statement end --")

                try:
                    cursor2.execute("SET FOREIGN_KEY_CHECKS=1;") # encender claves foraneas
                except Exception:
                    pass

            conexion.commit()
            # cuantas se ejecutaron bien
            print(f"Ejecución del SQL dump completada. Statements ejecutados: {ejecutadas}")
        else:
            print(f"No se encontró {ruta_sql}; salto de import completo del dump.")
    except Exception as error: # cuenta errores grandes
        print("Error al inicializar la base de datos:", error)
    finally: # cierra conexion, bien o mal
        try:
            conexion.close()
        except Exception:
            pass
