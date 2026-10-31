PORTFOLIO_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Midoxy · Systems & Cloud Architecture</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
:root {
  --bg: #090507;
  --bg-subtle: #12080d;
  --card: #160a10;
  --card-hover: #1f0f18;
  --border: rgba(255, 42, 75, 0.12);
  --border-focus: rgba(255, 42, 75, 0.35);
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
  line-height: 1.6;
  overflow-x: hidden;
  position: relative;
  min-height: 100vh;
}

.mono { font-family: 'JetBrains Mono', monospace; }

/* Background Glowing Orbs */
.orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
  z-index: 0;
  opacity: 0.45;
}
.orb-1 { width: 550px; height: 550px; top: -150px; right: -100px; background: rgba(255, 42, 75, 0.18); }
.orb-2 { width: 450px; height: 450px; bottom: -100px; left: -100px; background: rgba(184, 13, 40, 0.15); }

/* Navigation */
nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 8%;
  background: rgba(9, 5, 7, 0.75);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 19px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #fff;
  text-decoration: none;
}

.brand-icon {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: var(--primary-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 20px var(--primary-glow);
}

.nav-links {
  display: flex;
  gap: 28px;
  align-items: center;
}

.nav-link {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s;
}
.nav-link:hover { color: #fff; }

.btn-contact {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 18px;
  border-radius: 8px;
  background: var(--card);
  border: 1px solid var(--border);
  color: #fff;
  font-size: 13.5px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.25s;
}
.btn-contact:hover {
  border-color: var(--primary);
  box-shadow: 0 0 16px var(--primary-glow);
  transform: translateY(-1px);
}

/* Container */
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 130px 24px 80px;
  position: relative;
  z-index: 1;
}

/* Hero Section */
.hero {
  text-align: center;
  padding: 50px 0 70px;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 99px;
  background: rgba(255, 42, 75, 0.08);
  border: 1px solid var(--border);
  font-size: 12.5px;
  color: var(--primary);
  font-weight: 600;
  margin-bottom: 24px;
}
.pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 10px var(--green);
}

.hero h1 {
  font-size: clamp(34px, 5.5vw, 60px);
  font-weight: 800;
  letter-spacing: -0.035em;
  line-height: 1.15;
  margin-bottom: 20px;
  background: linear-gradient(180deg, #ffffff 40%, #c49ba9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero p {
  max-width: 620px;
  margin: 0 auto 34px;
  font-size: 16.5px;
  color: var(--text-muted);
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  border-radius: 10px;
  background: var(--primary-gradient);
  color: #fff;
  font-size: 14.5px;
  font-weight: 700;
  text-decoration: none;
  box-shadow: 0 8px 24px var(--primary-glow);
  transition: all 0.25s;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(255, 42, 75, 0.5);
}

/* Status Terminal */
.terminal-card {
  margin: 20px auto 60px;
  max-width: 760px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0,0,0,0.6);
}
.terminal-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  background: var(--bg-subtle);
  border-bottom: 1px solid var(--border);
  font-size: 12px;
  color: var(--text-dim);
}
.term-dots { display: flex; gap: 7px; }
.term-dot { width: 10px; height: 10px; border-radius: 50%; opacity: 0.7; }
.dot-red { background: #ff5f56; }
.dot-yellow { background: #ffbd2e; }
.dot-green { background: #27c93f; }
.terminal-body {
  padding: 22px 24px;
  font-size: 13.5px;
  color: #d6bac3;
  line-height: 1.9;
}
.term-line { display: flex; gap: 12px; }
.term-prompt { color: var(--primary); font-weight: 600; }

/* Grid Sections */
.section-title {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin-bottom: 26px;
  color: #fff;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
  gap: 20px;
  margin-bottom: 60px;
}

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 26px;
  transition: all 0.25s ease;
}
.card:hover {
  background: var(--card-hover);
  border-color: var(--border-focus);
  transform: translateY(-3px);
  box-shadow: 0 14px 34px rgba(0,0,0,0.4);
}

.card-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(255, 42, 75, 0.1);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: var(--primary);
  margin-bottom: 16px;
}

.card h3 {
  font-size: 17px;
  font-weight: 700;
  margin-bottom: 10px;
  color: #fff;
}
.card p {
  font-size: 13.5px;
  color: var(--text-muted);
  line-height: 1.6;
}

/* Footer */
footer {
  margin-top: 80px;
  border-top: 1px solid var(--border);
  padding: 30px 8%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: var(--text-dim);
}
.console-link {
  color: var(--text-dim);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  transition: color 0.2s;
}
.console-link:hover { color: var(--primary); }

@media (max-width: 640px) {
  nav { padding: 14px 5%; }
  .nav-links { display: none; }
  footer { flex-direction: column; gap: 14px; text-align: center; }
}
</style>
</head>
<body>

<div class="orb orb-1"></div>
<div class="orb orb-2"></div>

<nav>
  <a href="/" class="nav-brand">
    <div class="brand-icon"><i class="ti ti-brand-abstract"></i></div>
    Midoxy
  </a>
  <div class="nav-links">
    <a href="#architecture" class="nav-link">Architecture</a>
    <a href="#services" class="nav-link">Infrastructure</a>
    <a href="https://t.me/OFFL1NE" target="_blank" class="btn-contact">
      <i class="ti ti-brand-telegram"></i> @OFFL1NE
    </a>
  </div>
</nav>

<div class="container">
  <div class="hero">
    <div class="badge">
      <span class="pulse-dot"></span>
      <span>CLUSTER STATUS: HEALTHY & ACTIVE</span>
    </div>
    <h1>High-Performance Cloud &<br>Distributed Streaming Core</h1>
    <p>Designing zero-copy network pipelines, low-latency asynchronous socket relays, and resilient event streaming microservices.</p>
    <div class="hero-actions">
      <a href="https://t.me/OFFL1NE" target="_blank" class="btn-primary">
        <i class="ti ti-brand-telegram"></i> Connect on Telegram
      </a>
    </div>
  </div>

  <div class="terminal-card mono">
    <div class="terminal-head">
      <div class="term-dots">
        <span class="term-dot dot-red"></span>
        <span class="term-dot dot-yellow"></span>
        <span class="term-dot dot-green"></span>
      </div>
      <span>midoxy@runtime-node-01 ~ telemetry</span>
    </div>
    <div class="terminal-body">
      <div class="term-line">
        <span class="term-prompt">$</span>
        <span>midoxy-core status --verbose</span>
      </div>
      <div>[✓] Asynchronous event loop active (uvloop)</div>
      <div>[✓] Socket tuning: TCP_NODELAY enabled, SO_SNDBUF 512KB</div>
      <div>[✓] EWMA adaptive bandwidth throttle: Optimal</div>
      <div>[✓] Edge TLS terminations: Verified (Chrome FP / h2)</div>
      <div>[i] Active node instances: Distributed cluster online</div>
    </div>
  </div>

  <div id="architecture">
    <h2 class="section-title">Core Engineering Modules</h2>
    <div class="grid">
      <div class="card">
        <div class="card-icon"><i class="ti ti-arrows-transfer-down"></i></div>
        <h3>Adaptive Flow Engine</h3>
        <p>Exponentially weighted moving average (EWMA) quota evaluation to minimize lock contention during heavy traffic bursts.</p>
      </div>
      <div class="card">
        <div class="card-icon"><i class="ti ti-server-bolt"></i></div>
        <h3>High-Throughput IO Core</h3>
        <p>Zero-copy stream piping with kernel socket buffer tuning to eradicate latency bloat across challenging network links.</p>
      </div>
      <div class="card">
        <div class="card-icon"><i class="ti ti-shield-check"></i></div>
        <h3>Secure Edge Tunneling</h3>
        <p>End-to-end encrypted transport abstraction designed for reliable microservice communication over edge nodes.</p>
      </div>
    </div>
  </div>
</div>

<footer>
  <div>© 2026 Midoxy Core. Engineered by <a href="https://t.me/OFFL1NE" target="_blank" style="color:var(--text-muted);text-decoration:none;">@OFFL1NE</a></div>
  <div>
    <a href="/login" class="console-link">
      <i class="ti ti-lock"></i> System Console
    </a>
  </div>
</footer>

</body>
</html>
"""

