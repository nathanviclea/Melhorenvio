from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Token real da API do Melhor Envio
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiM2VjNzFlOTNjOTY1OWEyODExNjY1YzVjYmI4MDMxZGY2MTAyMmVkZTY0MmMzOTk5ZGJjODFhNDgxZGU4NGU1NDJmMjk5YmNmYzc3OTg1YmMiLCJpYXQiOjE3NDUwMjgyOTcuMTQzMjA1LCJuYmYiOjE3NDUwMjgyOTcuMTQzMjA2LCJleHAiOjE3NzY1NjQyOTcuMTMwMzgsInN1YiI6ImVjOGRjMTIyLTNmZjctNDMwZS1iYmYwLTYzZTQyOTY2NDc1ZiIsInNjb3BlcyI6WyJjYXJ0LXJlYWQiLCJjYXJ0LXdyaXRlIiwiY29tcGFuaWVzLXJlYWQiLCJjb21wYW5pZXMtd3JpdGUiLCJjb3Vwb25zLXJlYWQiLCJjb3Vwb25zLXdyaXRlIiwibm90aWZpY2F0aW9ucy1yZWFkIiwib3JkZXJzLXJlYWQiLCJwcm9kdWN0cy1yZWFkIiwicHJvZHVjdHMtZGVzdHJveSIsInByb2R1Y3RzLXdyaXRlIiwicHVyY2hhc2VzLXJlYWQiLCJzaGlwcGluZy1jYWxjdWxhdGUiLCJzaGlwcGluZy1jYW5jZWwiLCJzaGlwcGluZy1jaGVja291dCIsInNoaXBwaW5nLWNvbXBhbmllcyIsInNoaXBwaW5nLWdlbmVyYXRlIiwic2hpcHBpbmctcHJldmlldyIsInNoaXBwaW5nLXByaW50Iiwic2hpcHBpbmctc2hhcmUiLCJzaGlwcGluZy10cmFja2luZyIsImVjb21tZXJjZS1zaGlwcGluZyIsInRyYW5zYWN0aW9ucy1yZWFkIiwidXNlcnMtcmVhZCIsInVzZXJzLXdyaXRlIiwid2ViaG9va3MtcmVhZCIsIndlYmhvb2tzLXdyaXRlIiwid2ViaG9va3MtZGVsZXRlIiwidGRlYWxlci13ZWJob29rIl19.R_uDg5XpRfOZYbMScUcOVrTfwDbjSNpGswHU-UmDobwO4LgKFF_CMqGGeHaUBFqUuoFUcjadVHeTCiazQ03NQMRHL5EFcuYdDWMU-3TO2Q_OHon24N5erahgRLDZf9O9TuOnEx0QKY1pLRuc69PGXLNuC56_uSFT2A7zW7XIYmgne-jsyUryfUstVQUy7idA1mobsOwbTWKgZIVhL6dvB1Jsg2wPfkzDGr34vfveG9BQjjGBqWozjKMXvIS64G9uoRW4qqQGkDlRKrp5CGyPZnj59TWG1yTdm6ePEu_XwRlqZhOU3iaj0sNtvXMgeWoG3Tv4XtAYEt8_Y0BCNVbwbipnGbeDq7bDydmfFzr-n4jg6iMOE72rkaFeAIqfrp9yV-_5DWzgOk3laGSRC43sPhaLcBVbL6iLBBzHH-RT1dJpooePrhyl6J5310bdPLITpWNgHse2DEOx-1PwB4xa_Qi8bqJpc7COvpADyxlUTrxh9KWoyqGXLn02KqWxyXfLd3jktzcuYLhMl2VVFXANIIUhSk1-UXip27rP0t868IjpSyC-JtaDEjcetg05RCrcpVwJT8xZ_Rpgm67yDCKBSYtosTvCO-oQzFkumIVAkqWoHn_qCep2whz6m8k0ao8sYfCni3LJCc5i8PvWBsuKTuWv7PKbXTf6XIpZDCOcR5A"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Rogers (nathan@rogers.com.br)"
}

@app.route("/frete")
def calcular_frete():
    cep_destino = request.args.get("cep")

    if not cep_destino:
        return jsonify({"erro": "Informe um CEP"}), 400

    payload = {
        "from": {"postal_code": "08674090"},
        "to": {"postal_code": cep_destino},
        "products": [
            {
                "id": "1",
                "width": 15,
                "height": 5,
                "length": 20,
                "weight": 1.0,
                "insurance_value": 0,
                "quantity": 1
            }
        ]
    }

    try:
        response = requests.post(
            "https://www.melhorenvio.com.br/api/v2/me/shipment/calculate",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            return jsonify({"erro": "Erro na consulta"}), response.status_code

        resultado = []
        for option in response.json():
            nome = option.get("name")
            valor = option.get("price")
            prazo = option.get("delivery_time")

            if nome and valor and prazo:
                resultado.append({
                    "name": nome,
                    "price": valor,
                    "delivery_time": prazo
                })

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
