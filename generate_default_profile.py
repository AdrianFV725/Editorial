from PIL import Image, ImageDraw, ImageFont
import os

def generate_default_profile():
    # Configuración
    size = (400, 400)
    background_color = (52, 152, 219)  # Azul
    text_color = (255, 255, 255)  # Blanco
    
    # Crear una imagen cuadrada con fondo de color
    img = Image.new('RGB', size, color=background_color)
    draw = ImageDraw.Draw(img)
    
    # Dibujar un círculo para el avatar
    center = (size[0] // 2, size[1] // 2)
    radius = min(size) // 2 - 10
    
    # Dibujar el círculo
    draw.ellipse((center[0] - radius, center[1] - radius, 
                  center[0] + radius, center[1] + radius), 
                  fill=background_color, outline=(255, 255, 255), width=5)
    
    # Agregar un ícono de usuario
    # (En este caso, simplemente dibujamos un círculo más pequeño para la cabeza)
    head_radius = radius // 3
    draw.ellipse((center[0] - head_radius, center[1] - head_radius - head_radius // 2,
                  center[0] + head_radius, center[1] + head_radius - head_radius // 2),
                 fill=text_color)
    
    # Dibujar un cuerpo simplificado
    body_width = head_radius * 2
    body_height = head_radius * 2.5
    draw.rectangle((center[0] - body_width // 2, center[1] + head_radius - head_radius // 2,
                    center[0] + body_width // 2, center[1] + head_radius + body_height - head_radius // 2),
                   fill=text_color)
    
    # Guardar la imagen
    profiles_dir = os.path.join('app', 'static', 'img', 'profiles')
    if not os.path.exists(profiles_dir):
        os.makedirs(profiles_dir)
    
    img.save(os.path.join(profiles_dir, 'default.jpg'))
    print(f"Imagen de perfil predeterminada creada en {profiles_dir}/default.jpg")

if __name__ == "__main__":
    generate_default_profile() 