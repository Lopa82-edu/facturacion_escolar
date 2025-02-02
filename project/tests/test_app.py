import unittest
from datetime import datetime
from modelos.estudiante import Estudiante
from modelos.tutor import Tutor
from modelos.item_precio import ItemPrecio
from modelos.cupon_pago import CuponPago, ItemCupon
from modelos.pago import Pago
import os
#python -m unittest tests/test_app.py -v

class TestModelos(unittest.TestCase):
    """Tests para los modelos de datos"""
    
    def test_estudiante_modelo(self):
        """Test del modelo Estudiante"""
        estudiante_datos = {
            'dni': '12345678',
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'grado': '1ºA',
            'fecha_nacimiento': '2015-01-01',
            'genero': 'Masculino',
            'direccion': 'Calle 123',
            'telefono_emergencia': '11-1234-5678',
            'doble_jornada': True
        }
        estudiante = Estudiante(**estudiante_datos)
        self.assertEqual(estudiante.dni, estudiante_datos['dni'])
        self.assertEqual(estudiante.nombre, estudiante_datos['nombre'])
        self.assertEqual(estudiante.apellido, estudiante_datos['apellido'])
        self.assertTrue(estudiante.activo)
        self.assertTrue(estudiante.doble_jornada)

    def test_tutor_modelo(self):
        """Test del modelo Tutor"""
        tutor_datos = {
            'tipo_tutor': 'tutor1',
            'dni': '87654321',
            'nombre_completo': 'María Pérez',
            'telefono': '11-8765-4321',
            'email': 'maria@email.com',
            'parentesco': 'Madre'
        }
        tutor = Tutor(id_estudiante=1, **tutor_datos)
        self.assertEqual(tutor.tipo_tutor, tutor_datos['tipo_tutor'])
        self.assertEqual(tutor.dni, tutor_datos['dni'])
        self.assertEqual(tutor.nombre_completo, tutor_datos['nombre_completo'])

    def test_item_precio_modelo(self):
        """Test del modelo ItemPrecio"""
        item_datos = {
            'nivel': 'Primario',
            'nombre': 'Cuota Mensual',
            'monto': 1000.0,
            'solo_doble_jornada': False,
            'item_mantenimiento': False
        }
        item = ItemPrecio(**item_datos)
        self.assertEqual(item.nivel, item_datos['nivel'])
        self.assertEqual(item.nombre, item_datos['nombre'])
        self.assertEqual(item.monto, item_datos['monto'])
        self.assertTrue(item.activo)

    def test_cupon_pago_modelo(self):
        """Test del modelo CuponPago"""
        cupon_datos = {
            'id_estudiante': 1,
            'año_academico': 2024,
            'mes': 3,
            'nivel': 'Primario',
            'grado': '1ºA',
            'monto_total': 1000.0,
            'es_cargo_especial': False
        }
        cupon = CuponPago(**cupon_datos)
        self.assertEqual(cupon.id_estudiante, cupon_datos['id_estudiante'])
        self.assertEqual(cupon.año_academico, cupon_datos['año_academico'])
        self.assertEqual(cupon.mes, cupon_datos['mes'])
        self.assertEqual(cupon.estado, 'active')

    def test_pago_modelo(self):
        """Test del modelo Pago"""
        pago = Pago(id_cupon=1)
        self.assertEqual(pago.id_cupon, 1)
        self.assertIsNotNone(pago.fecha_pago)

class TestUtilidades(unittest.TestCase):
    """Tests para las utilidades"""

    def test_utilidades_meses(self):
        """Test de las utilidades de meses"""
        from utilidades.utilidades_meses import UtilidadesMeses
        
        # Test obtener meses
        meses = UtilidadesMeses.obtener_meses()
        self.assertEqual(len(meses), 10)  # De marzo a diciembre
        self.assertEqual(meses[0], "Marzo")
        self.assertEqual(meses[-1], "Diciembre")
        
        # Test conversión número-nombre
        self.assertEqual(UtilidadesMeses.obtener_nombre_mes(3), "Marzo")
        self.assertEqual(UtilidadesMeses.obtener_numero_mes("Marzo"), 3)
        
        # Test mes de mantenimiento
        self.assertTrue(UtilidadesMeses.es_mes_mantenimiento(6))  # Junio
        self.assertTrue(UtilidadesMeses.es_mes_mantenimiento(11))  # Noviembre
        self.assertFalse(UtilidadesMeses.es_mes_mantenimiento(3))  # Marzo

    def test_niveles_grados(self):
        """Test de las utilidades de niveles y grados"""
        from utilidades.niveles_grados import NivelesGrados
        
        # Test obtener niveles
        niveles = NivelesGrados.obtener_niveles()
        self.assertEqual(len(niveles), 3)
        self.assertIn("Inicial", niveles)
        self.assertIn("Primario", niveles)
        self.assertIn("Secundario", niveles)
        
        # Test obtener grados por nivel
        grados_inicial = NivelesGrados.obtener_grados_por_nivel("Inicial")
        self.assertTrue(len(grados_inicial) > 0)
        self.assertIn("Sala 3 TM", grados_inicial)
        
        grados_primario = NivelesGrados.obtener_grados_por_nivel("Primario")
        self.assertTrue(len(grados_primario) > 0)
        self.assertIn("1ºA", grados_primario)
        
        grados_secundario = NivelesGrados.obtener_grados_por_nivel("Secundario")
        self.assertTrue(len(grados_secundario) > 0)
        self.assertIn("1ºA", grados_secundario)

if __name__ == '__main__':
    unittest.main()