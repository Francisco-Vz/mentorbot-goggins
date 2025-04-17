from flask import Flask, request
from dotenv import load_dotenv
import openai
import os
import requests
import json

# ✅ Cargar variables desde .env
load_dotenv()

# ✅ Configuración inicial
app = Flask(__name__)
verify_token = 'gogginspower'
openai.api_key = os.getenv("OPENAI_API_KEY")  # Usa .env para mantenerlo seguro

print("🚀 MentorBot Goggins activo y conectado a OpenAI")

# ✅ Webhook para WhatsApp
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
        data = request.get_json()
        print("📩 MENSAJE RECIBIDO:", data)

        if data and 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if 'value' in change and 'messages' in change['value']:
                            for message in change['value']['messages']:
                                user_message = message['text']['body']
                                sender = message['from']
                                print(f"📨 De {sender}: {user_message}")

                                respuesta = generar_respuesta(user_message)
                                enviar_mensaje(sender, respuesta)

        return 'EVENT_RECEIVED', 200

# ✅ Generar respuesta usando OpenAI
def generar_respuesta(mensaje_usuario):
    prompt = f"Eres un mentor personal motivador como David Goggins. Alguien te escribe: '{mensaje_usuario}'. ¿Qué respuesta motivacional le darías para ayudarle a mejorar cada día?"
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un coach motivacional exigente pero empático, tipo David Goggins."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return respuesta.choices[0].message["content"].strip()
    except Exception as e:
        print("❌ Error al generar respuesta:", e)
        return "No pude procesar tu mensaje, pero sigue empujando, ¡no te detengas!"

# ✅ Enviar mensaje de vuelta a WhatsApp
def enviar_mensaje(destinatario, mensaje):
    url = "https://graph.facebook.com/v18.0/640462612481123/messages"  # ← tu ID de número correcto
    token = os.getenv("WHATSAPP_TOKEN")  # 🔐 Colócalo en .env también

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": destinatario,
        "text": {"body": mensaje}
    }

    try:
        r = requests.post(url, headers=headers, json=payload)
        print("✅ Enviado:", r.status_code, r.text)
    except Exception as e:
        print("❌ Error al enviar mensaje:", e)

# ✅ Ejecutar servidor
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
