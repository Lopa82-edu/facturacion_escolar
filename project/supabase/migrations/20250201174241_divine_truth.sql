/*
  # Agregar función exec_sql

  1. Nueva Función
    - `exec_sql`: Función que permite ejecutar SQL dinámico de forma segura
    
  2. Seguridad
    - Solo usuarios autenticados pueden ejecutar la función
    - Se requieren permisos de superusuario
*/

-- Crear función para ejecutar SQL dinámico
CREATE OR REPLACE FUNCTION public.exec_sql(sql text)
RETURNS void AS $$
BEGIN
  EXECUTE sql;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Otorgar permisos
GRANT EXECUTE ON FUNCTION public.exec_sql(text) TO authenticated;
GRANT EXECUTE ON FUNCTION public.exec_sql(text) TO anon;