from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/frete")
def calcular_frete():
    cep_destino = request.args.get("cep")

    if not cep_destino:
        return jsonify({"erro": "Informe um CEP"}), 400

    # Simulação de retorno
    resultados = [
        {"name": "PAC", "price": "19.90", "delivery_time": 5},
        {"name": "SEDEX", "price": "29.90", "delivery_time": 2}
    ]
    return jsonify(resultados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)