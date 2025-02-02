from base_datos.db_config import get_db_connection
from modelos.estudiante import Estudiante
from typing import List, Optional
import traceback

class RepositorioEstudiantes:
    @staticmethod
    def obtener_por_dni(dni: str, incluir_inactivos: bool = False) -> Optional[Estudiante]:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    query = 'SELECT * FROM estudiantes WHERE dni = ?'
                    
                    if not incluir_inactivos:
                        query += ' AND activo = 1'
                        
                    cursor.execute(query, (dni,))
                    row = cursor.fetchone()
                    
                    if row:
                        return Estudiante(
                            id=row['id'],
                            dni=row['dni'],
                            nombre=row['nombre'],
                            apellido=row['apellido'],
                            fecha_nacimiento=row['fecha_nacimiento'],
                            genero=row['genero'],
                            direccion=row['direccion'],
                            telefono_emergencia=row['telefono_emergencia'],
                            grado=row['grado'],
                            fecha_registro=row['fecha_registro'],
                            activo=bool(row['activo']),
                            doble_jornada=bool(row['doble_jornada'])
                        )
                    return None
                finally:
                    conn.close()
            return None
        except Exception as e:
            print(f"Error al obtener estudiante: {e}")
            print("Detalles del error:", traceback.format_exc())
            return None

    @staticmethod
    def guardar_estudiante(estudiante: Estudiante) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO estudiantes (
                            dni, nombre, apellido, fecha_nacimiento,
                            genero, direccion, telefono_emergencia,
                            grado, fecha_registro, activo, doble_jornada
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', estudiante.a_tupla())
                    
                    conn.commit()
                    estudiante.id = cursor.lastrowid
                    return True
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al guardar estudiante: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def actualizar_estudiante(estudiante: Estudiante) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE estudiantes SET
                            nombre = ?, apellido = ?,
                            fecha_nacimiento = ?, genero = ?,
                            direccion = ?, telefono_emergencia = ?,
                            grado = ?, doble_jornada = ?
                        WHERE dni = ?
                    ''', (
                        estudiante.nombre, estudiante.apellido,
                        estudiante.fecha_nacimiento, estudiante.genero,
                        estudiante.direccion, estudiante.telefono_emergencia,
                        estudiante.grado, estudiante.doble_jornada,
                        estudiante.dni
                    ))
                    conn.commit()
                    return cursor.rowcount > 0
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al actualizar estudiante: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def buscar_por_apellido(apellido: str, incluir_inactivos: bool = False) -> List[Estudiante]:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    query = "SELECT * FROM estudiantes WHERE apellido LIKE ?"
                    
                    if not incluir_inactivos:
                        query += " AND activo = 1"
                        
                    cursor.execute(query, (f"%{apellido}%",))
                    
                    estudiantes = []
                    for row in cursor.fetchall():
                        estudiantes.append(Estudiante(
                            id=row['id'],
                            dni=row['dni'],
                            nombre=row['nombre'],
                            apellido=row['apellido'],
                            fecha_nacimiento=row['fecha_nacimiento'],
                            genero=row['genero'],
                            direccion=row['direccion'],
                            telefono_emergencia=row['telefono_emergencia'],
                            grado=row['grado'],
                            fecha_registro=row['fecha_registro'],
                            activo=bool(row['activo']),
                            doble_jornada=bool(row['doble_jornada'])
                        ))
                    return estudiantes
                finally:
                    conn.close()
            return []
        except Exception as e:
            print(f"Error al buscar estudiantes: {e}")
            print("Detalles del error:", traceback.format_exc())
            return []

    @staticmethod
    def dar_de_baja_estudiante(dni: str) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE estudiantes
                        SET activo = 0
                        WHERE dni = ?
                    ''', (dni,))
                    conn.commit()
                    return cursor.rowcount > 0
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al dar de baja estudiante: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def reactivar_estudiante(dni: str) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE estudiantes
                        SET activo = 1
                        WHERE dni = ?
                    ''', (dni,))
                    conn.commit()
                    return cursor.rowcount > 0
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al reactivar estudiante: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def obtener_estudiantes_por_grado_y_año(grado: str, año: str) -> List[Estudiante]:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT *
                        FROM estudiantes
                        WHERE grado = ?
                        AND fecha_registro BETWEEN ? || '-01-01' AND ? || '-12-31'
                    ''', (grado, año, año))
                    
                    estudiantes = []
                    for row in cursor.fetchall():
                        estudiantes.append(Estudiante(
                            id=row['id'],
                            dni=row['dni'],
                            nombre=row['nombre'],
                            apellido=row['apellido'],
                            fecha_nacimiento=row['fecha_nacimiento'],
                            genero=row['genero'],
                            direccion=row['direccion'],
                            telefono_emergencia=row['telefono_emergencia'],
                            grado=row['grado'],
                            fecha_registro=row['fecha_registro'],
                            activo=bool(row['activo']),
                            doble_jornada=bool(row['doble_jornada'])
                        ))
                    return estudiantes
                finally:
                    conn.close()
            return []
        except Exception as e:
            print(f"Error al obtener estudiantes por grado y año: {e}")
            print("Detalles del error:", traceback.format_exc())
            return []

    @staticmethod
    def obtener_estudiantes_activos_por_nivel(nivel: str) -> List[Estudiante]:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    query = '''
                        SELECT * FROM estudiantes 
                        WHERE activo = 1 AND (
                    '''
                    
                    if nivel == 'Inicial':
                        query += "grado LIKE 'Sala%'"
                    elif nivel == 'Primario':
                        query += "grado LIKE '%º%'"
                    elif nivel == 'Secundario':
                        query += "grado LIKE '%º%' OR grado LIKE '%Economía%' OR grado LIKE '%Sociales%'"
                    
                    query += ")"
                    
                    cursor.execute(query)
                    
                    estudiantes = []
                    for row in cursor.fetchall():
                        estudiantes.append(Estudiante(
                            id=row['id'],
                            dni=row['dni'],
                            nombre=row['nombre'],
                            apellido=row['apellido'],
                            fecha_nacimiento=row['fecha_nacimiento'],
                            genero=row['genero'],
                            direccion=row['direccion'],
                            telefono_emergencia=row['telefono_emergencia'],
                            grado=row['grado'],
                            fecha_registro=row['fecha_registro'],
                            activo=bool(row['activo']),
                            doble_jornada=bool(row['doble_jornada'])
                        ))
                    return estudiantes
                finally:
                    conn.close()
            return []
        except Exception as e:
            print(f"Error al obtener estudiantes por nivel: {e}")
            print("Detalles del error:", traceback.format_exc())
            return []