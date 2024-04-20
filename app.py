from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db

# Configurar la aplicación Flask
app = Flask(__name__)

# Configurar Firebase
cred = credentials.Certificate("clavem.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://masm-289bb-default-rtdb.firebaseio.com/'
})
ref = db.reference('lecturas_temperatura')

# Ruta para mostrar el último dato de la base de datos en tiempo real de Firebase
@app.route('/temp')
def temp():
    last_data = ref.order_by_key().limit_to_last(1).get()

    if last_data:
        last_data_value = list(last_data.values())[0]  # Obtener el último valor
        print("Último dato:", last_data_value)
        return f'Último dato: {last_data_value}'
    else:
        print("No hay datos disponibles.")
        return 'No hay datos disponibles.'

# Ruta principal que renderiza un template HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
