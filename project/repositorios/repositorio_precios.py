from base_datos.db_config import get_db_connection
from modelos.item_precio import ItemPrecio
from typing import List
import traceback

class RepositorioPrecios:
    @staticmethod
    def guardar_item_precio(item: ItemPrecio) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO items_precio (
                            nivel, nombre, monto, activo,
                            solo_doble_jornada, item_mantenimiento
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        item.nivel, item.nombre, float(item.monto),
                        1 if item.activo else 0,
                        1 if item.solo_doble_jornada else 0,
                        1 if item.item_mantenimiento else 0
                    ))
                    
                    conn.commit()
                    return True
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al guardar item de precio: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def obtener_items_por_nivel(nivel: str, incluir_inactivos: bool = False) -> List[ItemPrecio]:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    query = "SELECT * FROM items_precio WHERE nivel = ?"
                    
                    if not incluir_inactivos:
                        query += " AND activo = 1"
                        
                    cursor.execute(query, (nivel,))
                    
                    items = []
                    for row in cursor.fetchall():
                        items.append(ItemPrecio(
                            id=row['id'],
                            nivel=row['nivel'],
                            nombre=row['nombre'],
                            monto=float(row['monto']),
                            activo=bool(row['activo']),
                            solo_doble_jornada=bool(row['solo_doble_jornada']),
                            item_mantenimiento=bool(row['item_mantenimiento'])
                        ))
                    return items
                finally:
                    conn.close()
            return []
        except Exception as e:
            print(f"Error al obtener items: {e}")
            print("Detalles del error:", traceback.format_exc())
            return []

    @staticmethod
    def actualizar_item_precio(item: ItemPrecio) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE items_precio SET
                            nombre = ?, monto = ?,
                            solo_doble_jornada = ?, item_mantenimiento = ?
                        WHERE id = ?
                    ''', (
                        item.nombre, float(item.monto),
                        1 if item.solo_doble_jornada else 0,
                        1 if item.item_mantenimiento else 0,
                        item.id
                    ))
                    conn.commit()
                    return cursor.rowcount > 0
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al actualizar item de precio: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def dar_de_baja_item_precio(id_item: int) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE items_precio
                        SET activo = 0
                        WHERE id = ?
                    ''', (id_item,))
                    conn.commit()
                    return cursor.rowcount > 0
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al dar de baja item de precio: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False

    @staticmethod
    def reactivar_item_precio(id_item: int) -> bool:
        try:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE items_precio
                        SET activo = 1
                        WHERE id = ?
                    ''', (id_item,))
                    conn.commit()
                    return cursor.rowcount > 0
                finally:
                    conn.close()
            return False
        except Exception as e:
            print(f"Error al reactivar item de precio: {e}")
            print("Detalles del error:", traceback.format_exc())
            return False