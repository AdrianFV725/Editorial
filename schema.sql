-- Crear tablas principales

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(20),
    ciudad VARCHAR(50),
    foto_perfil VARCHAR(255) DEFAULT 'default.jpg'
);

-- Tabla de autores
CREATE TABLE IF NOT EXISTS autores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    nacionalidad VARCHAR(50),
    fecha_nacimiento DATE
);

-- Tabla de libros
CREATE TABLE IF NOT EXISTS libros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    fecha_publicacion DATE,
    genero VARCHAR(50)
);

-- Tabla de relación autores-libros
CREATE TABLE IF NOT EXISTS libroautor (
    libro_id INTEGER REFERENCES libros(id) ON DELETE CASCADE,
    autor_id INTEGER REFERENCES autores(id) ON DELETE CASCADE,
    es_autor_principal BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (libro_id, autor_id)
);

-- Tabla de ventas
CREATE TABLE IF NOT EXISTS ventas (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
    libro_id INTEGER REFERENCES libros(id) ON DELETE CASCADE,
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    fecha_venta DATE DEFAULT CURRENT_DATE
);

-- Datos de ejemplo (descomentar y ejecutar si se desea tener datos de muestra)
/*
-- Insertar algunos clientes
INSERT INTO clientes (nombre, email, telefono, ciudad) VALUES
('María González', 'maria@ejemplo.com', '555-1234', 'Ciudad de México'),
('Juan Pérez', 'juan@ejemplo.com', '555-5678', 'Guadalajara'),
('Ana Rodríguez', 'ana@ejemplo.com', '555-9012', 'Monterrey');

-- Insertar algunos autores
INSERT INTO autores (nombre, apellido, nacionalidad, fecha_nacimiento) VALUES
('Gabriel', 'García Márquez', 'Colombiano', '1927-03-06'),
('Isabel', 'Allende', 'Chileno', '1942-08-02'),
('Mario', 'Vargas Llosa', 'Peruano', '1936-03-28');

-- Insertar algunos libros
INSERT INTO libros (titulo, fecha_publicacion, genero) VALUES
('Cien años de soledad', '1967-05-30', 'Realismo mágico'),
('La casa de los espíritus', '1982-01-01', 'Realismo mágico'),
('La ciudad y los perros', '1963-01-01', 'Novela');

-- Relacionar autores y libros
INSERT INTO libroautor (libro_id, autor_id, es_autor_principal) VALUES
(1, 1, TRUE),
(2, 2, TRUE),
(3, 3, TRUE);

-- Insertar algunas ventas
INSERT INTO ventas (cliente_id, libro_id, cantidad, precio_unitario, fecha_venta) VALUES
(1, 1, 2, 25.99, '2023-01-15'),
(2, 2, 1, 19.99, '2023-01-20'),
(3, 3, 3, 22.50, '2023-01-25');
*/ 