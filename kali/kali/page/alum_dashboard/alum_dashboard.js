frappe.pages['alum-dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: '🏭 Production Dashboard',
		single_column: true
	});

	page.add_action_item('Refresh', () => load_dashboard());

	$(wrapper).find('.layout-main-section').html(`
		<div id="alum-dashboard-root" style="padding:16px">
			<div style="text-align:center;padding:40px;color:#888">
				<i class="fa fa-spinner fa-spin fa-2x"></i>
				<p style="margin-top:10px">Loading dashboard...</p>
			</div>
		</div>
	`);

	load_dashboard();

	function load_dashboard() {
		Promise.all([
			frappe.call({ method: 'kali.kali.page.alum_dashboard.alum_dashboard.get_kpis' }),
			frappe.call({ method: 'kali.kali.page.alum_dashboard.alum_dashboard.get_shift_trend' }),
			frappe.call({ method: 'kali.kali.page.alum_dashboard.alum_dashboard.get_die_alerts' }),
			frappe.call({ method: 'kali.kali.page.alum_dashboard.alum_dashboard.get_active_jobs' }),
		]).then(([kpi_r, trend_r, die_r, jobs_r]) => {
			render_dashboard(
				kpi_r.message || {},
				trend_r.message || [],
				die_r.message || [],
				jobs_r.message || []
			);
		});
	}

	function kpi_card(title, value, unit, color, icon, trend) {
		return `
		<div style="background:#fff;border-radius:10px;padding:20px 24px;flex:1;min-width:160px;box-shadow:0 2px 8px rgba(0,0,0,0.08);border-left:4px solid ${color}">
			<div style="display:flex;justify-content:space-between;align-items:center">
				<div>
					<div style="font-size:12px;color:#888;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">${title}</div>
					<div style="font-size:28px;font-weight:700;color:${color};margin:4px 0">${value}<span style="font-size:13px;font-weight:400;color:#666;margin-left:4px">${unit}</span></div>
					${trend ? `<div style="font-size:11px;color:#28a745">↑ ${trend}</div>` : ''}
				</div>
				<div style="font-size:32px;opacity:0.3">${icon}</div>
			</div>
		</div>`;
	}

	function render_dashboard(kpis, trend, die_alerts, jobs) {
		var trend_labels = trend.map(t => t.label || '');
		var trend_outputs = trend.map(t => t.output_kg || 0);
		var trend_yields = trend.map(t => t.avg_yield || 0);

		var alert_rows = die_alerts.map(d => `
			<tr>
				<td style="padding:8px 12px;font-weight:600">${d.die_number}</td>
				<td style="padding:8px 12px">${d.die_name || ''}</td>
				<td style="padding:8px 12px">
					<div style="background:#e9ecef;border-radius:4px;height:14px;width:100px;overflow:hidden;display:inline-block">
						<div style="width:${Math.min(d.pct,100)}%;background:${d.pct>=90?'#dc3545':d.pct>=75?'#ffc107':'#28a745'};height:100%"></div>
					</div>
					<span style="margin-left:6px;font-size:11px">${d.pct.toFixed(0)}%</span>
				</td>
				<td style="padding:8px 12px"><span style="background:${d.pct>=90?'#dc3545':'#ffc107'};color:#fff;padding:2px 8px;border-radius:10px;font-size:10px">${d.pct>=90?'CRITICAL':'WARNING'}</span></td>
			</tr>
		`).join('') || '<tr><td colspan="4" style="padding:16px;text-align:center;color:#888">No alerts</td></tr>';

		var job_rows = jobs.map(j => {
			var color = j.status === 'Completed' ? '#28a745' : j.status === 'In Progress' ? '#17a2b8' : '#ffc107';
			return `
			<tr>
				<td style="padding:8px 12px"><a href="/app/extrusion-job-card/${j.name}">${j.name}</a></td>
				<td style="padding:8px 12px">${j.shift_date || ''}</td>
				<td style="padding:8px 12px">${j.profile_item || ''}</td>
				<td style="padding:8px 12px">${(j.yield_percentage||0).toFixed(1)}%</td>
				<td style="padding:8px 12px"><span style="background:${color};color:#fff;padding:2px 8px;border-radius:10px;font-size:10px">${j.status}</span></td>
			</tr>`;
		}).join('') || '<tr><td colspan="5" style="padding:16px;text-align:center;color:#888">No recent jobs</td></tr>';

		$('#alum-dashboard-root').html(`
			<div style="margin-bottom:8px;display:flex;justify-content:space-between;align-items:center">
				<h4 style="margin:0;color:#333;font-weight:700">Live Production Overview</h4>
				<span style="font-size:11px;color:#888">Auto-refreshes every 60s &bull; Last updated: ${new Date().toLocaleTimeString()}</span>
			</div>

			<!-- KPI Row -->
			<div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:20px">
				${kpi_card('Today Output', (kpis.today_output||0).toFixed(0), 'Kg', '#17a2b8', '⚡', '')}
				${kpi_card('Active Job Cards', kpis.active_jobs||0, '', '#28a745', '🔧', '')}
				${kpi_card('Avg Yield (30d)', (kpis.avg_yield_30d||0).toFixed(1), '%', kpis.avg_yield_30d>=80?'#28a745':'#dc3545', '📊', '')}
				${kpi_card('Dies Critical', kpis.dies_critical||0, '', kpis.dies_critical>0?'#dc3545':'#28a745', '⚠️', '')}
				${kpi_card('Month Output', (kpis.month_output||0).toFixed(0), 'Kg', '#6f42c1', '📦', '')}
			</div>

			<!-- Charts Row -->
			<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px">
				<div style="background:#fff;border-radius:10px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
					<h6 style="margin:0 0 12px;color:#555;font-weight:600">Daily Output (Last 14 Days)</h6>
					<div id="alum-output-chart"></div>
				</div>
				<div style="background:#fff;border-radius:10px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
					<h6 style="margin:0 0 12px;color:#555;font-weight:600">Yield Trend (%)</h6>
					<div id="alum-yield-chart"></div>
				</div>
			</div>

			<!-- Tables Row -->
			<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
				<div style="background:#fff;border-radius:10px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
					<h6 style="margin:0 0 12px;color:#dc3545;font-weight:600">⚠️ Die Alerts</h6>
					<table style="width:100%;border-collapse:collapse">
						<thead><tr style="background:#f8f9fa">
							<th style="padding:8px 12px;text-align:left;font-size:11px">Die</th>
							<th style="padding:8px 12px;text-align:left;font-size:11px">Profile</th>
							<th style="padding:8px 12px;text-align:left;font-size:11px">Shot Life</th>
							<th style="padding:8px 12px;text-align:left;font-size:11px">Alert</th>
						</tr></thead>
						<tbody>${alert_rows}</tbody>
					</table>
				</div>
				<div style="background:#fff;border-radius:10px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,0.08)">
					<h6 style="margin:0 0 12px;color:#555;font-weight:600">🔧 Recent Job Cards</h6>
					<table style="width:100%;border-collapse:collapse">
						<thead><tr style="background:#f8f9fa">
							<th style="padding:8px 12px;text-align:left;font-size:11px">Job Card</th>
							<th style="padding:8px 12px;text-align:left;font-size:11px">Date</th>
							<th style="padding:8px 12px;text-align:left;font-size:11px">Profile</th>
							<th style="padding:8px 12px;text-align:left;font-size:11px">Yield</th>
							<th style="padding:8px 12px;text-align:left;font-size:11px">Status</th>
						</tr></thead>
						<tbody>${job_rows}</tbody>
					</table>
				</div>
			</div>
		`);

		// Render charts using Frappe Charts
		if (trend_labels.length) {
			new frappe.Chart('#alum-output-chart', {
				data: { labels: trend_labels, datasets: [{ name: 'Output Kg', values: trend_outputs, chartType: 'bar' }] },
				type: 'axis-mixed', height: 200, colors: ['#17a2b8'],
				axisOptions: { xIsSeries: 1 }, tooltipOptions: {}
			});
			new frappe.Chart('#alum-yield-chart', {
				data: { labels: trend_labels, datasets: [{ name: 'Yield %', values: trend_yields }] },
				type: 'line', height: 200, colors: ['#28a745'],
				lineOptions: { regionFill: 1 },
				axisOptions: { xIsSeries: 1 }
			});
		}
	}

	// Auto-refresh every 60 seconds
	var refresh_interval = setInterval(load_dashboard, 60000);
	$(wrapper).on('remove', function() { clearInterval(refresh_interval); });
};
