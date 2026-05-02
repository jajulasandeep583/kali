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
		{"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
		{"label": _("SO No"), "fieldname": "name", "fieldtype": "Link", "options": "Sales Order", "width": 130},
		{"label": _("SO Date"), "fieldname": "transaction_date", "fieldtype": "Date", "width": 100},
		{"label": _("Delivery Date"), "fieldname": "delivery_date", "fieldtype": "Date", "width": 110},
		{"label": _("Item"), "fieldname": "item_code", "fieldtype": "Data", "width": 180},
		{"label": _("Qty (Kg)"), "fieldname": "qty", "fieldtype": "Float", "width": 90},
		{"label": _("Delivered"), "fieldname": "delivered_qty", "fieldtype": "Float", "width": 90},
		{"label": _("Pending"), "fieldname": "pending_qty", "fieldtype": "Float", "width": 90},
		{"label": _("Progress"), "fieldname": "progress_bar", "fieldtype": "HTML", "width": 160},
		{"label": _("Status"), "fieldname": "status_badge", "fieldtype": "HTML", "width": 110},
	]

def get_data(filters):
	conditions = "WHERE so.docstatus = 1"
	if filters.get("customer"):
		conditions += f" AND so.customer = '{filters['customer']}'"
	if filters.get("status"):
		conditions += f" AND so.status = '{filters['status']}'"

	rows = frappe.db.sql(f"""
		SELECT
			so.name,
			so.customer,
			so.transaction_date,
			so.delivery_date,
			so.status,
			soi.item_code,
			soi.qty,
			soi.delivered_qty
		FROM `tabSales Order` so
		INNER JOIN `tabSales Order Item` soi ON soi.parent = so.name
		{conditions}
		ORDER BY so.customer, so.transaction_date DESC
		LIMIT 300
	""", as_dict=1)

	status_map = {
		"Completed": ("#28a745", "&#10003; Done"),
		"To Deliver and Bill": ("#17a2b8", "In Progress"),
		"To Bill": ("#6f42c1", "Billing"),
		"To Deliver": ("#fd7e14", "To Deliver"),
		"On Hold": ("#6c757d", "On Hold"),
		"Cancelled": ("#dc3545", "Cancelled"),
	}
	for r in rows:
		qty = r.qty or 0
		delivered = r.delivered_qty or 0
		pending = max(0, qty - delivered)
		r.pending_qty = pending
		pct = (delivered / qty * 100) if qty else 0
		bar_color = "#28a745" if pct >= 100 else ("#17a2b8" if pct >= 50 else "#ffc107")
		r.progress_bar = (
			f'<div style="background:#e9ecef;border-radius:4px;height:16px;width:140px;overflow:hidden">'
			f'<div style="width:{min(pct,100):.0f}%;background:{bar_color};height:100%;text-align:center;font-size:10px;color:#fff;line-height:16px">{pct:.0f}%</div>'
			f'</div>'
		)
		color, label = status_map.get(r.status, ("#999", r.status or "-"))
		r.status_badge = f'<span style="background:{color};color:#fff;padding:2px 8px;border-radius:10px;font-size:10px">{label}</span>'
		r.indicator = "green" if r.status == "Completed" else "orange"
	return rows

def get_chart(data):
	if not data:
		return {}
	by_customer = {}
	for r in data:
		c = r.get("customer", "Unknown")
		by_customer.setdefault(c, 0)
		by_customer[c] += r.get("qty") or 0
	top = sorted(by_customer.items(), key=lambda x: -x[1])[:10]
	return {
		"data": {
			"labels": [x[0] for x in top],
			"datasets": [{"name": "Order Qty (Kg)", "values": [x[1] for x in top]}]
		},
		"type": "bar",
		"height": 260,
		"colors": ["#17a2b8"],
	}
