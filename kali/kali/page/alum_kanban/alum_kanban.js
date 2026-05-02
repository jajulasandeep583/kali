frappe.pages['alum-kanban'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: '📋 Job Card Kanban Board',
		single_column: true
	});

	page.add_action_item('Refresh', () => load_kanban());

	$(wrapper).find('.layout-main-section').html(`
		<div id="kanban-root" style="padding:16px;overflow-x:auto">
			<div style="text-align:center;padding:40px;color:#888"><i class="fa fa-spinner fa-spin fa-2x"></i></div>
		</div>
	`);

	var STATUSES = [
		{ key: 'Pending', label: 'Pending', color: '#6c757d', bg: '#f8f9fa' },
		{ key: 'Billet Loaded', label: 'Billet Loaded', color: '#fd7e14', bg: '#fff3cd' },
		{ key: 'Heating', label: 'Heating', color: '#e83e8c', bg: '#fce4ec' },
		{ key: 'In Progress', label: 'Extruding', color: '#17a2b8', bg: '#e3f2fd' },
		{ key: 'Stretching', label: 'Stretching', color: '#6f42c1', bg: '#ede7f6' },
		{ key: 'Aging', label: 'Aging', color: '#795548', bg: '#efebe9' },
		{ key: 'QC Pending', label: 'QC Check', color: '#ff9800', bg: '#fff8e1' },
		{ key: 'Completed', label: 'Completed', color: '#28a745', bg: '#e8f5e9' },
		{ key: 'On Hold', label: 'On Hold', color: '#dc3545', bg: '#fdecea' },
	];

	load_kanban();

	function load_kanban() {
		frappe.call({ method: 'kali.kali.page.alum_kanban.alum_kanban.get_job_cards' }).then(r => {
			render_kanban(r.message || []);
		});
	}

	function render_kanban(jobs) {
		var by_status = {};
		STATUSES.forEach(s => { by_status[s.key] = []; });
		jobs.forEach(j => {
			var bucket = by_status[j.status] || by_status['Pending'];
			(by_status[j.status] || by_status['Pending']).push(j);
		});

		var cols = STATUSES.map(s => {
			var cards = (by_status[s.key] || []).map(j => {
				var yc = (j.yield_percentage||0) >= 80 ? '#28a745' : '#dc3545';
				return `
				<div style="background:#fff;border-radius:8px;padding:12px;margin-bottom:10px;box-shadow:0 1px 4px rgba(0,0,0,0.1);border-left:3px solid ${s.color};cursor:pointer" onclick="frappe.set_route('Form','Extrusion Job Card','${j.name}')">
					<div style="font-weight:700;font-size:12px;color:#333">${j.name}</div>
					<div style="font-size:11px;color:#666;margin:4px 0">${j.profile_item || 'No Profile'}</div>
					<div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px">
						<span style="font-size:10px;color:#888">${j.shift_date || ''} ${(j.shift||'')[0]||''}</span>
						<span style="background:${yc};color:#fff;padding:1px 6px;border-radius:8px;font-size:10px;font-weight:600">${(j.yield_percentage||0).toFixed(1)}%</span>
					</div>
					${j.press ? `<div style="font-size:10px;color:#aaa;margin-top:2px">${j.press} | ${j.die_number||''}</div>` : ''}
				</div>`;
			}).join('');

			return `
			<div style="min-width:190px;background:${s.bg};border-radius:10px;padding:12px;flex-shrink:0">
				<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
					<span style="font-weight:700;font-size:12px;color:${s.color}">${s.label}</span>
					<span style="background:${s.color};color:#fff;border-radius:50%;width:22px;height:22px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700">${(by_status[s.key]||[]).length}</span>
				</div>
				<div style="max-height:600px;overflow-y:auto">${cards || '<div style="color:#aaa;font-size:11px;text-align:center;padding:20px">Empty</div>'}</div>
			</div>`;
		}).join('');

		$('#kanban-root').html(`
			<div style="margin-bottom:12px;display:flex;justify-content:space-between">
				<span style="color:#888;font-size:12px">Showing ${jobs.length} job cards &bull; Drag-drop coming soon</span>
				<span style="font-size:11px;color:#aaa">Last updated: ${new Date().toLocaleTimeString()}</span>
			</div>
			<div style="display:flex;gap:12px;overflow-x:auto;padding-bottom:16px">${cols}</div>
		`);
	}
};
