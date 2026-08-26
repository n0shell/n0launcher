# 🎮 n0launcher (Cartuchos Físicos para PC)

¡Buenas! Este es un proyecto personal que se me ocurrió montando un sistema de **"cartuchos físicos" para PC**. La idea es usar discos duros externos o unidades portátiles conectadas por adaptador (tipo dock) como si fueran cartuchos de toda la vida para tener varios discos con juegos, conectarlos y que cargue todo solo y ordenado.

He subido el código por aquí para tenerlo ordenado, respaldado y por si a alguien le mola la frikada y quiere montarse su propio invento.

---

## 📥 ¿Cómo empezar? (Sin complicaciones)

No hace falta que instales Python ni te compliques compilando nada:
1. Pásate por la sección de **Releases** del repositorio.
2. Descarga el archivo ejecutable (`n0launcher.exe`).
3. Mételo directamente en tu disco duro portátil o en la ruta donde tengas los juegos y ¡a correr! 

⚠️ **¡Atención a las novedades!** Si hay alguna actualización nueva o arreglos importantes, iré avisando por el **[Discord](https://discord.gg/QZhN5X3Ma8)**, así que pásate por ahí para estar al tanto de todo.

---

## 🚀 ¿Qué es y qué hace?

Es una app ligera para Windows pensada para ser la interfaz de este rollo de los discos/cartuchos:
* **Organizar tu biblioteca** con portadas verticales y banners chulos.
* **Meter varios ejecutables (.exe)** por juego (por ejemplo, para separar el modo campaña del multijugador sin volverte loco).
* **Cambiar de tema al vuelo** (trae varios estilos como Dracula, Paper, Retro CRT, Synthwave, Tactical y Nordic Light).
* **Todo guardado en local** con un `config.json` al lado del `.exe` para que no se pierda nada si cambias de PC o desconectas la unidad.
* **Modo pantalla completa** o ventana normal desde el panel de ajustes.

---

## 🛠️ Lo que he usado para hacerlo

Para montar este invento he mezclado un poco de código de escritorio y web:
* **Python**: Para manejar la lógica, leer las configs y lanzar los juegos sin dramas.
* **PyWebView**: Una librería que descubrí y que está guapísima para usar HTML/JS como si fuera una app de escritorio nativa.
* **HTML5, CSS3 y JavaScript**: Para diseñar toda la interfaz, las tarjetas de los juegos y que se mueva fluido.
* **PyInstaller**: Para empaquetar todo el chiringuito en un único archivo `.exe` y olvidarme de dependencias.

---

## ⚙️ ¿Cómo está montado por dentro?

Si te apetece echarle un ojo al código o trastear, la estructura es esta:
* **`main.py`**: El script principal que arranca la app, conecta Python con la interfaz y gestiona los archivos.
* **`main.spec`**: El archivo de configuración de PyInstaller para que empaquete bien los recursos y la carpeta de assets en el `.exe`.
* **`index.html`**: Toda la parte visual del lanzador y las ventanas de configuración.
* **Carpeta `css/`**: Donde tengo guardados los temas (`default.css` y los estilos alternativos).

---

## 💬 ¿Bugs, ideas o aportaciones?

Si le metes mano al código, encuentras algún fallo o se te ocurre alguna mejora guapa para añadirle, pásate por el **[Discord](https://discord.gg/QZhN5X3Ma8)** y me comentas por ahí cualquier cosa o aportación. ¡Toda ayuda es bienvenida!

---

## 📦 Si quieres compilarlo tú mismo

Si te da por modificar el código fuente y sacar tu propia versión del ejecutable, solo tienes que clonar el repositorio, instalar `pywebview` y tirar de este comando en la terminal:

```bash
python -m PyInstaller main.spec
