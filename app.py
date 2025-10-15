from flask import Flask, render_template, request, jsonify
from modelo import clasificador

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    texto = data.get('text', '')
    resultado = clasificador(texto)
    return jsonify(resultado)

if __name__ == '__main__':
    # Ejecuta el servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
