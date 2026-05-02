frappe.pages['alum-home'].on_page_load = function(wrapper) {
    frappe.alum_home = new AlumHome(wrapper);
};
frappe.pages['alum-home'].on_page_show = function(wrapper) {
    if (frappe.alum_home) frappe.alum_home.refresh();
};

class AlumHome {
    constructor(wrapper) {
        this.wrapper = $(wrapper);
        this._timer = null;
        this._clock = null;
        this.chart  = null;
        frappe.ui.make_app_page({ parent: wrapper, title: 'Plant Home', single_column: true });
        this.wrapper.find('.page-head').hide();
        this.wrapper.find('.layout-main-section-wrapper').css({ background: '#0d0d1a', padding: 0 });
        this.wrapper.find('.layout-main-section').css('padding', 0);
        this.$el = $('<div class="ah"></div>').appendTo(this.wrapper.find('.layout-main-section'));
        this._inject_css();
        this._skeleton();
        this.refresh();
        this._start_clock();
        this._timer = setInterval(() => this.refresh(), 60000);
        this.wrapper.on('page:before-leave', () => { clearInterval(this._timer); clearInterval(this._clock); });
    }

    refresh() {
        frappe.call({
            method: 'kali.kali.page.alum_home.alum_home.get_home_data',
            callback: r => { if (r.message) this._update(r.message); }
        });
    }

    _start_clock() {
        const tick = () => {
            const n = new Date();
            $('#ah-clock').text(n.toLocaleTimeString('en-US', { hour12: false }));
            $('#ah-date').text(n.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }));
        };
        tick();
        this._clock = setInterval(tick, 1000);
    }

    _update(d) {
        this._alerts(d);
        this._cards(d);
        this._flow(d);
        this._jobs(d);
        this._dies(d);
        this._trend(d);
    }

    _alerts(d) {
        const a = [];
        if (d.critical_dies  > 0) a.push(`<span class="ah-alert ah-ar" onclick="frappe.set_route('List','Die Master')">⚠️ ${d.critical_dies} Die${d.critical_dies>1?'s':''} Critical</span>`);
        if (d.delayed_orders > 0) a.push(`<span class="ah-alert ah-ao" onclick="frappe.set_route('List','Sales Order')">🚚 ${d.delayed_orders} Order${d.delayed_orders>1?'s':''} Delayed</span>`);
        if (d.qc_pending     > 0) a.push(`<span class="ah-alert ah-ab" onclick="frappe.set_route('List','Quality Check')">🔍 ${d.qc_pending} QC Pending</span>`);
        $('#ah-alert-bar').html(a.join('') || '<span style="color:rgba(255,255,255,.3);font-size:.75rem">✓ No alerts</span>');
    }

    _cards(d) {
        const fmt_rev = v => v >= 1e5 ? (v/1e5).toFixed(1)+' L' : '₹'+Math.round(v).toLocaleString();
        const p1run = d.press1_active > 0, p2run = d.press2_active > 0;
        const cards = [
            { icon:'⚡', lbl: d.press1_name||'Press 1 (1500T)', val: p1run?'RUNNING':'IDLE', sub: `${d.press1_active} active jobs`, col:'green',  badge: p1run?'run':'idle', href:'/app/extrusion-job-card' },
            { icon:'⚡', lbl: d.press2_name||'Press 2 (2500T)', val: p2run?'RUNNING':'IDLE', sub: `${d.press2_active} active jobs`, col:'green',  badge: p2run?'run':'idle', href:'/app/extrusion-job-card' },
            { icon:'📦', lbl:"Today's Output",  val: Math.round(d.today_kg||0).toLocaleString()+' kg',  sub:'produced today',         col:'blue',   href:'/app/production-shift-report' },
            { icon:'📋', lbl:'Active Orders',   val: d.active_orders||0,     sub:'in pipeline',          col:'blue',   href:'/app/sales-order' },
            { icon:'⚠️', lbl:'Delayed Orders',  val: d.delayed_orders||0,    sub:'past delivery date',   col: (d.delayed_orders||0)>0?'orange':'green', href:'/app/sales-order' },
            { icon:'💰', lbl:'Month Revenue',   val: fmt_rev(d.monthly_revenue||0), sub:'sales invoiced', col:'purple', href:'/app/sales-invoice' },
        ];
        const COLS = { green:'#00ff88', blue:'#00d4ff', orange:'#ff9500', red:'#ff3b3b', purple:'#bf5af2' };
        $('#ah-cards').html(cards.map(c => `
            <div class="ah-card ah-c-${c.col}" onclick="frappe.set_route('${c.href.slice(5)}')" style="cursor:pointer">
                <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <span style="font-size:1.4rem">${c.icon}</span>
                    ${c.badge ? `<span class="ah-badge ${c.badge==='run'?'b-run':'b-idle'}">${c.badge==='run'?'RUNNING':'IDLE'}</span>` : ''}
                </div>
                <div style="font-size:1.7rem;font-weight:700;color:${COLS[c.col]||'#fff'};margin:6px 0 3px;line-height:1">${c.val}</div>
                <div style="font-size:.68rem;color:rgba(255,255,255,.45);text-transform:uppercase;letter-spacing:1px">${c.lbl}</div>
                <div style="font-size:.72rem;color:rgba(255,255,255,.35);margin-top:4px">${c.sub}</div>
            </div>`).join(''));
    }

    _flow(d) {
        const f = d.flow || {};
        const stages = [
            { icon:'📄', name:'Orders',       cnt: f.sales_orders||0,  href:'/app/sales-order' },
            { icon:'🔩', name:'Die Ready',    cnt: f.die_active||0,    href:'/app/die-master' },
            { icon:'🟫', name:'Billet Prep',  cnt: f['Draft']||0,      href:'/app/extrusion-job-card?status=Draft' },
            { icon:'⚡', name:'Pressing',     cnt: (f['Billet Loaded']||0)+(f['Extrusion Running']||0), href:'/app/extrusion-job-card' },
            { icon:'💧', name:'Quenching',    cnt: f['Quenching']||0,  href:'/app/extrusion-job-card' },
            { icon:'🔧', name:'Stretching',   cnt: f['Stretching']||0, href:'/app/extrusion-job-card' },
            { icon:'✂️', name:'Cutting',      cnt: f['Cutting']||0,    href:'/app/extrusion-job-card' },
            { icon:'🔥', name:'Aging',        cnt: f['Aging']||0,      href:'/app/extrusion-job-card' },
            { icon:'🎨', name:'Surface Tx',   cnt: f['Surface Treatment']||0, href:'/app/extrusion-job-card' },
            { icon:'🔍', name:'QC',           cnt: (f['Quality Check']||0)+(f['Quality Hold']||0), href:'/app/quality-check' },
            { icon:'📦', name:'Completed',    cnt: f['Completed']||0,  href:'/app/extrusion-job-card' },
            { icon:'🚚', name:'Dispatch',     cnt: f['dispatch']||0,   href:'/app/delivery-note' },
        ];
        $('#ah-flow').html(stages.map((s, i) => {
            const cls = s.cnt > 5 ? 'fc-warn' : s.cnt > 0 ? 'fc-ok' : 'fc-zero';
            return (i > 0 ? '<div class="ah-arrow">›</div>' : '') +
                `<div class="ah-stage" onclick="frappe.set_route('${s.href.slice(5)}')">
                    <div style="font-size:1.1rem">${s.icon}</div>
                    <div class="ah-sname">${s.name}</div>
                    <div class="ah-scnt ${cls}">${s.cnt}</div>
                </div>`;
        }).join(''));
    }

    _jobs(d) {
        const jobs = d.jobs || [];
        const BADGE = {
            'Draft':'b-draft','Billet Loaded':'b-run','Extrusion Running':'b-run',
            'Quenching':'b-qc','Stretching':'b-age','Cutting':'b-age','Aging':'b-age',
            'Surface Treatment':'b-qc','Quality Check':'b-qc','Quality Hold':'b-hold',
            'Completed':'b-done','Rejected':'b-hold'
        };
        if (!jobs.length) {
            $('#ah-jobs-panel').html('<div class="ah-ph"><div class="ah-ph-hd">Active Job Cards <a href="/app/extrusion-job-card">View All →</a></div><div class="ah-empty">No active jobs</div></div>');
            return;
        }
        const rows = jobs.map(j => {
            const yp = parseFloat(j.yield_pct)||0;
            const ycl = yp>=85?'yg':yp>=75?'yw':'yr';
            return `<tr onclick="frappe.set_route('Form','Extrusion Job Card','${j.name}')" style="cursor:pointer">
                <td style="color:#00d4ff;font-weight:600">${j.name}</td>
                <td style="color:rgba(255,255,255,.55)">${j.sales_order||'—'}</td>
                <td>${j.press||'—'}</td>
                <td><span class="ah-badge ${BADGE[j.status]||'b-draft'}">${j.status}</span></td>
                <td>${Math.round(j.output_kg||0).toLocaleString()} kg</td>
                <td>
                    <div style="display:flex;align-items:center;gap:6px">
                        <span style="font-size:.7rem;min-width:34px">${yp.toFixed(1)}%</span>
                        <div style="flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,.1);min-width:40px">
                            <div class="${ycl}" style="height:100%;border-radius:2px;width:${Math.min(yp,100)}%"></div>
                        </div>
                    </div>
                </td></tr>`;
        }).join('');
        $('#ah-jobs-panel').html(`
            <div class="ah-ph">
                <div class="ah-ph-hd">Active Job Cards <a href="/app/extrusion-job-card">View All →</a></div>
                <div style="overflow-x:auto"><table class="ah-tbl">
                    <thead><tr><th>Job</th><th>Sales Order</th><th>Press</th><th>Stage</th><th>Output</th><th>Yield</th></tr></thead>
                    <tbody>${rows}</tbody>
                </table></div>
            </div>`);
    }

    _dies(d) {
        const dies = d.dies || [];
        if (!dies.length) { $('#ah-die-grid').html('<div class="ah-empty">No dies found</div>'); return; }
        $('#ah-die-grid').html(dies.map(die => {
            const used = parseInt(die.total_shots_used)||0;
            const max  = parseInt(die.max_shots_allowed)||500;
            const pct  = max>0 ? Math.min(Math.round(used/max*100),100) : 0;
            const cl   = pct>=90 ? 'dc-crit' : pct>=75 ? 'dc-warn' : '';
            const fc   = pct>=90 ? 'df-crit' : pct>=75 ? 'df-warn' : 'df-ok';
            const pc   = pct>=90 ? '#ff3b3b' : pct>=75 ? '#ff9500' : '#00ff88';
            return `<div class="ah-die ${cl}" onclick="frappe.set_route('Form','Die Master','${die.name}')">
                <div style="display:flex;justify-content:space-between;font-size:.7rem;margin-bottom:5px">
                    <span style="font-weight:600">${die.die_number||die.name}</span>
                    <span style="font-weight:700;color:${pc}">${pct}%</span>
                </div>
                <div style="height:5px;border-radius:3px;background:rgba(255,255,255,.08)">
                    <div class="${fc}" style="height:100%;border-radius:3px;width:${pct}%"></div>
                </div>
                <div style="font-size:.6rem;color:rgba(255,255,255,.3);margin-top:4px">${used}/${max} shots · ${die.die_status||'Active'}</div>
            </div>`;
        }).join(''));
    }

    _trend(d) {
        const trend = d.trend || [];
        if (!trend.length) return;
        if (!this.$el.find('#ah-trend').length) {
            this.$el.find('.ah-two-col').before(`
                <div class="ah-section" style="padding-bottom:5px">
                    <div class="ah-stitle">14-Day Production Trend</div>
                    <div class="ah-panel" style="padding:12px 18px 18px">
                        <canvas id="ah-trend" height="70"></canvas>
                    </div>
                </div>`);
        }
        const draw = () => {
            const ctx = document.getElementById('ah-trend');
            if (!ctx) return;
            if (this.chart) this.chart.destroy();
            this.chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: trend.map(t => (t.date||'').slice(5)),
                    datasets: [{ data: trend.map(t => parseFloat(t.kg)||0),
                        borderColor:'#00ff88', backgroundColor:'rgba(0,255,136,.08)',
                        borderWidth:2, pointBackgroundColor:'#00ff88', pointRadius:3,
                        tension:.4, fill:true }]
                },
                options: {
                    responsive:true,
                    plugins:{ legend:{display:false}, tooltip:{ callbacks:{ label: c => c.parsed.y.toFixed(0)+' kg' } } },
                    scales:{
                        x:{ grid:{color:'rgba(255,255,255,.05)'}, ticks:{color:'rgba(255,255,255,.4)',font:{size:10}} },
                        y:{ grid:{color:'rgba(255,255,255,.05)'}, ticks:{color:'rgba(255,255,255,.4)',font:{size:10}} }
                    }
                }
            });
        };
        if (window.Chart) { draw(); }
        else {
            const s = document.createElement('script');
            s.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
            s.onload = draw;
            document.head.appendChild(s);
        }
    }

    _nav(icon, lbl, href) {
        return `<a class="ah-nav" href="${href}"><span style="font-size:1.15rem">${icon}</span><span class="ah-nlbl">${lbl}</span></a>`;
    }

    _skeleton() {
        this.$el.html(`
        <div class="ah-header">
            <div style="display:flex;align-items:center;gap:15px">
                <div style="font-size:42px">🏭</div>
                <div>
                    <div class="ah-title">ALUMINIUM MANUFACTURING ERP</div>
                    <div class="ah-sub">Complete Plant Management System</div>
                </div>
            </div>
            <div style="text-align:right">
                <div class="ah-clock" id="ah-clock">--:--:--</div>
                <div class="ah-datec" id="ah-date">Loading…</div>
                <div class="ah-userc" id="ah-user">Welcome, ${(frappe.session.user||'User').split('@')[0]}</div>
            </div>
        </div>

        <div style="padding:0 30px"><div class="ah-alert-bar" id="ah-alert-bar"></div></div>

        <div class="ah-section">
            <div class="ah-stitle">Plant Status</div>
            <div class="ah-cards" id="ah-cards">
                ${[...Array(6)].map(()=>'<div class="ah-card ah-sk" style="height:90px"></div>').join('')}
            </div>
        </div>

        <div class="ah-section" style="padding-bottom:4px"><div class="ah-stitle">Production Flow</div></div>
        <div class="ah-flow-wrap"><div class="ah-flow" id="ah-flow"></div></div>

        <div class="ah-two-col">
            <div>
                <div class="ah-stitle" style="padding:0 0 10px">Active Job Cards</div>
                <div id="ah-jobs-panel" class="ah-panel">
                    <div class="ah-ph-hd">Loading…</div>
                </div>
            </div>
            <div>
                <div class="ah-stitle" style="padding:0 0 10px">Die Shot Life</div>
                <div class="ah-panel">
                    <div class="ah-ph-hd">Die Status <a href="/app/die-master">View All →</a></div>
                    <div class="ah-die-grid" id="ah-die-grid"></div>
                </div>
            </div>
        </div>

        <div class="ah-section" style="padding-bottom:4px"><div class="ah-stitle">Quick Actions</div></div>
        <div class="ah-actions">
            <button class="ah-btn ah-bp" onclick="frappe.new_doc('Extrusion Job Card')">+ New Job Card</button>
            <button class="ah-btn ah-bp" onclick="frappe.new_doc('Sales Order')">+ Sales Order</button>
            <button class="ah-btn ah-bs" onclick="frappe.new_doc('Quality Check')">+ Quality Check</button>
            <button class="ah-btn ah-bs" onclick="frappe.new_doc('Production Shift Report')">+ Shift Report</button>
            <a class="ah-btn ah-bo" href="/app/alum-dashboard">📊 Full Dashboard</a>
            <a class="ah-btn ah-bo" href="/app/query-report/Daily Production Summary">📈 Reports</a>
        </div>

        <div class="ah-footer">
            <div class="ah-stitle" style="padding:0 0 14px">Operations</div>
            <div class="ah-nav-row">
                ${this._nav('🔧','Job Cards','/app/extrusion-job-card')}
                ${this._nav('📋','Press Log','/app/press-log')}
                ${this._nav('🔥','Furnace Log','/app/furnace-log')}
                ${this._nav('⏱️','Aging Log','/app/aging-oven-log')}
                ${this._nav('📊','Shift Report','/app/production-shift-report')}
            </div>
            <div class="ah-stitle" style="padding:12px 0 14px">Quality & Masters</div>
            <div class="ah-nav-row">
                ${this._nav('✅','QC Check','/app/quality-check')}
                ${this._nav('🎨','Surface Tx','/app/surface-treatment-order')}
                ${this._nav('♻️','Scrap','/app/scrap-record')}
                ${this._nav('🔩','Die Master','/app/die-master')}
                ${this._nav('📦','Billet','/app/billet-receipt')}
            </div>
            <div class="ah-stitle" style="padding:12px 0 14px">Sales & Reports</div>
            <div class="ah-nav-row">
                ${this._nav('💰','Sales Order','/app/sales-order')}
                ${this._nav('🛒','Purchase','/app/purchase-order')}
                ${this._nav('🚚','Delivery','/app/delivery-note')}
                ${this._nav('📈','Prod Report','/app/query-report/Daily Production Summary')}
                ${this._nav('🎯','Order Track','/app/query-report/Order to Dispatch Tracker')}
            </div>
        </div>`);
    }

    _inject_css() {
        if ($('#ah-css').length) return;
        $('<style id="ah-css">').text(`
.ah{font-family:'Inter',system-ui,sans-serif;color:#e0e0e0;background:#0d0d1a}
.ah-header{background:linear-gradient(135deg,#1a1a2e,#16213e 50%,#0f3460);padding:20px 30px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(0,212,255,.25);box-shadow:0 4px 24px rgba(0,0,0,.5)}
.ah-title{font-size:1.4rem;font-weight:700;background:linear-gradient(90deg,#00ff88,#00d4ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:1px;margin:0}
.ah-sub{font-size:.7rem;color:rgba(255,255,255,.4);letter-spacing:3px;text-transform:uppercase;margin-top:2px}
.ah-clock{font-size:1.9rem;font-weight:300;color:#00d4ff;font-variant-numeric:tabular-nums}
.ah-datec{font-size:.75rem;color:rgba(255,255,255,.45)}
.ah-userc{font-size:.82rem;color:#00ff88;margin-top:3px}
.ah-alert-bar{display:flex;gap:10px;flex-wrap:wrap;padding:12px 0}
.ah-alert{padding:7px 15px;border-radius:20px;font-size:.78rem;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;gap:6px;animation:ahpulse 2s infinite}
.ah-ar{background:rgba(255,59,59,.15);border:1px solid #ff3b3b;color:#ff6b6b}
.ah-ao{background:rgba(255,149,0,.15);border:1px solid #ff9500;color:#ffb340}
.ah-ab{background:rgba(0,212,255,.15);border:1px solid #00d4ff;color:#00d4ff}
@keyframes ahpulse{0%,100%{opacity:1}50%{opacity:.65}}
.ah-section{padding:18px 30px}
.ah-stitle{font-size:.68rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,.35);margin-bottom:11px;display:flex;align-items:center;gap:8px}
.ah-stitle::after{content:'';flex:1;height:1px;background:rgba(255,255,255,.08)}
.ah-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.ah-card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:17px 19px;transition:all .3s;position:relative;overflow:hidden}
.ah-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px}
.ah-c-green::before{background:linear-gradient(90deg,#00ff88,#00d4ff)}
.ah-c-blue::before{background:linear-gradient(90deg,#00d4ff,#0077ff)}
.ah-c-orange::before{background:linear-gradient(90deg,#ff9500,#ff6b6b)}
.ah-c-purple::before{background:linear-gradient(90deg,#bf5af2,#ff375f)}
.ah-card:hover{background:rgba(255,255,255,.07);border-color:rgba(0,212,255,.3);transform:translateY(-2px);box-shadow:0 8px 28px rgba(0,0,0,.4)}
.ah-badge{padding:2px 8px;border-radius:10px;font-size:.6rem;font-weight:700}
.b-run{background:rgba(0,255,136,.18);color:#00ff88}
.b-idle{background:rgba(255,149,0,.18);color:#ff9500}
.b-draft{background:rgba(255,255,255,.1);color:rgba(255,255,255,.5)}
.b-qc{background:rgba(0,212,255,.15);color:#00d4ff}
.b-age{background:rgba(255,149,0,.15);color:#ff9500}
.b-done{background:rgba(0,255,136,.1);color:rgba(0,255,136,.7)}
.b-hold{background:rgba(255,59,59,.15);color:#ff6b6b}
.ah-flow-wrap{padding:0 30px 18px;overflow-x:auto}
.ah-flow{display:flex;align-items:center;min-width:max-content;padding:4px 0}
.ah-stage{display:flex;flex-direction:column;align-items:center;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:11px 14px;min-width:82px;cursor:pointer;transition:all .3s;text-align:center}
.ah-stage:hover{background:rgba(0,212,255,.1);border-color:rgba(0,212,255,.4);transform:translateY(-3px)}
.ah-sname{font-size:.58rem;text-transform:uppercase;letter-spacing:.5px;color:rgba(255,255,255,.5);margin:3px 0;white-space:nowrap}
.ah-scnt{font-size:1.05rem;font-weight:700}
.fc-ok{color:#00ff88}.fc-warn{color:#ff9500}.fc-zero{color:rgba(255,255,255,.25)}
.ah-arrow{color:rgba(255,255,255,.2);font-size:1.1rem;padding:0 3px;flex-shrink:0}
.ah-two-col{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:0 30px 18px}
.ah-panel{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:12px;overflow:hidden}
.ah-ph{overflow:hidden;border-radius:12px}
.ah-ph-hd{padding:13px 17px;background:rgba(0,0,0,.3);border-bottom:1px solid rgba(255,255,255,.07);font-size:.72rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,.65);display:flex;justify-content:space-between;align-items:center}
.ah-ph-hd a{color:#00d4ff;font-size:.65rem}
.ah-tbl{width:100%;border-collapse:collapse}
.ah-tbl th{padding:7px 11px;font-size:.58rem;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,.3);font-weight:600;border-bottom:1px solid rgba(255,255,255,.05);text-align:left}
.ah-tbl td{padding:8px 11px;font-size:.74rem;border-bottom:1px solid rgba(255,255,255,.04)}
.ah-tbl tr:last-child td{border-bottom:none}
.ah-tbl tr:hover td{background:rgba(255,255,255,.025)}
.yg{background:#00ff88}.yw{background:#ff9500}.yr{background:#ff3b3b}
.ah-die-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;padding:10px}
.ah-die{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:8px;padding:10px 11px;cursor:pointer;transition:all .3s}
.ah-die:hover{background:rgba(255,255,255,.06);transform:translateY(-1px)}
.dc-crit{border-color:rgba(255,59,59,.45)!important}
.dc-warn{border-color:rgba(255,149,0,.45)!important}
.df-crit{background:linear-gradient(90deg,#ff9500,#ff3b3b)}
.df-warn{background:linear-gradient(90deg,#ff9500,#ffcc00)}
.df-ok{background:linear-gradient(90deg,#00d4ff,#00ff88)}
.ah-empty{padding:24px;text-align:center;color:rgba(255,255,255,.3);font-size:.8rem}
.ah-actions{padding:0 30px 20px;display:flex;gap:11px;flex-wrap:wrap}
.ah-btn{padding:10px 19px;border-radius:8px;font-size:.8rem;font-weight:600;cursor:pointer;border:none;transition:all .3s;display:inline-flex;align-items:center;gap:7px;text-decoration:none;color:inherit}
.ah-bp{background:linear-gradient(135deg,#00ff88,#00d4ff);color:#0d0d1a}
.ah-bp:hover{transform:translateY(-2px);box-shadow:0 5px 22px rgba(0,255,136,.35);color:#0d0d1a}
.ah-bs{background:rgba(0,212,255,.14);border:1px solid rgba(0,212,255,.3);color:#00d4ff}
.ah-bs:hover{background:rgba(0,212,255,.22);transform:translateY(-2px)}
.ah-bo{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.13);color:rgba(255,255,255,.7)}
.ah-bo:hover{background:rgba(255,255,255,.09);transform:translateY(-2px)}
.ah-footer{background:rgba(0,0,0,.4);border-top:1px solid rgba(255,255,255,.06);padding:20px 30px 32px;margin-top:8px}
.ah-nav-row{display:grid;grid-template-columns:repeat(5,1fr);gap:7px;margin-bottom:7px}
.ah-nav{display:flex;flex-direction:column;align-items:center;gap:5px;padding:11px 7px;border-radius:10px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);cursor:pointer;transition:all .3s;text-decoration:none;color:inherit}
.ah-nav:hover{background:rgba(0,212,255,.1);border-color:rgba(0,212,255,.3);transform:translateY(-2px);color:inherit}
.ah-nlbl{font-size:.58rem;text-align:center;color:rgba(255,255,255,.45);text-transform:uppercase;letter-spacing:.5px}
.ah-sk{background:linear-gradient(90deg,rgba(255,255,255,.03) 25%,rgba(255,255,255,.07) 50%,rgba(255,255,255,.03) 75%);background-size:200% 100%;animation:ahsh 1.5s infinite;border-radius:12px}
@keyframes ahsh{0%{background-position:200% 0}100%{background-position:-200% 0}}
@media(max-width:768px){.ah-cards{grid-template-columns:repeat(2,1fr)}.ah-two-col{grid-template-columns:1fr}.ah-nav-row{grid-template-columns:repeat(3,1fr)}}
        `).appendTo('head');
    }
}
