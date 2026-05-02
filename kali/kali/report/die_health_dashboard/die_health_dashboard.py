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
		{"label": _("Die No"), "fieldname": "die_number", "fieldtype": "Link", "options": "Die Master", "width": 100},
		{"label": _("Die Name"), "fieldname": "die_name", "fieldtype": "Data", "width": 180},
		{"label": _("Alloy"), "fieldname": "alloy_grade", "fieldtype": "Data", "width": 70},
		{"label": _("Shots Used"), "fieldname": "total_shots_used", "fieldtype": "Int", "width": 100},
		{"label": _("Max Shots"), "fieldname": "max_shots_allowed", "fieldtype": "Int", "width": 100},
		{"label": _("Shot Life %"), "fieldname": "shot_life_bar", "fieldtype": "HTML", "width": 160},
		{"label": _("Last Maintenance"), "fieldname": "last_maintenance_date", "fieldtype": "Date", "width": 120},
		{"label": _("Nitriding Count"), "fieldname": "nitriding_count", "fieldtype": "Int", "width": 110},
		{"label": _("Maintenance Cost"), "fieldname": "total_maint_cost", "fieldtype": "Currency", "width": 130},
		{"label": _("Condition"), "fieldname": "condition_badge", "fieldtype": "HTML", "width": 120},
		{"label": _("Status"), "fieldname": "status_badge", "fieldtype": "HTML", "width": 110},
	]

def get_data(filters):
	rows = frappe.db.sql("""
		SELECT
			die_number, die_name, alloy_grade, total_shots_used,
			max_shots_allowed, die_status,
			last_maintenance_date
		FROM `tabDie Master`
		WHERE docstatus < 2
		ORDER BY die_number
	""", as_dict=1)

	maint_data = frappe.db.sql("""
		SELECT
			die,
			COUNT(CASE WHEN maintenance_type = 'Nitriding' THEN 1 END) as nitriding_count,
			SUM(cost) as total_cost
		FROM `tabDie Maintenance Log`
		WHERE docstatus < 2
		GROUP BY die
	""", as_dict=1)
	maint_map = {m.die: m for m in maint_data}

	condition_map = {
		"New": ("#17a2b8", "&#9679; New"),
		"Good": ("#28a745", "&#9679; Good"),
		"Worn": ("#ffc107", "&#9679; Worn"),
		"Needs Repair": ("#fd7e14", "&#9679; Repair"),
		"Condemned": ("#dc3545", "&#9679; Condemned"),
	}
	status_map = {
		"Active": ("#28a745", "Active"),
		"Under Maintenance": ("#ffc107", "Maint."),
		"Condemned": ("#dc3545", "Condemned"),
		"Retired": ("#6c757d", "Retired"),
	}

	for r in rows:
		m = maint_map.get(r.die_number, {})
		r.nitriding_count = m.get("nitriding_count") or 0
		r.total_maint_cost = m.get("total_cost") or 0

		shots = r.total_shots_used or 0
		max_shots = r.max_shots_allowed or 1
		pct = min(shots / max_shots * 100, 100)
		bar_color = "#28a745" if pct < 70 else ("#ffc107" if pct < 90 else "#dc3545")
		r.shot_life_bar = (
			f'<div style="background:#e9ecef;border-radius:4px;height:16px;width:140px;overflow:hidden">'
			f'<div style="width:{pct:.0f}%;background:{bar_color};height:100%;text-align:center;font-size:10px;color:#fff;line-height:16px">{pct:.0f}%</div>'
			f'</div>'
		)

		cond_color, cond_label = condition_map.get(r.die_status, ("#999", r.die_status or "-"))
		r.condition_badge = f'<span style="color:{cond_color};font-weight:600">{cond_label}</span>'

		stat_color, stat_label = status_map.get(r.die_status, ("#999", r.die_status or "-"))
		r.status_badge = f'<span style="background:{stat_color};color:#fff;padding:2px 8px;border-radius:10px;font-size:10px">{stat_label}</span>'
		r.indicator = "red" if r.die_status == "Condemned" else ("orange" if pct >= 90 else "green")
	return rows

def get_chart(data):
	if not data:
		return {}
	labels = [r.get("die_number", "") for r in data]
	shots = [r.get("total_shots_used") or 0 for r in data]
	max_shots = [r.get("max_shots_allowed") or 0 for r in data]
	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": "Shots Used", "values": shots, "chartType": "bar"},
				{"name": "Max Shots", "values": max_shots, "chartType": "line"},
			]
		},
		"type": "axis-mixed",
		"height": 280,
		"colors": ["#fd7e14", "#6c757d"],
		"axisOptions": {"xIsSeries": 1},
	}
