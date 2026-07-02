"""
Helper koneksi TiDB — dipakai oleh semua route
"""

import pymysql
import pymysql.cursors
import config
import os

def get_conn():
    """Buat koneksi baru ke TiDB. Panggil di setiap request."""
    cfg = config.TIDB_CONFIG.copy()
    
    # Ini dynamic path yang udah bener banget. Jangan diubah!
    pem_path = os.path.join(os.path.dirname(__file__), 'isrgrootx1.pem')
    
    return pymysql.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        ssl_ca=pem_path,
        ssl_verify_cert=cfg.get("ssl_verify_cert", True),
        ssl_verify_identity=cfg.get("ssl_verify_identity", True),
        charset=cfg.get("charset", "utf8mb4"),
        autocommit=cfg.get("autocommit", True),
        cursorclass=pymysql.cursors.DictCursor,   # hasil query jadi dict
    )


def query(sql: str, params=None, fetchall=True):
    """
    Jalankan SELECT. Return list of dict (fetchall=True)
    atau single dict (fetchall=False).
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchall() if fetchall else cur.fetchone()
    except pymysql.MySQLError as e:
        print(f"[DB QUERY ERROR]: {e}")
        raise e
    finally:
        conn.close()


def execute(sql: str, params=None):
    """
    Jalankan INSERT / UPDATE / DELETE.
    Mengembalikan lastrowid (Gunakan LAST_INSERT_ID() di SQL jika AUTO_RANDOM).
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            # conn.commit() dihapus karena sudah di-handle oleh autocommit=True
            return cur.lastrowid
    except pymysql.MySQLError as e:
        print(f"[DB EXECUTE ERROR]: {e}")
        raise e
    finally:
        conn.close()