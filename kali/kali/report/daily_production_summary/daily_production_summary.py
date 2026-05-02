import frappe
from frappe import _

def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Date"), "fieldname": "shift_date", "fieldtype": "Date", "width": 100},
        {"label": _("Shift"), "fieldname": "shift", "fieldtype": "Data", "width": 80},
        {"label": _("Press"), "fieldname": "press", "fieldtype": "Data", "width": 150},
        {"label": _("Die No"), "fieldname": "die_number", "fieldtype": "Data", "width": 90},
        {"label": _("Profile"), "fieldname": "profile_item", "fieldtype": "Data", "width": 200},
        {"label": _("Billet Used (Kg)"), "fieldname": "billet_weight_used_kg", "fieldtype": "Float", "width": 120},
        {"label": _("Output (Kg)"), "fieldname": "net_output_kg", "fieldtype": "Float", "width": 100},
        {"label": _("Scrap (Kg)"), "fieldname": "total_scrap_kg", "fieldtype": "Float", "width": 100},
        {"label": _("Yield %"), "fieldname": "yield_percentage", "fieldtype": "Percent", "width": 80},
        {"label": _("Operator"), "fieldname": "operator_name", "fieldtype": "Data", "width": 120},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 120},
    ]

def get_data(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += f" AND shift_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND shift_date <= '{filters['to_date']}'"
    if filters.get("shift"):
        conditions += f" AND shift = '{filters['shift']}'"

    data = frappe.db.sql(f"""
        SELECT
            shift_date,
            shift,
            press,
            die_number,
            profile_item,
            billet_weight_used_kg,
            net_output_kg,
            (butt_end_scrap_kg + front_end_scrap_kg + other_scrap_kg) as total_scrap_kg,
            yield_percentage,
            operator_name,
            status
        FROM `tabExtrusion Job Card`
        WHERE docstatus < 2
        {conditions}
        ORDER BY shift_date DESC, shift
    """, as_dict=1)
    return data
