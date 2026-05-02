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
		{"label": _("Log No"), "fieldname": "name", "fieldtype": "Link", "options": "Aging Oven Log", "width": 130},
		{"label": _("Oven No"), "fieldname": "oven_no", "fieldtype": "Data", "width": 90},
		{"label": _("Job Card"), "fieldname": "job_card", "fieldtype": "Link", "options": "Extrusion Job Card", "width": 140},
		{"label": _("Temper"), "fieldname": "temper_target", "fieldtype": "Data", "width": 70},
		{"label": _("Set Temp (°C)"), "fieldname": "set_temp_c", "fieldtype": "Float", "width": 110},
		{"label": _("Soak Hrs"), "fieldname": "soak_hours", "fieldtype": "Float", "width": 90},
		{"label": _("Started"), "fieldname": "actual_start", "fieldtype": "Datetime", "width": 140},
		{"label": _("Ended"), "fieldname": "actual_end", "fieldtype": "Datetime", "width": 140},
		{"label": _("Hardness (HV)"), "fieldname": "final_hardness_hv", "fieldtype": "Float", "width": 110},
		{"label": _("Energy (kWh)"), "fieldname": "energy_kwh", "fieldtype": "Float", "width": 100},
		{"label": _("Result"), "fieldname": "result_badge", "fieldtype": "HTML", "width": 110},
	]

def get_data(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += f" AND DATE(actual_start) >= '{filters['from_date']}'"
	if filters.get("to_date"):
		conditions += f" AND DATE(actual_start) <= '{filters['to_date']}'"
	if filters.get("temper"):
		conditions += f" AND temper_target = '{filters['temper']}'"

	rows = frappe.db.sql(f"""
		SELECT
			name, oven_no, job_card, temper_target, set_temp_c, soak_hours,
			actual_start, actual_end, final_hardness_hv, energy_kwh, result
		FROM `tabAging Oven Log`
		WHERE docstatus < 2
		{conditions}
		ORDER BY actual_start DESC
		LIMIT 150
	""", as_dict=1)

	badge_map = {
		"Pass": ('<span style="background:#28a745;color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">&#10003; Pass</span>', "green"),
		"Fail": ('<span style="background:#dc3545;color:#fff;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">&#10007; Fail</span>', "red"),
		"Re-age": ('<span style="background:#ffc107;color:#000;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600">&#8635; Re-age</span>', "orange"),
	}
	for r in rows:
		badge, ind = badge_map.get(r.result, ('<span style="color:#999">-</span>', ""))
		r.result_badge = badge
		r.indicator = ind
	return rows

def get_chart(data):
	if not data:
		return {}
	pass_count = sum(1 for r in data if r.get("result") == "Pass")
	fail_count = sum(1 for r in data if r.get("result") == "Fail")
	reage_count = sum(1 for r in data if r.get("result") == "Re-age")
	return {
		"data": {
			"labels": ["Pass", "Fail", "Re-age"],
			"datasets": [{"name": "Count", "values": [pass_count, fail_count, reage_count]}]
		},
		"type": "donut",
		"height": 240,
		"colors": ["#28a745", "#dc3545", "#ffc107"],
	}
