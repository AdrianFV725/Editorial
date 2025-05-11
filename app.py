from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import psycopg2
import psycopg2.extras
import os
import shutil
from werkzeug.utils import secure_filename
from datetime import datetime
import sys

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'editorial_secreto')

# Configuración para subir imágenes
# Usar una ruta absoluta para guardar las imágenes
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'img', 'profiles')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Asegurar que todas las carpetas en la ruta existan
def ensure_folders_exist(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Carpeta creada: {path}")
        except Exception as e:
            print(f"Error al crear carpeta {path}: {e}")

# Crear las carpetas necesarias
ensure_folders_exist(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para servir imágenes de perfiles (como fallback)
@app.route('/profiles/<path:filename>')
def serve_profile_image(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except:
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'default.jpg')

# Configuración de conexión a la base de datos
def get_db_connection():
    # Imprimir información de diagnóstico
    print("===== DIAGNÓSTICO DE CONEXIÓN A LA BASE DE DATOS =====")
    print(f"DATABASE_URL existe: {os.environ.get('DATABASE_URL') is not None}")
    if os.environ.get('DATABASE_URL'):
        print(f"DATABASE_URL comienza con: {os.environ.get('DATABASE_URL')[:15]}...")
    else:
        print("Variables alternativas:")
        print(f"- DATABASE_HOST: {os.environ.get('DATABASE_HOST', 'no definido')}")
        print(f"- DATABASE_NAME: {os.environ.get('DATABASE_NAME', 'no definido')}")
        print(f"- DATABASE_USER: {os.environ.get('DATABASE_USER', 'no definido')}")
    
    try:
        database_url = os.environ.get('DATABASE_URL')
        
        if database_url:
            # Railway usa 'postgres://' pero psycopg2 necesita 'postgresql://'
            if database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql://", 1)
                print(f"URL convertida a postgresql://...")
            
            # Si existe DATABASE_URL, usamos esa cadena de conexión (formato de Railway)
            print("Intentando conectar usando DATABASE_URL...")
            conn = psycopg2.connect(database_url)
            print("¡Conexión exitosa usando DATABASE_URL!")
        else:
            # Si no, usamos los parámetros individuales (entorno local)
            print("Intentando conectar usando parámetros individuales...")
            conn = psycopg2.connect(
                host=os.environ.get('DATABASE_HOST', 'localhost'),
                database=os.environ.get('DATABASE_NAME', 'editorial'),
                user=os.environ.get('DATABASE_USER', 'adrianfloresvillatoro'),
                password=os.environ.get('DATABASE_PASSWORD', '')
            )
            print("¡Conexión exitosa usando parámetros individuales!")
        
        conn.cursor_factory = psycopg2.extras.DictCursor
        return conn
    except Exception as e:
        print(f"ERROR DE CONEXIÓN: {e}")
        # En un entorno de producción, podrías redirigir a una página de error
        # o tener un plan de respaldo
        raise e

# Ruta principal - Dashboard
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Obtener estadísticas para el dashboard
    cur.execute('SELECT COUNT(*) FROM clientes')
    total_clientes = cur.fetchone()[0]
    
    cur.execute('SELECT COUNT(*) FROM libros')
    total_libros = cur.fetchone()[0]
    
    cur.execute('SELECT COUNT(*) FROM autores')
    total_autores = cur.fetchone()[0]
    
    cur.execute('SELECT SUM(cantidad * precio_unitario) FROM ventas')
    total_ventas = cur.fetchone()[0] or 0
    
    # Obtener datos para el gráfico de libros más vendidos (top 5)
    cur.execute('''
        SELECT l.titulo, SUM(v.cantidad) as total_vendidos
        FROM libros l
        JOIN ventas v ON l.id = v.libro_id
        GROUP BY l.titulo
        ORDER BY total_vendidos DESC
        LIMIT 5
    ''')
    top_libros = cur.fetchall()
    
    # Obtener datos para el gráfico de ingresos por autor (top 5)
    cur.execute('''
        SELECT a.nombre || ' ' || a.apellido as autor, 
               SUM(v.cantidad * v.precio_unitario) as ingresos
        FROM autores a
        JOIN libroautor la ON a.id = la.autor_id
        JOIN libros l ON la.libro_id = l.id
        JOIN ventas v ON l.id = v.libro_id
        GROUP BY a.id, a.nombre, a.apellido
        ORDER BY ingresos DESC
        LIMIT 5
    ''')
    top_autores = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('index.html', 
                          total_clientes=total_clientes,
                          total_libros=total_libros,
                          total_autores=total_autores,
                          total_ventas=total_ventas,
                          top_libros=top_libros,
                          top_autores=top_autores)

# Rutas para Clientes
@app.route('/clientes')
def listar_clientes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM clientes ORDER BY nombre')
    clientes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('clientes/lista.html', clientes=clientes)

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        ciudad = request.form['ciudad']
        
        # Manejar la imagen de perfil
        foto_perfil = 'default.jpg'  # Imagen por defecto
        
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename != '' and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    # Agregar timestamp al nombre del archivo para evitar duplicados
                    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    foto_perfil = filename
                    print(f"Archivo guardado en: {file_path}")
                except Exception as e:
                    print(f"Error al guardar la imagen: {e}")
                    flash(f"No se pudo guardar la imagen: {e}", "error")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO clientes (nombre, email, telefono, ciudad, foto_perfil) VALUES (%s, %s, %s, %s, %s) RETURNING id',
                   (nombre, email, telefono, ciudad, foto_perfil))
        conn.commit()
        cur.close()
        conn.close()
        
        flash('Cliente agregado con éxito')
        return redirect(url_for('listar_clientes'))
        
    return render_template('clientes/nuevo.html')

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        ciudad = request.form['ciudad']
        
        # Obtener la foto de perfil actual
        cur.execute('SELECT foto_perfil FROM clientes WHERE id = %s', (id,))
        cliente_actual = cur.fetchone()
        foto_perfil = cliente_actual['foto_perfil'] if cliente_actual else 'default.jpg'
        
        # Actualizar foto si se proporcionó una nueva
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename != '' and allowed_file(file.filename):
                try:
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    # Si había una foto anterior y no es la default, eliminarla
                    if foto_perfil != 'default.jpg':
                        old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], foto_perfil)
                        if os.path.exists(old_file_path):
                            try:
                                os.remove(old_file_path)
                                print(f"Imagen anterior eliminada: {old_file_path}")
                            except:
                                print(f"No se pudo eliminar la imagen anterior: {old_file_path}")
                    
                    foto_perfil = filename
                    print(f"Archivo guardado en: {file_path}")
                except Exception as e:
                    print(f"Error al guardar la imagen: {e}")
                    flash(f"No se pudo guardar la imagen: {e}", "error")
        
        cur.execute('UPDATE clientes SET nombre = %s, email = %s, telefono = %s, ciudad = %s, foto_perfil = %s WHERE id = %s',
                   (nombre, email, telefono, ciudad, foto_perfil, id))
        conn.commit()
        flash('Cliente actualizado con éxito')
        return redirect(url_for('listar_clientes'))
    
    cur.execute('SELECT * FROM clientes WHERE id = %s', (id,))
    cliente = cur.fetchone()
    cur.close()
    conn.close()
    
    return render_template('clientes/editar.html', cliente=cliente)

@app.route('/clientes/eliminar/<int:id>')
def eliminar_cliente(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM clientes WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Cliente eliminado con éxito')
    return redirect(url_for('listar_clientes'))

# Rutas para Libros
@app.route('/libros')
def listar_libros():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Obtener todos los libros con sus autores
    cur.execute('''
        SELECT l.id, l.titulo, l.fecha_publicacion, l.genero, 
               string_agg(a.nombre || ' ' || a.apellido, ', ') as autores
        FROM libros l
        LEFT JOIN libroautor la ON l.id = la.libro_id
        LEFT JOIN autores a ON la.autor_id = a.id
        GROUP BY l.id, l.titulo, l.fecha_publicacion, l.genero
        ORDER BY l.titulo
    ''')
    
    libros = cur.fetchall()
    
    # Obtener todos los géneros para el filtro
    cur.execute('SELECT DISTINCT genero FROM libros ORDER BY genero')
    generos = [row['genero'] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return render_template('libros/lista.html', libros=libros, generos=generos)

@app.route('/libros/filtrar')
def filtrar_libros():
    genero = request.args.get('genero', '')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    if genero:
        cur.execute('''
            SELECT l.id, l.titulo, l.fecha_publicacion, l.genero, 
                   string_agg(a.nombre || ' ' || a.apellido, ', ') as autores
            FROM libros l
            LEFT JOIN libroautor la ON l.id = la.libro_id
            LEFT JOIN autores a ON la.autor_id = a.id
            WHERE l.genero = %s
            GROUP BY l.id, l.titulo, l.fecha_publicacion, l.genero
            ORDER BY l.titulo
        ''', (genero,))
    else:
        cur.execute('''
            SELECT l.id, l.titulo, l.fecha_publicacion, l.genero, 
                   string_agg(a.nombre || ' ' || a.apellido, ', ') as autores
            FROM libros l
            LEFT JOIN libroautor la ON l.id = la.libro_id
            LEFT JOIN autores a ON la.autor_id = a.id
            GROUP BY l.id, l.titulo, l.fecha_publicacion, l.genero
            ORDER BY l.titulo
        ''')
    
    libros = cur.fetchall()
    
    cur.execute('SELECT DISTINCT genero FROM libros ORDER BY genero')
    generos = [row['genero'] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return render_template('libros/lista.html', libros=libros, generos=generos, filtro_actual=genero)

@app.route('/libros/nuevo', methods=['GET', 'POST'])
def nuevo_libro():
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        fecha_publicacion = request.form['fecha_publicacion']
        genero = request.form['genero']
        autores = request.form.getlist('autores')
        
        # Insertar nuevo libro
        cur.execute(
            'INSERT INTO libros (titulo, fecha_publicacion, genero) VALUES (%s, %s, %s) RETURNING id',
            (titulo, fecha_publicacion, genero)
        )
        nuevo_libro_id = cur.fetchone()[0]
        
        # Asociar autores al libro
        for autor_id in autores:
            es_principal = autor_id == request.form.get('autor_principal')
            cur.execute(
                'INSERT INTO libroautor (libro_id, autor_id, es_autor_principal) VALUES (%s, %s, %s)',
                (nuevo_libro_id, autor_id, es_principal)
            )
        
        conn.commit()
        flash('Libro agregado con éxito')
        return redirect(url_for('listar_libros'))
    
    # Obtener lista de autores para el formulario
    cur.execute('SELECT id, nombre, apellido FROM autores ORDER BY apellido, nombre')
    autores = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('libros/nuevo.html', autores=autores)

@app.route('/libros/editar/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        fecha_publicacion = request.form['fecha_publicacion']
        genero = request.form['genero']
        autores = request.form.getlist('autores')
        
        # Actualizar libro
        cur.execute(
            'UPDATE libros SET titulo = %s, fecha_publicacion = %s, genero = %s WHERE id = %s',
            (titulo, fecha_publicacion, genero, id)
        )
        
        # Eliminar asociaciones anteriores de autores
        cur.execute('DELETE FROM libroautor WHERE libro_id = %s', (id,))
        
        # Agregar nuevas asociaciones de autores
        for autor_id in autores:
            es_principal = autor_id == request.form.get('autor_principal')
            cur.execute(
                'INSERT INTO libroautor (libro_id, autor_id, es_autor_principal) VALUES (%s, %s, %s)',
                (id, autor_id, es_principal)
            )
        
        conn.commit()
        flash('Libro actualizado con éxito')
        return redirect(url_for('listar_libros'))
    
    # Obtener datos del libro
    cur.execute('SELECT * FROM libros WHERE id = %s', (id,))
    libro = cur.fetchone()
    
    # Obtener autores actuales del libro
    cur.execute('''
        SELECT autor_id, es_autor_principal 
        FROM libroautor 
        WHERE libro_id = %s
    ''', (id,))
    autores_libro = cur.fetchall()
    
    autores_ids = [autor['autor_id'] for autor in autores_libro]
    autor_principal = next((autor['autor_id'] for autor in autores_libro if autor['es_autor_principal']), None)
    
    # Obtener lista de todos los autores
    cur.execute('SELECT id, nombre, apellido FROM autores ORDER BY apellido, nombre')
    autores = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('libros/editar.html', libro=libro, autores=autores, 
                          autores_ids=autores_ids, autor_principal=autor_principal)

@app.route('/libros/eliminar/<int:id>')
def eliminar_libro(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM libros WHERE id = %s', (id,))
    conn.commit()
    
    cur.close()
    conn.close()
    
    flash('Libro eliminado con éxito')
    return redirect(url_for('listar_libros'))

# Rutas para Autores
@app.route('/autores')
def listar_autores():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM autores ORDER BY apellido, nombre')
    autores = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('autores/lista.html', autores=autores)

@app.route('/autores/nuevo', methods=['GET', 'POST'])
def nuevo_autor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        nacionalidad = request.form['nacionalidad']
        fecha_nacimiento = request.form['fecha_nacimiento']
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            'INSERT INTO autores (nombre, apellido, nacionalidad, fecha_nacimiento) VALUES (%s, %s, %s, %s)',
            (nombre, apellido, nacionalidad, fecha_nacimiento)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        flash('Autor agregado con éxito')
        return redirect(url_for('listar_autores'))
        
    return render_template('autores/nuevo.html')

@app.route('/autores/editar/<int:id>', methods=['GET', 'POST'])
def editar_autor(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        nacionalidad = request.form['nacionalidad']
        fecha_nacimiento = request.form['fecha_nacimiento']
        
        cur.execute(
            'UPDATE autores SET nombre = %s, apellido = %s, nacionalidad = %s, fecha_nacimiento = %s WHERE id = %s',
            (nombre, apellido, nacionalidad, fecha_nacimiento, id)
        )
        
        conn.commit()
        flash('Autor actualizado con éxito')
        return redirect(url_for('listar_autores'))
    
    cur.execute('SELECT * FROM autores WHERE id = %s', (id,))
    autor = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return render_template('autores/editar.html', autor=autor)

@app.route('/autores/eliminar/<int:id>')
def eliminar_autor(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM autores WHERE id = %s', (id,))
    conn.commit()
    
    cur.close()
    conn.close()
    
    flash('Autor eliminado con éxito')
    return redirect(url_for('listar_autores'))

# Rutas para Ventas
@app.route('/ventas')
def listar_ventas():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT v.id, v.fecha_venta, v.cantidad, v.precio_unitario, 
               (v.cantidad * v.precio_unitario) as total,
               c.nombre as cliente, l.titulo as libro
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN libros l ON v.libro_id = l.id
        ORDER BY v.fecha_venta DESC
    ''')
    
    ventas = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('ventas/lista.html', ventas=ventas)

@app.route('/ventas/nueva', methods=['GET', 'POST'])
def nueva_venta():
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        libro_id = request.form['libro_id']
        cantidad = request.form['cantidad']
        precio_unitario = request.form['precio_unitario']
        fecha_venta = request.form['fecha_venta'] or datetime.now().strftime('%Y-%m-%d')
        
        cur.execute(
            'INSERT INTO ventas (cliente_id, libro_id, cantidad, precio_unitario, fecha_venta) VALUES (%s, %s, %s, %s, %s)',
            (cliente_id, libro_id, cantidad, precio_unitario, fecha_venta)
        )
        
        conn.commit()
        flash('Venta registrada con éxito')
        return redirect(url_for('listar_ventas'))
    
    # Obtener clientes para el formulario
    cur.execute('SELECT id, nombre FROM clientes ORDER BY nombre')
    clientes = cur.fetchall()
    
    # Obtener libros para el formulario
    cur.execute('SELECT id, titulo FROM libros ORDER BY titulo')
    libros = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('ventas/nueva.html', clientes=clientes, libros=libros)

@app.route('/ventas/eliminar/<int:id>')
def eliminar_venta(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM ventas WHERE id = %s', (id,))
    conn.commit()
    
    cur.close()
    conn.close()
    
    flash('Venta eliminada con éxito')
    return redirect(url_for('listar_ventas'))

# Estadísticas
@app.route('/estadisticas/libros')
def estadisticas_libros():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Obtener estadísticas de ventas por libro
    cur.execute('''
        SELECT l.id, l.titulo, l.genero,
               SUM(v.cantidad) as total_vendidos,
               SUM(v.cantidad * v.precio_unitario) as ingresos_totales
        FROM libros l
        LEFT JOIN ventas v ON l.id = v.libro_id
        GROUP BY l.id, l.titulo, l.genero
        ORDER BY ingresos_totales DESC NULLS LAST
    ''')
    
    estadisticas_libros = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('estadisticas/libros.html', estadisticas=estadisticas_libros)

@app.route('/estadisticas/autores')
def estadisticas_autores():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Obtener estadísticas de ventas por autor
    cur.execute('''
        SELECT a.id, a.nombre, a.apellido,
               SUM(v.cantidad) as total_vendidos,
               SUM(v.cantidad * v.precio_unitario) as ingresos_totales
        FROM autores a
        JOIN libroautor la ON a.id = la.autor_id
        JOIN libros l ON la.libro_id = l.id
        JOIN ventas v ON l.id = v.libro_id
        GROUP BY a.id, a.nombre, a.apellido
        ORDER BY ingresos_totales DESC
    ''')
    
    estadisticas_autores = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('estadisticas/autores.html', estadisticas=estadisticas_autores)

# Ruta de diagnóstico para verificar la configuración
@app.route('/diagnostico')
def diagnostico():
    info = {
        'app': {
            'debug': app.debug,
            'env': os.environ.get('FLASK_ENV', 'no definido'),
            'secret_key_set': app.secret_key is not None,
        },
        'db_config': {
            'database_url_set': os.environ.get('DATABASE_URL') is not None,
            'database_host': os.environ.get('DATABASE_HOST', 'no definido'),
            'database_name': os.environ.get('DATABASE_NAME', 'no definido'),
            'database_user': os.environ.get('DATABASE_USER', 'no definido'),
        },
        'system': {
            'python_version': sys.version,
            'platform': sys.platform,
            'port': os.environ.get('PORT', 'no definido'),
        }
    }
    
    db_status = "Unknown"
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT version()")
        version = cur.fetchone()
        cur.close()
        conn.close()
        db_status = f"Connected: {version[0]}"
    except Exception as e:
        db_status = f"Error: {str(e)}"
    
    info['db_status'] = db_status
    
    return jsonify(info)

# Página de error para problemas de base de datos
@app.route('/db_error')
def db_error():
    error_details = request.args.get('error', 'Error desconocido')
    return render_template('error.html', 
                          error_title="Error de Base de Datos", 
                          error_message="No se pudo conectar a la base de datos.", 
                          error_details=error_details)

if __name__ == '__main__':
    # Agregar columna foto_perfil a la tabla clientes si no existe
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute('''
            ALTER TABLE clientes 
            ADD COLUMN IF NOT EXISTS foto_perfil VARCHAR(255) DEFAULT 'default.jpg'
        ''')
        conn.commit()
    except Exception as e:
        print(f"Error al actualizar tabla: {e}")
        conn.rollback()
    
    cur.close()
    conn.close()
    
    # Obtener puerto de la variable de entorno PORT (para Railway) o usar 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    
    # En producción, probablemente querrás deshabilitar el modo debug
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
