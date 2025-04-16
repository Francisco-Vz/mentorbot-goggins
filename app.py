from flask import Flask, request
import os
import sys
import json
from datetime import datetime

print("MentorBot Goggins activo en la nube.", flush=True)
verify_token = 'gogginspower'

app = Flask(__name__)

LOGFILE = "messages.log"

def guardar_log(texto):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {texto}\n")


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == verify_token:
            return challenge, 200
        else:
            return 'Forbidden', 403

    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            print("🔔 JSON recibido completo:", flush=True)
            print(data, flush=True)
            guardar_log(f"JSON recibido: {json.dumps(data, indent=2, ensure_ascii=False)}")

            entry = data.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])

            if messages:
                msg = messages[0]
                phone = msg.get("from")
                text = msg.get("text", {}).get("body")

                mensaje_log = f"📩 Mensaje de {phone}: {text}"
                print(mensaje_log, flush=True)
                guardar_log(mensaje_log)
            else:
                print("⚠️ No se encontraron mensajes dentro del webhook", flush=True)
                guardar_log("⚠️ Webhook sin mensajes")

        except Exception as e:
            error_msg = f"❌ Error procesando el mensaje: {str(e)}"
            print(error_msg, flush=True)
            guardar_log(error_msg)

        return 'EVENT_RECEIVED', 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
