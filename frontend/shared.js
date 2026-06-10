// shared.js — Medicare+ utilities
const API = 'http://localhost:5000/api';
const getToken = () => localStorage.getItem('token');
const getUser  = () => JSON.parse(localStorage.getItem('user') || 'null');

function logout() { localStorage.clear(); window.location.href = 'index.html'; }
function requireAuth() { if (!getToken()) { window.location.href = 'login.html'; return false; } return true; }

async function apiFetch(path, opts = {}) {
  const headers = { 'Content-Type': 'application/json', Authorization: `Bearer ${getToken()}`, ...opts.headers };
  const res = await fetch(`${API}${path}`, { ...opts, headers });
  if (res.status === 401) { logout(); return; }
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Request failed');
  return data;
}
async function apiUpload(path, formData) {
  const res = await fetch(`${API}${path}`, { method: 'POST', headers: { Authorization: `Bearer ${getToken()}` }, body: formData });
  if (res.status === 401) { logout(); return; }
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Upload failed');
  return data;
}

let _toastTimer;
function showToast(msg, type = 'success') {
  document.getElementById('toast')?.remove();
  clearTimeout(_toastTimer);
  const t = document.createElement('div');
  t.id = 'toast'; t.className = `toast toast-${type}`;
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  t.innerHTML = `<span>${icons[type]||'✓'}</span><span>${msg}</span>`;
  document.body.appendChild(t);
  _toastTimer = setTimeout(() => t.remove(), 3500);
}

function openModal(id)  { document.getElementById(id).style.display = 'flex'; }
function closeModal(id) { document.getElementById(id).style.display = 'none'; }
window.addEventListener('click', e => { if (e.target.classList.contains('modal-overlay')) e.target.style.display = 'none'; });

function buildSidebar(active) {
  const user = getUser();
  if (!user) return;
  const items = [
    { id:'dashboard',     label:'Dashboard',       icon:'⊞',  href:'dashboard.html',     roles:['patient','doctor'] },
    { id:'appointments',  label:'Appointments',     icon:'📅', href:'appointments.html',  roles:['patient','doctor'] },
    { id:'doctors',       label:'Find Doctors',     icon:'🔍', href:'doctors.html',       roles:['patient'] },
    { id:'prescriptions', label:'Prescriptions',    icon:'💊', href:'prescriptions.html', roles:['patient','doctor'] },
    { id:'symptoms',      label:'Symptom Checker',  icon:'🤖', href:'symptoms.html',      roles:['patient'] },
    { id:'chat',          label:'Messages',         icon:'💬', href:'chat.html',          roles:['patient','doctor'] },
    { id:'reports',       label:'Reports',          icon:'📄', href:'reports.html',       roles:['patient'] },
    { id:'reminders',     label:'Reminders',        icon:'⏰', href:'reminders.html',     roles:['patient'] },
    { id:'emergency',     label:'Emergency',        icon:'🚨', href:'emergency.html',     roles:['patient','doctor'] },
  ].filter(n => n.roles.includes(user.role));

  document.getElementById('sidebar').innerHTML = `
    <div class="sb-logo">
      <a href="index.html" style="display:flex;align-items:center;gap:10px;text-decoration:none">
        <div class="sb-logo-icon">
          <svg viewBox="0 0 28 28" fill="none" width="20" height="20"><path d="M16 5H12V12H5V16H12V23H16V16H23V12H16V5Z" fill="white"/></svg>
        </div>
        <div>
          <div class="sb-brand">Medicare<strong>+</strong></div>
        </div>
      </a>
    </div>
    <nav class="sb-nav">
      ${items.map(i => `<a href="${i.href}" class="sb-item ${active===i.id?'active':''}"><span class="si">${i.icon}</span>${i.label}</a>`).join('')}
    </nav>
    <div class="sb-foot">
      <div class="sb-user">
        <div class="sb-av">${(user.name||'U')[0].toUpperCase()}</div>
        <div><div class="sb-uname">${user.name||''}</div><div class="sb-urole">${user.role||''}</div></div>
      </div>
      <button class="btn-logout" onclick="logout()">Sign out</button>
    </div>`;
}

function fmtDate(s) { if (!s) return '—'; return new Date(s).toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'}); }
function fmtTime(t) { if (!t) return ''; const [h,m]=t.split(':'); const hr=+h; return `${hr>12?hr-12:hr||12}:${m} ${hr>=12?'PM':'AM'}`; }
function statusBadge(s) {
  const m={pending:'badge-amber',confirmed:'badge-teal',completed:'badge-blue',cancelled:'badge-red'};
  return `<span class="badge ${m[s]||'badge-gray'}">${s}</span>`;
}
function renderStars(r, size=14) {
  return `<span style="color:#f59e0b;font-size:${size}px">${'★'.repeat(Math.round(r))}${'☆'.repeat(5-Math.round(r))}</span>`;
}
function escHtml(s) { const d=document.createElement('div'); d.textContent=s; return d.innerHTML; }
