PUBLIC_PAGE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Midoxy · Configuration View</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>
<style>
:root {
  --bg: #090507;
  --card: #150a10;
  --border: rgba(255, 42, 75, 0.15);
  --primary: #ff2a4b;
  --primary-glow: rgba(255, 42, 75, 0.35);
  --primary-gradient: linear-gradient(135deg, #ff2a4b 0%, #b80d28 100%);
  --text: #f5e6eb;
  --text-muted: #9e818c;
  --text-dim: #6e5560;
  --green: #00e676;
}

* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: var(--bg);
  color: var(--text);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.mono { font-family: 'JetBrains Mono', monospace; }

.card {
  width: 100%;
  max-width: 440px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 32px 28px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.8);
  text-align: center;
}

.brand-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--primary-gradient);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #fff;
  margin-bottom: 12px;
  box-shadow: 0 0 20px var(--primary-glow);
}

.title { font-size: 19px; font-weight: 800; color: #fff; margin-bottom: 4px; }
.sub { font-size: 12.5px; color: var(--text-muted); margin-bottom: 22px; }

#qrcode-box {
  background: #fff;
  padding: 14px;
  border-radius: 12px;
  display: inline-block;
  margin-bottom: 22px;
}

.stats-box {
  background: rgba(9, 5, 7, 0.7);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 20px;
  text-align: left;
  font-size: 13px;
}
.stat-row { display: flex; justify-content: space-between; margin-bottom: 6px; }
.stat-row:last-child { margin-bottom: 0; }
.stat-label { color: var(--text-dim); }
.stat-val { color: #fff; font-weight: 600; }

.btn {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  border: none;
  background: var(--primary-gradient);
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 16px var(--primary-glow);
  transition: all 0.2s;
}
.btn:hover { filter: brightness(1.1); transform: translateY(-1px); }

.foot {
  margin-top: 22px;
  font-size: 12px;
  color: var(--text-dim);
}
.foot a { color: var(--text-muted); text-decoration: none; }
.foot a:hover { color: var(--primary); }
</style>
</head>
<body>

<div class="card">
  <div class="brand-icon"><i class="ti ti-brand-abstract"></i></div>
  <div class="title">{{label}}</div>
  <div class="sub">Midoxy Stream Configuration</div>

  <div id="qrcode-box"></div>

  <div class="stats-box mono">
    <div class="stat-row">
      <span class="stat-label">STATUS</span>
      <span class="stat-val" style="color:var(--green)">● {{status}}</span>
    </div>
    <div class="stat-row">
      <span class="stat-label">USAGE</span>
      <span class="stat-val">{{used}} / {{limit}}</span>
    </div>
    <div class="stat-row">
      <span class="stat-label">EXPIRES</span>
      <span class="stat-val">{{expires}}</span>
    </div>
  </div>

  <button class="btn" onclick="copyConfig()">
    <i class="ti ti-clipboard-copy"></i>
    <span>Copy VLESS Link</span>
  </button>

  <div class="foot">
    Powered by <a href="https://t.me/OFFL1NE" target="_blank">@OFFL1NE</a>
  </div>
</div>

<script>
const vlessUrl = "{{vless_url}}";

new QRCode(document.getElementById('qrcode-box'), {
  text: vlessUrl,
  width: 190,
  height: 190,
  colorDark: "#090507",
  colorLight: "#ffffff",
  correctLevel: QRCode.CorrectLevel.M
});

function copyConfig() {
  navigator.clipboard.writeText(vlessUrl).then(() => {
    alert('VLESS link copied to clipboard!');
  });
}
</script>

</body>
</html>
"""

