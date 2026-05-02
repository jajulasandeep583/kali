import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters or {})
	chart = get_chart(data)
	return columns, data, None, chart

def get_columns():
	return [
		{"label": _("Date"), "fieldname": "scrap_date", "fieldtype": "Date", "width": 100},
		{"label": _("Scrap No"), "fieldname": "scrap_no", "fieldtype": "Link", "options": "Scrap Record", "width": 120},
		{"label": _("Job Card"), "fieldname": "job_card", "fieldtype": "Link", "options": "Extrusion Job Card", "width": 150},
		{"label": _("Scrap Type"), "fieldname": "scrap_type_badge", "fieldtype": "HTML", "width": 130},
		{"label": _("Alloy"), "fieldname": "alloy_grade", "fieldtype": "Data", "width": 70},
		{"label": _("Weight (Kg)"), "fieldname": "weight_kg", "fieldtype": "Float", "width": 100},
		{"label": _("Recovery Value"), "fieldname": "recovery_amount", "fieldtype": "Currency", "width": 120},
		{"label": _("Disposed"), "fieldname": "disposed_badge", "fieldtype": "HTML", "width": 90},
	]

def get_data(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += f" AND scrap_date >= '{filters['from_date']}'"
	if filters.get("to_date"):
		conditions += f" AND scrap_date <= '{filters['to_date']}'"

	rows = frappe.db.sql(f"""
		SELECT
			scrap_date, scrap_no, job_card, scrap_type,
			alloy_grade, weight_kg, recovery_amount, disposed
		FROM `tabScrap Record`
		WHERE docstatus < 2
		{conditions}
		ORDER BY scrap_date DESC
	""", as_dict=1)

	type_colors = {
		"Butt End": "#fd7e14", "Front End": "#6f42c1",
		"Handling Loss": "#dc3545", "Saw Cutting": "#17a2b8", "Other": "#6c757d",
	}
	for r in rows:
		tc = type_colors.get(r.scrap_type, "#6c757d")
		r.scrap_type_badge = f'<span style="background:{tc};color:#fff;padding:2px 8px;border-radius:10px;font-size:10px">{r.scrap_type or "-"}</span>'
		if r.disposed:
			r.disposed_badge = '<span style="color:#28a745;font-weight:700">&#10003; Yes</span>'
		else:
			r.disposed_badge = '<span style="color:#dc3545">&#10007; No</span>'
	return rows

def get_chart(data):
	if not data:
		return {}
	by_type = {}
	for r in data:
		t = r.get("scrap_type") or "Other"
		by_type[t] = by_type.get(t, 0) + (r.get("weight_kg") or 0)
	return {
		"data": {
			"labels": list(by_type.keys()),
			"datasets": [{"name": "Weight (Kg)", "values": list(by_type.values())}]
		},
		"type": "donut",
		"height": 240,
		"colors": ["#fd7e14", "#6f42c1", "#dc3545", "#17a2b8", "#6c757d"],
	}
