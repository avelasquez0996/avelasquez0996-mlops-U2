from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Función de predicción ---
def predecir_enfermedad(edad, fiebre, dolor):
    """
    Función que simula la predicción de un modelo médico.
    Retorna uno de los siguientes estados:
    - NO ENFERMO
    - ENFERMEDAD LEVE
    - ENFERMEDAD AGUDA
    - ENFERMEDAD CRÓNICA
    """
    if fiebre < 37 and dolor < 3:
        return "NO ENFERMO"
    elif fiebre < 38 and dolor < 5:
        return "ENFERMEDAD LEVE"
    elif fiebre < 39 and dolor < 8:
        return "ENFERMEDAD AGUDA"
    else:
        return "ENFERMEDAD CRÓNICA"


# --- Endpoint principal ---
@app.route("/predecir", methods=["POST"])
def predecir():
    datos = request.get_json()

    # Validación de campos
    if not datos or not all(k in datos for k in ("edad", "fiebre", "dolor")):
        return jsonify({"error": "Faltan datos. Se requieren: edad, fiebre y dolor"}), 400

    edad = datos["edad"]
    fiebre = datos["fiebre"]
    dolor = datos["dolor"]

    resultado = predecir_enfermedad(edad, fiebre, dolor)

    return jsonify({
        "resultado": resultado,
        "entrada": {"edad": edad, "fiebre": fiebre, "dolor": dolor}
    })


# --- Ruta raíz informativa ---
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "mensaje": "API de predicción médica. Usa POST /predecir con JSON {'edad':..,'fiebre':..,'dolor':..}"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
