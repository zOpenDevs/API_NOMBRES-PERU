import socket
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import buscar_dni, formatear_resultados

app = Flask(__name__)
CORS(app)


@app.route("/api/buscar-dni", methods=["GET", "POST"])
def api_buscar_dni():
    if request.method == "POST":
        data = request.get_json(silent=True) or request.form
    else:
        data = request.args

    nombres = (data.get("nombres") or "").strip().upper()
    ap_paterno = (data.get("apellido_paterno") or "").strip().upper()
    ap_materno = (data.get("apellido_materno") or "").strip().upper()

    if not nombres or not ap_paterno or not ap_materno:
        return jsonify({"error": "Faltan datos: nombres, apellido_paterno, apellido_materno"}), 400

    session = requests.Session()
    try:
        resultados = buscar_dni(session, nombres, ap_paterno, ap_materno)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if resultados.get("success") and resultados.get("data", {}).get("resultados"):
        return jsonify(formatear_resultados(resultados))

    msg = resultados.get("data", {}).get("message", "Sin resultados")
    return jsonify({"error": msg}), 404


if __name__ == "__main__":
    hostname = socket.gethostbyname(socket.gethostname())
    print(f"\ntu endpoint:\nhttp://{hostname}:5000/api/buscar-dni\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
