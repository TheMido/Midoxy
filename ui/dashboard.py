DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Midoxy · Control Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>
<style>
:root {
  --bg: #090507;
  --bg-subtle: #12080d;
  --card: #150a10;
  --card-hover: #1c0e16;
  --border: rgba(255, 42, 75, 0.15);
  --border-focus: rgba(255, 42, 75, 0.4);
  --primary: #ff2a4b;
  --primary-hover: #ff4765;
  --primary-glow: rgba(255, 42, 75, 0.35);
  --primary-gradient: linear-gradient(135deg, #ff2a4b 0%, #b80d28 100%);
  --text: #f5e6eb;
  --text-muted: #9e818c;
  --text-dim: #6e5560;
  --green: #00e676;
  --green-glow: rgba(0, 230, 118, 0.25);
  --yellow: #ffb300;
  --danger: #ff2a4b;
}

* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 0 0 60px;
}

.mono { font-family: 'JetBrains Mono', monospace; font-variant-numeric: tabular-nums; }

/* Top Navigation */
header {
  position: sticky;
  top: 0;
  z-index: 40;
  background: rgba(9, 5, 7, 0.85);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
  padding: 14px 6%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--primary-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 19px;
  box-shadow: 0 0 16px var(--primary-glow);
}

.brand-title {
  font-size: 17px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #fff;
}
.brand-sub {
  font-size: 11px;
  color: var(--text-dim);
}

.nav-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.btn-nav {
  padding: 8px 14px;
  border-radius: 8px;
  background: var(--card);
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
  text-decoration: none;
}
.btn-nav:hover {
  color: #fff;
  border-color: var(--primary);
}

/* Layout Container */
.container {
  max-width: 1160px;
  margin: 30px auto 0;
  padding: 0 20px;
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.metric-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
  position: relative;
  overflow: hidden;
}
.metric-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--primary-gradient);
  opacity: 0.7;
}

.metric-label {
  font-size: 12.5px;
  color: var(--text-muted);
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.metric-val {
  font-size: 26px;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
}

/* Master Subscription Banner */
.sub-banner {
  background: linear-gradient(135deg, rgba(255, 42, 75, 0.12) 0%, rgba(22, 10, 16, 0.8) 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 22px 26px;
  margin-bottom: 26px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 18px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.5);
}

.sub-info h2 {
  font-size: 17px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.sub-info p {
  font-size: 13px;
  color: var(--text-muted);
}

.sub-actions {
  display: flex;
  gap: 10px;
}

.btn-primary {
  padding: 10px 18px;
  border-radius: 9px;
  border: none;
  background: var(--primary-gradient);
  color: #fff;
  font-size: 13.5px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 16px var(--primary-glow);
  transition: all 0.2s;
}
.btn-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}

/* Section Header */
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.section-title {
  font-size: 19px;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
}

/* Create Config Card */
.create-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 22px;
  margin-bottom: 26px;
}

.create-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto;
  gap: 14px;
  align-items: end;
}

.form-group label {
  display: block;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 6px;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--bg-subtle);
  color: #fff;
  font-size: 13.5px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
}
.form-group input:focus {
  border-color: var(--border-focus);
}

/* Config List / Table */
.configs-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.config-item {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 18px 22px;
  display: grid;
  grid-template-columns: 2fr 2fr 1fr auto;
  align-items: center;
  gap: 16px;
  transition: all 0.2s;
}
.config-item:hover {
  background: var(--card-hover);
  border-color: var(--border-focus);
}

.config-main {
  display: flex;
  align-items: center;
  gap: 12px;
}

.config-avatar {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(255, 42, 75, 0.12);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  font-size: 19px;
  flex-shrink: 0;
}

.config-name {
  font-size: 15px;
  font-weight: 700;
  color: #fff;
}
.config-uuid {
  font-size: 11.5px;
  color: var(--text-dim);
}

.traffic-section {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.traffic-text {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  justify-content: space-between;
}
.progress-bar-bg {
  width: 100%;
  height: 6px;
  border-radius: 4px;
  background: var(--bg-subtle);
  overflow: hidden;
}
.progress-bar-fill {
  height: 100%;
  border-radius: 4px;
  background: var(--primary-gradient);
  transition: width 0.3s;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 99px;
  font-size: 11.5px;
  font-weight: 700;
  justify-self: start;
}
.badge-active { background: rgba(0, 230, 118, 0.12); color: var(--green); border: 1px solid rgba(0, 230, 118, 0.25); }
.badge-disabled { background: rgba(255, 255, 255, 0.06); color: var(--text-dim); border: 1px solid rgba(255, 255, 255, 0.1); }
.badge-exceeded { background: rgba(255, 42, 75, 0.12); color: var(--danger); border: 1px solid rgba(255, 42, 75, 0.25); }

.config-actions {
  display: flex;
  gap: 6px;
  justify-content: flex-end;
}

.btn-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 15px;
  transition: all 0.2s;
}
.btn-icon:hover {
  color: #fff;
  border-color: var(--primary);
  background: rgba(255, 42, 75, 0.1);
}
.btn-icon.delete:hover {
  color: var(--danger);
  border-color: var(--danger);
}

/* Modals */
.modal-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(8px);
  z-index: 100;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-card {
  width: 100%;
  max-width: 440px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 28px;
  position: relative;
  box-shadow: 0 20px 50px rgba(0,0,0,0.8);
}

.modal-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.modal-head h3 {
  font-size: 17px;
  font-weight: 800;
  color: #fff;
}
.btn-close {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 18px;
}
.btn-close:hover { color: #fff; }

#qrcode-container {
  display: flex;
  justify-content: center;
  padding: 16px;
  background: #fff;
  border-radius: 12px;
  margin: 16px 0;
}

/* Toast */
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 12px 20px;
  background: var(--card);
  border: 1px solid var(--primary);
  border-radius: 10px;
  color: #fff;
  font-size: 13.5px;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(0,0,0,0.6);
  z-index: 200;
  display: none;
  align-items: center;
  gap: 8px;
  animation: slideIn 0.25s ease;
}
@keyframes slideIn {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

footer {
  margin-top: 50px;
  text-align: center;
  font-size: 12.5px;
  color: var(--text-dim);
}
footer a { color: var(--text-muted); text-decoration: none; }
footer a:hover { color: var(--primary); }

@media (max-width: 840px) {
  .create-grid { grid-template-columns: 1fr; }
  .config-item { grid-template-columns: 1fr; gap: 12px; }
  .config-actions { justify-content: flex-start; }
}
</style>
</head>
<body>

<header>
  <div class="brand-section">
    <div class="brand-icon"><i class="ti ti-brand-abstract"></i></div>
    <div>
      <div class="brand-title">Midoxy Console</div>
      <div class="brand-sub mono" id="host-label">Loading host...</div>
    </div>
  </div>
  <div class="nav-actions">
    <button class="btn-nav" onclick="openPwdModal()"><i class="ti ti-key"></i> Password</button>
    <button class="btn-nav" onclick="logout()"><i class="ti ti-logout"></i> Logout</button>
  </div>
</header>

<div class="container">
  <!-- Metrics -->
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-label">ACTIVE CONNECTIONS <i class="ti ti-activity" style="color:var(--green)"></i></div>
      <div class="metric-val mono" id="stat-conns">0</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">TOTAL DATA TRANSFERRED <i class="ti ti-chart-bar" style="color:var(--primary)"></i></div>
      <div class="metric-val mono" id="stat-traffic">0 B</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">TOTAL REQUESTS <i class="ti ti-arrows-exchange"></i></div>
      <div class="metric-val mono" id="stat-reqs">0</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">SERVER UPTIME <i class="ti ti-clock"></i></div>
      <div class="metric-val mono" id="stat-uptime">0m</div>
    </div>
  </div>

  <!-- Master Subscription Banner -->
  <div class="sub-banner">
    <div class="sub-info">
      <h2><i class="ti ti-rss"></i> Master Subscription Link</h2>
      <p>Import all your active configs into v2rayNG, Sing-box, or Streisand with one single link.</p>
    </div>
    <div class="sub-actions">
      <button class="btn-primary" onclick="copyMasterSub()"><i class="ti ti-copy"></i> Copy Sub URL</button>
      <button class="btn-nav" onclick="showMasterQR()"><i class="ti ti-qrcode"></i> QR</button>
    </div>
  </div>

  <!-- Create Config Section -->
  <div class="create-card">
    <div class="section-title" style="margin-bottom:14px;font-size:16px;">Quick Add Configuration</div>
    <form id="create-form" class="create-grid" onsubmit="createConfig(event)">
      <div class="form-group">
        <label>Config Remark / Label</label>
        <input type="text" id="cfg-label" value="Midoxy" required placeholder="e.g. Midoxy">
      </div>
      <div class="form-group">
        <label>Traffic Quota (GB)</label>
        <input type="number" id="cfg-quota" value="0" min="0" step="1" placeholder="0 = Unlimited">
      </div>
      <div class="form-group">
        <label>Expiration (Days)</label>
        <input type="number" id="cfg-days" value="0" min="0" step="1" placeholder="0 = Never">
      </div>
      <button type="submit" class="btn-primary" style="height:42px;"><i class="ti ti-plus"></i> Create</button>
    </form>
  </div>

  <!-- Configurations List -->
  <div class="section-head">
    <div class="section-title">Active Stream Configs (<span id="cfg-count">0</span>)</div>
    <button class="btn-nav" onclick="fetchData()"><i class="ti ti-refresh"></i> Refresh</button>
  </div>

  <div class="configs-list" id="configs-container">
    <div style="text-align:center;padding:40px;color:var(--text-dim);">Loading configs...</div>
  </div>
</div>

<!-- QR Code Modal -->
<div class="modal-overlay" id="qr-modal" onclick="closeModalOnBg(event, 'qr-modal')">
  <div class="modal-card">
    <div class="modal-head">
      <h3 id="qr-modal-title">Config QR Code</h3>
      <button class="btn-close" onclick="closeModal('qr-modal')"><i class="ti ti-x"></i></button>
    </div>
    <div id="qrcode-container"></div>
    <p class="mono" id="qr-link-text" style="font-size:11px;color:var(--text-dim);word-break:break-all;text-align:center;max-height:80px;overflow-y:auto;"></p>
    <button class="btn-primary" style="width:100%;margin-top:16px;" onclick="copyFromModal()"><i class="ti ti-copy"></i> Copy Link</button>
  </div>
</div>

<!-- Password Change Modal -->
<div class="modal-overlay" id="pwd-modal" onclick="closeModalOnBg(event, 'pwd-modal')">
  <div class="modal-card">
    <div class="modal-head">
      <h3>Change Admin Password</h3>
      <button class="btn-close" onclick="closeModal('pwd-modal')"><i class="ti ti-x"></i></button>
    </div>
    <form onsubmit="changePassword(event)">
      <div class="form-group" style="margin-bottom:14px;">
        <label>Current Password</label>
        <input type="password" id="old-pwd" required placeholder="Enter current password">
      </div>
      <div class="form-group" style="margin-bottom:18px;">
        <label>New Password</label>
        <input type="password" id="new-pwd" required placeholder="Enter new password (min 6 chars)">
      </div>
      <button type="submit" class="btn-primary" style="width:100%;"><i class="ti ti-check"></i> Update Password</button>
    </form>
  </div>
</div>

<!-- Toast -->
<div class="toast" id="toast">
  <i class="ti ti-check" style="color:var(--green)"></i>
  <span id="toast-msg">Copied!</span>
</div>

<footer>
  <div>Midoxy Stream Core · Powered by <a href="https://t.me/OFFL1NE" target="_blank">@OFFL1NE</a></div>
</footer>

<script>
let currentHost = window.location.host;
let currentConfigs = [];
let modalCopyText = '';

function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showToast(msg) {
  const toast = document.getElementById('toast');
  document.getElementById('toast-msg').textContent = msg;
  toast.style.display = 'flex';
  setTimeout(() => { toast.style.display = 'none'; }, 2500);
}

function copyToClipboard(text, msg = 'Copied to clipboard!') {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => showToast(msg));
  } else {
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast(msg);
  }
}

async function fetchData() {
  try {
    const res = await fetch('/api/stats');
    if (res.status === 401) {
      window.location.href = '/login';
      return;
    }
    const data = await res.json();
    currentHost = data.host || window.location.host;
    document.getElementById('host-label').textContent = currentHost;
    document.getElementById('stat-conns').textContent = data.active_connections;
    document.getElementById('stat-traffic').textContent = formatBytes(data.total_bytes);
    document.getElementById('stat-reqs').textContent = data.total_requests;
    document.getElementById('stat-uptime').textContent = data.uptime;

    const linksRes = await fetch('/api/links');
    currentConfigs = await linksRes.json();
    renderConfigs(currentConfigs);
  } catch (err) {
    console.error('Fetch error:', err);
  }
}

function renderConfigs(configs) {
  const container = document.getElementById('configs-container');
  document.getElementById('cfg-count').textContent = configs.length;

  if (configs.length === 0) {
    container.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-dim);">No configs created yet. Use the form above to add one.</div>';
    return;
  }

  container.innerHTML = configs.map(c => {
    const used = c.used_bytes || 0;
    const limit = c.limit_bytes || 0;
    let pct = 0;
    let quotaText = `${formatBytes(used)} / Unlimited`;

    if (limit > 0) {
      pct = Math.min(100, Math.round((used / limit) * 100));
      quotaText = `${formatBytes(used)} / ${formatBytes(limit)} (${pct}%)`;
    }

    let statusHtml = '<span class="status-badge badge-active"><i class="ti ti-point-filled"></i> Active</span>';
    if (!c.active) {
      statusHtml = '<span class="status-badge badge-disabled">Disabled</span>';
    } else if (limit > 0 && used >= limit) {
      statusHtml = '<span class="status-badge badge-exceeded">Quota Exceeded</span>';
    }

    return `
      <div class="config-item">
        <div class="config-main">
          <div class="config-avatar"><i class="ti ti-shield-bolt"></i></div>
          <div>
            <div class="config-name">${c.label || 'Midoxy'}</div>
            <div class="config-uuid mono">${c.uuid.substring(0, 18)}...</div>
          </div>
        </div>

        <div class="traffic-section">
          <div class="traffic-text mono">
            <span>${quotaText}</span>
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: ${pct}%;"></div>
          </div>
        </div>

        <div>${statusHtml}</div>

        <div class="config-actions">
          <button class="btn-icon" title="Copy VLESS Link" onclick="copyVless('${c.uuid}', '${c.label}')"><i class="ti ti-clipboard-copy"></i></button>
          <button class="btn-icon" title="Show QR Code" onclick="showConfigQR('${c.uuid}', '${c.label}')"><i class="ti ti-qrcode"></i></button>
          <button class="btn-icon" title="Copy Single Subscription" onclick="copySingleSub('${c.uuid}')"><i class="ti ti-rss"></i></button>
          <button class="btn-icon" title="${c.active ? 'Disable' : 'Enable'}" onclick="toggleConfig('${c.uuid}', ${!c.active})">
            <i class="ti ti-${c.active ? 'player-pause' : 'player-play'}"></i>
          </button>
          <button class="btn-icon delete" title="Delete" onclick="deleteConfig('${c.uuid}')"><i class="ti ti-trash"></i></button>
        </div>
      </div>
    `;
  }).join('');
}

async function createConfig(e) {
  e.preventDefault();
  const label = document.getElementById('cfg-label').value.trim() || 'Midoxy';
  const quotaGb = parseFloat(document.getElementById('cfg-quota').value) || 0;
  const days = parseInt(document.getElementById('cfg-days').value) || 0;

  try {
    const res = await fetch('/api/links', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ label, limit_gb: quotaGb, expires_days: days })
    });
    if (res.ok) {
      showToast('Config created successfully!');
      fetchData();
    }
  } catch (err) {
    showToast('Failed to create config');
  }
}

async function toggleConfig(uuid, active) {
  try {
    await fetch(`/api/links/${uuid}/toggle`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ active })
    });
    fetchData();
  } catch (err) {
    console.error(err);
  }
}

async function deleteConfig(uuid) {
  if (!confirm('Are you sure you want to delete this config?')) return;
  try {
    await fetch(`/api/links/${uuid}`, { method: 'DELETE' });
    showToast('Config deleted');
    fetchData();
  } catch (err) {
    console.error(err);
  }
}

function getVlessUrl(uuid, label) {
  const remark = encodeURIComponent(label || 'Midoxy');
  const path = encodeURIComponent(`/stream/${uuid}`);
  return `vless://${uuid}@${currentHost}:443?encryption=none&security=tls&type=ws&host=${currentHost}&path=${path}&sni=${currentHost}&fp=chrome&alpn=h2#${remark}`;
}

function copyVless(uuid, label) {
  const url = getVlessUrl(uuid, label);
  copyToClipboard(url, 'VLESS link copied!');
}

function copySingleSub(uuid) {
  const subUrl = `${window.location.protocol}//${currentHost}/feed/${uuid}`;
  copyToClipboard(subUrl, 'Subscription link copied!');
}

function copyMasterSub() {
  const subUrl = `${window.location.protocol}//${currentHost}/manifest`;
  copyToClipboard(subUrl, 'Master subscription copied!');
}

function showConfigQR(uuid, label) {
  const url = getVlessUrl(uuid, label);
  modalCopyText = url;
  document.getElementById('qr-modal-title').textContent = `QR: ${label || 'Midoxy'}`;
  document.getElementById('qr-link-text').textContent = url;
  renderQR(url);
  document.getElementById('qr-modal').style.display = 'flex';
}

function showMasterQR() {
  const subUrl = `${window.location.protocol}//${currentHost}/manifest`;
  modalCopyText = subUrl;
  document.getElementById('qr-modal-title').textContent = 'Master Subscription QR';
  document.getElementById('qr-link-text').textContent = subUrl;
  renderQR(subUrl);
  document.getElementById('qr-modal').style.display = 'flex';
}

function renderQR(text) {
  const qrBox = document.getElementById('qrcode-container');
  qrBox.innerHTML = '';
  new QRCode(qrBox, {
    text: text,
    width: 220,
    height: 220,
    colorDark: "#090507",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.M
  });
}

function copyFromModal() {
  if (modalCopyText) copyToClipboard(modalCopyText);
}

function openPwdModal() { document.getElementById('pwd-modal').style.display = 'flex'; }
function closeModal(id) { document.getElementById(id).style.display = 'none'; }
function closeModalOnBg(e, id) { if (e.target.id === id) closeModal(id); }

async function changePassword(e) {
  e.preventDefault();
  const oldPwd = document.getElementById('old-pwd').value;
  const newPwd = document.getElementById('new-pwd').value;

  try {
    const res = await fetch('/api/change-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ old_password: oldPwd, new_password: newPwd })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      showToast('Password updated!');
      closeModal('pwd-modal');
    } else {
      alert(data.message || 'Failed to update password');
    }
  } catch (err) {
    alert('Error connecting to server');
  }
}

async function logout() {
  await fetch('/api/logout', { method: 'POST' });
  window.location.href = '/login';
}

// Initial fetch & auto-refresh every 8s
fetchData();
setInterval(fetchData, 8000);
</script>

</body>
</html>
"""

