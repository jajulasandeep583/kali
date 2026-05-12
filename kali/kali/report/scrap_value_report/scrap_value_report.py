import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "month", "label": _("Month"), "fieldtype": "Data", "width": 120},
        {"fieldname": "butt_end_kg", "label": _("Butt End Kg"), "fieldtype": "Float", "width": 120},
        {"fieldname": "front_cut_kg", "label": _("Front Cut Kg"), "fieldtype": "Float", "width": 120},
        {"fieldname": "discard_kg", "label": _("Discard Kg"), "fieldtype": "Float", "width": 110},
        {"fieldname": "qc_reject_kg", "label": _("QC Reject Kg"), "fieldtype": "Float", "width": 110},
        {"fieldname": "total_scrap_kg", "label": _("Total Scrap Kg"), "fieldtype": "Float", "width": 120},
        {"fieldname": "scrap_value", "label": _("Scrap Value Rs"), "fieldtype": "Currency", "width": 140},
        {"fieldname": "pct_of_production", "label": _("%% of Production"), "fieldtype": "Percent", "width": 130},
    ]

def get_data(filters):
    entries = frappe.db.get_all(
        "Stock Entry",
        filters={"stock_entry_type": "Manufacture", "docstatus": 1},
        fields=["name", "posting_date"],
    )
    
    monthly = {}
    for entry in entries:
        se = frappe.get_doc("Stock Entry", entry["name"])
        month_key = entry["posting_date"].strftime("%Y-%m") if entry["posting_date"] else "Unknown"
        
        if month_key not in monthly:
            monthly[month_key] = {
                "butt_end": 0, "front_cut": 0, "discard": 0,
                "qc_reject": 0, "total_input": 0
            }
        
        for item in se.items:
            if item.s_warehouse:
                monthly[month_key]["total_input"] += item.qty
            elif item.t_warehouse and not item.is_finished_item:
                if item.item_code == "SCRAP-BUTT":
                    monthly[month_key]["butt_end"] += item.qty
                elif item.item_code == "SCRAP-FRONT":
                    monthly[month_key]["front_cut"] += item.qty
                elif item.item_code == "SCRAP-DISC":
                    monthly[month_key]["discard"] += item.qty
                elif item.item_code == "SCRAP-REJ":
                    monthly[month_key]["qc_reject"] += item.qty
    
    data = []
    for month_key in sorted(monthly.keys(), reverse=True):
        m = monthly[month_key]
        total_scrap = m["butt_end"] + m["front_cut"] + m["discard"] + m["qc_reject"]
        scrap_value = (m["butt_end"] + m["front_cut"]) * 85 + (m["discard"] + m["qc_reject"]) * 75
        pct = (total_scrap / m["total_input"] * 100) if m["total_input"] > 0 else 0
        
        data.append({
            "month": month_key,
            "butt_end_kg": m["butt_end"],
            "front_cut_kg": m["front_cut"],
            "discard_kg": m["discard"],
            "qc_reject_kg": m["qc_reject"],
            "total_scrap_kg": total_scrap,
            "scrap_value": scrap_value,
            "pct_of_production": round(pct, 2),
        })
    
    return data
