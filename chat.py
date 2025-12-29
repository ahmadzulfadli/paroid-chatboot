import random
import json
import pickle
import numpy as np
import string
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# --- 1. INISIALISASI (LOAD OTAK AI) ---
print("[INFO] Loading Keras Model & Artifacts...")

# Load Model Bi-LSTM (Path Anda)
model = load_model('model/chat_model.h5')

# Load Tokenizer & Encoder (Path Anda)
with open('tokenizer/tokenizers.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

with open('tokenizer/le.pkl', 'rb') as f:
    le = pickle.load(f)

# Load Database Jawaban (JSON)
with open('dataset/datahseet.json', 'r') as f:
    intents = json.load(f)

# Simpan respon dalam dictionary agar pencarian cepat
responses = {}
for intent in intents['intents']:
    responses[intent['tag']] = intent['responses']

# Dapatkan Input Shape otomatis dari model
input_shape = model.input_shape[1]
print("[INFO] System Ready!")


# --- 2. FUNGSI UTAMA (Dipanggil oleh app.py) ---
def get_response(msg):
    try:
        # A. Preprocessing
        msg_processed = [letters.lower() for letters in msg if letters not in string.punctuation]
        msg_processed = ''.join(msg_processed)
        
        seq = tokenizer.texts_to_sequences([msg_processed])
        
        # Cek apakah kata dikenali (PENTING)
        if not seq or not seq[0]:
             print(f"[DEBUG] Input '{msg}' tidak dikenali sama sekali oleh Tokenizer.")
             # Jika tidak ada kata yang dikenal, langsung tolak
             return "Maaf, saya tidak mengerti kata-kata tersebut. Gunakan bahasa Indonesia yang baku."

        padded = pad_sequences(seq, maxlen=input_shape)

        # B. Prediksi Model
        prediction = model.predict(padded, verbose=0)
        
        # Ambil data prediksi
        results = prediction[0]
        prediction_idx = np.argmax(results)
        confidence_score = results[prediction_idx]
        tag_prediksi = le.inverse_transform([prediction_idx])[0]

        # --- C. LOGIKA HYBRID (FILTER CERDAS) ---
        
        # 1. Daftar Kata Kunci Wajib (VIP List)
        # Jika user menyebut ini, kita anggap pertanyaan serius
        keywords_wajib = [
            "ibu", "ayah", "suami", "istri", "anak", "saudara", "saudari",
            "paman", "kakek", "nenek", "waris", "faraidh", "bagian", 
            "harta", "meninggal", "mayit", "cucu", "ashabah", "hajib"
        ]
        
        # Cek apakah ada kata kunci di pesan user
        is_priority = any(word in msg.lower() for word in keywords_wajib)

        # 2. Tentukan Threshold (Batas Minimal Keyakinan)
        if is_priority:
            # JALUR VIP: Turunkan standar ke 10% agar pertanyaan sulit tetap dijawab
            current_threshold = 0.10 
            status_jalur = "Jalur VIP (Ada kata kunci waris)"
        else:
            # JALUR UMUM: Standar tinggi 50% untuk filter pertanyaan iseng (nasi goreng, dll)
            current_threshold = 0.50
            status_jalur = "Jalur Umum (Tidak ada kata kunci)"

        # --- D. DEBUGGING (TAMPIL DI TERMINAL) ---
        print(f"\n[DEBUG SISTEM]")
        print(f"Pesan User     : {msg}")
        print(f"Tebakan Bot    : {tag_prediksi}")
        print(f"Tingkat Yakin  : {confidence_score:.4f} ({confidence_score*100:.2f}%)")
        print(f"Filter Mode    : {status_jalur}")
        print(f"Syarat Lolos   : > {current_threshold}")
        print(f"------------------------------------------------")

        # --- E. KEPUTUSAN AKHIR ---
        if confidence_score > current_threshold:
            if tag_prediksi in responses:
                return random.choice(responses[tag_prediksi])
        
        # Jika skor masih di bawah threshold (sangat tidak yakin)
        return "Maaf, pertanyaan tersebut di luar konteks Fara'idh. Silakan tanya seputar hukum waris."

    except Exception as e:
        print(f"[ERROR] {e}")
        return "Terjadi kesalahan sistem."

if __name__ == "__main__":
    # Test lokal
    print("Cek Bot: ", get_response("berapa bagian ibu"))