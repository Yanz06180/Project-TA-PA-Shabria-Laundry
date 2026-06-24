"""
=============================================================
  KONFIGURASI DATABASE TIDB — SHABRIA LAUNDRY
=============================================================
  CARA MENGISI:
  1. Login ke https://tidbcloud.com
  2. Klik cluster Anda → Connect
  3. Pilih "Connect With: General"
  4. Salin nilai HOST, PORT, USERNAME, PASSWORD, DATABASE
  5. Tempel di bagian TIDB_CONFIG di bawah ini
=============================================================
"""

TIDB_CONFIG = {
    "host":     "gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com",  # ← HOST TiDB Anda
    "port":     4000,                                                    # ← Port TiDB Cloud
    "user":     "3gEW8w9g8ZZf3e4.root",                                  # ← USERNAME TiDB
    "password": "hNFHkpIYFN4d6ugd",                                      # ← PASSWORD TiDB
    "database": "shabria_laundry",                                       # ← Nama DB Anda
    "ssl_ca": r"C:\Kuliah\Pengembangan Aplikasi\Laundry Shabria\App\Project-TA-PA-Shabria-Laundry\backend\isrgrootx1.pem", # ← Path sertifikat SSL
    "ssl_verify_cert": True,
    "ssl_verify_identity": True,
    "charset":  "utf8mb4",
    "autocommit": True,
}

# Secret key Flask untuk enkripsi Session
SECRET_KEY = "shabria-laundry-secret-key-ganti-ini"

# Debug mode — set False di production
DEBUG = True

# CORS origins yang diizinkan mengakses backend (Port Live Server Anda)
CORS_ORIGINS = [
    "http://localhost:5500", 
    "http://127.0.0.1:5500",
    "http://localhost:5501",
    "http://127.0.0.1:5501"
]

# Keamanan Session Cookie untuk Lintas Port Origin (Localhost)
# Menggunakan 'Lax' dan 'False' agar cookie tetap dikirim oleh browser meskipun beda port tanpa HTTPS
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False