frappe.pages['die-room-dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: '🔩 Die Room Dashboard',
		single_column: true
	});

	page.add_action_item('Refresh', () => load_page());

	$(wrapper).find('.layout-main-section').html(`
		<div id="die-room-root" style="padding:16px">
			<div style="text-align:center;padding:40px;color:#888"><i class="fa fa-spinner fa-spin fa-2x"></i></div>
		</div>
	`);

	load_page();

	function load_page() {
		frappe.call({ method: 'kali.kali.page.die_room_dashboard.die_room_dashboard.get_dies' }).then(r => {
			render(r.message || []);
		});
	}

	function render(dies) {
		var total = dies.length;
		var active = dies.filter(d => d.die_status === 'Active').length;
		var critical = dies.filter(d => d.pct >= 90 && d.die_status === 'Active').length;
		var maint = dies.filter(d => d.die_status === 'Under Maintenance').length;
		var condemned = dies.filter(d => d.die_status === 'Condemned').length;

		function summary_kpi(label, val, color) {
			return `<div style="background:#fff;border-radius:8px;padding:16px 20px;flex:1;text-align:center;box-shadow:0 2px 6px rgba(0,0,0,0.08);border-top:3px solid ${color}">
				<div style="font-size:28px;font-weight:700;color:${color}">${val}</div>
				<div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.5px;margin-top:4px">${label}</div>
			</div>`;
		}

		var cards = dies.map(d => {
			var pct = d.pct || 0;
			var bar_color = pct >= 90 ? '#dc3545' : pct >= 75 ? '#ffc107' : '#28a745';
			var status_colors = {
				'Active': '#28a745', 'Under Maintenance': '#ffc107',
				'Condemned': '#dc3545', 'Retired': '#6c757d'
			};
			var sc = status_colors[d.die_status] || '#6c757d';
			var cond_colors = { 'Active': '#28a745', 'Under Maintenance': '#ffc107', 'Condemned': '#dc3545', 'Retired': '#6c757d' };
			var cc = cond_colors[d.die_status] || '#6c757d';
			var border = pct >= 90 ? '2px solid #dc3545' : pct >= 75 ? '2px solid #ffc107' : '1px solid #e9ecef';
			return `
			<div style="background:#fff;border-radius:10px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,0.07);border:${border};cursor:pointer" onclick="frappe.set_route('Form','Die Master','${d.die_number}')">
				<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
					<div>
						<div style="font-weight:700;font-size:14px;color:#333">${d.die_number}</div>
						<div style="font-size:11px;color:#666;margin-top:2px">${d.die_name || ''}</div>
					</div>
					<span style="background:${sc};color:#fff;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600">${d.die_status}</span>
				</div>
				<div style="margin-bottom:8px">
					<div style="display:flex;justify-content:space-between;font-size:10px;color:#888;margin-bottom:3px">
						<span>Shot Life</span><span>${d.total_shots_used||0}/${d.max_shots_allowed||'?'}</span>
					</div>
					<div style="background:#e9ecef;border-radius:4px;height:8px;overflow:hidden">
						<div style="width:${pct}%;background:${bar_color};height:100%;transition:width 0.3s"></div>
					</div>
					<div style="text-align:right;font-size:10px;color:${bar_color};font-weight:600;margin-top:2px">${pct.toFixed(0)}%</div>
				</div>
				<div style="display:flex;justify-content:space-between;align-items:center">
					<span style="font-size:10px;color:#aaa">${d.alloy_grade||''} | ${d.die_shape||''}</span>
					<span style="background:${cc};color:#fff;padding:1px 6px;border-radius:8px;font-size:9px">${d.die_status||''}</span>
				</div>
				${pct >= 90 ? '<div style="background:#fdecea;color:#dc3545;font-size:10px;font-weight:700;text-align:center;padding:4px;border-radius:4px;margin-top:8px">⚠️ REPLACE SOON</div>' :
				  pct >= 75 ? '<div style="background:#fff3cd;color:#856404;font-size:10px;text-align:center;padding:4px;border-radius:4px;margin-top:8px">⚠ Plan Maintenance</div>' : ''}
			</div>`;
		}).join('');

		$('#die-room-root').html(`
			<div style="display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap">
				${summary_kpi('Total Dies', total, '#17a2b8')}
				${summary_kpi('Active', active, '#28a745')}
				${summary_kpi('In Maintenance', maint, '#ffc107')}
				${summary_kpi('Critical (>90%)', critical, '#dc3545')}
				${summary_kpi('Condemned', condemned, '#6c757d')}
			</div>
			<div style="margin-bottom:12px;display:flex;justify-content:space-between;align-items:center">
				<h6 style="margin:0;color:#555;font-weight:600">Die Inventory (${total} total)</h6>
				<span style="font-size:11px;color:#aaa">Last updated: ${new Date().toLocaleTimeString()}</span>
			</div>
			<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px">
				${cards || '<div style="color:#aaa;text-align:center;padding:40px">No dies found</div>'}
			</div>
		`);
	}
};
