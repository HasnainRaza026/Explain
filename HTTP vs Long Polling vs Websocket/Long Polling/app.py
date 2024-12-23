from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)
app.secret_key = 'bhyguihjbhvgy byuhjkbhjhytfyuguh hjbhvhvgfygujbhjbhg'

messages = []


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    global messages
    data = request.json
    message = data.get('message')
    if message:
        messages.append(message)
        with open("messages.txt", "a") as file:
            file.write(f"{message}\n")
        return jsonify({"success": True}), 200
    return jsonify({"error": "No message provided"}), 400


@app.route('/get_messages', methods=['GET'])
def get_messages():
    global messages
    last_received = int(request.args.get('last_received', 0))
    start_time = time.time()

    while time.time() - start_time < 30:
        if len(messages) > last_received:
            return jsonify({
                "messages": messages[last_received:],
                "last_received": len(messages)
            })
        time.sleep(1)
    
    return jsonify({"messages": [], "last_received": last_received})

if __name__ == "__main__":
    app.run(debug=True)
