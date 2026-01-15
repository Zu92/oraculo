from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
import os

app = Flask(__name__)

# Configuración de oráculos (Asegúrate de que las rutas coincidan con tus carpetas)
ORACULOS_CONFIG = {
    "gotico": {
        "titulo": "Oráculo Lenormand Gótico",
        "csv_path": "gotico/cartas_lenormand.csv",
        "background": "linear-gradient(to bottom, #1a0033, #330066)",
        "card_color": "#ffd700",
        "text_color": "#fff",
        "card_background": "rgba(0, 0, 0, 0.8)"
    },
    "navegante": {
        "titulo": "Oráculo Lenormand - Navegante",
        "csv_path": "navegante/cartas_lenormand.csv",
        "background": "linear-gradient(to bottom, #2c1810, #5c3317)",
        "card_color": "#daa520",
        "text_color": "#fff",
        "card_background": "rgba(0, 0, 0, 0.7)"
    },
    "japones": {
        "titulo": "Oráculo Lenormand Japonés",
        "csv_path": "oriental/cartas_lenormand.csv",
        "background": "linear-gradient(135deg, #ff91a4 0%, #ffc0cb 30%, #ffffff 40%, #ffc0cb 70%, #ff91a4 100%)",
        "card_color": "#f30625",
        "text_color": "#1a1a1a",
        "card_background": "rgba(255, 255, 255, 0.9)"
    },
    "rosa": {
        "titulo": "Oráculo Lenormand Rosa",
        "csv_path": "rosa/cartas_lenormand.csv",
        "background": "linear-gradient(135deg, #ff91a4 0%, #ffc0cb 30%, #ffffff 40%, #ffc0cb 70%, #ff91a4 100%)",
        "card_color": "#373637",
        "text_color": "#424143",
        "card_background": "rgba(255, 182, 193, 0.8)"
    }
}

@app.route('/')
def home():
    # Carga la página principal
    return render_template('index.html')

@app.route('/tirar')
def tirar():
    # Obtenemos los parámetros que el usuario eligió en el navegador
    oraculo_id = request.args.get('oraculo', 'rosa')
    cantidad = int(request.args.get('cantidad', 1))

    if oraculo_id not in ORACULOS_CONFIG:
        return jsonify({"error": "Oráculo no encontrado"}), 404

    config = ORACULOS_CONFIG[oraculo_id]
    
    # Leemos el CSV
    try:
        df = pd.read_csv(config["csv_path"])
        cartas_seleccionadas = df.sample(n=cantidad)
        
        # Convertimos a una lista de diccionarios para que JavaScript lo entienda
        resultado = []
        for _, row in cartas_seleccionadas.iterrows():
            resultado.append({
                "nombre": row['nombre'],
                "imagen": str(row['imagen']).replace('\\', '/'), # Ejemplo: "rosa/carta1.jpg"
                "descripcion": row['descripcion'],
                "pregunta": row['pregunta'],
                "accion": row['accion']
            })
        
# Al final de la función tirar()
        return jsonify({
            "cartas": resultado,
            "estilo": {
                "background": config["background"],
                "card_color": config["card_color"],
                "text_color": config["text_color"],
                "card_background": config["card_background"],
                "titulo": config["titulo"]
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)