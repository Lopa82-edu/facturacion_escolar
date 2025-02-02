from base_datos.db_config import get_db_connection
from modelos.tutor import Tutor
from typing import List
import traceback

class RepositorioTutores:
    @staticmethod
    def guardar_tutor(tutor: Tutor) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO tutores (
                            id_estudiante, tipo_tutor, dni, nombre_completo,
                            telefono, email, parentesco
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', tutor.a_tupla())
                    
                    conn.commit()
                    tutor.id = cursor.lastrowid
                    return True
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al guardar tutor: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def obtener_tutores_por_id_estudiante(id_estudiante: int) -> List[Tutor]:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT * FROM tutores 
                        WHERE id_estudiante = ?
                    ''', (id_estudiante,))
                    
                    tutores = []
                    for row in cursor.fetchall():
                        tutores.append(Tutor(
                            id=row['id'],
                            id_estudiante=row['id_estudiante'],
                            tipo_tutor=row['tipo_tutor'],
                            dni=row['dni'],
                            nombre_completo=row['nombre_completo'],
                            telefono=row['telefono'],
                            email=row['email'],
                            parentesco=row['parentesco']
                        ))
                    return tutores
                finally:
                    conn.close()
            return []
        except Exception as e:
            print(f"Error al obtener tutores: {e}")
            print("Detalles del error:", traceback.format_exc())
            return []

    @staticmethod
    def actualizar_tutor(tutor: Tutor) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE tutores SET 
                            dni = ?, nombre_completo = ?, telefono = ?,
                            email = ?, parentesco = ?
                        WHERE id_estudiante = ? AND tipo_tutor = ?
                    ''', (
                        tutor.dni, tutor.nombre_completo,
                        tutor.telefono, tutor.email,
                        tutor.parentesco, tutor.id_estudiante,
                        tutor.tipo_tutor
                    ))
                    conn.commit()
                    return cursor.rowcount > 0
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al actualizar tutor: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False