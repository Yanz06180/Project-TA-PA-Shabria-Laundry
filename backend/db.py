"""
Helper koneksi TiDB — dipakai oleh semua route
"""

import pymysql
from dbutils.pooled_db import PooledDB
import pymysql.cursors
import config
import os

# Inisialisasi PooledDB
pool = PooledDB(
    creator=pymysql,
    host=config.TIDB_CONFIG["host"],
    port=config.TIDB_CONFIG["port"],
    user=config.TIDB_CONFIG["user"],
    password=config.TIDB_CONFIG["password"],
    database=config.TIDB_CONFIG["database"],
    ssl_ca=os.path.join(os.path.dirname(__file__), 'isrgrootx1.pem'),
    ssl_verify_cert=config.TIDB_CONFIG.get("ssl_verify_cert", True),
    ssl_verify_identity=config.TIDB_CONFIG.get("ssl_verify_identity", True),
    charset=config.TIDB_CONFIG.get("charset", "utf8mb4"),
    autocommit=config.TIDB_CONFIG.get("autocommit", True),
    cursorclass=pymysql.cursors.DictCursor,
    maxconnections=5,
    blocking=True,
    maxconnections=5,
    blocking=True,
    mincached=2,  # Wajib! Biar ada 2 koneksi SSL yang selalu standby siap pakai
    ping=1        # Wajib! Biar otomatis ngecek koneksi mati/hidup
)

def get_conn():
    # 2. get_conn() sekarang TIDAK buka koneksi baru,
    # tapi cuma nyomot koneksi yang udah standby di kolam. (Instant!)
    return pool.connection()


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