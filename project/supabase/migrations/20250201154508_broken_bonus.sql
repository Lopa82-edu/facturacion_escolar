/*
  # Initial Schema Setup
  
  1. Tables
    - Creates all necessary tables for the school management system
  2. Security
    - Enables RLS on all tables
    - Sets up permissive policies for testing
*/

-- Create tables
CREATE TABLE IF NOT EXISTS estudiantes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    dni text UNIQUE NOT NULL,
    nombre text NOT NULL,
    apellido text NOT NULL,
    fecha_nacimiento text,
    genero text,
    direccion text,
    telefono_emergencia text,
    grado text NOT NULL,
    fecha_registro timestamptz DEFAULT now(),
    activo boolean DEFAULT true,
    doble_jornada boolean DEFAULT false
);

CREATE TABLE IF NOT EXISTS tutores (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    id_estudiante uuid NOT NULL REFERENCES estudiantes(id),
    tipo_tutor text NOT NULL,
    dni text,
    nombre_completo text,
    telefono text,
    email text,
    parentesco text
);

CREATE TABLE IF NOT EXISTS items_precio (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    nivel text NOT NULL,
    nombre text NOT NULL,
    monto decimal NOT NULL,
    activo boolean DEFAULT true,
    solo_doble_jornada boolean DEFAULT false,
    item_mantenimiento boolean DEFAULT false
);

CREATE TABLE IF NOT EXISTS cupones_pago (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    id_estudiante uuid NOT NULL REFERENCES estudiantes(id),
    año_academico integer NOT NULL,
    mes integer NOT NULL,
    nivel text NOT NULL,
    grado text NOT NULL,
    monto_total decimal NOT NULL,
    es_cargo_especial boolean DEFAULT false,
    porcentaje_cargo_especial decimal DEFAULT 0,
    estado text DEFAULT 'active',
    fecha_creacion timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS items_cupon (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    id_cupon uuid NOT NULL REFERENCES cupones_pago(id),
    id_item uuid NOT NULL REFERENCES items_precio(id),
    monto decimal NOT NULL
);

CREATE TABLE IF NOT EXISTS pagos (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    id_cupon uuid NOT NULL REFERENCES cupones_pago(id),
    fecha_pago timestamptz DEFAULT now(),
    numero_recibo integer NOT NULL UNIQUE
);

-- Enable RLS
ALTER TABLE estudiantes ENABLE ROW LEVEL SECURITY;
ALTER TABLE tutores ENABLE ROW LEVEL SECURITY;
ALTER TABLE items_precio ENABLE ROW LEVEL SECURITY;
ALTER TABLE cupones_pago ENABLE ROW LEVEL SECURITY;
ALTER TABLE items_cupon ENABLE ROW LEVEL SECURITY;
ALTER TABLE pagos ENABLE ROW LEVEL SECURITY;

-- Create permissive policies for testing
CREATE POLICY "Enable read for all" ON estudiantes FOR SELECT USING (true);
CREATE POLICY "Enable insert for all" ON estudiantes FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all" ON estudiantes FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all" ON estudiantes FOR DELETE USING (true);

CREATE POLICY "Enable read for all" ON tutores FOR SELECT USING (true);
CREATE POLICY "Enable insert for all" ON tutores FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all" ON tutores FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all" ON tutores FOR DELETE USING (true);

CREATE POLICY "Enable read for all" ON items_precio FOR SELECT USING (true);
CREATE POLICY "Enable insert for all" ON items_precio FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all" ON items_precio FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all" ON items_precio FOR DELETE USING (true);

CREATE POLICY "Enable read for all" ON cupones_pago FOR SELECT USING (true);
CREATE POLICY "Enable insert for all" ON cupones_pago FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all" ON cupones_pago FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all" ON cupones_pago FOR DELETE USING (true);

CREATE POLICY "Enable read for all" ON items_cupon FOR SELECT USING (true);
CREATE POLICY "Enable insert for all" ON items_cupon FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all" ON items_cupon FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all" ON items_cupon FOR DELETE USING (true);

CREATE POLICY "Enable read for all" ON pagos FOR SELECT USING (true);
CREATE POLICY "Enable insert for all" ON pagos FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all" ON pagos FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all" ON pagos FOR DELETE USING (true);