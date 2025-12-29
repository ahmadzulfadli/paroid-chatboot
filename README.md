# 🤖 Chatbot Fara'idh - Asisten Hukum Waris Islam

Aplikasi chatbot berbasis web cerdas yang dirancang untuk membantu pengguna memahami dan berkonsultasi mengenai hukum waris Islam (Fara'idh). Sistem ini menggunakan model *Machine Learning* **Bi-Directional LSTM (Bi-LSTM)** untuk memahami konteks pertanyaan pengguna dengan akurasi tinggi.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Keras-orange)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![Tailwind](https://img.shields.io/badge/Frontend-TailwindCSS-06B6D4)

## ✨ Fitur Utama
* **Smart Understanding:** Menggunakan arsitektur Bi-LSTM untuk memahami variasi kalimat tanya dari 185 topik (kelas) berbeda.
* **Real-time Response:** Menjawab pertanyaan seputar definisi, syarat waris, dan perhitungan bagian ahli waris secara instan.
* **Modern UI:** Antarmuka responsif dan bersih menggunakan Tailwind CSS.
* **Offline Inference:** Model berjalan lokal tanpa memerlukan koneksi internet untuk proses prediksi (setelah setup awal).

## 🛠️ Teknologi yang Digunakan
* **Backend:** Python (Flask)
* **AI/ML:** TensorFlow, Keras, NLTK, Scikit-learn
* **Arsitektur Model:** Bi-Directional Long Short-Term Memory (Bi-LSTM)
* **Frontend:** HTML5, Tailwind CSS (via CDN), JavaScript

## 📋 Prasyarat Sistem
Sebelum menjalankan aplikasi, pastikan komputer Anda memiliki:
1.  **Python** (Versi 3.8 hingga 3.11 direkomendasikan).
2.  **Git** (Untuk mengunduh repository).
3.  **Virtual Environment** (Disarankan agar library tidak bentrok).

## 🚀 Panduan Instalasi (Step-by-Step)

### 1. Clone Repository
Unduh kode sumber ke komputer Anda:
```bash
git clone [https://github.com/MIstamiAlfariski/TA_1.git](https://github.com/MIstamiAlfariski/TA_1.git)
cd TA_1

# Untuk Windows
python -m venv venv
venv\Scripts\activate

# Untuk Linux/Mac
python3 -m venv venv
source venv/bin/activate

#install library
pip install -r requirements.txt


#pastikan struktur file seperti di bawah
Folder_Proyek/
├── app.py
├── chat.py
├── model/
│   └── chat_model.h5       <-- Letakkan file .h5 di sini
├── tokenizer/
│   ├── tokenizers.pkl      <-- Letakkan file .pkl di sini
│   └── le.pkl
└── dataset/
    └── datahseet.json      <-- Pastikan dataset ada di sini

#jalankan aplikasi
python app.py
#atau
flask run