from flask import Flask, request, jsonify
from src.preprocessor import Preprocessor
from src.model import MedicalModel
from src.validator import DataValidator

app = Flask(__name__)

# --- Inicializar componentes ---
preprocessor = Preprocessor()
model = MedicalModel()
validator = DataValidator()


# --- Ruta raíz informativa ---
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "mensaje": "API de predicción médica",
        "version": "1.0",
        "uso": "POST /predecir con JSON {'edad': number, 'fiebre': number, 'dolor': number}"
    })


# --- Endpoint principal de predicción ---
@app.route("/predecir", methods=["POST"])
def predecir():
    """
    Endpoint para predecir enfermedad basado en síntomas del paciente.
    Entrada esperada: {"edad": number, "fiebre": number, "dolor": number}
    """
    try:
        datos = request.get_json()
        
        # Validación de entrada
        if not datos:
            return jsonify({"error": "Se requiere JSON en el body"}), 400
        
        # Validar campos requeridos
        campos_requeridos = ["edad", "fiebre", "dolor"]
        if not all(k in datos for k in campos_requeridos):
            return jsonify({
                "error": f"Faltan datos. Se requieren: {', '.join(campos_requeridos)}"
            }), 400
        
        # Validar tipos y rangos
        validacion = validator.validar(datos)
        if not validacion["valido"]:
            return jsonify({"error": validacion["mensaje"]}), 400
        
        # Preprocesar datos
        datos_procesados = preprocessor.procesar(datos)
        
        # Predicción del modelo
        resultado = model.predecir(datos_procesados)
        
        # Respuesta con estructura solicitada
        return jsonify({
            "resultado": resultado,
            "entrada": datos
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
