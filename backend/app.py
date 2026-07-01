from flask import Flask
from flask_cors import CORS
import config
from routes.invoice import invoice_bp  

from routes.auth      import auth_bp
from routes.pelanggan import pelanggan_bp
from routes.layanan   import layanan_bp
from routes.transaksi import transaksi_bp
from routes.laporan   import laporan_bp
from routes.addon     import addon_bp
from routes.user      import user_bp
from routes.report    import report_bp
from flask import Flask, request, jsonify
from db import query, execute # 🌟 WAJIB: Import dari db.py
import requests # 🌟 WAJIB: Biar bisa nembak API Fonnte
import config


app = Flask(__name__)
app.secret_key = config.SECRET_KEY

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
)


CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.register_blueprint(auth_bp,      url_prefix="/api/auth")
app.register_blueprint(pelanggan_bp, url_prefix="/api/pelanggan")
app.register_blueprint(layanan_bp,   url_prefix="/api/layanan")
app.register_blueprint(transaksi_bp, url_prefix="/api/transaksi")
app.register_blueprint(laporan_bp,   url_prefix="/api/laporan")
app.register_blueprint(addon_bp,     url_prefix="/api/addon")
app.register_blueprint(user_bp,      url_prefix="/api/user")
app.register_blueprint(report_bp)
app.register_blueprint(invoice_bp, url_prefix='/api')

@app.route("/api/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
    
