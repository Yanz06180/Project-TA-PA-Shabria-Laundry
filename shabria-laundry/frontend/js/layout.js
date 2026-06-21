/* ─────────────────────────────────────────────────────────────
   layout.js
   PENTING: BASE_URL, requireAuth, doLogout, formatRupiah, dan
   showToast SENGAJA tidak dideklarasikan ulang di sini karena
   sudah ada di api.js. File ini wajib dimuat SETELAH api.js:
     <script src="../js/api.js"></script>
     <script src="../js/layout.js"></script>
   Mendeklarasikan ulang `const BASE_URL` di dua file yang
   berbagi global scope yang sama akan menyebabkan SyntaxError
   ("Identifier 'BASE_URL' has already been declared") saat
   layout.js dimuat, sehingga SELURUH isi layout.js (termasuk
   initAdminLayout/initManagerLayout yang merender sidebar,
   header, dan tombol logout) gagal dieksekusi.
   ───────────────────────────────────────────────────────────── */

const ADMIN_NAV = [
  { href:'dashboard.html',  icon:'📊', label:'Dashboard'       },
  { href:'customers.html',  icon:'👥', label:'Customer'         },
  { href:'transaksi.html',  icon:'🧾', label:'Transaksi'        },
  { href:'laporan.html',    icon:'📈', label:'Laporan'          },
  { href:'layanan.html',    icon:'⚙️',  label:'Kelola Layanan'  },
];

const MANAGER_NAV = [
  { href:'dashboard.html',    icon:'📊', label:'Dashboard'           },
  { href:'monitor.html',      icon:'📋', label:'Monitor Transaksi'   },
  { href:'laporan.html',      icon:'📈', label:'Laporan'             },
  { href:'akun-admin.html',   icon:'👤', label:'Akun Admin'          },
];

function _sidebarHTML(navItems, user, accent, accentLight, roleLabel) {
  var page = window.location.pathname.split('/').pop() || 'dashboard.html';
  var html = '<aside style="width:240px;height:100%;background:white;'
    + 'border-right:1px solid #E5E7EB;display:flex;flex-direction:column;'
    + 'box-shadow:2px 0 12px rgba(0,0,0,0.06);">';

  // Logo
  html += '<div style="display:flex;align-items:center;gap:10px;padding:18px 14px 14px;'
    + 'border-bottom:1px solid #F3F4F6;">'
    + '<img src="../assets/logo.jpg" style="width:38px;height:38px;border-radius:9px;'
    + 'border:1px solid #E5E7EB;padding:4px;object-fit:contain;" onerror="this.style.display=\'none\'">'
    + '<div style="flex:1;">'
    + '<p style="font-size:13px;font-weight:800;color:#111827;margin:0;">Shabria Laundry</p>'
    + '<p style="font-size:10px;font-weight:600;color:' + accent + ';margin:0;">' + roleLabel + '</p>'
    + '</div>'
    + '<button onclick="closeSidebar()" style="background:none;border:none;cursor:pointer;'
    + 'font-size:16px;color:#9CA3AF;flex-shrink:0;" class="sb-close-btn">✕</button>'
    + '</div>';

  // User badge
  if (user) {
    html += '<div style="margin:10px 8px 4px;padding:10px 12px;border-radius:12px;background:'
      + accentLight + ';">'
      + '<p style="font-size:12px;font-weight:700;color:' + accent + ';margin:0;">' + (user.nama||'') + '</p>'
      + '<p style="font-size:10px;color:#9CA3AF;margin:2px 0 0;">' + (user.email||'') + '</p>'
      + '</div>';
  }

  // Nav
  html += '<nav style="padding:8px 8px;flex:1;overflow-y:auto;">';
  navItems.forEach(function(n) {
    var isActive = (page === n.href);
    html += '<a href="' + n.href + '" style="display:flex;align-items:center;gap:11px;'
      + 'padding:10px 12px;border-radius:11px;text-decoration:none;font-size:14px;'
      + 'margin-bottom:2px;transition:all 0.12s;'
      + 'font-weight:' + (isActive ? 700 : 500) + ';'
      + 'color:' + (isActive ? accent : '#6B7280') + ';'
      + 'background:' + (isActive ? accentLight : 'transparent') + ';">'
      + '<span style="font-size:17px;">' + n.icon + '</span>'
      + '<span style="flex:1;">' + n.label + '</span>'
      + (isActive ? '<span style="color:' + accent + ';">›</span>' : '')
      + '</a>';
  });
  html += '</nav>';

  // Logout
  html += '<div style="padding:10px 8px;border-top:1px solid #F3F4F6;">'
    + '<button onclick="doLogout()" style="display:flex;align-items:center;gap:10px;'
    + 'width:100%;padding:10px 12px;border-radius:11px;border:none;cursor:pointer;'
    + 'background:#FEF2F2;color:#DC2626;font-size:13px;font-weight:700;">🚪 Keluar</button>'
    + '</div>';

  html += '</aside>';
  return html;
}

function _headerHTML(user, pageLabel, accent, accentLight, roleLabel) {
  return '<header style="height:60px;display:flex;align-items:center;gap:12px;'
    + 'padding:0 20px;background:white;border-bottom:1px solid #E5E7EB;'
    + 'box-shadow:0 1px 6px rgba(0,0,0,0.05);flex-shrink:0;">'
    // Hamburger
    + '<button onclick="openSidebar()" class="hamburger-btn" style="background:none;border:none;'
    + 'cursor:pointer;font-size:20px;display:none;">☰</button>'
    // Logo mobile
    + '<div class="logo-mobile" style="display:none;align-items:center;gap:8px;">'
    + '<img src="../assets/logo.jpg" style="width:28px;height:28px;border-radius:7px;'
    + 'border:1px solid #E5E7EB;padding:3px;object-fit:contain;" onerror="this.style.display=\'none\'">'
    + '<span style="font-size:13px;font-weight:800;color:#111827;">Shabria Laundry</span>'
    + '</div>'
    + '<div style="flex:1;"></div>'
    // Breadcrumb
    + '<span class="page-label" style="font-size:13px;color:#9CA3AF;">' + pageLabel + '</span>'
    // User + logout
    + '<div style="display:flex;align-items:center;gap:10px;margin-left:8px;">'
    + '<div class="user-block" style="text-align:right;">'
    + '<p style="font-size:13px;font-weight:700;color:#111827;margin:0;">' + (user ? user.nama : '') + '</p>'
    + '<p style="font-size:10px;color:#9CA3AF;margin:0;">' + roleLabel + '</p>'
    + '</div>'
    + '<button onclick="doLogout()" style="display:flex;align-items:center;gap:5px;'
    + 'padding:7px 12px;border-radius:10px;background:#FEF2F2;border:none;cursor:pointer;'
    + 'color:#DC2626;font-size:12px;font-weight:600;">🚪 <span class="logout-txt">Keluar</span></button>'
    + '</div>'
    + '</header>';
}

function initAdminLayout(user, page) {
  _init(user, page, ADMIN_NAV, '#1565C0', '#EFF6FF', 'Panel Admin (Kasir)');
}

function initManagerLayout(user, page) {
  _init(user, page, MANAGER_NAV, '#15803D', '#F0FDF4', 'Panel Manager (Owner)');
}

function _init(user, page, navItems, accent, accentLight, roleLabel) {
  var pageLabel = '';
  navItems.forEach(function(n) {
    if (n.href.includes(page)) pageLabel = n.label;
  });

  var sideHTML = _sidebarHTML(navItems, user, accent, accentLight, roleLabel);
  var hdrHTML  = _headerHTML(user, pageLabel, accent, accentLight, roleLabel);

  var sideEl   = document.getElementById('sidebar');
  var mobileEl = document.getElementById('mobileSidebar');
  var headerEl = document.getElementById('topHeader');

  if (sideEl)   sideEl.innerHTML   = sideHTML;
  if (mobileEl) mobileEl.innerHTML = sideHTML;
  if (headerEl) headerEl.innerHTML = hdrHTML;

  _injectCSS();
}

function _injectCSS() {
  if (document.getElementById('_lc')) return;
  var s = document.createElement('style');
  s.id = '_lc';
  s.textContent = `
    @media (min-width:1024px) {
      #sidebar          { display:flex !important; }
      .hamburger-btn    { display:none  !important; }
      .logo-mobile      { display:none  !important; }
      .sb-close-btn     { display:none  !important; }
    }
    @media (max-width:1023px) {
      #sidebar          { display:none  !important; }
      .hamburger-btn    { display:flex  !important; align-items:center; }
      .logo-mobile      { display:flex  !important; }
      .user-block       { display:none  !important; }
      .page-label       { display:none  !important; }
    }
    @media (max-width:480px) {
      .logout-txt { display:none !important; }
    }
    main::-webkit-scrollbar { display:none; }
    main { scrollbar-width:none; }
  `;
  document.head.appendChild(s);
}

function openSidebar() {
  var o = document.getElementById('overlay');
  var m = document.getElementById('mobileSidebar');
  if (o) o.style.display = 'block';
  if (m) { m.style.display = 'block'; m.style.position = 'fixed'; m.style.top = '0';
           m.style.left = '0'; m.style.bottom = '0'; m.style.width = '260px';
           m.style.zIndex = '999'; }
}

function closeSidebar() {
  var o = document.getElementById('overlay');
  var m = document.getElementById('mobileSidebar');
  if (o) o.style.display = 'none';
  if (m) m.style.display = 'none';
}

/* doLogout, formatRupiah, showToast, dan requireAuth TIDAK
   didefinisikan di sini lagi — gunakan versi dari api.js
   (file ini sudah dimuat setelah api.js di setiap halaman). */