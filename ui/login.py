LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Midoxy · Admin Console</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
:root {
  --bg: #090507;
  --card: #150a10;
  --border: rgba(255, 42, 75, 0.15);
  --border-focus: rgba(255, 42, 75, 0.4);
  --primary: #ff2a4b;
  --primary-hover: #ff4765;
  --primary-glow: rgba(255, 42, 75, 0.35);
  --primary-gradient: linear-gradient(135deg, #ff2a4b 0%, #b80d28 100%);
  --text: #f5e6eb;
  --text-muted: #9e818c;
  --text-dim: #6e5560;
  --danger: #ff334b;
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
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.mono { font-family: 'JetBrains Mono', monospace; }

/* Subtle background aura */
.aura {
  position: fixed;
  border-radius: 50%;
  filter: blur(100px);
  pointer-events: none;
  z-index: 0;
}
.aura-1 { width: 420px; height: 420px; top: -120px; right: -100px; background: rgba(255, 42, 75, 0.16); }
.aura-2 { width: 380px; height: 380px; bottom: -100px; left: -80px; background: rgba(184, 13, 40, 0.14); }

.card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 38px 32px 32px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.8), 0 0 30px rgba(255, 42, 75, 0.08);
}

.brand-header {
  text-align: center;
  margin-bottom: 28px;
}

.brand-icon {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  background: var(--primary-gradient);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #fff;
  margin-bottom: 14px;
  box-shadow: 0 8px 24px var(--primary-glow);
}

.brand-header h1 {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #fff;
  margin-bottom: 4px;
}

.brand-header p {
  font-size: 13px;
  color: var(--text-muted);
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 8px;
}

.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrap input {
  width: 100%;
  padding: 13px 44px 13px 14px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: rgba(9, 5, 7, 0.7);
  color: #fff;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  transition: all 0.2s;
}

.input-wrap input:focus {
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(255, 42, 75, 0.15);
}

.toggle-pwd {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 17px;
  padding: 4px;
  display: flex;
  align-items: center;
}
.toggle-pwd:hover { color: #fff; }

.btn-submit {
  width: 100%;
  padding: 13px;
  border-radius: 10px;
  border: none;
  background: var(--primary-gradient);
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  box-shadow: 0 8px 20px var(--primary-glow);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.22s;
}

.btn-submit:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
  box-shadow: 0 10px 26px rgba(255, 42, 75, 0.5);
}

.btn-submit:active {
  transform: translateY(0);
}

.error-alert {
  display: none;
  padding: 11px 14px;
  border-radius: 8px;
  background: rgba(255, 51, 75, 0.12);
  border: 1px solid rgba(255, 51, 75, 0.25);
  color: var(--danger);
  font-size: 13px;
  margin-bottom: 18px;
  text-align: center;
}

.card-foot {
  margin-top: 26px;
  padding-top: 18px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: var(--text-dim);
}

.card-foot a {
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.2s;
}
.card-foot a:hover { color: var(--primary); }
</style>
</head>
<body>

<div class="aura aura-1"></div>
<div class="aura aura-2"></div>

<div class="card">
  <div class="brand-header">
    <div class="brand-icon"><i class="ti ti-brand-abstract"></i></div>
    <h1>Midoxy Console</h1>
    <p>Sign in to manage your private stream gateway</p>
  </div>

  <div id="error-box" class="error-alert"></div>

  <form id="login-form">
    <div class="form-group">
      <label class="form-label" for="password">Admin Password</label>
      <div class="input-wrap">
        <input type="password" id="password" required autocomplete="current-password" placeholder="Enter password...">
        <button type="button" class="toggle-pwd" id="toggle-btn" aria-label="Toggle password visibility">
          <i class="ti ti-eye" id="eye-icon"></i>
        </button>
      </div>
    </div>

    <button type="submit" class="btn-submit" id="submit-btn">
      <i class="ti ti-login-2"></i>
      <span>Sign In</span>
    </button>
  </form>

  <div class="card-foot">
    <a href="/">← Return to Site</a>
    <a href="https://t.me/OFFL1NE" target="_blank"><i class="ti ti-brand-telegram"></i> @OFFL1NE</a>
  </div>
</div>

<script>
const pwdInput = document.getElementById('password');
const toggleBtn = document.getElementById('toggle-btn');
const eyeIcon = document.getElementById('eye-icon');
const errorBox = document.getElementById('error-box');
const form = document.getElementById('login-form');
const submitBtn = document.getElementById('submit-btn');

toggleBtn.addEventListener('click', () => {
  const isPwd = pwdInput.type === 'password';
  pwdInput.type = isPwd ? 'text' : 'password';
  eyeIcon.className = 'ti ' + (isPwd ? 'ti-eye-off' : 'ti-eye');
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  errorBox.style.display = 'none';
  submitBtn.disabled = true;
  submitBtn.style.opacity = '0.7';

  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: pwdInput.value })
    });
    const data = await res.json();
    if (res.ok && data.success) {
      window.location.href = '/dashboard';
    } else {
      errorBox.textContent = data.message || 'Invalid password';
      errorBox.style.display = 'block';
    }
  } catch (err) {
    errorBox.textContent = 'Connection error. Please try again.';
    errorBox.style.display = 'block';
  } finally {
    submitBtn.disabled = false;
    submitBtn.style.opacity = '1';
  }
});
</script>

</body>
</html>
"""

