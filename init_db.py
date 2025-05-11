import os
import psycopg2
import sys

def init_db():
    """
    Inicializa la base de datos creando las tablas necesarias.
    Usa la variable de entorno DATABASE_URL si está disponible,
    o las variables individuales como alternativa.
    """
    print("Inicializando base de datos...")
    
    # Leer el schema SQL
    try:
        with open('schema.sql', 'r') as f:
            schema = f.read()
    except Exception as e:
        print(f"Error al leer schema.sql: {e}")
        sys.exit(1)
    
    # Conectar a la base de datos
    try:
        database_url = os.environ.get('DATABASE_URL')
        
        if database_url:
            # Railway usa 'postgres://' pero psycopg2 necesita 'postgresql://'
            if database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql://", 1)
                print(f"URL convertida a postgresql://...")
            
            print(f"Conectando usando DATABASE_URL...")
            conn = psycopg2.connect(database_url)
        else:
            # Usar parámetros individuales
            print("Conectando usando parámetros individuales...")
            conn = psycopg2.connect(
                host=os.environ.get('DATABASE_HOST', 'localhost'),
                database=os.environ.get('DATABASE_NAME', 'editorial'),
                user=os.environ.get('DATABASE_USER', 'adrianfloresvillatoro'),
                password=os.environ.get('DATABASE_PASSWORD', '')
            )
        
        # Ejecutar el schema
        cur = conn.cursor()
        cur.execute(schema)
        conn.commit()
        
        # Verificar si las tablas se crearon
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cur.fetchall()
        print("Tablas creadas:")
        for table in tables:
            print(f"- {table[0]}")
        
        cur.close()
        conn.close()
        
        print("Base de datos inicializada con éxito!")
        return True
        
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        return False

if __name__ == '__main__':
    init_db() 