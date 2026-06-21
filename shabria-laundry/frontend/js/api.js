/* ============================================================
   api.js — ganti BASE_URL sesuai server Flask kamu
   ============================================================ */
const BASE_URL = 'http://localhost:5000/api';

async function _req(method, path, body = null) {
  const opts = {
    method,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);
  const res  = await fetch(BASE_URL + path, opts);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'HTTP ' + res.status);
  return data;
}

const api = {
  get:    (path)        => _req('GET',    path),
  post:   (path, body)  => _req('POST',   path, body),
  put:    (path, body)  => _req('PUT',    path, body),
  patch:  (path, body)  => _req('PATCH',  path, body),
  delete: (path)        => _req('DELETE', path),

  auth: {
    login:  (email, pw) => api.post('/auth/login', { email, password: pw }),
    logout: ()          => api.post('/auth/logout', {}),
    me:     ()          => api.get('/auth/me'),
  },
  pelanggan: {
    all:    (q = '')     => api.get('/pelanggan/' + (q ? '?q=' + q : '')),
    one:    (id)         => api.get('/pelanggan/' + id),
    create: (d)          => api.post('/pelanggan/', d),
    update: (id, d)      => api.put('/pelanggan/' + id, d),
    delete: (id)         => api.delete('/pelanggan/' + id),
  },
  layanan: {
    all:    ()           => api.get('/layanan/'),
    jenis:  ()           => api.get('/layanan/jenis'),
    create: (d)          => api.post('/layanan/', d),
    update: (id, d)      => api.put('/layanan/' + id, d),
    delete: (id)         => api.delete('/layanan/' + id),
  },
  transaksi: {
    all:          (params) => api.get('/transaksi/?' + new URLSearchParams(params || {})),
    one:          (id)     => api.get('/transaksi/' + id),
    create:       (d)      => api.post('/transaksi/', d),
    updateStatus: (id, st) => api.patch('/transaksi/' + id + '/status', { status_pengerjaan: st }),
  },
  laporan: {
    pengeluaran:    (params) => api.get('/laporan/pengeluaran?' + new URLSearchParams(params || {})),
    addPengeluaran: (d)      => api.post('/laporan/pengeluaran', d),
    ringkasan:      (params) => api.get('/laporan/ringkasan?' + new URLSearchParams(params || {})),
    perKategori:    (params) => api.get('/laporan/per-kategori?' + new URLSearchParams(params || {})),
  },
  addon: {
    all: () => api.get('/addon/'),
  },
  user: {
    all:         ()          => api.get('/user/'),
    create:      (d)         => api.post('/user/', d),
    toggleAktif: (id, aktif) => api.patch('/user/' + id + '/aktif', { aktif }),
  },
};

async function requireAuth(allowedRoles) {
  try {
    const user = await api.auth.me();
    if (allowedRoles && allowedRoles.length && !allowedRoles.includes(user.role)) {
      window.location.href = '../index.html';
    }
    return user;
  } catch {
    window.location.href = '../index.html';
  }
}

function showToast(msg, type) {
  let c = document.getElementById('toast-container');
  if (!c) { c = document.createElement('div'); c.id = 'toast-container'; document.body.appendChild(c); }
  const el = document.createElement('div');
  el.className = 'toast ' + (type || '');
  el.textContent = msg;
  c.appendChild(el);
  setTimeout(() => el.remove(), 3000);
}

function formatRupiah(n) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(n || 0);
}
