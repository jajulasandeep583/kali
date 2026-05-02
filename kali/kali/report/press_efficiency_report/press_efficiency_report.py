import frappe
from frappe import _

def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)
	return columns, data, None, chart

def get_columns():
	return [
		{"label": _("Job Card"), "fieldname": "name", "fieldtype": "Link", "options": "Extrusion Job Card", "width": 140},
		{"label": _("Date"), "fieldname": "shift_date", "fieldtype": "Date", "width": 100},
		{"label": _("Shift"), "fieldname": "shift", "fieldtype": "Data", "width": 80},
		{"label": _("Press"), "fieldname": "press", "fieldtype": "Data", "width": 120},
		{"label": _("Die No"), "fieldname": "die_number", "fieldtype": "Data", "width": 90},
		{"label": _("Profile"), "fieldname": "profile_item", "fieldtype": "Data", "width": 180},
		{"label": _("Billet (Kg)"), "fieldname": "billet_weight_used_kg", "fieldtype": "Float", "width": 100},
		{"label": _("Output (Kg)"), "fieldname": "net_output_kg", "fieldtype": "Float", "width": 100},
		{"label": _("Strokes"), "fieldname": "no_of_billets_used", "fieldtype": "Int", "width": 80},
		{"label": _("Yield %"), "fieldname": "yield_percentage", "fieldtype": "Float", "width": 90},
		{"label": _("Avg Ram Speed"), "fieldname": "ram_speed_mmpm", "fieldtype": "Float", "width": 110},
		{"label": _("Downtime (Hrs)"), "fieldname": "total_downtime_hours", "fieldtype": "Float", "width": 110},
		{"label": _("Status"), "fieldname": "status_badge", "fieldtype": "HTML", "width": 120},
	]

def get_data(filters):
	conditions = build_conditions(filters)
	rows = frappe.db.sql(f"""
		SELECT
			name,
			shift_date,
			shift,
			press,
			die_number,
			profile_item,
			billet_weight_used_kg,
			net_output_kg,
			no_of_billets_used,
			yield_percentage,
			ram_speed_mmpm,
			total_downtime_hours,
			status
		FROM `tabExtrusion Job Card`
		WHERE docstatus < 2
		{conditions}
		ORDER BY shift_date DESC, shift
		LIMIT 200
	""", as_dict=1)

	for r in rows:
		y = r.yield_percentage or 0
		if y >= 88:
			color, label = "#28a745", "Excellent"
		elif y >= 82:
			color, label = "#17a2b8", "Good"
		elif y >= 75:
			color, label = "#ffc107", "Average"
		else:
			color, label = "#dc3545", "Poor"
		r.status_badge = f'<span style="background:{color};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:600">{label} ({y:.1f}%)</span>'
		r.indicator = label.lower()

	return rows

def build_conditions(filters):
	c = ""
	if filters.get("from_date"):
		c += f" AND shift_date >= '{filters['from_date']}'"
	if filters.get("to_date"):
		c += f" AND shift_date <= '{filters['to_date']}'"
	if filters.get("press"):
		c += f" AND press = '{filters['press']}'"
	return c

def get_chart(data):
	if not data:
		return {}
	labels = [f"{r.get('shift_date','')}-{r.get('shift','')}" for r in data[:20]]
	yields = [r.get("yield_percentage") or 0 for r in data[:20]]
	outputs = [r.get("net_output_kg") or 0 for r in data[:20]]
	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": "Yield %", "values": yields, "chartType": "line"},
				{"name": "Output Kg", "values": outputs, "chartType": "bar"},
			]
		},
		"type": "axis-mixed",
		"height": 280,
		"colors": ["#28a745", "#17a2b8"],
		"axisOptions": {"xIsSeries": 1},
	}
