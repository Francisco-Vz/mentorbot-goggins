from flask import Flask, request
import os
import json

print("MentorBot Goggins activo en la nube.")
verify_token = 'gogginspower'

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == verify_token:
            print("✅ Verificación de webhook exitosa.")
            return challenge, 200
        else:
            print("❌ Verificación de webhook fallida.")
            return 'Forbidden', 403

    if request.method == 'POST':
        try:
            print("✅ POST recibido")
            raw = request.data
            print("📦 Raw (bytes):", raw)
            json_data = request.get_json(force=True, silent=True)
            print("🧾 JSON parsed:", json.dumps(json_data, indent=2, ensure_ascii=False))
        except Exception as e:
            print("⚠️ Error al procesar POST:", e)
        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
