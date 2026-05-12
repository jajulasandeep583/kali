import frappe
from datetime import date

@frappe.whitelist()
def get_sidebar_counts():
	today = date.today()
	def q(sql, *args):
		return frappe.db.sql(sql, args or ())[0][0] or 0

	return {
		"active_jobs":    q("SELECT COUNT(*) FROM `tabExtrusion Job Card` WHERE status NOT IN ('Completed','On Hold','Pending') AND docstatus<2"),
		"pending_qc":     q("SELECT COUNT(*) FROM `tabQuality Check` WHERE (overall_result IS NULL OR overall_result='') AND docstatus<2"),
		"delayed_orders": q("SELECT COUNT(*) FROM `tabSales Order` WHERE delivery_date<%s AND status NOT IN ('Completed','Cancelled') AND docstatus=1", today),
		"active_orders":  q("SELECT COUNT(*) FROM `tabSales Order` WHERE status NOT IN ('Completed','Cancelled') AND docstatus=1"),
	}
