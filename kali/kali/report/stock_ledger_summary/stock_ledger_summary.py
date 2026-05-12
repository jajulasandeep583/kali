import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "warehouse", "label": _("Warehouse"), "fieldtype": "Link", "options": "Warehouse", "width": 220},
        {"fieldname": "item_code", "label": _("Item Code"), "fieldtype": "Link", "options": "Item", "width": 180},
        {"fieldname": "item_name", "label": _("Item Name"), "fieldtype": "Data", "width": 220},
        {"fieldname": "item_group", "label": _("Item Group"), "fieldtype": "Data", "width": 130},
        {"fieldname": "actual_qty", "label": _("Stock Qty (Kg)"), "fieldtype": "Float", "width": 130},
        {"fieldname": "valuation_rate", "label": _("Rate Rs/Kg"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "stock_value", "label": _("Stock Value Rs"), "fieldtype": "Currency", "width": 140},
    ]

def get_data(filters):
    target_warehouses = [
        "Billet Store - A",
        "Finished Goods Warehouse - A",
        "Scrap Yard - A",
    ]
    
    data = []
    current_warehouse = None
    warehouse_total = 0
    
    for wh in target_warehouses:
        bins = frappe.db.get_all(
            "Bin",
            filters={"warehouse": wh, "actual_qty": [">", 0]},
            fields=["item_code", "actual_qty", "valuation_rate", "stock_value"],
            order_by="item_code"
        )
        
        if not bins:
            continue
        
        wh_total = 0
        for b in bins:
            item_name = frappe.db.get_value("Item", b["item_code"], "item_name") or ""
            item_group = frappe.db.get_value("Item", b["item_code"], "item_group") or ""
            val = b["actual_qty"] * (b["valuation_rate"] or 0)
            wh_total += val
            data.append({
                "warehouse": wh,
                "item_code": b["item_code"],
                "item_name": item_name,
                "item_group": item_group,
                "actual_qty": b["actual_qty"],
                "valuation_rate": b["valuation_rate"] or 0,
                "stock_value": val,
            })
        
        # Subtotal row per warehouse
        data.append({
            "warehouse": "<b>" + wh + " Total</b>",
            "item_code": "",
            "item_name": "",
            "item_group": "",
            "actual_qty": sum(b["actual_qty"] for b in bins),
            "valuation_rate": 0,
            "stock_value": wh_total,
            "bold": 1,
        })
    
    return data
