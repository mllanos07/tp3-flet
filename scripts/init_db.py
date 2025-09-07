import pymysql
import os
import sys

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "taller_mecanico",
}

CREATE_REPUESTOS = """
CREATE TABLE IF NOT EXISTS repuestos (
  cod_repuesto VARCHAR(30) NOT NULL PRIMARY KEY,
  descripcion VARCHAR(255) DEFAULT NULL,
  pcio_unit FLOAT DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

CREATE_PROVEEDOR = """
CREATE TABLE IF NOT EXISTS proveedor (
    cod_proveedor VARCHAR(30) NOT NULL PRIMARY KEY,
    nombre VARCHAR(255) DEFAULT NULL,
    direccion VARCHAR(255) DEFAULT NULL,
    telefono VARCHAR(50) DEFAULT NULL,
    email VARCHAR(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

if __name__ == "__main__":
    try:
        conn = pymysql.connect(**DB_CONFIG, ssl_disabled=True)
        with conn.cursor() as cur:
            cur.execute(CREATE_REPUESTOS)
            cur.execute(CREATE_PROVEEDOR)
        conn.commit()
        print("Tabla 'repuestos' creada o ya existente.")
        print("Tabla 'proveedor' creada o ya existente.")

        sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'archivos', 'taller_mecanico.sql')
        if os.path.exists(sql_path):
            print(f"Encontrado SQL dump en: {sql_path} — intentando ejecutar...")
            with open(sql_path, 'r', encoding='utf-8') as f:
                sql_text = f.read()

            statements = []
            cur_stmt = []
            for line in sql_text.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith('--') or stripped.startswith('/*') or stripped.startswith('*/'):
                    continue
                cur_stmt.append(line)
                if stripped.endswith(';'):
                    stmt = '\n'.join(cur_stmt).strip()
                    if stmt.endswith(';'):
                        stmt = stmt[:-1]
                    if stmt:
                        statements.append(stmt)
                    cur_stmt = []

            executed = 0
            with conn.cursor() as cur2:
                try:
                    cur2.execute("SET FOREIGN_KEY_CHECKS=0;")
                except Exception:
                    pass

                for stmt in statements:
                    s = stmt.strip()
                    if not s:
                        continue
                    up = s.upper()
                    if up.startswith("CREATE DATABASE") or up.startswith("USE ") or up.startswith("LOCK TABLES") or up.startswith("UNLOCK TABLES") or s.startswith('/*!'):
                        continue
                    try:
                        cur2.execute(s)
                        executed += 1
                    except Exception as ex_stmt:
                        print(f"Omitiendo statement por error: {ex_stmt}\n-- Statement start --\n{s}\n-- Statement end --")

                try:
                    cur2.execute("SET FOREIGN_KEY_CHECKS=1;")
                except Exception:
                    pass
            conn.commit()
            print(f"Ejecución del SQL dump completada. Statements ejecutados: {executed}")
        else:
            print(f"No se encontró {sql_path}; salto de import completo del dump.")
    except Exception as ex:
        print("Error al inicializar la base de datos:", ex)
    finally:
        try:
            conn.close()
        except Exception:
            pass
