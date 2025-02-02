from base_datos.db_config import get_db_connection
from modelos.cupon_pago import CuponPago, ItemCupon
from typing import List, Optional
import traceback

class RepositorioCuponesPago:
    @staticmethod
    def obtener_cupones_por_dni_estudiante(dni: str) -> List[CuponPago]:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT c.*, e.dni as dni_estudiante, 
                               e.nombre || " " || e.apellido as nombre_estudiante
                        FROM cupones_pago c
                        INNER JOIN estudiantes e ON c.id_estudiante = e.id
                        WHERE e.dni = ?
                        ORDER BY c.año_academico DESC, c.mes DESC
                    ''', (dni,))
                    
                    cupones = []
                    for row in cursor.fetchall():
                        cupon = CuponPago(
                            id=row['id'],
                            id_estudiante=row['id_estudiante'],
                            año_academico=row['año_academico'],
                            mes=row['mes'],
                            nivel=row['nivel'],
                            grado=row['grado'],
                            monto_total=float(row['monto_total']),
                            es_cargo_especial=bool(row['es_cargo_especial']),
                            porcentaje_cargo_especial=float(row['porcentaje_cargo_especial']),
                            estado=row['estado'],
                            fecha_creacion=row['fecha_creacion']
                        )
                        cupon.dni_estudiante = row['dni_estudiante']
                        cupon.nombre_estudiante = row['nombre_estudiante']
                        cupones.append(cupon)
                    
                    return cupones
                finally:
                    conn.close()
            return []
        except Exception as e:
            print(f"Error al obtener cupones por DNI: {e}")
            print("Detalles del error:", traceback.format_exc())
            return []

    @staticmethod
    def obtener_cupones_por_filtros(nivel: str, mes: int, año: int) -> List[CuponPago]:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    # Primero obtenemos los estudiantes activos del nivel
                    cursor.execute('''
                        SELECT c.*, e.dni as dni_estudiante,
                               e.apellido || ", " || e.nombre as nombre_estudiante
                        FROM cupones_pago c
                        INNER JOIN estudiantes e ON c.id_estudiante = e.id
                        WHERE c.nivel = ? AND c.mes = ? AND c.año_academico = ?
                        AND e.activo = 1
                        ORDER BY e.apellido, e.nombre
                    ''', (nivel, mes, año))
                    
                    cupones = []
                    for row in cursor.fetchall():
                        cupon = CuponPago(
                            id=row['id'],
                            id_estudiante=row['id_estudiante'],
                            año_academico=row['año_academico'],
                            mes=row['mes'],
                            nivel=row['nivel'],
                            grado=row['grado'],
                            monto_total=float(row['monto_total']),
                            es_cargo_especial=bool(row['es_cargo_especial']),
                            porcentaje_cargo_especial=float(row['porcentaje_cargo_especial']),
                            estado=row['estado'],
                            fecha_creacion=row['fecha_creacion']
                        )
                        cupon.dni_estudiante = row['dni_estudiante']
                        cupon.nombre_estudiante = row['nombre_estudiante']
                        cupones.append(cupon)
                    
                    return cupones
                finally:
                    conn.close()
            return []
        except Exception as e:
            print(f"Error al obtener cupones por filtros: {e}")
            print("Detalles del error:", traceback.format_exc())
            return []

    @staticmethod
    def obtener_cupon_por_estudiante_mes_año(id_estudiante: int, mes: int, año: int) -> Optional[CuponPago]:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT *
                        FROM cupones_pago
                        WHERE id_estudiante = ? AND mes = ? AND año_academico = ?
                    ''', (id_estudiante, mes, año))
                    
                    row = cursor.fetchone()
                    if row:
                        return CuponPago(
                            id=row['id'],
                            id_estudiante=row['id_estudiante'],
                            año_academico=row['año_academico'],
                            mes=row['mes'],
                            nivel=row['nivel'],
                            grado=row['grado'],
                            monto_total=float(row['monto_total']),
                            es_cargo_especial=bool(row['es_cargo_especial']),
                            porcentaje_cargo_especial=float(row['porcentaje_cargo_especial']),
                            estado=row['estado'],
                            fecha_creacion=row['fecha_creacion']
                        )
                    return None
                finally:
                    conn.close()
            return None
        except Exception as e:
            print(f"Error al obtener cupón por estudiante y fecha: {e}")
            print("Detalles del error:", traceback.format_exc())
            return None

    @staticmethod
    def guardar_cupon(cupon: CuponPago) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO cupones_pago (
                            id_estudiante, año_academico, mes, nivel, grado,
                            monto_total, es_cargo_especial, porcentaje_cargo_especial,
                            estado, fecha_creacion
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        cupon.id_estudiante, cupon.año_academico, cupon.mes,
                        cupon.nivel, cupon.grado, float(cupon.monto_total),
                        1 if cupon.es_cargo_especial else 0,
                        float(cupon.porcentaje_cargo_especial),
                        cupon.estado, cupon.fecha_creacion
                    ))
                    
                    id_cupon = cursor.lastrowid
                    
                    if cupon.items:
                        for item in cupon.items:
                            cursor.execute('''
                                INSERT INTO items_cupon (id_cupon, id_item, monto)
                                VALUES (?, ?, ?)
                            ''', (id_cupon, item.id_item, float(item.monto)))
                    
                    conn.commit()
                    return True
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al guardar cupón: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def anular_cupon(id_cupon: int) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE cupones_pago
                        SET estado = 'voided'
                        WHERE id = ?
                    ''', (id_cupon,))
                    conn.commit()
                    return cursor.rowcount > 0
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al anular cupón: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def reactivar_cupon(id_cupon: int) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE cupones_pago
                        SET estado = 'active'
                        WHERE id = ?
                    ''', (id_cupon,))
                    conn.commit()
                    return cursor.rowcount > 0
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al reactivar cupón: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def eliminar_cupon(id_cupon: int) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    # Eliminar items del cupón primero
                    cursor.execute('DELETE FROM items_cupon WHERE id_cupon = ?', (id_cupon,))
                    # Luego eliminar el cupón
                    cursor.execute('DELETE FROM cupones_pago WHERE id = ?', (id_cupon,))
                    conn.commit()
                    return cursor.rowcount > 0
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al eliminar cupón: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False