import tensorflow as tf
import pickle
import numpy as np
import json
import random
import re
from fractions import Fraction
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from pathlib import Path

# ==========================================
# 1. KONFIGURASI PATH DINAMIS (Pathlib)
# ==========================================
# Mendapatkan direktori root project (TA_1)
BASE_DIR = Path(__file__).resolve().parent

# Mendefinisikan lokasi file secara relatif terhadap BASE_DIR
MODEL_PATH = BASE_DIR / "model" / "faraidh_model_final.h5"
TOKENIZER_PATH = BASE_DIR / "tokenizer" / "tokenizer.pickle"
ENCODER_PATH = BASE_DIR / "tokenizer" / "label_encoder.pickle"  # Disarankan dipisah
DATASET_PATH = BASE_DIR / "dataset" / "faraidh_dataset.json"

# ==========================================
# 2. INISIALISASI MODEL & ARTIFACTS
# ==========================================
print("🔄 [Engine] Sedang memuat Model AI & Dictionary...")

try:
    # Load Model Keras
    model = load_model(str(MODEL_PATH))
    
    # Load Tokenizer
    with open(TOKENIZER_PATH, 'rb') as handle:
        tokenizer = pickle.load(handle)
        
    # Load Label Encoder 
    # Pastikan file ini ada, jika label encoder digabung di tokenizer.pickle, 
    # sesuaikan kembali ke TOKENIZER_PATH
    with open(ENCODER_PATH, 'rb') as handle:
        lbl_encoder = pickle.load(handle)
    
    # Load Dataset untuk Response Teks
    with open(DATASET_PATH, 'r') as f:
        data_source = json.load(f)
        responses_lookup = {i['tag']: i['responses'] for i in data_source['intents']}
        
    print(f"✅ [Engine] Berhasil dimuat dari: {BASE_DIR}")

except Exception as e:
    print(f"❌ [Engine Error] Gagal load file: {e}")
    model, tokenizer, lbl_encoder, responses_lookup = None, None, None, {}

# ==========================================
# 3. CLASS CALCULATOR (Engine Matematika)
# ==========================================
class FaraidhCalculator:
    def __init__(self):
        self.hijab_rules = {
            'anak_laki': ['cucu_laki', 'cucu_perempuan', 'saudara_kandung', 'saudara_seayah', 'saudara_seibu', 'paman_kandung', 'paman_seayah', 'sepupu'],
            'anak_perempuan': ['saudara_seibu'], 
            'ayah': ['kakek', 'saudara_seibu', 'paman_kandung', 'paman_seayah', 'sepupu', 'cucu_laki'], 
            'ibu': ['nenek_ibu', 'nenek_ayah'],
            'kakek': ['paman_kandung', 'paman_seayah', 'sepupu'],
            'suami': [], 'istri': []
        }

    def _apply_hijab(self, heirs):
        active = heirs.copy()
        if 'anak_laki' in active:
            for h in ['cucu_laki', 'cucu_perempuan', 'saudara_kandung', 'saudara_seayah', 'saudara_seibu', 'paman_kandung']:
                if h in active: active.pop(h, None)
        if 'ayah' in active:
            for h in ['kakek', 'saudara_seibu', 'saudara_kandung', 'saudara_seayah', 'paman_kandung']:
                if h in active: active.pop(h, None)
        if 'ibu' in active:
            for h in ['nenek_ibu', 'nenek_ayah']:
                if h in active: active.pop(h, None)
        return active

    def run_calculation(self, total_harta, heirs_count):
        active_heirs = self._apply_hijab(heirs_count)
        shares = {}
        total_share_fraction = Fraction(0, 1)
        
        has_descendant = any(x in active_heirs for x in ['anak_laki', 'anak_perempuan', 'cucu_laki'])
        
        # --- LOGIKA BAGIAN PASTI (Ashabul Furud) ---
        if 'suami' in active_heirs:
            share = Fraction(1, 4) if has_descendant else Fraction(1, 2)
            shares['suami'] = share; total_share_fraction += share
        if 'istri' in active_heirs:
            share = Fraction(1, 8) if has_descendant else Fraction(1, 4)
            shares['istri'] = share; total_share_fraction += share
        if 'ibu' in active_heirs:
            num_siblings = sum(active_heirs.get(k, 0) for k in ['saudara_kandung', 'saudara_seayah', 'saudara_seibu'])
            share = Fraction(1, 6) if has_descendant or num_siblings >= 2 else Fraction(1, 3)
            shares['ibu'] = share; total_share_fraction += share
        if 'ayah' in active_heirs:
            if 'anak_laki' in active_heirs or 'cucu_laki' in active_heirs:
                shares['ayah'] = Fraction(1, 6); total_share_fraction += Fraction(1, 6)
            elif 'anak_perempuan' in active_heirs:
                shares['ayah'] = Fraction(1, 6); total_share_fraction += Fraction(1, 6)
        if 'anak_perempuan' in active_heirs and 'anak_laki' not in active_heirs:
            count = active_heirs['anak_perempuan']
            share = Fraction(2, 3) if count >= 2 else Fraction(1, 2)
            shares['anak_perempuan'] = share; total_share_fraction += share

        # --- LOGIKA SISA (ASABAH) ---
        remaining = Fraction(1, 1) - total_share_fraction
        if remaining < 0: remaining = Fraction(0, 1)

        if 'anak_laki' in active_heirs:
            sons = active_heirs['anak_laki']
            daughters = active_heirs.get('anak_perempuan', 0)
            total_parts = (sons * 2) + daughters
            shares['anak_laki'] = remaining * Fraction(sons * 2, total_parts)
            if daughters > 0: shares['anak_perempuan'] = remaining * Fraction(daughters, total_parts)
        elif 'ayah' in active_heirs and 'anak_laki' not in active_heirs and 'cucu_laki' not in active_heirs:
            shares['ayah'] = shares.get('ayah', Fraction(0,1)) + remaining

        final_report = []
        for heir, frac in shares.items():
            if frac > 0:
                count = active_heirs.get(heir, 1)
                nominal = float(frac) * total_harta
                percentage = float(frac) * 100
                nominal_str = f"Rp {nominal:,.0f}".replace(",", ".")
                
                final_report.append({
                    'heir': heir.upper().replace('_', ' '), 
                    'count': count, 
                    'fraction': str(frac),
                    'nominal': nominal_str,
                    'percentage': round(percentage, 2)
                })
        return final_report

engine = FaraidhCalculator()

# ==========================================
# 4. HELPER FUNCTIONS & BOT LOGIC
# ==========================================
def parse_nominal_harta(text):
    text = text.lower().replace('.', '').replace(',', '.')
    multipliers = {'t': 1e12, 'm': 1e9, 'milyar': 1e9, 'jt': 1e6, 'juta': 1e6, 'rb': 1e3}
    for unit, mult in multipliers.items():
        match = re.search(r"(\d+(?:\.\d+)?)\s*" + unit, text)
        if match: return int(float(match.group(1)) * mult)
    raw = re.findall(r"(\d{6,})", text)
    return int(raw[0]) if raw else 0

heir_synonyms = {
    'anak_laki': ['anak laki', 'anak cowok', 'putra', 'lk', 'anak lk', 'anak pria', 'pria', 'laki-laki', 'laki'],
    'anak_perempuan': ['anak perempuan', 'anak cewek', 'putri', 'pr', 'anak pr', 'anak wanita', 'wanita', 'perempuan', 'gadis'],
    'ibu': ['ibu', 'bunda', 'mamak', 'umi'], 
    'ayah': ['ayah', 'bapak', 'abi', 'papa'],
    'suami': ['suami', 'pasangan pria'], 
    'istri': ['istri', 'pasangan wanita'], 
    'saudara_kandung': ['saudara', 'kakak', 'adik']
}

def parse_kasus_waris(text):
    text = text.lower()
    detected = {}
    for key, syns in heir_synonyms.items():
        for s in syns:
            pattern = r"(\b\d{1,2}\b)\s*" + re.escape(s) + r"\b" 
            matches = re.findall(pattern, text)
            for count in matches: 
                detected[key] = detected.get(key, 0) + int(count)
    
    for key, syns in heir_synonyms.items():
        if key not in detected:
            for s in syns:
                pattern_single = r"\b" + re.escape(s) + r"\b"
                if re.search(pattern_single, text): 
                    detected[key] = 1
                    break
    return detected

keyword_map = {
    "pembunuh": "hukum_waris_pembunuh", 
    "ibu": "rincian_bagian_ibu",
    "ayah": "rincian_bagian_ayah", 
    "faraidh": "definisi_ilmu_waris",
    "sebatang kara": "sebatang_kara"
}

def get_bot_response(text):
    if model is None:
        return {"type": "text", "message": "Error: Model AI belum dimuat."}

    text_lower = text.lower()
    for k, v in {"faridh": "faraidh", "jelasin": "jelaskan", "brp": "berapa"}.items(): 
        text_lower = text_lower.replace(k, v)

    # LAYER 1: Perhitungan Matematika
    if (any(c.isdigit() for c in text_lower) and 
       ("hitung" in text_lower or "harta" in text_lower or "waris" in text_lower)):
        data_waris = parse_kasus_waris(text_lower)
        harta = parse_nominal_harta(text_lower)
        harta_used = harta if harta > 0 else 0
        
        if len(data_waris) > 0:
            try:
                result = engine.run_calculation(harta_used, data_waris)
                return {"type": "calculation", "data": result, "total_harta": harta_used}
            except: pass

    # LAYER 2: Rule Based
    for k, tag in keyword_map.items():
        if k in text_lower and tag in responses_lookup:
            return {"type": "text", "message": random.choice(responses_lookup[tag])}

    # LAYER 3: AI Prediction
    seq = tokenizer.texts_to_sequences([text_lower])
    padded = pad_sequences(seq, maxlen=25)
    pred = model.predict(padded, verbose=0)
    
    confidence_score = np.max(pred)
    tag_index = np.argmax(pred)
    tag = lbl_encoder.inverse_transform([tag_index])[0]
    
    if confidence_score < 0.70:
        return {
            "type": "text", 
            "message": "Maaf, saya hanya dilatih untuk menjawab seputar Hukum Waris Islam (Faraidh)."
        }
    
    return {"type": "text", "message": random.choice(responses_lookup[tag])}