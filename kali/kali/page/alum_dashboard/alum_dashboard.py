import frappe
from datetime import date, timedelta

@frappe.whitelist()
def get_kpis():
	today = date.today()
	month_start = today.replace(day=1)
	thirty_ago = today - timedelta(days=30)

	today_output = frappe.db.sql("""
		SELECT COALESCE(SUM(net_output_kg), 0) FROM `tabExtrusion Job Card`
		WHERE shift_date = %s AND docstatus < 2
	""", today)[0][0] or 0

	active_jobs = frappe.db.sql("""
		SELECT COUNT(*) FROM `tabExtrusion Job Card`
		WHERE status = 'In Progress' AND docstatus < 2
	""")[0][0] or 0

	avg_yield_30d = frappe.db.sql("""
		SELECT COALESCE(AVG(yield_percentage), 0) FROM `tabExtrusion Job Card`
		WHERE shift_date >= %s AND docstatus < 2 AND yield_percentage > 0
	""", thirty_ago)[0][0] or 0

	dies_critical = frappe.db.sql("""
		SELECT COUNT(*) FROM `tabDie Master`
		WHERE total_shots_used >= max_shots_before_maintenance * 0.9
		AND die_status = 'Active' AND docstatus < 2
	""")[0][0] or 0

	month_output = frappe.db.sql("""
		SELECT COALESCE(SUM(net_output_kg), 0) FROM `tabExtrusion Job Card`
		WHERE shift_date >= %s AND docstatus < 2
	""", month_start)[0][0] or 0

	return {
		"today_output": float(today_output),
		"active_jobs": int(active_jobs),
		"avg_yield_30d": float(avg_yield_30d),
		"dies_critical": int(dies_critical),
		"month_output": float(month_output),
	}

@frappe.whitelist()
def get_shift_trend():
	rows = frappe.db.sql("""
		SELECT
			shift_date,
			SUM(actual_production_kg) as output_kg,
			AVG(shift_yield_percentage) as avg_yield
		FROM `tabProduction Shift Report`
		WHERE shift_date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)
		AND docstatus < 2
		GROUP BY shift_date
		ORDER BY shift_date ASC
	""", as_dict=1)
	for r in rows:
		r["label"] = str(r.shift_date)[-5:] if r.shift_date else ""
	return rows

@frappe.whitelist()
def get_die_alerts():
	rows = frappe.db.sql("""
		SELECT
			die_number, die_name,
			total_shots_used,
			max_shots_before_maintenance,
			ROUND(total_shots_used / NULLIF(max_shots_before_maintenance, 0) * 100, 1) as pct
		FROM `tabDie Master`
		WHERE total_shots_used >= max_shots_before_maintenance * 0.75
		AND die_status = 'Active' AND docstatus < 2
		ORDER BY pct DESC
		LIMIT 8
	""", as_dict=1)
	for r in rows:
		r.pct = float(r.pct or 0)
	return rows

@frappe.whitelist()
def get_active_jobs():
	return frappe.db.sql("""
		SELECT name, shift_date, profile_item, yield_percentage, status
		FROM `tabExtrusion Job Card`
		WHERE docstatus < 2
		ORDER BY shift_date DESC
		LIMIT 8
	""", as_dict=1)
