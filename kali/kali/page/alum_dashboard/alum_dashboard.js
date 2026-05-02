frappe.pages['alum-dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: '🏭 Production Dashboard',
		single_column: true
	});
	page.add_action_item('Refresh', () => load_all());

	$(wrapper).find('.layout-main-section').html(
		'<div id="pm-root" style="padding:12px 16px;font-family:Inter,sans-serif"></div>'
	);

	var REFRESH_SEC = 30;
	var timer_interval;

	load_all();

	function load_all() {
		Promise.all([
			frappe.call({method:'kali.kali.page.alum_dashboard.alum_dashboard.get_kpis'}),
			frappe.call({method:'kali.kali.page.alum_dashboard.alum_dashboard.get_press_status'}),
			frappe.call({method:'kali.kali.page.alum_dashboard.alum_dashboard.get_pipeline'}),
			frappe.call({method:'kali.kali.page.alum_dashboard.alum_dashboard.get_shift_trend'}),
			frappe.call({method:'kali.kali.page.alum_dashboard.alum_dashboard.get_die_alerts'}),
			frappe.call({method:'kali.kali.page.alum_dashboard.alum_dashboard.get_active_jobs'}),
		]).then(([k,p,pl,t,d,j]) => {
			render(k.message||{}, p.message||[], pl.message||{}, t.message||[], d.message||[], j.message||[]);
		});
	}

	function fmt(n,dec=0){ return (n||0).toLocaleString('en-IN',{maximumFractionDigits:dec}); }
	function fmtc(n){ return '₹'+fmt(n); }

	function kpi(title, val, unit, color, icon, sub){
		return `<div style="background:#fff;border-radius:10px;padding:14px 18px;flex:1;min-width:140px;
			box-shadow:0 2px 8px rgba(0,0,0,.07);border-left:4px solid ${color}">
			<div style="display:flex;justify-content:space-between;align-items:flex-start">
				<div style="flex:1">
					<div style="font-size:10px;color:#888;font-weight:700;text-transform:uppercase;letter-spacing:.6px">${title}</div>
					<div style="font-size:26px;font-weight:800;color:${color};margin:3px 0;line-height:1">${val}<span style="font-size:11px;font-weight:400;color:#777;margin-left:3px">${unit}</span></div>
					${sub?`<div style="font-size:10px;color:#999">${sub}</div>`:''}
				</div>
				<div style="font-size:26px;opacity:.25;margin-left:8px">${icon}</div>
			</div>
		</div>`;
	}

	function render(kpis, presses, pipeline, trend, die_alerts, jobs){
		// Alert Bar
		var alerts = [];
		if(kpis.delayed_orders>0) alerts.push(`<span style="background:#dc3545;color:#fff;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;margin-right:6px">⚠ ${kpis.delayed_orders} DELAYED ORDER${kpis.delayed_orders>1?'S':''}</span>`);
		if(kpis.dies_critical>0) alerts.push(`<span style="background:#fd7e14;color:#fff;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;margin-right:6px">🔩 ${kpis.dies_critical} DIE${kpis.dies_critical>1?'S':''} CRITICAL</span>`);
		if(kpis.pending_qc>0) alerts.push(`<span style="background:#17a2b8;color:#fff;padding:3px 10px;border-radius:12px;font-size:11px;margin-right:6px">🔬 ${kpis.pending_qc} QC PENDING</span>`);
		var alert_bar = alerts.length
			? `<div style="background:#fff3cd;border:1px solid #ffc107;border-radius:8px;padding:8px 14px;margin-bottom:12px;display:flex;align-items:center;flex-wrap:wrap;gap:4px">
				<span style="font-weight:700;color:#856404;margin-right:8px">⚡ PLANT ALERTS:</span>${alerts.join('')}
			   </div>`
			: `<div style="background:#d4edda;border:1px solid #c3e6cb;border-radius:8px;padding:8px 14px;margin-bottom:12px;color:#155724;font-weight:600;font-size:12px">✅ All systems normal — No active alerts</div>`;

		// Press status pills
		var press_html = presses.map(p => {
			var run = p.running;
			var bg = run ? '#d4edda' : '#f8f9fa';
			var bc = run ? '#28a745' : '#adb5bd';
			var dot = run ? '🟢' : '⚪';
			return `<div style="background:${bg};border:1.5px solid ${bc};border-radius:8px;padding:10px 14px;flex:1;min-width:160px">
				<div style="font-size:11px;font-weight:700;color:${bc}">${dot} ${p.press}</div>
				<div style="font-size:13px;font-weight:600;color:#333;margin-top:4px">${p.running?p.status:'IDLE'}</div>
				${p.running?`<div style="font-size:10px;color:#555;margin-top:2px">${p.profile||''}</div>
				<div style="font-size:10px;color:#28a745;font-weight:600">Yield: ${(p.yield_pct||0).toFixed(1)}%</div>`:'<div style="font-size:10px;color:#aaa">No active job</div>'}
			</div>`;
		}).join('') || '<div style="color:#aaa;font-size:12px;padding:10px">No press data</div>';

		// Pipeline
		var pl_stages = [
			{label:'Sales Orders', val:pipeline.so, color:'#17a2b8', icon:'📋'},
			{label:'Work Orders',  val:pipeline.wo, color:'#6f42c1', icon:'🔨'},
			{label:'On Press',     val:pipeline.press,color:'#fd7e14',icon:'⚙️'},
			{label:'QC Check',     val:pipeline.qc, color:'#ffc107', icon:'🔬'},
			{label:'Surface Tmt',  val:pipeline.surface,color:'#e83e8c',icon:'🎨'},
			{label:'Dispatch',     val:pipeline.dispatch,color:'#28a745',icon:'🚚'},
		];
		var pl_html = pl_stages.map((s,i) => `
			<div style="display:flex;align-items:center">
				<div style="text-align:center">
					<div style="background:${s.color};color:#fff;border-radius:50%;width:42px;height:42px;
						display:flex;align-items:center;justify-content:center;font-size:18px;margin:0 auto">${s.icon}</div>
					<div style="font-size:10px;color:#666;margin-top:4px;font-weight:600">${s.label}</div>
					<div style="font-size:20px;font-weight:800;color:${s.color}">${s.val||0}</div>
				</div>
				${i<pl_stages.length-1?'<div style="flex:1;height:2px;background:linear-gradient(90deg,'+s.color+','+pl_stages[i+1].color+');margin:0 6px;margin-bottom:20px"></div>':''}
			</div>`).join('');

		// Jobs table
		var status_colors = {'Completed':'#28a745','Extrusion Running':'#17a2b8','Billet Loaded':'#fd7e14','Heating':'#e83e8c','Stretching':'#6f42c1','Aging':'#795548','QC Pending':'#ffc107','On Hold':'#dc3545','Pending':'#6c757d'};
		var job_rows = jobs.map(j=>{
			var sc = status_colors[j.status]||'#6c757d';
			var yc = (j.yield_percentage||0)>=80?'#28a745':'#dc3545';
			return `<tr style="border-bottom:1px solid #f0f0f0">
				<td style="padding:7px 10px"><a href="/app/extrusion-job-card/${j.name}" style="color:#17a2b8;font-weight:600">${j.name}</a></td>
				<td style="padding:7px 10px;font-size:11px">${j.shift_date||''}</td>
				<td style="padding:7px 10px;font-size:11px">${j.press||'-'}</td>
				<td style="padding:7px 10px;font-size:11px;max-width:120px;overflow:hidden;text-overflow:ellipsis">${j.profile_item||'-'}</td>
				<td style="padding:7px 10px;font-size:11px">${fmt(j.net_output_kg,0)}</td>
				<td style="padding:7px 10px;font-size:11px">${j.operator_name||'-'}</td>
				<td style="padding:7px 10px"><span style="background:${sc};color:#fff;padding:2px 7px;border-radius:10px;font-size:10px;white-space:nowrap">${j.status}</span></td>
				<td style="padding:7px 10px"><span style="color:${yc};font-weight:700;font-size:12px">${(j.yield_percentage||0).toFixed(1)}%</span></td>
			</tr>`;
		}).join('') || '<tr><td colspan="8" style="text-align:center;color:#aaa;padding:16px">No job cards found</td></tr>';

		// Die alerts
		var die_rows = die_alerts.map(d=>{
			var bc = d.pct>=90?'#dc3545':d.pct>=80?'#fd7e14':'#ffc107';
			return `<tr style="border-bottom:1px solid #f0f0f0">
				<td style="padding:7px 10px;font-weight:700"><a href="/app/die-master/${d.die_number}" style="color:#17a2b8">${d.die_number}</a></td>
				<td style="padding:7px 10px;font-size:11px">${d.die_name||''}</td>
				<td style="padding:7px 10px">
					<div style="background:#e9ecef;border-radius:4px;height:12px;width:80px;overflow:hidden;display:inline-block;vertical-align:middle">
						<div style="width:${Math.min(d.pct,100)}%;background:${bc};height:100%"></div>
					</div>
					<span style="margin-left:6px;font-size:11px;font-weight:700;color:${bc}">${d.pct.toFixed(0)}%</span>
				</td>
				<td style="padding:7px 10px"><span style="background:${bc};color:#fff;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700">${d.pct>=90?'CRITICAL':'WARNING'}</span></td>
			</tr>`;
		}).join('') || '<tr><td colspan="4" style="text-align:center;color:#aaa;padding:12px">No die alerts</td></tr>';

		$('#pm-root').html(`
		${alert_bar}

		<!-- Press Status + Timestamp -->
		<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
			<h5 style="margin:0;color:#444;font-weight:700">Press Status</h5>
			<span style="font-size:11px;color:#aaa" id="pm-ts">Updated: ${new Date().toLocaleTimeString()}</span>
		</div>
		<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px">${press_html}</div>

		<!-- KPI Row 1: Production -->
		<h5 style="margin:0 0 6px;color:#444;font-weight:700">Production KPIs</h5>
		<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px">
			${kpi('Today Output', fmt(kpis.today_output), 'Kg', '#17a2b8', '⚡', '')}
			${kpi('This Week', fmt(kpis.week_output), 'Kg', '#6f42c1', '📅', '')}
			${kpi('This Month', fmt(kpis.month_output), 'Kg', '#28a745', '📦', '')}
			${kpi('Avg Yield (30d)', (kpis.avg_yield_30d||0).toFixed(1), '%', kpis.avg_yield_30d>=80?'#28a745':'#dc3545', '📊', '')}
			${kpi('Dies Critical', kpis.dies_critical, '', kpis.dies_critical>0?'#dc3545':'#28a745', '🔩', '')}
		</div>

		<!-- KPI Row 2: Orders -->
		<h5 style="margin:0 0 6px;color:#444;font-weight:700">Order Status</h5>
		<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px">
			${kpi('Active Orders', kpis.active_orders, '', '#17a2b8', '📋', '')}
			${kpi('In Production', kpis.in_production, '', '#fd7e14', '⚙️', '')}
			${kpi('QC Pending', kpis.pending_qc, '', '#ffc107', '🔬', '')}
			${kpi('Dispatched Today', kpis.dispatched_today, '', '#28a745', '🚚', '')}
			${kpi('Delayed', kpis.delayed_orders, '', kpis.delayed_orders>0?'#dc3545':'#28a745', '⚠️', '')}
			${kpi('Revenue (Month)', fmtc(kpis.revenue_month), '', '#28a745', '💰', '')}
		</div>

		<!-- Pipeline -->
		<div style="background:#fff;border-radius:10px;padding:16px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,.07)">
			<h6 style="margin:0 0 14px;color:#555;font-weight:700">📊 Order Pipeline</h6>
			<div style="display:flex;align-items:center;flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px">${pl_html}</div>
		</div>

		<!-- Charts + Die Alerts side by side -->
		<div style="display:grid;grid-template-columns:1.5fr 1fr;gap:14px;margin-bottom:16px">
			<div style="background:#fff;border-radius:10px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.07)">
				<h6 style="margin:0 0 10px;color:#555;font-weight:700">📈 Daily Output Trend</h6>
				<div id="pm-output-chart"></div>
			</div>
			<div style="background:#fff;border-radius:10px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.07)">
				<h6 style="margin:0 0 10px;color:#dc3545;font-weight:700">⚠️ Die Alerts</h6>
				<table style="width:100%;border-collapse:collapse">
					<thead><tr style="background:#f8f9fa">
						<th style="padding:6px 10px;text-align:left;font-size:10px;color:#666">Die</th>
						<th style="padding:6px 10px;text-align:left;font-size:10px;color:#666">Name</th>
						<th style="padding:6px 10px;text-align:left;font-size:10px;color:#666">Shot Life</th>
						<th style="padding:6px 10px;text-align:left;font-size:10px;color:#666">Alert</th>
					</tr></thead>
					<tbody>${die_rows}</tbody>
				</table>
			</div>
		</div>

		<!-- Active Job Cards -->
		<div style="background:#fff;border-radius:10px;padding:14px;box-shadow:0 2px 8px rgba(0,0,0,.07)">
			<h6 style="margin:0 0 10px;color:#555;font-weight:700">🔧 Recent Job Cards</h6>
			<div style="overflow-x:auto">
			<table style="width:100%;border-collapse:collapse;min-width:600px">
				<thead><tr style="background:#f8f9fa">
					<th style="padding:7px 10px;text-align:left;font-size:10px;color:#666">Job Card</th>
					<th style="padding:7px 10px;text-align:left;font-size:10px;color:#666">Date</th>
					<th style="padding:7px 10px;text-align:left;font-size:10px;color:#666">Press</th>
					<th style="padding:7px 10px;text-align:left;font-size:10px;color:#666">Profile</th>
					<th style="padding:7px 10px;text-align:left;font-size:10px;color:#666">Output Kg</th>
					<th style="padding:7px 10px;text-align:left;font-size:10px;color:#666">Operator</th>
					<th style="padding:7px 10px;text-align:left;font-size:10px;color:#666">Status</th>
					<th style="padding:7px 10px;text-align:left;font-size:10px;color:#666">Yield</th>
				</tr></thead>
				<tbody>${job_rows}</tbody>
			</table>
			</div>
		</div>

		<!-- Refresh counter -->
		<div style="text-align:center;margin-top:10px;font-size:11px;color:#aaa">
			Auto-refresh every ${REFRESH_SEC}s &bull; <span id="pm-countdown">${REFRESH_SEC}</span>s remaining
		</div>
		`);

		// Render chart
		if(trend && trend.length){
			try {
				new frappe.Chart('#pm-output-chart', {
					data:{labels:trend.map(r=>r.label||''),datasets:[
						{name:'Output Kg',values:trend.map(r=>r.output_kg||0),chartType:'bar'},
						{name:'Yield %',values:trend.map(r=>r.avg_yield||0),chartType:'line'},
					]},
					type:'axis-mixed',height:200,
					colors:['#17a2b8','#28a745'],
					axisOptions:{xIsSeries:1}
				});
			} catch(e){}
		}

		// countdown
		clearInterval(timer_interval);
		var secs = REFRESH_SEC;
		timer_interval = setInterval(()=>{
			secs--;
			$('#pm-countdown').text(secs);
			if(secs<=0){ clearInterval(timer_interval); load_all(); }
		}, 1000);
	}

	$(wrapper).on('remove', ()=>clearInterval(timer_interval));
};
