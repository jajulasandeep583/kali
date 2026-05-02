import frappe

@frappe.whitelist()
def get_dies():
	dies = frappe.db.sql("""
		SELECT die_number, die_name, alloy_grade, die_shape, die_status,
			total_shots_used, max_shots_before_maintenance,
			die_condition, last_used_date, last_nitriding_date
		FROM `tabDie Master`
		WHERE docstatus < 2
		ORDER BY die_number
	""", as_dict=1)

	maint = frappe.db.sql("""
		SELECT die, COUNT(*) as maint_count, MAX(maintenance_date) as last_maint
		FROM `tabDie Maintenance Log`
		WHERE docstatus < 2
		GROUP BY die
	""", as_dict=1)
	maint_map = {m.die: m for m in maint}

	for d in dies:
		m = maint_map.get(d.die_number, {})
		d.maint_count = m.get("maint_count") or 0
		d.last_maint = m.get("last_maint")
		shots = d.total_shots_used or 0
		max_s = d.max_shots_before_maintenance or 1
		d.pct = round(min(shots / max_s * 100, 100), 1) if max_s else 0

	return dies
