from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'archivos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    archivos = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', archivos=archivos)

@app.route('/guardar', methods=['POST'])
def guardar():
    contenido = request.form['contenido']
    nombre = request.form['nombre']

    if not nombre.endswith('.txt'):
        nombre += '.txt'

    ruta = os.path.join(UPLOAD_FOLDER, nombre)
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return f"✅ Archivo '{nombre}' guardado en el servidor."
    except Exception as e:
        return f"❌ Error al guardar: {str(e)}"

@app.route('/abrir/<nombre>')
def abrir(nombre):
    ruta = os.path.join(UPLOAD_FOLDER, nombre)
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        return {'contenido': contenido}
    except Exception as e:
        return {'error': str(e)}

@app.route('/descargar/<nombre>')
def descargar(nombre):
    return send_from_directory(UPLOAD_FOLDER, nombre, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)