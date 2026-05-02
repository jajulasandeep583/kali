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
		{"label": _("Date"), "fieldname": "shift_date", "fieldtype": "Date", "width": 100},
		{"label": _("Shift"), "fieldname": "shift", "fieldtype": "Data", "width": 80},
		{"label": _("Press"), "fieldname": "press", "fieldtype": "Data", "width": 130},
		{"label": _("Die No"), "fieldname": "die_number", "fieldtype": "Data", "width": 90},
		{"label": _("Profile"), "fieldname": "profile_item", "fieldtype": "Data", "width": 200},
		{"label": _("Billet (Kg)"), "fieldname": "billet_weight_used_kg", "fieldtype": "Float", "width": 100},
		{"label": _("Output (Kg)"), "fieldname": "net_output_kg", "fieldtype": "Float", "width": 100},
		{"label": _("Scrap (Kg)"), "fieldname": "total_scrap_kg", "fieldtype": "Float", "width": 100},
		{"label": _("Yield"), "fieldname": "yield_badge", "fieldtype": "HTML", "width": 130},
		{"label": _("Operator"), "fieldname": "operator_name", "fieldtype": "Data", "width": 120},
		{"label": _("Status"), "fieldname": "status_badge", "fieldtype": "HTML", "width": 110},
	]

def get_data(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += f" AND shift_date >= '{filters['from_date']}'"
	if filters.get("to_date"):
		conditions += f" AND shift_date <= '{filters['to_date']}'"
	if filters.get("shift"):
		conditions += f" AND shift = '{filters['shift']}'"

	rows = frappe.db.sql(f"""
		SELECT
			shift_date, shift, press, die_number, profile_item,
			billet_weight_used_kg, net_output_kg,
			(butt_end_scrap_kg + front_end_scrap_kg + other_scrap_kg) as total_scrap_kg,
			yield_percentage, operator_name, status
		FROM `tabExtrusion Job Card`
		WHERE docstatus < 2
		{conditions}
		ORDER BY shift_date DESC, shift
	""", as_dict=1)

	status_colors = {
		"Completed": "#28a745", "In Progress": "#17a2b8",
		"Pending": "#ffc107", "On Hold": "#6c757d",
	}
	for r in rows:
		y = r.yield_percentage or 0
		if y >= 88:
			yc = "#28a745"
		elif y >= 80:
			yc = "#17a2b8"
		elif y >= 70:
			yc = "#ffc107"
		else:
			yc = "#dc3545"
		warn = " &#9888;" if y < 80 else ""
		r.yield_badge = f'<span style="background:{yc};color:#fff;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">{y:.1f}%{warn}</span>'
		sc = status_colors.get(r.status, "#6c757d")
		r.status_badge = f'<span style="background:{sc};color:#fff;padding:2px 8px;border-radius:10px;font-size:10px">{r.status or "-"}</span>'
		r.indicator = "green" if y >= 80 else "red"
	return rows

def get_chart(data):
	if not data:
		return {}
	labels, outputs, yields = [], [], []
	for r in data[:20]:
		labels.append(f"{r.get('shift_date','')} {(r.get('shift') or '')[:3]}")
		outputs.append(r.get("net_output_kg") or 0)
		yields.append(r.get("yield_percentage") or 0)
	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": "Output (Kg)", "values": outputs, "chartType": "bar"},
				{"name": "Yield %", "values": yields, "chartType": "line"},
			]
		},
		"type": "axis-mixed",
		"height": 270,
		"colors": ["#17a2b8", "#28a745"],
		"axisOptions": {"xIsSeries": 1},
	}
