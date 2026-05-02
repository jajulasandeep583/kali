import frappe
from datetime import date, timedelta

@frappe.whitelist()
def get_kpis():
	today = date.today()
	week_start = today - timedelta(days=today.weekday())
	month_start = today.replace(day=1)
	thirty_ago = today - timedelta(days=30)

	def q(sql, *args):
		return frappe.db.sql(sql, args or None)[0][0] or 0

	today_output  = q("SELECT COALESCE(SUM(net_output_kg),0) FROM `tabExtrusion Job Card` WHERE shift_date=%s AND docstatus<2", today)
	week_output   = q("SELECT COALESCE(SUM(net_output_kg),0) FROM `tabExtrusion Job Card` WHERE shift_date>=%s AND docstatus<2", week_start)
	month_output  = q("SELECT COALESCE(SUM(net_output_kg),0) FROM `tabExtrusion Job Card` WHERE shift_date>=%s AND docstatus<2", month_start)
	avg_yield_30d = q("SELECT COALESCE(AVG(yield_percentage),0) FROM `tabExtrusion Job Card` WHERE shift_date>=%s AND docstatus<2 AND yield_percentage>0", thirty_ago)
	dies_critical = q("SELECT COUNT(*) FROM `tabDie Master` WHERE total_shots_used>=max_shots_allowed*0.9 AND die_status='Active' AND docstatus<2")

	active_orders = q("SELECT COUNT(*) FROM `tabSales Order` WHERE status NOT IN ('Completed','Cancelled') AND docstatus=1")
	in_production = q("SELECT COUNT(*) FROM `tabExtrusion Job Card` WHERE status NOT IN ('Completed','On Hold','Pending') AND docstatus<2")
	pending_qc    = q("SELECT COUNT(*) FROM `tabQuality Check` WHERE overall_result IS NULL OR overall_result='' AND docstatus<2")
	dispatched_td = q("SELECT COUNT(*) FROM `tabDelivery Note` WHERE posting_date=%s AND docstatus=1", today)
	delayed_ords  = q("SELECT COUNT(*) FROM `tabSales Order` WHERE delivery_date<%s AND status NOT IN ('Completed','Cancelled') AND docstatus=1", today)

	revenue = q("SELECT COALESCE(SUM(grand_total),0) FROM `tabSales Invoice` WHERE MONTH(posting_date)=MONTH(CURDATE()) AND YEAR(posting_date)=YEAR(CURDATE()) AND docstatus=1")

	return {
		"today_output": float(today_output),
		"week_output": float(week_output),
		"month_output": float(month_output),
		"avg_yield_30d": float(avg_yield_30d),
		"dies_critical": int(dies_critical),
		"active_orders": int(active_orders),
		"in_production": int(in_production),
		"pending_qc": int(pending_qc),
		"dispatched_today": int(dispatched_td),
		"delayed_orders": int(delayed_ords),
		"revenue_month": float(revenue),
	}

@frappe.whitelist()
def get_press_status():
	active = frappe.db.sql("""
		SELECT press, name, profile_item, net_output_kg, billet_weight_used_kg,
			yield_percentage, status, shift_date, operator_name
		FROM `tabExtrusion Job Card`
		WHERE status IN ('Extrusion Running','Billet Loaded','Heating','Stretching')
		AND docstatus < 2
		ORDER BY shift_date DESC
	""", as_dict=1)
	press_map = {}
	for r in active:
		if r.press and r.press not in press_map:
			press_map[r.press] = r

	all_presses = frappe.db.sql_list("SELECT DISTINCT press FROM `tabExtrusion Job Card` WHERE press IS NOT NULL AND press != '' LIMIT 10")
	result = []
	for p in sorted(all_presses):
		if p in press_map:
			r = press_map[p]
			result.append({"press": p, "running": True, "job_card": r.name,
				"profile": r.profile_item, "yield_pct": float(r.yield_percentage or 0),
				"output_kg": float(r.net_output_kg or 0), "status": r.status, "operator": r.operator_name})
		else:
			result.append({"press": p, "running": False, "job_card": None,
				"profile": None, "yield_pct": 0, "output_kg": 0, "status": "Idle", "operator": None})
	return result

@frappe.whitelist()
def get_pipeline():
	def q(sql):
		return frappe.db.sql(sql)[0][0] or 0
	return {
		"so":      q("SELECT COUNT(*) FROM `tabSales Order` WHERE status NOT IN ('Completed','Cancelled') AND docstatus=1"),
		"wo":      q("SELECT COUNT(*) FROM `tabWork Order` WHERE status NOT IN ('Completed','Cancelled','Stopped') AND docstatus=1"),
		"press":   q("SELECT COUNT(*) FROM `tabExtrusion Job Card` WHERE status NOT IN ('Completed','On Hold') AND docstatus<2"),
		"qc":      q("SELECT COUNT(*) FROM `tabQuality Check` WHERE overall_result NOT IN ('Pass','Fail') OR overall_result IS NULL AND docstatus<2"),
		"surface": q("SELECT COUNT(*) FROM `tabSurface Treatment Order` WHERE status='In Progress' AND docstatus<2"),
		"dispatch":q("SELECT COUNT(*) FROM `tabDelivery Note` WHERE status='Draft' AND docstatus=0"),
	}

@frappe.whitelist()
def get_shift_trend():
	rows = frappe.db.sql("""
		SELECT shift_date,
			SUM(actual_production_kg) as output_kg,
			AVG(shift_yield_percentage) as avg_yield
		FROM `tabProduction Shift Report`
		WHERE shift_date >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)
		AND docstatus < 2
		GROUP BY shift_date ORDER BY shift_date ASC
	""", as_dict=1)
	if not rows:
		rows = frappe.db.sql("""
			SELECT shift_date,
				SUM(net_output_kg) as output_kg,
				AVG(yield_percentage) as avg_yield
			FROM `tabExtrusion Job Card`
			WHERE shift_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
			AND docstatus < 2 GROUP BY shift_date ORDER BY shift_date ASC
		""", as_dict=1)
	for r in rows:
		r["label"] = str(r.shift_date)[5:] if r.shift_date else ""
	return rows

@frappe.whitelist()
def get_die_alerts():
	rows = frappe.db.sql("""
		SELECT die_number, die_name, total_shots_used, max_shots_allowed,
			ROUND(total_shots_used/NULLIF(max_shots_allowed,0)*100,1) as pct
		FROM `tabDie Master`
		WHERE total_shots_used >= max_shots_allowed*0.75
		AND die_status='Active' AND docstatus<2
		ORDER BY pct DESC LIMIT 8
	""", as_dict=1)
	for r in rows:
		r.pct = float(r.pct or 0)
	return rows

@frappe.whitelist()
def get_active_jobs():
	return frappe.db.sql("""
		SELECT name, shift_date, shift, press, profile_item,
			billet_weight_used_kg, net_output_kg,
			yield_percentage, status, operator_name
		FROM `tabExtrusion Job Card`
		WHERE docstatus < 2
		ORDER BY shift_date DESC LIMIT 10
	""", as_dict=1)

@frappe.whitelist()
def get_recent_activity():
	rows = []
	for dt, label_field, date_field, status_field in [
		("Extrusion Job Card", "name", "shift_date", "status"),
		("Quality Check", "name", "check_date", "overall_result"),
		("Delivery Note", "name", "posting_date", "status"),
		("Sales Order", "name", "transaction_date", "status"),
	]:
		try:
			items = frappe.db.sql(f"""
				SELECT name, {label_field} as label, {date_field} as event_date, {status_field} as event_status
				FROM `tab{dt}` WHERE docstatus<2 ORDER BY modified DESC LIMIT 3
			""", as_dict=1)
			for i in items:
				i["doctype"] = dt
				rows.append(i)
		except Exception:
			pass
	rows.sort(key=lambda x: str(x.get("modified","") or x.get("event_date","")), reverse=True)
	return rows[:10]
