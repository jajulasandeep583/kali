import frappe

@frappe.whitelist()
def get_job_cards():
	return frappe.db.sql("""
		SELECT name, shift_date, shift, press, die_number, profile_item,
			net_output_kg, yield_percentage, status, operator_name
		FROM `tabExtrusion Job Card`
		WHERE docstatus < 2
		ORDER BY shift_date DESC
		LIMIT 100
	""", as_dict=1)
