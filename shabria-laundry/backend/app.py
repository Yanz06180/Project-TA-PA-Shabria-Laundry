"""
Shabria Laundry — Flask Backend
Jalankan: python app.py
"""
from flask import Flask
from flask_cors import CORS
import config

# 1. Inisialisasi Flask app
app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Load konfigurasi keamanan session cookie dari file config.py
app.config["SESSION_COOKIE_SAMESITE"] = config.SESSION_COOKIE_SAMESITE
app.config["SESSION_COOKIE_SECURE"] = config.SESSION_COOKIE_SECURE

# 2. Pasang CORS dengan mengaktifkan supports_credentials=True agar Cookie diizinkan lewat
CORS(app, origins=config.CORS_ORIGINS, supports_credentials=True)

# 3. Import semua blueprint route
from routes.auth import auth_bp
from routes.pelanggan import pelanggan_bp
from routes.layanan import layanan_bp
from routes.transaksi import transaksi_bp
from routes.laporan import laporan_bp
from routes.addon import addon_bp
from routes.user import user_bp

# ── Register blueprints (prefix /api) ────────────────────────
app.register_blueprint(auth_bp,       url_prefix="/api/auth")
app.register_blueprint(pelanggan_bp,  url_prefix="/api/pelanggan")
app.register_blueprint(layanan_bp,    url_prefix="/api/layanan")
app.register_blueprint(transaksi_bp,  url_prefix="/api/transaksi")
app.register_blueprint(laporan_bp,    url_prefix="/api/laporan")
app.register_blueprint(addon_bp,      url_prefix="/api/addon")
app.register_blueprint(user_bp,       url_prefix="/api/user")

@app.route("/api/health")
def health():
    return {"status": "ok", "app": "Shabria Laundry API"}

if __name__ == "__main__":
    # Jalankan server di port 5000 dengan mode debug aktif
    app.run(host="127.0.0.1", port=5000, debug=config.DEBUG)