import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters or {})
	chart = get_chart(data)
	return columns, data, None, chart

def get_columns():
	return [
		{"label": _("Die No"), "fieldname": "die_number", "fieldtype": "Link", "options": "Die Master", "width": 100},
		{"label": _("Profile"), "fieldname": "die_name", "fieldtype": "Data", "width": 180},
		{"label": _("Shots Used"), "fieldname": "total_shots_used", "fieldtype": "Int", "width": 100},
		{"label": _("Max Shots"), "fieldname": "max_shots_allowed", "fieldtype": "Int", "width": 100},
		{"label": _("Shot Life"), "fieldname": "shot_bar", "fieldtype": "HTML", "width": 160},
		{"label": _("% Used"), "fieldname": "pct_used", "fieldtype": "Float", "width": 80},
		{"label": _("Last Used"), "fieldname": "last_used_date", "fieldtype": "Date", "width": 100},
		{"label": _("Status"), "fieldname": "status_badge", "fieldtype": "HTML", "width": 130},
		{"label": _("Alert"), "fieldname": "alert_badge", "fieldtype": "HTML", "width": 170},
	]

def get_data(filters):
	rows = frappe.db.get_all("Die Master",
		fields=["die_number", "die_name", "die_shape", "total_shots_used",
				"max_shots_allowed", "last_used_date", "die_status", "alloy_grade"],
		order_by="die_number asc"
	)
	status_colors = {
		"Active": "#28a745", "Under Maintenance": "#ffc107",
		"Condemned": "#dc3545", "Retired": "#6c757d",
	}
	result = []
	for r in rows:
		total = r.total_shots_used or 0
		max_s = r.max_shots_allowed or 1
		pct = min(total / max_s * 100, 100) if max_s else 0
		bar_color = "#28a745" if pct < 70 else ("#ffc107" if pct < 90 else "#dc3545")
		shot_bar = (
			f'<div style="background:#e9ecef;border-radius:4px;height:16px;width:140px;overflow:hidden">'
			f'<div style="width:{pct:.0f}%;background:{bar_color};height:100%;text-align:center;font-size:10px;color:#fff;line-height:16px">{pct:.0f}%</div>'
			f'</div>'
		)
		sc = status_colors.get(r.die_status, "#6c757d")
		status_badge = f'<span style="background:{sc};color:#fff;padding:2px 8px;border-radius:10px;font-size:10px">{r.die_status or "-"}</span>'
		if pct >= 95:
			alert_badge = '<span style="background:#dc3545;color:#fff;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:700">&#9888; CRITICAL</span>'
		elif pct >= 80:
			alert_badge = '<span style="background:#fd7e14;color:#fff;padding:2px 10px;border-radius:10px;font-size:11px">&#9888; Plan Maint.</span>'
		elif r.die_status == "Under Maintenance":
			alert_badge = '<span style="background:#ffc107;color:#000;padding:2px 10px;border-radius:10px;font-size:11px">&#128296; In Maint.</span>'
		else:
			alert_badge = '<span style="background:#28a745;color:#fff;padding:2px 10px;border-radius:10px;font-size:11px">&#10003; OK</span>'
		result.append({
			"die_number": r.die_number,
			"die_name": r.die_name,
			"total_shots_used": total,
			"max_shots_allowed": r.max_shots_allowed,
			"shot_bar": shot_bar,
			"pct_used": round(pct, 1),
			"last_used_date": r.last_used_date,
			"status_badge": status_badge,
			"alert_badge": alert_badge,
			"indicator": "red" if pct >= 95 else ("orange" if pct >= 80 else "green"),
		})
	return result

def get_chart(data):
	if not data:
		return {}
	labels = [r.get("die_number", "") for r in data]
	shots = [r.get("total_shots_used") or 0 for r in data]
	return {
		"data": {
			"labels": labels,
			"datasets": [{"name": "Shots Used", "values": shots}]
		},
		"type": "bar",
		"height": 250,
		"colors": ["#fd7e14"],
		"axisOptions": {"xIsSeries": 1},
	}
