import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data

def get_columns():
    return [
        {"label": _("Die No"), "fieldname": "die_number", "fieldtype": "Link", "options": "Die Master", "width": 100},
        {"label": _("Profile"), "fieldname": "die_name", "fieldtype": "Data", "width": 200},
        {"label": _("Shape"), "fieldname": "die_shape", "fieldtype": "Data", "width": 120},
        {"label": _("Total Shots Used"), "fieldname": "total_shots_used", "fieldtype": "Int", "width": 120},
        {"label": _("Max Shots"), "fieldname": "max_shots_allowed", "fieldtype": "Int", "width": 100},
        {"label": _("Remaining Shots"), "fieldname": "remaining_shots", "fieldtype": "Int", "width": 120},
        {"label": _("% Used"), "fieldname": "pct_used", "fieldtype": "Percent", "width": 80},
        {"label": _("Last Used"), "fieldname": "last_used_date", "fieldtype": "Date", "width": 100},
        {"label": _("Status"), "fieldname": "die_status", "fieldtype": "Data", "width": 100},
        {"label": _("Alert"), "fieldname": "alert", "fieldtype": "Data", "width": 150},
    ]

def get_data(filters):
    data = frappe.db.get_all('Die Master',
        fields=['die_number', 'die_name', 'die_shape', 'total_shots_used',
                'max_shots_allowed', 'last_used_date', 'die_status', 'alloy_grade'],
        order_by='die_number asc'
    )
    result = []
    for row in data:
        total = row.total_shots_used or 0
        max_s = row.max_shots_allowed or 1
        remaining = max_s - total
        pct = round((total / max_s) * 100, 1) if max_s else 0
        alert = ''
        if pct >= 90:
            alert = '🔴 CRITICAL - Replace Soon'
        elif pct >= 75:
            alert = '🟡 WARNING - Plan Maintenance'
        elif row.die_status == 'Under Repair':
            alert = '🔧 Under Repair'
        else:
            alert = '🟢 OK'
        result.append({
            'die_number': row.die_number,
            'die_name': row.die_name,
            'die_shape': row.die_shape,
            'total_shots_used': total,
            'max_shots_allowed': max_s,
            'remaining_shots': remaining,
            'pct_used': pct,
            'last_used_date': row.last_used_date,
            'die_status': row.die_status,
            'alert': alert,
        })
    return result
