import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data

def get_columns():
    return [
        {"label": _("Date"), "fieldname": "scrap_date", "fieldtype": "Date", "width": 100},
        {"label": _("Scrap No"), "fieldname": "scrap_no", "fieldtype": "Link", "options": "Scrap Record", "width": 120},
        {"label": _("Job Card"), "fieldname": "job_card", "fieldtype": "Link", "options": "Extrusion Job Card", "width": 150},
        {"label": _("Scrap Type"), "fieldname": "scrap_type", "fieldtype": "Data", "width": 120},
        {"label": _("Alloy"), "fieldname": "alloy_grade", "fieldtype": "Data", "width": 70},
        {"label": _("Weight (Kg)"), "fieldname": "weight_kg", "fieldtype": "Float", "width": 100},
        {"label": _("Recovery Value"), "fieldname": "recovery_amount", "fieldtype": "Currency", "width": 120},
        {"label": _("Disposed"), "fieldname": "disposed", "fieldtype": "Check", "width": 80},
    ]

def get_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += f" AND scrap_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND scrap_date <= '{filters['to_date']}'"
    if filters.get("scrap_type"):
        conditions += f" AND scrap_type = '{filters['scrap_type']}'"

    return frappe.db.sql(f"""
        SELECT
            scrap_date, scrap_no, job_card, scrap_type,
            alloy_grade, weight_kg, recovery_amount, disposed
        FROM `tabScrap Record`
        WHERE docstatus < 2
        {conditions}
        ORDER BY scrap_date DESC
    """, as_dict=1)
