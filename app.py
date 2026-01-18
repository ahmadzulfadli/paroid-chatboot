from flask import Flask, render_template, request, jsonify

# Kita import logika otak bot dari file sebelah (faraidh_engine.py)
# Pastikan file faraidh_engine.py ada di folder yang sama
from chat import get_bot_response

app = Flask(__name__)

# ==========================================
# 1. ROUTE HALAMAN WEBSITE (UI)
# ==========================================

@app.route('/')
def home():
    """
    Route untuk halaman Beranda (Home).
    Diakses via: http://localhost:5000/
    File HTML: templates/index.html
    """
    return render_template('index.html')

@app.route('/chat')
def aaa():
    """
    Route untuk halaman Room Chatbot.
    Diakses via: http://localhost:5000/chat
    File HTML: templates/aaa.html
    
    Catatan: Nama fungsi ini adalah 'aaa', jadi di HTML
    Anda bisa memanggilnya dengan {{ url_for('aaa') }}
    """
    return render_template('aaa.html')

# ==========================================
# 2. ROUTE API (Jalur Data Chat)
# ==========================================

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """
    API ini menerima pesan JSON dari JavaScript di aaa.html,
    mengirimnya ke Engine AI, dan mengembalikan jawaban.
    """
    # 1. Ambil data pesan dari user
    user_input = request.json.get('message')
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    # 2. Proses pesan menggunakan Engine Faraidh
    # (Fungsi ini ada di file faraidh_engine.py)
    bot_response = get_bot_response(user_input)
    
    # 3. Kembalikan jawaban ke frontend
    return jsonify(bot_response)

# ==========================================
# 3. MENJALANKAN SERVER
# ==========================================
if __name__ == '__main__':
    print("🚀 Server Flask Faraidh berjalan...")
    print("👉 Buka di browser: http://127.0.0.1:5000")
    # debug=True agar server auto-restart kalau ada perubahan kode
    app.run(debug=True, port=5000)