/*
 * This file is part of NeuraSelf-UwU.
 * Copyright (c) 2025-Present Routo
 *
 * NeuraSelf-UwU is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * You should have received a copy of the GNU General Public License
 * along with NeuraSelf-UwU. If not, see <https://www.gnu.org/licenses/>.
 */

let currentConfig = {}, globalAnalyticsData = null;
let distChart = null, lineChart = null, sessChart = null, cashChart = null;
let currentAccountId = null;
let accountsList = [];

async function testSecurity(btn) {
    const q = currentAccountId ? `?id=${currentAccountId}` : '';
    const original = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> TESTING...';
    btn.disabled = true;

    try {
        const res = await fetch(`/api/security/test${q}`, { method: 'POST' });
        const d = await res.json();
        if (d.status === 'success') {
            btn.style.borderColor = 'var(--success)';
            btn.innerHTML = '<i class="fa-solid fa-check"></i> SIGNALS SENT';
        } else {
            alert("Test failed: " + d.message);
            btn.innerHTML = original;
        }
    } catch (e) {
        alert("Request failed");
        btn.innerHTML = original;
    } finally {
        setTimeout(() => {
            btn.innerHTML = original;
            btn.disabled = false;
            btn.style.border = '';
        }, 3000);
    }
}

function nav(id, el) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active-view'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.getElementById(id).classList.add('active-view');
    el.classList.add('active');

    const mobileControls = document.querySelector('.mobile-top-controls');
    if (mobileControls) {
        mobileControls.style.display = (id === 'dash') ? 'flex' : 'none';
    }

    if (id === 'dash') {
        document.body.classList.add('active-dash-header');
    } else {
        document.body.classList.remove('active-dash-header');
    }

    if (window.innerWidth <= 768) {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar && sidebar.classList.contains('active')) {
            toggleMobileMenu();
        }
    }

    if (id === 'config') loadConfig();
    if (id === 'history') loadHistory();
}

function toggleMobileMenu() {
    const s = document.querySelector('.sidebar'), o = document.querySelector('.sidebar-overlay'), t = document.querySelector('.mobile-menu-toggle');
    s.classList.toggle('active'); o.classList.toggle('active'); t.classList.toggle('active');
    document.body.style.overflow = s.classList.contains('active') ? 'hidden' : '';
}

async function fetchAccounts() {
    try {
        const res = await fetch('/api/accounts/list');
        const data = await res.json();
        accountsList = data;

        if (data.length > 0) {
            if (!currentAccountId || !data.find(a => a.id === currentAccountId)) {
                currentAccountId = data[0].id;
            }
            renderAccountDropdown();
            updateAccountHeader();
        }
    } catch (e) { console.error("Failed to fetch accounts", e); }
}

function toggleAccountDropdown() {
    const opts = document.getElementById('accountOptions');
    opts.classList.toggle('open');
    const icon = document.querySelector('#accountDropdownHeader i.fa-chevron-down');
    icon.style.transform = opts.classList.contains('open') ? 'rotate(180deg)' : 'rotate(0deg)';
}

function selectAccount(id) {
    currentAccountId = id;
    updateAccountHeader();
    toggleAccountDropdown();
    if (lineChart) lineChart.data.datasets[0].data = Array(30).fill(0);
    update();
}

function updateAccountHeader() {
    const acc = accountsList.find(a => a.id === currentAccountId);
    if (acc) {
        document.getElementById('currentAccountName').innerText = acc.username;
    }
}

function renderAccountDropdown() {
    const container = document.getElementById('accountOptions');
    container.innerHTML = accountsList.map(acc => `
        <div class="custom-option ${acc.id === currentAccountId ? 'selected' : ''}" onclick="selectAccount('${acc.id}')">
            ${acc.avatar ? `<img src="${acc.avatar}" class="account-avatar">` : '<i class="fa-brands fa-discord"></i>'}
            <span>${acc.username}</span>
            ${acc.paused ? '<span style="margin-left:auto; font-size:0.7em; color:var(--warning)">PAUSED</span>' : ''}
        </div>
    `).join('');
}

async function loadConfig() {
    const r = await fetch('/api/settings');
    currentConfig = await r.json();
    renderSettings(currentConfig);
}

function renderSettings(cfg) {
    const grid = document.getElementById('settings-grid');
    grid.innerHTML = '';

    Object.keys(cfg).forEach(key => {
        if (key === 'commands') {
            Object.keys(cfg[key]).forEach(cmd => {
                grid.appendChild(createModuleCard(cmd.toUpperCase(), cfg[key][cmd], `commands.${cmd}`));
            });
        } else if (typeof cfg[key] === 'object' && !Array.isArray(cfg[key])) {
            grid.appendChild(createModuleCard(key.toUpperCase(), cfg[key], key));
        }
    });
}

function createModuleCard(title, data, path) {
    const card = document.createElement('div');
    card.className = 'module-card';
    card.innerHTML = `
        <div class="module-header" onclick="toggleDropdown(this, event)">
            <span class="module-title">${title}</span>
            <i class="fa-solid fa-chevron-down"></i>
        </div>
        <div class="dropdown-content">
            ${renderCategory(data, path)}
        </div>
    `;
    return card;
}

function renderCategory(obj, path) {
    let h = '';
    let keys = Object.keys(obj);
    const isTiers = path.includes('tiers');
    const isTypes = path.includes('types');

    if (isTiers) {
        const tierOrder = ['common', 'uncommon', 'rare', 'epic', 'mythical', 'legendary', 'fabled'];
        keys.sort((a, b) => tierOrder.indexOf(a) - tierOrder.indexOf(b));
    }

    if (isTiers || isTypes) h += '<div class="gem-tier-group">';

    keys.forEach(key => {
        const val = obj[key];
        const fullPath = `${path}.${key}`;

        if ((isTiers || isTypes) && typeof val === 'boolean') {
            h += `
                <div class="gem-tier-item ${key}">
                    <span class="gem-label">${key}</span>
                    <div class="module-toggle ${val ? 'on' : 'off'}" onclick="toggleMod('${fullPath}', this, event)">
                        <i class="fa-solid ${val ? 'fa-toggle-on' : 'fa-toggle-off'}"></i> ${val ? 'ON' : 'OFF'}
                    </div>
                </div>
            `;
        } else if (typeof val === 'boolean') {
            h += renderField(fullPath, { l: key, type: 'toggle' }, val);
        } else if (Array.isArray(val) && val.length === 2 && typeof val[0] === 'number') {
            h += renderField(fullPath, { l: key, type: 'range' }, val);
        } else if (typeof val === 'object' && val !== null && !Array.isArray(val)) {
            h += `
                <div class="module-header" onclick="toggleDropdown(this, event)" style="margin-top: 15px; border: none; padding: 10px 0;">
                    <span class="module-title" style="font-size: 0.85rem;">${key}</span>
                    <i class="fa-solid fa-chevron-down"></i>
                </div>
                <div class="dropdown-content">
                    ${renderCategory(val, fullPath)}
                </div>
            `;
        } else {
            h += renderField(fullPath, { l: key, type: key.includes('url') ? 'password' : 'text' }, val);
        }
    });

    if (isTiers || isTypes) h += '</div>';
    return h;
}

function renderField(path, f, v) {
    if (f.type === 'toggle') return `<div class="field-group"><label class="field-label">${f.l}</label><div class="module-toggle ${v ? 'on' : 'off'}" onclick="toggleMod('${path}', this, event)"><i class="fa-solid ${v ? 'fa-toggle-on' : 'fa-toggle-off'}"></i> ${v ? 'ON' : 'OFF'}</div></div>`;
    if (f.type === 'range') return `<div class="field-row"><div class="field-group"><label class="field-label">Min</label><input type="number" class="field-input" value="${v[0]}" onclick="event.stopPropagation()" onchange="updateArrVal('${path}',0,this.value)"></div><div class="field-group"><label class="field-label">Max</label><input type="number" class="field-input" value="${v[1]}" onclick="event.stopPropagation()" onchange="updateArrVal('${path}',1,this.value)"></div></div>`;
    return `<div class="field-group"><label class="field-label">${f.l}</label><input type="${f.type === 'password' ? 'password' : 'text'}" class="field-input" value="${v}" onclick="event.stopPropagation()" onchange="updateDeepVal('${path}',this.value)"></div>`;
}

function toggleMod(p, el, ev) {
    if (ev) ev.stopPropagation();
    const v = !el.classList.contains('on');
    setDeep(currentConfig, p.split('.'), v);
    el.className = `module-toggle ${v ? 'on' : 'off'}`;
    el.innerHTML = `<i class="fa-solid ${v ? 'fa-toggle-on' : 'fa-toggle-off'}"></i> ${v ? 'ON' : 'OFF'}`;
}
function updateDeepVal(p, v) {
    let val = v;
    if (!isNaN(v) && v !== "") {
        val = (v.length < 15) ? Number(v) : v;
    }
    setDeep(currentConfig, p.split('.'), val);
}
function updateArrVal(p, i, v) {
    const a = getDeep(currentConfig, p.split('.'));
    if (a) {
        let val = v;
        if (!isNaN(v) && v !== "") {
            val = (v.length < 15) ? Number(v) : v;
        }
        a[i] = val;
    }
}

function saveAllConfigs() {
    fetch('/api/settings', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(currentConfig) }).then(() => alert("Settings Saved!"));
}

function setDeep(o, p, v) { if (p.length === 1) o[p[0]] = v; else { if (!o[p[0]]) o[p[0]] = {}; setDeep(o[p[0]], p.slice(1), v); } }
function getDeep(o, p) { if (!o || p.length === 0) return o; return getDeep(o[p[0]], p.slice(1)); }

function initDashCharts() {
    try {
        const c1 = document.getElementById('distChart').getContext('2d');
        distChart = new Chart(c1, {
            type: 'pie',
            data: { labels: ['Hunt', 'Battle', 'Others'], datasets: [{ data: [1, 1, 1], backgroundColor: ['#ff1f1f', '#3b82f6', '#888'], borderWidth: 0 }] },
            options: { plugins: { legend: { position: 'right' } } }
        });
        const c2 = document.getElementById('lineChart').getContext('2d');
        lineChart = new Chart(c2, {
            type: 'line',
            data: { labels: Array(30).fill(''), datasets: [{ data: Array(30).fill(0), borderColor: '#ff1f1f', backgroundColor: 'rgba(255,31,31,0.05)', fill: true, pointRadius: 2, pointHoverRadius: 5, tension: 0.3 }] },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { x: { display: false }, y: { min: 0, suggestedMax: 10, grid: { color: '#222' }, ticks: { color: '#555', font: { size: 10 } } } },
                plugins: { legend: { display: false } }
            }
        });
    } catch (e) { console.warn("Dashboard charts blocked"); }
}

function update() {
    const q = currentAccountId ? `?id=${currentAccountId}` : '';
    fetch(`/api/stats${q}`).then(r => r.json()).then(d => {
        if (!d || Object.keys(d).length === 0) return;

        if (d.cash) document.getElementById('cash').innerText = d.cash.toLocaleString();
        if (d.uptime) document.getElementById('uptimeDisplay').innerText = d.uptime;
        if (d.logs) renderLogs(d.logs);
        const dot = document.getElementById('statusDot'), lbl = document.getElementById('botStatus');
        lbl.innerText = d.status; dot.className = "ping-dot " + (d.status === "PAUSED" ? "paused" : "");
        if (d.status === "PAUSED" && d.security) {
            document.getElementById('securityAlert').style.display = 'flex';
            const msgEl = document.getElementById('captchaMsg');
            if (msgEl) msgEl.innerText = d.security.last_message || "No details available";
        } else {
            document.getElementById('securityAlert').style.display = 'none';
        }

        if (d.chart_data) {
            document.getElementById('huntsToday').innerText = d.chart_data.hunt;
            document.getElementById('battlesToday').innerText = d.chart_data.battle;
            document.getElementById('cpm').innerText = d.chart_data.perf_bpm;
            if (document.getElementById('totalOwO')) document.getElementById('totalOwO').innerText = d.chart_data.total;
        }

        if (d.security) {
            document.getElementById('sec-captchas').innerText = d.security.captchas;
            document.getElementById('sec-bans').innerText = d.security.bans;
            document.getElementById('sec-warns').innerText = d.security.warnings;
        }

        if (distChart && d.chart_data) {
            distChart.data.datasets[0].data = [d.chart_data.hunt, d.chart_data.battle, d.chart_data.other];
            distChart.update();
        }

        if (lineChart && d.chart_data) {
            lineChart.data.datasets[0].data.push(d.chart_data.perf_bpm);
            lineChart.data.datasets[0].data.shift();
            lineChart.update('none');
        }

        renderQuests(d.quest_data, d.next_quest_timer);
    });
}
setInterval(update, 1000);

function renderQuests(quests, timer) {
    const list = document.getElementById('questList');
    const timerEl = document.getElementById('nextQuestTimer');
    if (!list || !timerEl) return;

    if (timer) {
        timerEl.innerHTML = `<i class="fa-solid fa-clock"></i> Next quest in: ${timer}`;
        timerEl.style.display = 'block';
    } else {
        timerEl.style.display = 'none';
    }

    if (!quests || quests.length === 0) {
        list.innerHTML = '<div style="color:#666; font-style:italic;">No active quests found. Use oquest to refresh.</div>';
        return;
    }

    list.innerHTML = quests.map(q => {
        const percent = Math.min(100, Math.round((q.current / q.total) * 100));
        const color = q.completed ? 'var(--success)' : 'var(--primary)';
        return `
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:15px; border-radius:8px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:0.9rem;">
                    <span style="color:#eee;">${q.description}</span>
                    <span style="color:${color}; font-weight:bold;">${q.current}/${q.total}</span>
                </div>
                <div style="height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden;">
                    <div style="width:${percent}%; height:100%; background:${color}; box-shadow: 0 0 10px ${color}44; transition: width 0.5s ease;"></div>
                </div>
            </div>
        `;
    }).join('');
}

const timeFormatter = new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
});

let lastLogsHash = '';
function renderLogs(logs) {
    const t = document.getElementById('term'); if (!t) return;

    // Simple hash to prevent re-rendering identical content
    const currentHash = logs.slice(0, 5).map(l => l.timestamp).join('|');
    if (currentHash === lastLogsHash) return;
    lastLogsHash = currentHash;

    t.innerHTML = logs.map(l => {
        const tagClass = l.type ? `tag-${l.type.toLowerCase()}` : '';
        const localTime = l.timestamp ? timeFormatter.format(new Date(l.timestamp * 1000)) : l.time;
        const botTag = l.bot_name ? `<span style="color:magenta; margin-right:5px;">[${l.bot_name}]</span>` : '';
        return `<div class="history-item ${l.type ? l.type.toLowerCase() : ''}">${botTag}<span class="history-time">[${localTime}]</span> <span class="history-tag ${tagClass}">${l.type}</span> <span class="history-msg">${l.message}</span></div>`;
    }).join('');
}


function toggleDropdown(element, event) {
    if (event) event.stopPropagation();
    const dropdown = element.nextElementSibling;
    const icon = element.querySelector('i');

    if (!dropdown || !dropdown.classList.contains('dropdown-content')) {
        // Fallback for different structures if any
        const parent = element.closest('.module-card') || element.closest('.nested-category');
        const altDropdown = parent ? parent.querySelector('.dropdown-content') : null;
        if (altDropdown) {
            altDropdown.classList.toggle('active');
        }
    } else {
        dropdown.classList.toggle('active');
    }

    element.classList.toggle('active');

    const isActive = dropdown ? dropdown.classList.contains('active') : element.classList.contains('active');
    if (icon) {
        icon.style.transform = isActive ? 'rotate(180deg)' : 'rotate(0deg)';
    }
}


function populateSessionDropdown() {
    // ... (History logic remains mostly same but might need multi-account considerations later)
    // For now keeping simpler view
    const select = document.getElementById('session-select');
    const currentVal = select.value;
    select.innerHTML = '<option value="all">ALL SESSIONS</option>';
    if (!globalAnalyticsData || !globalAnalyticsData.sessions) return;
    [...globalAnalyticsData.sessions].reverse().forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.id;
        opt.innerText = `Session #${s.id}: ${s.date} ${s.start_time}`;
        select.appendChild(opt);
    });
    if (currentVal) select.value = currentVal;
}

function renderSessionChart() {
    const filterId = document.getElementById('session-select').value;
    if (!globalAnalyticsData) return;
    let filtered = filterId === 'all' ? globalAnalyticsData.sessions.slice(-20) : [globalAnalyticsData.sessions.find(x => String(x.id) === filterId)];
    const sctx = document.getElementById('sessionChart').getContext('2d');
    if (sessChart) sessChart.destroy();
    sessChart = new Chart(sctx, {
        type: 'bar',
        data: {
            labels: filtered.map(s => `S${s.id}`),
            datasets: [
                { label: 'Hunts', data: filtered.map(s => s.stats.hunts), backgroundColor: '#ff1f1f' },
                { label: 'Battles', data: filtered.map(s => s.stats.battles), backgroundColor: '#3b82f6' }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, scales: { x: { grid: { display: false }, ticks: { color: '#666' } }, y: { grid: { color: '#222' }, ticks: { color: '#666' } } } }
    });
}

function renderCashChart() {
    if (!globalAnalyticsData) return;
    const cctx = document.getElementById('cashHistoryChart').getContext('2d');
    if (cashChart) cashChart.destroy();
    cashChart = new Chart(cctx, {
        type: 'line',
        data: {
            labels: globalAnalyticsData.cash_history.map(c => c.timestamp.split(' ')[1]),
            datasets: [{ label: 'Cash', data: globalAnalyticsData.cash_history.map(c => c.amount), borderColor: '#ffd700', backgroundColor: 'rgba(255, 215, 0, 0.1)', fill: true, tension: 0.3 }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { grid: { color: '#222' }, ticks: { color: '#666' } } } }
    });
}

let currentFilter = 'all';
function filterHistory(type, el) {
    currentFilter = type;
    document.querySelectorAll('.badge').forEach(b => b.classList.remove('active'));
    if (el) el.classList.add('active');
    renderHistoryFeed();
}

function renderHistoryFeed() {
    const feed = document.getElementById('history-feed');
    if (!feed || !globalAnalyticsData || !globalAnalyticsData.recent_logs) return;
    feed.innerHTML = globalAnalyticsData.recent_logs
        .filter(l => {
            if (currentFilter === 'all') return true;
            if (currentFilter === 'SECURITY') return l.type === 'SECURITY' || l.type === 'ALARM';
            return l.type === currentFilter;
        })
        .slice(-100).reverse().map(l => {
            const tagClass = l.type ? `tag-${l.type.toLowerCase()}` : '';
            return `<div class="history-item ${l.type ? l.type.toLowerCase() : ''}"><span class="history-time">[${l.time}]</span> <span class="history-tag ${tagClass}">${l.type}</span> <span class="history-msg">${l.message}</span></div>`;
        }).join('');
}

async function loadHistory() {
    try {
        const res = await fetch('/api/history/analytics');
        globalAnalyticsData = await res.json();
        const totals = globalAnalyticsData.totals || {};
        document.getElementById('total-sessions').innerText = totals.total_sessions || 0;
        document.getElementById('total-hunts').innerText = (totals.all_time_hunts || 0).toLocaleString();
        document.getElementById('total-battles').innerText = (totals.all_time_battles || 0).toLocaleString();
        document.getElementById('total-cmds').innerText = (totals.all_time_commands || 0).toLocaleString();
        populateSessionDropdown();
        renderCashChart();
        renderSessionChart();
        renderHistoryFeed();
    } catch (e) { console.error("History Error:", e); }
}

function resumeBot() { fetch('/api/security', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ action: 'resume', id: currentAccountId }) }).then(() => { document.getElementById('securityAlert').style.display = 'none'; update(); }); }
function action(a, el) { fetch('/api/control', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ action: a, id: currentAccountId }) }).then(() => update()); }

function initDynamicTilt() {
    const cards = document.querySelectorAll('.kpi-card');
    cards.forEach(card => {
        const icon = card.querySelector('.kpi-icon');
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            // Higher multiplier = more tilt
            const rotateX = -(y - centerY) / 5;
            const rotateY = (x - centerX) / 5;

            icon.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
        });

        card.addEventListener('mouseleave', () => {
            icon.style.transform = `rotateX(0deg) rotateY(0deg) translateZ(0px)`;
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initDashCharts();
    fetchAccounts();
    loadConfig();
    initDynamicTilt();
    setInterval(fetchAccounts, 5000);
});
