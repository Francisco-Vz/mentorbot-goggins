from flask import Flask, request

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
            return challenge, 200
        else:
            return 'Forbidden', 403

    if request.method == 'POST':
        data = request.get_json()
        print("MENSAJE RECIBIDO:", data)
        return 'EVENT_RECEIVED', 200

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)