/*
  # Esquema inicial de la base de datos escolar

  1. Nuevas Tablas
    - `estudiantes` - Almacena información de estudiantes
    - `tutores` - Almacena información de tutores/responsables
    - `items_precio` - Almacena los items y precios por nivel
    - `cupones_pago` - Almacena los cupones de pago generados
    - `items_cupon` - Almacena los items incluidos en cada cupón
    - `pagos` - Almacena los pagos realizados

  2. Seguridad
    - RLS habilitado en todas las tablas
    - Políticas para acceso autenticado

  3. Relaciones
    - Tutores -> Estudiantes
    - Cupones -> Estudiantes
    - Items Cupón -> Cupones
    - Items Cupón -> Items Precio
    - Pagos -> Cupones
*/

-- Tabla estudiantes
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

-- Tabla tutores
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

-- Tabla items_precio
CREATE TABLE IF NOT EXISTS items_precio (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    nivel text NOT NULL,
    nombre text NOT NULL,
    monto decimal NOT NULL,
    activo boolean DEFAULT true,
    solo_doble_jornada boolean DEFAULT false,
    item_mantenimiento boolean DEFAULT false
);

-- Tabla cupones_pago
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

-- Tabla items_cupon
CREATE TABLE IF NOT EXISTS items_cupon (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    id_cupon uuid NOT NULL REFERENCES cupones_pago(id),
    id_item uuid NOT NULL REFERENCES items_precio(id),
    monto decimal NOT NULL
);

-- Tabla pagos
CREATE TABLE IF NOT EXISTS pagos (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    id_cupon uuid NOT NULL REFERENCES cupones_pago(id),
    fecha_pago timestamptz DEFAULT now(),
    numero_recibo integer NOT NULL UNIQUE
);

-- Habilitar RLS
ALTER TABLE estudiantes ENABLE ROW LEVEL SECURITY;
ALTER TABLE tutores ENABLE ROW LEVEL SECURITY;
ALTER TABLE items_precio ENABLE ROW LEVEL SECURITY;
ALTER TABLE cupones_pago ENABLE ROW LEVEL SECURITY;
ALTER TABLE items_cupon ENABLE ROW LEVEL SECURITY;
ALTER TABLE pagos ENABLE ROW LEVEL SECURITY;

-- Políticas de seguridad
CREATE POLICY "Acceso total para usuarios autenticados" ON estudiantes
    FOR ALL TO authenticated
    USING (true);

CREATE POLICY "Acceso total para usuarios autenticados" ON tutores
    FOR ALL TO authenticated
    USING (true);

CREATE POLICY "Acceso total para usuarios autenticados" ON items_precio
    FOR ALL TO authenticated
    USING (true);

CREATE POLICY "Acceso total para usuarios autenticados" ON cupones_pago
    FOR ALL TO authenticated
    USING (true);

CREATE POLICY "Acceso total para usuarios autenticados" ON items_cupon
    FOR ALL TO authenticated
    USING (true);

CREATE POLICY "Acceso total para usuarios autenticados" ON pagos
    FOR ALL TO authenticated
    USING (true);