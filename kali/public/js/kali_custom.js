// Kali App — Custom JS for navigation badges and list view enhancements

frappe.ready(function() {
	// Load sidebar badges after page loads
	setTimeout(load_sidebar_badges, 2000);
});

frappe.router.on('change', function() {
	setTimeout(apply_list_row_colors, 500);
});

function load_sidebar_badges() {
	frappe.call({
		method: 'kali.kali.utils.get_sidebar_counts',
		callback: function(r) {
			if (!r.message) return;
			var counts = r.message;
			add_badge('Extrusion Job Card', counts.active_jobs, '#17a2b8');
			add_badge('Quality Check', counts.pending_qc, '#ffc107');
			add_badge('Order to Dispatch Tracker', counts.delayed_orders, '#dc3545');
			add_badge('Sales Order', counts.active_orders, '#28a745');
		}
	});
}

function add_badge(label, count, color) {
	if (!count || count <= 0) return;
	$('.standard-sidebar-item').each(function() {
		var text = $(this).text().trim();
		if (text.indexOf(label) >= 0 && $(this).find('.kali-badge').length === 0) {
			$(this).append(
				`<span class="kali-badge" style="background:${color};color:#fff;border-radius:10px;
					font-size:9px;font-weight:700;padding:1px 6px;margin-left:6px;
					display:inline-block;line-height:1.4">${count}</span>`
			);
		}
	});
}

function apply_list_row_colors() {
	var dt = frappe.get_route && frappe.get_route()[1];
	if (!dt) return;

	// Color list rows based on indicator field value
	var color_maps = {
		'Extrusion Job Card': {
			field: 'status',
			map: {
				'Completed':        '#28a745',
				'Extrusion Running':'#17a2b8',
				'In Progress':      '#17a2b8',
				'Billet Loaded':    '#fd7e14',
				'Heating':          '#e83e8c',
				'Stretching':       '#6f42c1',
				'Aging':            '#795548',
				'QC Pending':       '#ffc107',
				'Quality Hold':     '#dc3545',
				'On Hold':          '#dc3545',
				'Pending':          '#adb5bd',
			}
		},
		'Quality Check': {
			field: 'overall_result',
			map: {'Pass':'#28a745','Fail':'#dc3545','Hold':'#ffc107','Conditional':'#ffc107'}
		},
		'Die Master': {
			field: 'die_status',
			map: {'Active':'#28a745','Under Maintenance':'#ffc107','Condemned':'#dc3545','Retired':'#adb5bd'}
		}
	};

	if (!color_maps[dt]) return;
	var cfg = color_maps[dt];

	$('.list-row').each(function() {
		var val = $(this).attr('data-' + cfg.field) || $(this).find('[data-field="'+ cfg.field +'"]').text().trim();
		if (!val) {
			// Try reading from indicator span
			var ind = $(this).find('.indicator-pill').first().text().trim();
			val = ind;
		}
		var color = cfg.map[val];
		if (color) {
			$(this).css('border-left', '3px solid ' + color);
			$(this).css('border-radius', '0 4px 4px 0');
		}
	});
}

// Re-apply on list render
$(document).on('frappe.ui.listview:render', function() {
	setTimeout(apply_list_row_colors, 300);
});
