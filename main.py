import webview
import json
import os
import sys
import subprocess

# Detectar si estamos ejecutando en el .exe compilado o en desarrollo normal
if getattr(sys, 'frozen', False):
    # Directorio temporal de PyInstaller para los recursos incluidos (assets, html, css)
    BASE_DIR = sys._MEIPASS
    # Directorio real donde está guardado el .exe (para guardar el config.json permanentemente)
    REAL_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    REAL_DIR = BASE_DIR

CONFIG_FILE = os.path.join(REAL_DIR, 'config.json')
HTML_FILE = os.path.join(BASE_DIR, 'assets', 'index.html') 

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "games": [],
        "theme": "default.css",
        "fullscreen": False
    }

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

class Api:
    def __init__(self):
        self.window = None

    def get_config(self):
        return load_config()

    def set_theme(self, theme_name):
        config = load_config()
        config['theme'] = theme_name
        save_config(config)
        return {"status": "ok"}

    def set_fullscreen(self, is_fullscreen):
        config = load_config()
        config['fullscreen'] = is_fullscreen
        save_config(config)
        if self.window:
            self.window.toggle_fullscreen()
        return {"status": "ok"}

    def add_game(self, game_data):
        config = load_config()
        config['games'].append(game_data)
        save_config(config)
        return {"status": "ok"}

    def update_game(self, game_data):
        config = load_config()
        config['games'] = [g if g['id'] != game_data['id'] else game_data for g in config['games']]
        save_config(config)
        return {"status": "ok"}

    def delete_game(self, game_id):
        config = load_config()
        config['games'] = [g for g in config['games'] if g['id'] != game_id]
        save_config(config)
        return {"status": "ok"}

    def select_image(self):
        if not self.window:
            return ""
        file_types = ('Archivos de Imagen (*.jpg;*.jpeg;*.png;*.webp)', 'Todos los archivos (*.*)')
        result = self.window.create_file_dialog(webview.OPEN_DIALOG, dialog_title="Seleccionar Portada o Banner", file_types=file_types)
        if result and len(result) > 0:
            return result[0]
        return ""

    def select_file(self, file_type):
        if not self.window:
            return ""
        file_types = ('Ejecutables (*.exe)', 'Todos los archivos (*.*)') if file_type == "exe" else ('Todos los archivos (*.*)',)
        result = self.window.create_file_dialog(webview.OPEN_DIALOG, dialog_title="Seleccionar Ejecutable", file_types=file_types)
        if result and len(result) > 0:
            return result[0]
        return ""

    def import_custom_theme(self):
        if not self.window:
            return {"status": "error"}
        file_types = ('Hojas de estilo (*.css)', 'Todos los archivos (*.*)')
        result = self.window.create_file_dialog(webview.OPEN_DIALOG, dialog_title="Importar Tema CSS", file_types=file_types)
        if result and len(result) > 0:
            source_path = result[0]
            filename = os.path.basename(source_path)
            
            # Los temas personalizados se guardarán en la carpeta real junto al ejecutable para que no se pierdan
            css_dir = os.path.join(REAL_DIR, 'assets', 'css')
            if not os.path.exists(css_dir):
                os.makedirs(css_dir)
                
            dest_path = os.path.join(css_dir, filename)
            try:
                with open(source_path, 'r', encoding='utf-8') as src, open(dest_path, 'w', encoding='utf-8') as dest:
                    dest.write(src.read())
                return {"status": "ok", "filename": filename}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        return {"status": "cancelled"}

    def get_available_themes(self):
        # Busca tanto en los temas por defecto de los assets como en la carpeta externa por si hay añadidos
        css_dirs = [
            os.path.join(BASE_DIR, 'assets', 'css'),
            os.path.join(REAL_DIR, 'assets', 'css')
        ]
        themes = set()
        for css_dir in css_dirs:
            if os.path.exists(css_dir):
                for f in os.listdir(css_dir):
                    if f.endswith('.css'):
                        themes.add(f)
        
        theme_list = list(themes)
        if not theme_list:
            theme_list = ['default.css']
        return theme_list

    def launch_executable(self, path):
        try:
            if not os.path.exists(path):
                return {"status": "error", "message": f"No se encuentra el archivo:\n{path}"}
            
            subprocess.Popen(path, cwd=os.path.dirname(path))
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    api = Api()
    
    # Crear carpeta css local si no existe
    css_folder = os.path.join(REAL_DIR, 'assets', 'css')
    if not os.path.exists(css_folder):
        os.makedirs(css_folder)

    if not os.path.exists(HTML_FILE):
        print(f"\n[ERROR CRÍTICO] No se encuentra el archivo index.html en:\n{HTML_FILE}\n")
    
    config = load_config()

    window = webview.create_window(
        'Launcher', 
        HTML_FILE, 
        js_api=api, 
        width=1280, 
        height=720,
        fullscreen=config.get("fullscreen", False),
        background_color='#111111'
    )
    
    api.window = window
    webview.start(debug=False)