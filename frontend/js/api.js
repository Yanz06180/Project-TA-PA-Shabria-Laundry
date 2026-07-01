const BASE_URL = 'https://project-ta-pa-shabria-laundry-backend.vercel.app';

async function _req(method, path, body) {
  var opts = {
    method: method,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
  };
  if (body !== undefined && body !== null) {
    opts.body = JSON.stringify(body);
  }
  var res  = await fetch(BASE_URL + path, opts);
  var data = await res.json().catch(function() { return {}; });
  if (!res.ok) throw new Error(data.error || 'HTTP ' + res.status);
  return data;
}

var api = {
  get:    function(p)      { return _req('GET',    p, null); },
  post:   function(p, b)   { return _req('POST',   p, b);    },
  put:    function(p, b)   { return _req('PUT',    p, b);    },
  patch:  function(p, b)   { return _req('PATCH',  p, b);    },
  delete: function(p)      { return _req('DELETE', p, null); },

  auth: {
    login:  function(e, p) { return api.post('/auth/login', { email: e, password: p }); },
    logout: function()     { return api.post('/auth/logout', {}); },
    me:     function()     { return api.get('/auth/me'); },
  },
  pelanggan: {
    all:    function(q)     { return api.get('/pelanggan/' + (q ? '?q='+q : '')); },
    one:    function(id)    { return api.get('/pelanggan/'+id); },
    create: function(d)     { return api.post('/pelanggan/', d); },
    update: function(id,d)  { return api.put('/pelanggan/'+id, d); },
    delete: function(id)    { return api.delete('/pelanggan/'+id); },
  },
  layanan: {
    all:         function()      { return api.get('/layanan/'); },
    jenis:       function()      { return api.get('/layanan/jenis'); },
    create:      function(d)     { return api.post('/layanan/', d); },
    createJenis: function(d)     { return api.post('/layanan/jenis', d); }, // 👈 INI TAMBAHANNYA
    update:      function(id,d)  { return api.put('/layanan/'+id, d); },
    delete:      function(id)    { return api.delete('/layanan/'+id); }, // (Biarkan aja di API buat jaga-jaga)
  },
  transaksi: {
    all: function(p) {
      return api.get('/transaksi/?'+ new URLSearchParams(p||{}).toString());
    },
    one:          function(id)    { return api.get('/transaksi/'+id); },
    create:       function(d)     { return api.post('/transaksi/', d); },
    updateStatus: function(id,st) {
      return api.patch('/transaksi/'+id+'/status', { status_pengerjaan: st });
    },
  },
  laporan: {
    pengeluaran:    function(p) {
      return api.get('/laporan/pengeluaran?'+new URLSearchParams(p||{}).toString());
    },
    addPengeluaran: function(d) { return api.post('/laporan/pengeluaran', d); },
    ringkasan:      function(p) {
      return api.get('/laporan/ringkasan?'+new URLSearchParams(p||{}).toString());
    },
    perKategori:    function(p) {
      return api.get('/laporan/per-kategori?'+new URLSearchParams(p||{}).toString());
    },
    kirimEmail:     function(d) { return api.post('/send-report', d); }, // 🌟 BARU: Untuk kirim email laporan
  },
  addon: {
    all:    function()      { return api.get('/addon/'); },
    create: function(d)     { return api.post('/addon/', d); },
    update: function(id, d) { return api.put('/addon/'+id, d); },
    delete: function(id)    { return api.delete('/addon/'+id); }
  },
  user: {
    all:         function()      { return api.get('/user/'); },
    create:      function(d)     { return api.post('/user/', d); },
    toggleAktif: function(id,a)  { return api.patch('/user/'+id+'/aktif', { aktif: a }); },
  },
};

// ── Auth guard ─────────────────────────────────────────────────
async function requireAuth(roles) {
  var stored = sessionStorage.getItem('currentUser');
  if (stored) {
    try {
      var u = JSON.parse(stored);
      if (u && u.role) {
        var r = u.role.toLowerCase();
        if (roles && roles.length && !roles.includes(r)) {
          sessionStorage.removeItem('currentUser');
          window.location.href = '../index.html';
          return null;
        }
        u.role = r;
        return u;
      }
    } catch(e) {
      sessionStorage.removeItem('currentUser');
    }
  }
  try {
    var u = await api.auth.me();
    u.role = (u.role || '').toLowerCase();
    sessionStorage.setItem('currentUser', JSON.stringify(u));
    if (roles && roles.length && !roles.includes(u.role)) {
      sessionStorage.removeItem('currentUser');
      window.location.href = '../index.html';
      return null;
    }
    return u;
  } catch(e) {
    window.location.href = '../index.html';
    return null;
  }
}

function formatRupiah(n) {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency', currency: 'IDR', minimumFractionDigits: 0
  }).format(n || 0);
}

function showToast(msg, type) {
  var c = document.getElementById('toast-container');
  if (!c) {
    c = document.createElement('div');
    c.id = 'toast-container';
    document.body.appendChild(c);
  }
  var el = document.createElement('div');
  el.className = 'toast ' + (type || '');
  el.textContent = msg;
  c.appendChild(el);
  setTimeout(function() { if(el.parentNode) el.remove(); }, 3000);
}

async function doLogout() {
  try { await api.auth.logout(); } catch(e) {}
  sessionStorage.removeItem('currentUser');
  window.location.href = '../index.html';
}

