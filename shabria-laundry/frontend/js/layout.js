const BASE_URL = 'http://localhost:5000/api';

const ADMIN_NAV = [
  { href: 'dashboard.html',   icon: '📊', label: 'Dashboard' },
  { href: 'customers.html',   icon: '👥', label: 'Customer' },
  { href: 'transaksi.html',   icon: '🧾', label: 'Transaksi' },
  { href: 'laporan.html',     icon: '📈', label: 'Laporan' },
  { href: 'layanan.html',     icon: '⚙️',  label: 'Kelola Layanan' },
];

const MANAGER_NAV = [
  { href: 'dashboard.html',   icon: '📊', label: 'Dashboard' },
  { href: 'monitor.html',     icon: '📋', label: 'Monitor Transaksi' },
  { href: 'laporan.html',     icon: '📈', label: 'Laporan' },
  { href: 'akun-admin.html',  icon: '👤', label: 'Akun Admin' },
];

function _buildSidebar(navItems, user, accent, accentLight, role) {
  const currentPage = window.location.pathname.split('/').pop();
  return `
    <aside style="
      width:240px; height:100%; background:white;
      border-right:1px solid #E5E7EB;
      display:flex; flex-direction:column;
      box-shadow:2px 0 12px rgba(0,0,0,0.06);
    ">
      <!-- Logo + brand -->
      <div style="padding:20px 16px 16px; border-bottom:1px solid #F3F4F6; display:flex; align-items:center; gap:10px;">
        <img src="../assets/logo.jpg" alt="Shabria"
          style="width:40px;height:40px;border-radius:10px;border:1px solid #E5E7EB;padding:4px;object-fit:contain;"
          onerror="this.style.display='none'">
        <div style="flex:1;">
          <p style="font-size:13px;font-weight:800;color:#111827;margin:0;">Shabria Laundry</p>
          <p style="font-size:10px;font-weight:600;color:${accent};margin:0;">
            ${role === 'manager' ? 'Panel Manager (Owner)' : 'Panel Admin (Kasir)'}
          </p>
        </div>
        <button onclick="closeSidebar()" class="sb-close"
          style="background:none;border:none;cursor:pointer;font-size:18px;line-height:1;color:#9CA3AF;">✕</button>
      </div>

      <!-- User badge -->
      <div style="margin:12px 10px 4px;padding:10px 14px;border-radius:12px;background:${accentLight};">
        <p style="font-size:12px;font-weight:700;color:${accent};margin:0;">${user.nama || ''}</p>
        <p style="font-size:10px;color:#9CA3AF;margin:0;">${user.email || ''}</p>
      </div>

      <!-- Nav items -->
      <nav style="padding:8px 10px;flex:1;">
        ${navItems.map(n => {
          const isActive = currentPage === n.href || (currentPage === '' && n.href === 'dashboard.html');
          return `
            <a href="${n.href}" style="
              display:flex;align-items:center;gap:12px;
              padding:11px 14px;border-radius:12px;
              text-decoration:none;font-size:14px;
              font-weight:${isActive ? 700 : 500};
              color:${isActive ? accent : '#6B7280'};
              background:${isActive ? accentLight : 'transparent'};
              margin-bottom:2px;
              transition:all 0.15s;
            ">
              <span style="font-size:18px;">${n.icon}</span>
              <span style="flex:1;">${n.label}</span>
              ${isActive ? `<span style="color:${accent};">›</span>` : ''}
            </a>`;
        }).join('')}
      </nav>

      <!-- Logout -->
      <div style="padding:12px 10px;border-top:1px solid #F3F4F6;">
        <button onclick="doLogout()" style="
          display:flex;align-items:center;gap:10px;width:100%;
          padding:10px 14px;border-radius:12px;border:none;cursor:pointer;
          background:#FEF2F2;color:#DC2626;font-size:13px;font-weight:700;
        ">🚪 Keluar</button>
      </div>
    </aside>`;
}

function _buildHeader(user, currentLabel, role) {
  const accent = role === 'manager' ? '#15803D' : '#1565C0';
  const accentLight = role === 'manager' ? '#F0FDF4' : '#EFF6FF';
  return `
    <header style="
      height:62px;display:flex;align-items:center;gap:14px;
      padding:0 24px;background:white;
      border-bottom:1px solid #E5E7EB;
      box-shadow:0 1px 6px rgba(0,0,0,0.05);
      flex-shrink:0;
    ">
      <button onclick="openSidebar()" class="hamburger"
        style="background:none;border:none;cursor:pointer;font-size:22px;line-height:1;">☰</button>
      <div class="mobile-logo" style="display:flex;align-items:center;gap:8px;">
        <img src="../assets/logo.jpg" alt="Shabria"
          style="width:30px;height:30px;border-radius:8px;border:1px solid #E5E7EB;padding:3px;object-fit:contain;"
          onerror="this.style.display='none'">
        <p style="font-size:13px;font-weight:800;color:#111827;margin:0;">Shabria Laundry</p>
      </div>
      <div style="flex:1;"></div>
      <span class="page-label" style="font-size:13px;color:#9CA3AF;">${currentLabel}</span>
      <div style="display:flex;align-items:center;gap:10px;">
        <div class="header-user" style="text-align:right;">
          <p style="font-size:13px;font-weight:700;color:#111827;margin:0;">${user.nama || ''}</p>
          <p style="font-size:10px;color:#9CA3AF;margin:0;">
            ${role === 'manager' ? 'Manager / Owner' : 'Admin / Kasir'}
          </p>
        </div>
        <button onclick="doLogout()" style="
          display:flex;align-items:center;gap:6px;
          padding:7px 12px;border-radius:10px;
          background:#FEF2F2;border:none;cursor:pointer;
          color:#DC2626;font-size:12px;font-weight:600;
        ">🚪 <span class="logout-text">Keluar</span></button>
      </div>
    </header>`;
}

function initAdminLayout(user, page) {
  _init(user, page, ADMIN_NAV, '#1565C0', '#EFF6FF', 'admin');
}

function initManagerLayout(user, page) {
  _init(user, page, MANAGER_NAV, '#15803D', '#F0FDF4', 'manager');
}

function _init(user, page, navItems, accent, accentLight, role) {
  const label = navItems.find(n => n.href.includes(page))?.label || '';

  const sideEl   = document.getElementById('sidebar');
  const mobileEl = document.getElementById('mobileSidebar');
  const headerEl = document.getElementById('topHeader');
  const html     = _buildSidebar(navItems, user, accent, accentLight, role);

  if (sideEl)   sideEl.innerHTML   = html;
  if (mobileEl) mobileEl.innerHTML = html;
  if (headerEl) headerEl.innerHTML = _buildHeader(user, label, role);

  // Inject responsive CSS once
  if (!document.getElementById('layout-css')) {
    const s = document.createElement('style');
    s.id = 'layout-css';
    s.textContent = `
      @media (min-width:1024px) {
        .desktop-sidebar { display:flex !important; }
        .hamburger        { display:none  !important; }
        .sb-close         { display:none  !important; }
        .mobile-logo      { display:none  !important; }
      }
      @media (max-width:1023px) {
        .desktop-sidebar { display:none  !important; }
        .header-user     { display:none  !important; }
        .page-label      { display:none  !important; }
      }
      @media (max-width:480px) {
        .logout-text { display:none !important; }
      }
      main::-webkit-scrollbar { display:none; }
      main { scrollbar-width:none; }
      a:hover { opacity:0.85; }
    `;
    document.head.appendChild(s);
  }
}

function openSidebar() {
  document.getElementById('overlay').style.display      = 'block';
  document.getElementById('mobileSidebar').style.display = 'block';
}
function closeSidebar() {
  document.getElementById('overlay').style.display      = 'none';
  document.getElementById('mobileSidebar').style.display = 'none';
}

async function doLogout() {
  try { await _req('POST', '/auth/logout'); } catch {}
  sessionStorage.removeItem('currentUser');
  window.location.href = '../index.html';
}

function formatRupiah(n) {
  return new Intl.NumberFormat('id-ID',{style:'currency',currency:'IDR',minimumFractionDigits:0}).format(n||0);
}

function showToast(msg, type) {
  let c = document.getElementById('toast-container');
  if (!c) { c = document.createElement('div'); c.id='toast-container'; document.body.appendChild(c); }
  const el = document.createElement('div');
  el.className = 'toast ' + (type||'');
  el.textContent = msg;
  c.appendChild(el);
  setTimeout(()=>el.remove(), 3000);
}

async function requireAuth(roles) {
  try {
    const user = await _req('GET', '/auth/me');
    if (roles && roles.length && !roles.includes(user.role))
      window.location.href = '../index.html';
    return user;
  } catch { window.location.href = '../index.html'; }
}