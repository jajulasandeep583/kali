import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data

def get_columns():
    return [
        {"label": _("Sales Order"), "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 160},
        {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
        {"label": _("Profile Item"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 200},
        {"label": _("Ordered (Kg)"), "fieldname": "ordered_qty", "fieldtype": "Float", "width": 110},
        {"label": _("Produced (Kg)"), "fieldname": "produced_qty", "fieldtype": "Float", "width": 110},
        {"label": _("Dispatched (Kg)"), "fieldname": "dispatched_qty", "fieldtype": "Float", "width": 120},
        {"label": _("Pending (Kg)"), "fieldname": "pending_qty", "fieldtype": "Float", "width": 110},
        {"label": _("Delivery Date"), "fieldname": "delivery_date", "fieldtype": "Date", "width": 110},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]

def get_data(filters):
    conditions = "WHERE so.docstatus = 1"
    if filters.get("customer"):
        conditions += f" AND so.customer = '{filters['customer']}'"
    if filters.get("from_date"):
        conditions += f" AND so.transaction_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND so.transaction_date <= '{filters['to_date']}'"

    data = frappe.db.sql(f"""
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
            FROM `tabWork Order`
            WHERE docstatus = 1
            GROUP BY sales_order
        ) wo_sum ON wo_sum.sales_order = soi.parent
        LEFT JOIN (
            SELECT against_sales_order, SUM(dni.qty) as dispatched
            FROM `tabDelivery Note Item` dni
            JOIN `tabDelivery Note` dn ON dn.name = dni.parent
            WHERE dn.docstatus = 1
            GROUP BY against_sales_order
        ) dn_sum ON dn_sum.against_sales_order = soi.parent
        {conditions}
        ORDER BY soi.delivery_date ASC
    """, as_dict=1)
    return data
