import frappe
from frappe import _
from datetime import date

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters or {})
	return columns, data

def get_columns():
	return [
		{"label": _("Sales Order"), "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 150},
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
		{"label": _("Item"), "fieldname": "item_code", "fieldtype": "Data", "width": 180},
		{"label": _("Ordered (Kg)"), "fieldname": "ordered_qty", "fieldtype": "Float", "width": 100},
		{"label": _("Produced"), "fieldname": "produced_qty", "fieldtype": "Float", "width": 100},
		{"label": _("Dispatched"), "fieldname": "dispatched_qty", "fieldtype": "Float", "width": 100},
		{"label": _("Pending"), "fieldname": "pending_qty", "fieldtype": "Float", "width": 100},
		{"label": _("Delivery Date"), "fieldname": "delivery_date", "fieldtype": "Date", "width": 110},
		{"label": _("Progress"), "fieldname": "progress_bar", "fieldtype": "HTML", "width": 160},
		{"label": _("Status"), "fieldname": "status_badge", "fieldtype": "HTML", "width": 130},
	]

def get_data(filters):
	conditions = "WHERE so.docstatus = 1"
	if filters.get("customer"):
		conditions += f" AND so.customer = '{filters['customer']}'"
	if filters.get("from_date"):
		conditions += f" AND so.transaction_date >= '{filters['from_date']}'"
	if filters.get("to_date"):
		conditions += f" AND so.transaction_date <= '{filters['to_date']}'"

	rows = frappe.db.sql(f"""
		SELECT
			soi.parent as sales_order,
			so.customer,
			soi.item_code,
			soi.qty as ordered_qty,
			COALESCE(wo_sum.produced, 0) as produced_qty,
			COALESCE(dn_sum.dispatched, 0) as dispatched_qty,
			soi.qty - COALESCE(dn_sum.dispatched, 0) as pending_qty,
			soi.delivery_date,
			so.status
		FROM `tabSales Order Item` soi
		JOIN `tabSales Order` so ON so.name = soi.parent
		LEFT JOIN (
			SELECT sales_order, SUM(produced_qty) as produced
			FROM `tabWork Order` WHERE docstatus = 1 GROUP BY sales_order
		) wo_sum ON wo_sum.sales_order = soi.parent
		LEFT JOIN (
			SELECT against_sales_order, SUM(dni.qty) as dispatched
			FROM `tabDelivery Note Item` dni
			JOIN `tabDelivery Note` dn ON dn.name = dni.parent
			WHERE dn.docstatus = 1 GROUP BY against_sales_order
		) dn_sum ON dn_sum.against_sales_order = soi.parent
		{conditions}
		ORDER BY soi.delivery_date ASC
	""", as_dict=1)

	today = date.today()
	status_colors = {
		"Completed": "#28a745", "To Deliver and Bill": "#17a2b8",
		"To Bill": "#6f42c1", "To Deliver": "#fd7e14",
		"On Hold": "#6c757d", "Cancelled": "#dc3545",
	}
	for r in rows:
		qty = r.ordered_qty or 0
		disp = r.dispatched_qty or 0
		pct = (disp / qty * 100) if qty else 0
		bar_color = "#28a745" if pct >= 100 else ("#17a2b8" if pct >= 50 else "#ffc107")
		r.progress_bar = (
			f'<div style="background:#e9ecef;border-radius:4px;height:16px;width:140px;overflow:hidden">'
			f'<div style="width:{min(pct,100):.0f}%;background:{bar_color};height:100%;text-align:center;font-size:10px;color:#fff;line-height:16px">{pct:.0f}%</div>'
			f'</div>'
		)
		sc = status_colors.get(r.status, "#6c757d")
		overdue = r.delivery_date and r.delivery_date < today and r.status not in ("Completed", "Cancelled")
		label = f'&#9888; {r.status}' if overdue else r.status or "-"
		bg = "#dc3545" if overdue else sc
		r.status_badge = f'<span style="background:{bg};color:#fff;padding:2px 8px;border-radius:10px;font-size:10px">{label}</span>'
		r.indicator = "red" if overdue else ("green" if r.status == "Completed" else "orange")
	return rows
