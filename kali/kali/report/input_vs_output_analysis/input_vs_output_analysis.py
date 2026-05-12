import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "job_card", "label": _("Job Card"), "fieldtype": "Data", "width": 140},
        {"fieldname": "date", "label": _("Date"), "fieldtype": "Date", "width": 100},
        {"fieldname": "stock_entry", "label": _("Stock Entry"), "fieldtype": "Link", "options": "Stock Entry", "width": 150},
        {"fieldname": "billet_input_kg", "label": _("Billet Input Kg"), "fieldtype": "Float", "width": 120},
        {"fieldname": "good_output_kg", "label": _("Good Output Kg"), "fieldtype": "Float", "width": 120},
        {"fieldname": "butt_end_kg", "label": _("Butt End Kg"), "fieldtype": "Float", "width": 110},
        {"fieldname": "front_cut_kg", "label": _("Front Cut Kg"), "fieldtype": "Float", "width": 110},
        {"fieldname": "discard_kg", "label": _("Discard Kg"), "fieldtype": "Float", "width": 110},
        {"fieldname": "qc_reject_kg", "label": _("QC Reject Kg"), "fieldtype": "Float", "width": 110},
        {"fieldname": "total_scrap_kg", "label": _("Total Scrap Kg"), "fieldtype": "Float", "width": 120},
        {"fieldname": "yield_pct", "label": _("Yield %"), "fieldtype": "Percent", "width": 90},
        {"fieldname": "scrap_pct", "label": _("Scrap %"), "fieldtype": "Percent", "width": 90},
        {"fieldname": "recovery_value", "label": _("Recovery Value Rs"), "fieldtype": "Currency", "width": 140},
    ]

def get_data(filters):
    entries = frappe.db.get_all(
        "Stock Entry",
        filters={"stock_entry_type": "Manufacture", "docstatus": 1},
        fields=["name", "posting_date", "remarks"],
        order_by="posting_date desc"
    )
    
    data = []
    for entry in entries:
        se = frappe.get_doc("Stock Entry", entry["name"])
        
        billet_input = 0
        good_output = 0
        butt_end = 0
        front_cut = 0
        discard = 0
        qc_reject = 0
        
        for item in se.items:
            if item.s_warehouse:
                billet_input += item.qty
            elif item.t_warehouse:
                if item.is_finished_item:
                    good_output += item.qty
                elif item.item_code == "SCRAP-BUTT":
                    butt_end += item.qty
                elif item.item_code == "SCRAP-FRONT":
                    front_cut += item.qty
                elif item.item_code == "SCRAP-DISC":
                    discard += item.qty
                elif item.item_code == "SCRAP-REJ":
                    qc_reject += item.qty
        
        total_scrap = butt_end + front_cut + discard + qc_reject
        yield_pct = (good_output / billet_input * 100) if billet_input > 0 else 0
        scrap_pct = (total_scrap / billet_input * 100) if billet_input > 0 else 0
        recovery_value = (butt_end + front_cut) * 85 + (discard + qc_reject) * 75
        
        row = {
            "job_card": entry.get("remarks", ""),
            "date": entry["posting_date"],
            "stock_entry": entry["name"],
            "billet_input_kg": billet_input,
            "good_output_kg": good_output,
            "butt_end_kg": butt_end,
            "front_cut_kg": front_cut,
            "discard_kg": discard,
            "qc_reject_kg": qc_reject,
            "total_scrap_kg": total_scrap,
            "yield_pct": round(yield_pct, 2),
            "scrap_pct": round(scrap_pct, 2),
            "recovery_value": recovery_value,
        }

        if yield_pct >= 85:
            row["indicator"] = "green"
        elif yield_pct >= 80:
            row["indicator"] = "orange"
        else:
            row["indicator"] = "red"
        
        data.append(row)
    
    return data
