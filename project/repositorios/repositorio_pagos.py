from base_datos.db_config import get_db_connection
from modelos.pago import Pago
from datetime import datetime
import traceback

class RepositorioPagos:
    @staticmethod
    def guardar_pago(pago: Pago) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    
                    # Obtener el nivel del cupón
                    cursor.execute('''
                        SELECT nivel
                        FROM cupones_pago
                        WHERE id = ?
                    ''', (pago.id_cupon,))
                    
                    result = cursor.fetchone()
                    if not result:
                        return False
                    
                    nivel = result['nivel']
                    
                    # Establecer número de recibo basado en el nivel
                    numero_base = 400025000 if nivel == "Secundario" else 300050000
                    
                    # Obtener último número de recibo para este rango de nivel
                    cursor.execute('''
                        SELECT numero_recibo
                        FROM pagos
                        WHERE numero_recibo >= ? AND numero_recibo < ?
                        ORDER BY numero_recibo DESC
                        LIMIT 1
                    ''', (numero_base, numero_base + 1000000))
                    
                    result = cursor.fetchone()
                    if result:
                        pago.numero_recibo = result['numero_recibo'] + 1
                    else:
                        pago.numero_recibo = numero_base
                    
                    # Insertar pago
                    cursor.execute('''
                        INSERT INTO pagos (id_cupon, fecha_pago, numero_recibo)
                        VALUES (?, ?, ?)
                    ''', (pago.id_cupon, pago.fecha_pago, pago.numero_recibo))
                    
                    # Actualizar estado del cupón
                    cursor.execute('''
                        UPDATE cupones_pago
                        SET estado = 'paid'
                        WHERE id = ?
                    ''', (pago.id_cupon,))
                    
                    conn.commit()
                    return True
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al guardar pago: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def obtener_pago_por_id_cupon(id_cupon: int) -> Pago:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT *
                        FROM pagos
                        WHERE id_cupon = ?
                    ''', (id_cupon,))
                    
                    row = cursor.fetchone()
                    if row:
                        return Pago(
                            id=row['id'],
                            id_cupon=row['id_cupon'],
                            fecha_pago=row['fecha_pago'],
                            numero_recibo=row['numero_recibo']
                        )
                    return None
                finally:
                    conn.close()
            return None
        except Exception as e:
            print(f"Error al obtener pago: {e}")
            print("Detalles del error:", traceback.format_exc())
            return None

    @staticmethod
    def anular_pago(id_cupon: int) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    # Eliminar pago
                    cursor.execute('DELETE FROM pagos WHERE id_cupon = ?', (id_cupon,))
                    
                    # Actualizar estado del cupón a activo
                    cursor.execute('''
                        UPDATE cupones_pago
                        SET estado = 'active'
                        WHERE id = ?
                    ''', (id_cupon,))
                    
                    conn.commit()
                    return True
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al anular pago: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False