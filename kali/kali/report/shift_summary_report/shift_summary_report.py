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
		{"label": _("Morning (Kg)"), "fieldname": "morning_kg", "fieldtype": "Float", "width": 110},
		{"label": _("Morning Eff%"), "fieldname": "morning_eff", "fieldtype": "HTML", "width": 120},
		{"label": _("Evening (Kg)"), "fieldname": "evening_kg", "fieldtype": "Float", "width": 110},
		{"label": _("Evening Eff%"), "fieldname": "evening_eff", "fieldtype": "HTML", "width": 120},
		{"label": _("Night (Kg)"), "fieldname": "night_kg", "fieldtype": "Float", "width": 110},
		{"label": _("Night Eff%"), "fieldname": "night_eff", "fieldtype": "HTML", "width": 120},
		{"label": _("Day Total (Kg)"), "fieldname": "day_total_kg", "fieldtype": "Float", "width": 120},
		{"label": _("Day Yield %"), "fieldname": "day_yield_pct", "fieldtype": "HTML", "width": 120},
		{"label": _("Incidents"), "fieldname": "incidents", "fieldtype": "HTML", "width": 90},
	]

def _eff_badge(pct):
	if pct is None:
		return '<span style="color:#999">-</span>'
	if pct >= 90:
		bg = "#28a745"
	elif pct >= 75:
		bg = "#ffc107"
	else:
		bg = "#dc3545"
	return f'<span style="background:{bg};color:#fff;padding:1px 7px;border-radius:10px;font-size:11px">{pct:.1f}%</span>'

def get_data(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += f" AND shift_date >= '{filters['from_date']}'"
	if filters.get("to_date"):
		conditions += f" AND shift_date <= '{filters['to_date']}'"

	rows = frappe.db.sql(f"""
		SELECT
			shift_date,
			shift,
			actual_production_kg,
			planned_production_kg,
			shift_yield_percentage,
			safety_incidents
		FROM `tabProduction Shift Report`
		WHERE docstatus < 2
		{conditions}
		ORDER BY shift_date ASC
	""", as_dict=1)

	by_date = {}
	for r in rows:
		d = str(r.shift_date)
		if d not in by_date:
			by_date[d] = {}
		by_date[d][r.shift] = r

	result = []
	for d in sorted(by_date.keys(), reverse=True):
		s = by_date[d]
		mor = s.get("Morning", {})
		eve = s.get("Evening", {})
		nig = s.get("Night", {})
		day_kg = (mor.get("actual_production_kg") or 0) + (eve.get("actual_production_kg") or 0) + (nig.get("actual_production_kg") or 0)
		plan_kg = (mor.get("planned_production_kg") or 0) + (eve.get("planned_production_kg") or 0) + (nig.get("planned_production_kg") or 0)
		day_yield = (day_kg / plan_kg * 100) if plan_kg else None
		has_incident = any(x.get("safety_incidents") for x in [mor, eve, nig] if x)
		result.append({
			"shift_date": d,
			"morning_kg": mor.get("actual_production_kg"),
			"morning_eff": _eff_badge(mor.get("shift_yield_percentage")),
			"evening_kg": eve.get("actual_production_kg"),
			"evening_eff": _eff_badge(eve.get("shift_yield_percentage")),
			"night_kg": nig.get("actual_production_kg"),
			"night_eff": _eff_badge(nig.get("shift_yield_percentage")),
			"day_total_kg": day_kg,
			"day_yield_pct": _eff_badge(day_yield),
			"incidents": '<span style="color:#dc3545;font-weight:700">&#9888; Yes</span>' if has_incident else '<span style="color:#28a745">&#10003;</span>',
		})
	return result

def get_chart(data):
	if not data:
		return {}
	labels = [str(r.get("shift_date", "")) for r in data[:30]]
	totals = [r.get("day_total_kg") or 0 for r in data[:30]]
	return {
		"data": {
			"labels": labels,
			"datasets": [{"name": "Daily Output (Kg)", "values": totals}]
		},
		"type": "bar",
		"height": 260,
		"colors": ["#17a2b8"],
		"axisOptions": {"xIsSeries": 1},
	}
