import sqlite3
import os
from pathlib import Path

DB_PATH = Path('database.db')

def get_db_connection():
    """Obtiene una conexión a la base de datos SQLite"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def init_db():
    """Inicializa la base de datos con las tablas necesarias"""
    conn = get_db_connection()
    if conn is not None:
        try:
            with conn:
                # Crear tablas
                conn.executescript('''
                    CREATE TABLE IF NOT EXISTS estudiantes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        dni TEXT UNIQUE NOT NULL,
                        nombre TEXT NOT NULL,
                        apellido TEXT NOT NULL,
                        fecha_nacimiento TEXT,
                        genero TEXT,
                        direccion TEXT,
                        telefono_emergencia TEXT,
                        grado TEXT NOT NULL,
                        fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP,
                        activo INTEGER DEFAULT 1,
                        doble_jornada INTEGER DEFAULT 0
                    );

                    CREATE TABLE IF NOT EXISTS tutores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_estudiante INTEGER NOT NULL,
                        tipo_tutor TEXT NOT NULL,
                        dni TEXT,
                        nombre_completo TEXT,
                        telefono TEXT,
                        email TEXT,
                        parentesco TEXT,
                        FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id)
                    );

                    CREATE TABLE IF NOT EXISTS items_precio (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nivel TEXT NOT NULL,
                        nombre TEXT NOT NULL,
                        monto REAL NOT NULL,
                        activo INTEGER DEFAULT 1,
                        solo_doble_jornada INTEGER DEFAULT 0,
                        item_mantenimiento INTEGER DEFAULT 0
                    );

                    CREATE TABLE IF NOT EXISTS cupones_pago (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_estudiante INTEGER NOT NULL,
                        año_academico INTEGER NOT NULL,
                        mes INTEGER NOT NULL,
                        nivel TEXT NOT NULL,
                        grado TEXT NOT NULL,
                        monto_total REAL NOT NULL,
                        es_cargo_especial INTEGER DEFAULT 0,
                        porcentaje_cargo_especial REAL DEFAULT 0,
                        estado TEXT DEFAULT 'active',
                        fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id)
                    );

                    CREATE TABLE IF NOT EXISTS items_cupon (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cupon INTEGER NOT NULL,
                        id_item INTEGER NOT NULL,
                        monto REAL NOT NULL,
                        FOREIGN KEY (id_cupon) REFERENCES cupones_pago(id),
                        FOREIGN KEY (id_item) REFERENCES items_precio(id)
                    );

                    CREATE TABLE IF NOT EXISTS pagos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cupon INTEGER NOT NULL,
                        fecha_pago TEXT DEFAULT CURRENT_TIMESTAMP,
                        numero_recibo INTEGER NOT NULL UNIQUE,
                        FOREIGN KEY (id_cupon) REFERENCES cupones_pago(id)
                    );

                    -- Crear índices para mejorar el rendimiento
                    CREATE INDEX IF NOT EXISTS idx_estudiantes_dni ON estudiantes(dni);
                    CREATE INDEX IF NOT EXISTS idx_estudiantes_apellido ON estudiantes(apellido);
                    CREATE INDEX IF NOT EXISTS idx_cupones_estudiante ON cupones_pago(id_estudiante);
                    CREATE INDEX IF NOT EXISTS idx_cupones_mes_año ON cupones_pago(mes, año_academico);
                    CREATE INDEX IF NOT EXISTS idx_pagos_cupon ON pagos(id_cupon);
                ''')
                print("Base de datos inicializada correctamente")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    init_db()