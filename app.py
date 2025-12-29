from flask import Flask, render_template, request, jsonify
# Pastikan file chat.py yang baru (Bi-LSTM) sudah ada di folder yang sama
from chat import get_response

app = Flask(__name__)

# Route untuk halaman utama (Landing Page)
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk halaman chatbot (Interface Chat)
@app.route('/chatbot')
def chatbot():
    return render_template('aaa.html')

# Route API untuk memproses pesan
# PENTING: JavaScript di aaa.html harus melakukan POST ke alamat '/get' ini
@app.post("/get")
def predict():
    try:
        # Mengambil data JSON dari frontend
        data = request.get_json()
        text = data.get("message")
        
        # Validasi input kosong
        if not text:
            return jsonify({"answer": "Mohon ketik sesuatu."})

        # Dapatkan jawaban dari model Bi-LSTM (via chat.py)
        response = get_response(text)
        
        # Kembalikan ke frontend
        message = {"answer": response}
        return jsonify(message)

    except Exception as e:
        print(f"[Error di app.py]: {e}")
        return jsonify({"answer": "Maaf, terjadi kesalahan internal server."})

if __name__ == '__main__':
    # Gunakan debug=True saat pengembangan agar error terlihat jelas
    app.run(debug=True, host='0.0.0.0', port=5000)
