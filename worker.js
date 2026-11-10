/**
 * ZM Results — leads Worker
 *
 * Routes (attach to zmresults.co.za/api/* and zmresults.co.za/admin*):
 *   POST /api/audit            Save a free-audit request to D1
 *   GET  /admin                Password-protected list of leads
 *   GET  /admin/leads.csv      Download all leads as CSV
 *   POST /admin/leads/:id      Update a lead's status
 *
 * Bindings needed:
 *   DB              D1 database "zmresults-leads"
 *   ADMIN_PASSWORD  Secret (Settings → Variables and Secrets → type "Secret")
 */

const ALLOWED_ORIGINS = ['https://zmresults.co.za', 'https://www.zmresults.co.za'];
const STATUSES = ['new', 'contacted', 'audit sent', 'won', 'lost'];
const MAX_PER_IP_PER_HOUR = 5;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, '') || '/';

    try {
      if (path === '/api/audit') {
        if (request.method === 'OPTIONS') return cors(request, new Response(null, { status: 204 }));
        if (request.method === 'POST') return cors(request, await saveLead(request, env));
        return json({ ok: false, error: 'Method not allowed' }, 405);
      }

      if (path === '/admin' || path.startsWith('/admin/')) {
        const denied = checkAuth(request, env);
        if (denied) return denied;
        if (path === '/admin' && request.method === 'GET') return adminPage(url, env);
        if (path === '/admin/leads.csv' && request.method === 'GET') return leadsCsv(env);
        const m = path.match(/^\/admin\/leads\/(\d+)$/);
        if (m && request.method === 'POST') return updateLead(request, env, Number(m[1]), url);
        return new Response('Not found', { status: 404 });
      }

      if (path === '/api/health') return json({ ok: true, db: Boolean(env.DB) });

      // Anything else: pass through to the normal website (GitHub Pages)
      return fetch(request);
    } catch (err) {
      console.error(err);
      return json({ ok: false, error: 'Server error' }, 500);
    }
  },
};

/* ---------------- Lead capture ---------------- */

async function saveLead(request, env) {
  if (!env.DB) return json({ ok: false, error: 'Database not connected' }, 500);

  const origin = request.headers.get('Origin');
  if (origin && !ALLOWED_ORIGINS.includes(origin)) return json({ ok: false, error: 'Forbidden' }, 403);

  let data;
  const type = request.headers.get('Content-Type') || '';
  if (type.includes('application/json')) {
    data = await request.json().catch(() => null);
  } else {
    data = Object.fromEntries((await request.formData().catch(() => new FormData())).entries());
  }
  if (!data || typeof data !== 'object') return json({ ok: false, error: 'Invalid request' }, 400);

  // Honeypot: bots fill hidden fields. Pretend success so they don't retry.
  if (clean(data.company_url, 200)) return json({ ok: true });

  const lead = {
    name: clean(data.name, 100),
    business_name: clean(data.business_name, 120),
    phone: clean(data.phone, 30),
    email: clean(data.email, 160),
    service: clean(data.service, 80),
    message: clean(data.message, 2000),
    source_page: clean(data.source_page, 200),
  };

  const errors = [];
  if (!lead.name) errors.push('name');
  if (!lead.business_name) errors.push('business_name');
  if (!/^[+\d][\d\s()-]{6,}$/.test(lead.phone)) errors.push('phone');
  if (lead.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(lead.email)) errors.push('email');
  if (errors.length) return json({ ok: false, error: 'Please check: ' + errors.join(', ') }, 422);

  const ip = request.headers.get('CF-Connecting-IP') || '';
  const ipHash = ip ? await sha256(ip) : '';
  if (ipHash) {
    const row = await env.DB.prepare(
      "SELECT COUNT(*) AS n FROM leads WHERE ip_hash = ? AND created_at > datetime('now', '-1 hour')"
    ).bind(ipHash).first();
    if (row && row.n >= MAX_PER_IP_PER_HOUR) return json({ ok: false, error: 'Too many requests' }, 429);
  }

  await env.DB.prepare(
    `INSERT INTO leads (name, business_name, phone, email, service, message, source_page, ip_country, ip_hash)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`
  ).bind(
    lead.name, lead.business_name, lead.phone, lead.email || null, lead.service || null,
    lead.message || null, lead.source_page || null, request.cf?.country || null, ipHash || null
  ).run();

  return json({ ok: true });
}

/* ---------------- Admin ---------------- */

function checkAuth(request, env) {
  if (!env.ADMIN_PASSWORD) return new Response('Admin password not set. Add an ADMIN_PASSWORD secret to this Worker.', { status: 500 });
  const header = request.headers.get('Authorization') || '';
  const [scheme, encoded] = header.split(' ');
  if (scheme === 'Basic' && encoded) {
    let decoded = '';
    try { decoded = atob(encoded); } catch {}
    const pass = decoded.slice(decoded.indexOf(':') + 1);
    if (safeEqual(pass, env.ADMIN_PASSWORD)) return null;
  }
  return new Response('Login required', {
    status: 401,
    headers: { 'WWW-Authenticate': 'Basic realm="ZM Results leads", charset="UTF-8"', 'Cache-Control': 'no-store' },
  });
}

async function adminPage(url, env) {
  const status = url.searchParams.get('status') || '';
  const q = (url.searchParams.get('q') || '').trim();
  const where = [];
  const params = [];
  if (STATUSES.includes(status)) { where.push('status = ?'); params.push(status); }
  if (q) {
    where.push('(name LIKE ? OR business_name LIKE ? OR phone LIKE ? OR email LIKE ?)');
    const like = '%' + q + '%';
    params.push(like, like, like, like);
  }
  const sql = `SELECT * FROM leads ${where.length ? 'WHERE ' + where.join(' AND ') : ''} ORDER BY id DESC LIMIT 500`;
  const { results = [] } = await env.DB.prepare(sql).bind(...params).all();
  const counts = await env.DB.prepare('SELECT status, COUNT(*) AS n FROM leads GROUP BY status').all();
  const countMap = Object.fromEntries((counts.results || []).map((r) => [r.status, r.n]));
  const total = Object.values(countMap).reduce((a, b) => a + b, 0);

  const tabs = [['', 'All', total], ...STATUSES.map((s) => [s, cap(s), countMap[s] || 0])]
    .map(([s, label, n]) => `<a class="tab${s === status ? ' on' : ''}" href="/admin${s ? '?status=' + encodeURIComponent(s) : ''}">${label} <b>${n}</b></a>`).join('');

  const rows = results.map((r) => {
    const digits = (r.phone || '').replace(/\D/g, '').replace(/^0/, '27');
    const opts = STATUSES.map((s) => `<option${s === r.status ? ' selected' : ''}>${s}</option>`).join('');
    return `<tr>
      <td class="muted">${esc(formatDate(r.created_at))}</td>
      <td><strong>${esc(r.name)}</strong><br><span class="muted">${esc(r.business_name)}</span></td>
      <td><a href="tel:${esc(r.phone)}">${esc(r.phone)}</a><br><a class="wa" href="https://wa.me/${digits}" target="_blank" rel="noopener">WhatsApp</a>${r.email ? `<br><a href="mailto:${esc(r.email)}">${esc(r.email)}</a>` : ''}</td>
      <td>${esc(r.service || '')}${r.message ? `<div class="msg">${esc(r.message)}</div>` : ''}<div class="muted small">${esc(r.source_page || '')}</div></td>
      <td><form method="post" action="/admin/leads/${r.id}"><select name="status" onchange="this.form.submit()">${opts}</select><noscript><button>Save</button></noscript></form></td>
    </tr>`;
  }).join('');

  const body = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Leads | ZM Results</title>
<style>
:root{--paper:#f5f2eb;--card:#fffdf9;--ink:#1d221f;--muted:#5b615c;--line:rgba(29,34,31,.13);--forest:#1e3b2e;--lime:#d4ef6b}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
header{background:var(--forest);color:#fff;padding:18px 0}.wrap{width:min(1200px,100% - 32px);margin:auto}
header .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}h1{margin:0;font-size:1.25rem}h1 span{color:var(--lime)}
header a{color:var(--lime);font-weight:600}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;margin:22px 0}
.tabs{display:flex;flex-wrap:wrap;gap:6px}.tab{padding:7px 12px;border-radius:999px;background:var(--card);border:1px solid var(--line);text-decoration:none;color:inherit;font-weight:500}
.tab b{font-weight:700;margin-left:4px;color:var(--muted)}.tab.on{background:var(--forest);color:#fff;border-color:var(--forest)}.tab.on b{color:var(--lime)}
.search input{padding:9px 12px;border:1px solid var(--line);border-radius:10px;min-width:220px;font:inherit}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
th,td{padding:14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}th{font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);background:#f0ece2}
td a{color:var(--forest)}.wa{font-weight:600}.muted{color:var(--muted)}.small{font-size:.8rem;margin-top:4px}
.msg{margin-top:6px;padding:8px 10px;background:var(--paper);border-radius:8px;white-space:pre-wrap;max-width:420px}
select{padding:7px 9px;border-radius:8px;border:1px solid var(--line);font:inherit;background:#fff}
.empty{padding:40px;text-align:center;color:var(--muted)}
@media(max-width:760px){thead{display:none}table,tbody,tr,td{display:block;width:100%}tr{border-bottom:8px solid var(--paper)}td{border:0;padding:8px 14px}}
</style></head><body>
<header><div class="wrap"><h1>ZM <span>Results</span> · Leads</h1><a href="/admin/leads.csv">Download CSV</a></div></header>
<main class="wrap">
<div class="bar"><nav class="tabs">${tabs}</nav>
<form class="search" method="get" action="/admin">${status ? `<input type="hidden" name="status" value="${esc(status)}">` : ''}<input type="search" name="q" value="${esc(q)}" placeholder="Search name, business, phone…"></form></div>
${results.length ? `<table><thead><tr><th>Received</th><th>Who</th><th>Contact</th><th>Request</th><th>Status</th></tr></thead><tbody>${rows}</tbody></table>` : `<div class="empty">No leads ${status || q ? 'match this filter' : 'yet — they will appear here as soon as someone submits the form'}.</div>`}
</main></body></html>`;

  return new Response(body, { headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Frame-Options': 'DENY' } });
}

async function updateLead(request, env, id, url) {
  // Only accept status changes submitted from the admin page itself
  const origin = request.headers.get('Origin');
  if (origin && origin !== url.origin) return new Response('Forbidden', { status: 403 });
  const form = await request.formData();
  const status = String(form.get('status') || '');
  if (!STATUSES.includes(status)) return new Response('Invalid status', { status: 400 });
  await env.DB.prepare('UPDATE leads SET status = ? WHERE id = ?').bind(status, id).run();
  const back = request.headers.get('Referer');
  return Response.redirect(back && back.startsWith(url.origin + '/admin') ? back : url.origin + '/admin', 303);
}

async function leadsCsv(env) {
  const { results = [] } = await env.DB.prepare(
    'SELECT id, created_at, status, name, business_name, phone, email, service, message, source_page, ip_country FROM leads ORDER BY id DESC'
  ).all();
  const cols = ['id', 'created_at', 'status', 'name', 'business_name', 'phone', 'email', 'service', 'message', 'source_page', 'ip_country'];
  const cell = (v) => {
    let s = v == null ? '' : String(v);
    if (/^[=+\-@]/.test(s)) s = "'" + s; // stop spreadsheet formula injection
    return '"' + s.replace(/"/g, '""') + '"';
  };
  const csv = [cols.join(','), ...results.map((r) => cols.map((c) => cell(r[c])).join(','))].join('\r\n');
  return new Response('﻿' + csv, {
    headers: {
      'Content-Type': 'text/csv; charset=utf-8',
      'Content-Disposition': `attachment; filename="zmresults-leads-${new Date().toISOString().slice(0, 10)}.csv"`,
      'Cache-Control': 'no-store',
    },
  });
}

/* ---------------- Helpers ---------------- */

function cors(request, response) {
  const origin = request.headers.get('Origin');
  const res = new Response(response.body, response);
  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    res.headers.set('Access-Control-Allow-Origin', origin);
    res.headers.set('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.headers.set('Access-Control-Allow-Headers', 'Content-Type');
    res.headers.set('Vary', 'Origin');
  }
  return res;
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
}

function clean(v, max) {
  return String(v ?? '').replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max);
}

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

function formatDate(utc) {
  if (!utc) return '';
  const d = new Date(utc.replace(' ', 'T') + 'Z');
  return d.toLocaleString('en-ZA', { timeZone: 'Africa/Johannesburg', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
}

function safeEqual(a, b) {
  a = String(a); b = String(b);
  let diff = a.length ^ b.length;
  for (let i = 0; i < Math.max(a.length, b.length); i++) diff |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return diff === 0;
}

async function sha256(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode('zmr:' + text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}
