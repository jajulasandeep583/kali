import frappe, json

def _id():
    _id.n = getattr(_id, 'n', 0) + 1
    return str(_id.n)

def apply_workspace(name, title, label, icon, color, seq, parent,
                    shortcuts_def, links_def, content_def):
    exists = frappe.db.exists("Workspace", name)
    doc = frappe.get_doc("Workspace", name) if exists else frappe.new_doc("Workspace")
    doc.name = name; doc.title = title; doc.label = label
    doc.icon = icon; doc.indicator_color = color; doc.sequence_id = seq
    doc.parent_page = parent; doc.public = 1; doc.is_hidden = 0
    doc.module = "Kali"; doc.app = "kali"; doc.type = "Workspace"; doc.for_user = ""
    doc.shortcuts = []
    for s in shortcuts_def: doc.append("shortcuts", s)
    doc.links = []
    for lnkd in links_def: doc.append("links", lnkd)
    doc.content = json.dumps(content_def)
    doc.save(ignore_permissions=True)
    print("  saved: " + name)

def sc(label, typ, link_to=None, url=None, icon=None, color=None):
    d = {"label": label, "type": typ}
    if link_to: d["link_to"] = link_to
    if url:     d["url"] = url
    if icon:    d["icon"] = icon
    if color:   d["color"] = color
    return d

def cb(label, count=0):
    return {"type": "Card Break", "label": label, "link_count": count,
            "hidden": 0, "is_query_report": 0, "onboard": 0}

def lnk(label, lt, lo, ob=0):
    return {"type": "Link", "label": label, "link_type": lt, "link_to": lo,
            "hidden": 0, "is_query_report": 1 if lt == "Report" else 0,
            "onboard": ob, "link_count": 0}

def hdr(text, col=12):
    return {"id": "h" + _id(), "type": "header",
            "data": {"text": "<span class=\"h4\"><b>" + text + "</b></span>", "col": col}}

def crd(name, col=6):
    return {"id": "c" + _id(), "type": "card", "data": {"card_name": name, "col": col}}

def sct(name, col=4):
    return {"id": "s" + _id(), "type": "shortcut", "data": {"shortcut_name": name, "col": col}}

def sp(i=0):
    return {"id": "sp" + str(i), "type": "spacer", "data": {"col": 12}}


def update_all():
    _id.n = 0  # reset counter

    # 1. ALUMINIUM MANUFACTURING (parent hub)
    apply_workspace(
        "Aluminium Manufacturing", "Aluminium Manufacturing", "Aluminium Manufacturing",
        "manufacturing", "blue", 1.0, "",
        [sc("Plant Overview",        "URL", url="/app/plant-overview",        icon="factory",       color="blue"),
         sc("Sales and Orders",      "URL", url="/app/sales-and-orders",      icon="cart",          color="green"),
         sc("Production Planning",   "URL", url="/app/production-planning",   icon="calendar",      color="purple"),
         sc("Raw Materials",         "URL", url="/app/raw-materials",         icon="stock",         color="orange"),
         sc("Extrusion Production",  "URL", url="/app/extrusion-production",  icon="manufacturing", color="orange"),
         sc("Heat Treatment",        "URL", url="/app/heat-treatment",        icon="thermometer",   color="red"),
         sc("Die Management",        "URL", url="/app/die-management",        icon="settings",      color="grey"),
         sc("Quality Control",       "URL", url="/app/quality-control",       icon="check",         color="cyan"),
         sc("Reports and Analytics", "URL", url="/app/reports-and-analytics", icon="bar-chart",     color="blue"),
         sc("Masters and Setup",     "URL", url="/app/masters-and-setup",     icon="tools",         color="darkgrey")],
        [],
        [hdr("Aluminium Manufacturing"), sp(0),
         sct("Plant Overview", 3),        sct("Sales and Orders", 3),
         sct("Production Planning", 3),   sct("Raw Materials", 3),
         sct("Extrusion Production", 3),  sct("Heat Treatment", 3),
         sct("Die Management", 3),        sct("Quality Control", 3),
         sct("Reports and Analytics", 3), sct("Masters and Setup", 3)]
    )

    # 2. PLANT OVERVIEW
    apply_workspace(
        "Plant Overview", "Plant Overview", "Plant Overview",
        "factory", "blue", 1.0, "Aluminium Manufacturing",
        [sc("Plant Home Dashboard", "Page", link_to="alum-home",          icon="home",      color="blue"),
         sc("Production Dashboard",  "Page", link_to="alum-dashboard",     icon="bar-chart", color="green"),
         sc("Job Card Kanban",       "Page", link_to="alum-kanban",        icon="kanban",    color="orange"),
         sc("Die Room Dashboard",    "Page", link_to="die-room-dashboard", icon="settings",  color="grey")],
        [cb("Live Dashboards", 4),
         lnk("Plant Home Dashboard", "Page", "alum-home",          ob=1),
         lnk("Production Dashboard",  "Page", "alum-dashboard",     ob=1),
         lnk("Job Card Kanban",       "Page", "alum-kanban",        ob=1),
         lnk("Die Room Dashboard",    "Page", "die-room-dashboard", ob=1)],
        [hdr("Plant Overview"), sp(0),
         sct("Plant Home Dashboard", 3), sct("Production Dashboard", 3),
         sct("Job Card Kanban", 3),      sct("Die Room Dashboard", 3),
         sp(1), crd("Live Dashboards", 12)]
    )

    # 3. SALES AND ORDERS
    apply_workspace(
        "Sales and Orders", "Sales and Orders", "Sales and Orders",
        "cart", "green", 2.0, "Aluminium Manufacturing",
        [sc("Customer Requirement Sheet", "DocType", link_to="Customer Requirement Sheet", icon="file",      color="blue"),
         sc("Sales Order",                "DocType", link_to="Sales Order",                icon="cart",      color="green"),
         sc("Customer Order Status",      "Report",  link_to="Customer Order Status",      icon="bar-chart", color="orange")],
        [cb("Customers & Requirements", 3),
         lnk("Customer",                   "DocType", "Customer",                   ob=1),
         lnk("Customer Drawing",           "DocType", "Customer Drawing"),
         lnk("Customer Requirement Sheet", "DocType", "Customer Requirement Sheet", ob=1),
         cb("Sales Transactions", 4),
         lnk("Sales Order",   "DocType", "Sales Order",   ob=1),
         lnk("Delivery Note", "DocType", "Delivery Note"),
         lnk("Sales Invoice", "DocType", "Sales Invoice"),
         lnk("Payment Entry", "DocType", "Payment Entry"),
         cb("Order Reports", 2),
         lnk("Customer Order Status",     "Report", "Customer Order Status",     ob=1),
         lnk("Order to Dispatch Tracker", "Report", "Order to Dispatch Tracker")],
        [hdr("Sales and Orders"), sp(0),
         sct("Customer Requirement Sheet", 4), sct("Sales Order", 4), sct("Customer Order Status", 4),
         sp(1),
         crd("Customers & Requirements", 4), crd("Sales Transactions", 4), crd("Order Reports", 4)]
    )

    # 4. PRODUCTION PLANNING
    apply_workspace(
        "Production Planning", "Production Planning", "Production Planning",
        "calendar", "purple", 3.0, "Aluminium Manufacturing",
        [sc("Production Planning Sheet", "DocType", link_to="Production Planning Sheet", icon="list",         color="blue"),
         sc("Work Order",                "DocType", link_to="Work Order",                icon="manufacturing", color="green"),
         sc("BOM",                       "DocType", link_to="BOM",                       icon="tools",         color="orange")],
        [cb("Planning Documents", 2),
         lnk("Production Planning Sheet", "DocType", "Production Planning Sheet", ob=1),
         lnk("Work Order",                "DocType", "Work Order",                ob=1),
         cb("Setup & Reference", 3),
         lnk("BOM",         "DocType", "BOM"),
         lnk("Item",        "DocType", "Item"),
         lnk("Workstation", "DocType", "Workstation")],
        [hdr("Production Planning"), sp(0),
         sct("Production Planning Sheet", 4), sct("Work Order", 4), sct("BOM", 4),
         sp(1),
         crd("Planning Documents", 6), crd("Setup & Reference", 6)]
    )

    # 5. RAW MATERIALS
    apply_workspace(
        "Raw Materials", "Raw Materials", "Raw Materials",
        "stock", "orange", 4.0, "Aluminium Manufacturing",
        [sc("Billet Receipt",       "DocType", link_to="Billet Receipt",       icon="package",   color="blue"),
         sc("Purchase Order",       "DocType", link_to="Purchase Order",       icon="cart",      color="orange"),
         sc("Stock Ledger Summary", "Report",  link_to="Stock Ledger Summary", icon="bar-chart", color="green")],
        [cb("Raw Material Records", 4),
         lnk("Log Master",               "DocType", "Log Master",               ob=1),
         lnk("Billet Receipt",           "DocType", "Billet Receipt",           ob=1),
         lnk("Log to Billet Conversion", "DocType", "Log to Billet Conversion"),
         lnk("Billet Cutting Log",       "DocType", "Billet Cutting Log"),
         cb("Procurement", 4),
         lnk("Supplier",         "DocType", "Supplier"),
         lnk("Purchase Order",   "DocType", "Purchase Order",   ob=1),
         lnk("Purchase Receipt", "DocType", "Purchase Receipt"),
         lnk("Purchase Invoice", "DocType", "Purchase Invoice"),
         cb("Inventory Reports", 1),
         lnk("Stock Ledger Summary", "Report", "Stock Ledger Summary", ob=1)],
        [hdr("Raw Materials"), sp(0),
         sct("Billet Receipt", 4), sct("Purchase Order", 4), sct("Stock Ledger Summary", 4),
         sp(1),
         crd("Raw Material Records", 4), crd("Procurement", 4), crd("Inventory Reports", 4)]
    )

    # 6. EXTRUSION PRODUCTION
    apply_workspace(
        "Extrusion Production", "Extrusion Production", "Extrusion Production",
        "manufacturing", "orange", 5.0, "Aluminium Manufacturing",
        [sc("Extrusion Job Card",       "DocType", link_to="Extrusion Job Card",       icon="manufacturing", color="blue"),
         sc("Daily Production Summary", "Report",  link_to="Daily Production Summary", icon="bar-chart",    color="green"),
         sc("Press Log",                "DocType", link_to="Press Log",                icon="settings",      color="orange")],
        [cb("Production Records", 5),
         lnk("Extrusion Job Card",      "DocType", "Extrusion Job Card",      ob=1),
         lnk("Press Log",               "DocType", "Press Log"),
         lnk("Furnace Log",             "DocType", "Furnace Log"),
         lnk("Production Shift Report", "DocType", "Production Shift Report"),
         lnk("Scrap Record",            "DocType", "Scrap Record"),
         cb("Production Reports", 6),
         lnk("Daily Production Summary", "Report", "Daily Production Summary", ob=1),
         lnk("Press Efficiency Report",  "Report", "Press Efficiency Report"),
         lnk("Shift Summary Report",     "Report", "Shift Summary Report"),
         lnk("Input vs Output Analysis", "Report", "Input vs Output Analysis"),
         lnk("Scrap Analysis Report",    "Report", "Scrap Analysis Report"),
         lnk("Scrap Value Report",       "Report", "Scrap Value Report")],
        [hdr("Extrusion Production"), sp(0),
         sct("Extrusion Job Card", 4), sct("Daily Production Summary", 4), sct("Press Log", 4),
         sp(1),
         crd("Production Records", 6), crd("Production Reports", 6)]
    )

    # 7. HEAT TREATMENT
    apply_workspace(
        "Heat Treatment", "Heat Treatment", "Heat Treatment",
        "thermometer", "red", 6.0, "Aluminium Manufacturing",
        [sc("Aging Oven Log",          "DocType", link_to="Aging Oven Log",          icon="thermometer", color="red"),
         sc("Surface Treatment Order", "DocType", link_to="Surface Treatment Order", icon="settings",    color="blue"),
         sc("Aging Oven Tracker",      "Report",  link_to="Aging Oven Tracker",      icon="bar-chart",   color="orange")],
        [cb("Heat Treatment Records", 2),
         lnk("Aging Oven Log",          "DocType", "Aging Oven Log",          ob=1),
         lnk("Surface Treatment Order", "DocType", "Surface Treatment Order", ob=1),
         cb("Heat Treatment Reports", 1),
         lnk("Aging Oven Tracker", "Report", "Aging Oven Tracker", ob=1)],
        [hdr("Heat Treatment"), sp(0),
         sct("Aging Oven Log", 4), sct("Surface Treatment Order", 4), sct("Aging Oven Tracker", 4),
         sp(1),
         crd("Heat Treatment Records", 6), crd("Heat Treatment Reports", 6)]
    )

    # 8. DIE MANAGEMENT
    apply_workspace(
        "Die Management", "Die Management", "Die Management",
        "settings", "grey", 7.0, "Aluminium Manufacturing",
        [sc("Die Master",             "DocType", link_to="Die Master",             icon="tools",     color="grey"),
         sc("Die Maintenance Log",    "DocType", link_to="Die Maintenance Log",    icon="settings",  color="blue"),
         sc("Die Performance Report", "Report",  link_to="Die Performance Report", icon="bar-chart", color="orange")],
        [cb("Die Records", 2),
         lnk("Die Master",          "DocType", "Die Master",          ob=1),
         lnk("Die Maintenance Log", "DocType", "Die Maintenance Log", ob=1),
         cb("Die Reports", 2),
         lnk("Die Performance Report", "Report", "Die Performance Report", ob=1),
         lnk("Die Health Dashboard",   "Report", "Die Health Dashboard")],
        [hdr("Die Management"), sp(0),
         sct("Die Master", 4), sct("Die Maintenance Log", 4), sct("Die Performance Report", 4),
         sp(1),
         crd("Die Records", 6), crd("Die Reports", 6)]
    )

    # 9. QUALITY CONTROL
    apply_workspace(
        "Quality Control", "Quality Control", "Quality Control",
        "check", "cyan", 8.0, "Aluminium Manufacturing",
        [sc("Quality Check",    "DocType", link_to="Quality Check",    icon="check",   color="cyan"),
         sc("Customer Drawing", "DocType", link_to="Customer Drawing", icon="file",    color="blue"),
         sc("Scrap Record",     "DocType", link_to="Scrap Record",     icon="warning", color="red")],
        [cb("Quality Records", 2),
         lnk("Quality Check",    "DocType", "Quality Check",    ob=1),
         lnk("Customer Drawing", "DocType", "Customer Drawing", ob=1),
         cb("Rejection & Scrap", 1),
         lnk("Scrap Record", "DocType", "Scrap Record", ob=1)],
        [hdr("Quality Control"), sp(0),
         sct("Quality Check", 4), sct("Customer Drawing", 4), sct("Scrap Record", 4),
         sp(1),
         crd("Quality Records", 6), crd("Rejection & Scrap", 6)]
    )

    # 10. REPORTS AND ANALYTICS
    apply_workspace(
        "Reports and Analytics", "Reports and Analytics", "Reports and Analytics",
        "bar-chart", "blue", 9.0, "Aluminium Manufacturing",
        [sc("Daily Production Summary", "Report", link_to="Daily Production Summary", icon="bar-chart", color="blue"),
         sc("Customer Order Status",    "Report", link_to="Customer Order Status",    icon="cart",      color="green"),
         sc("Die Health Dashboard",     "Report", link_to="Die Health Dashboard",     icon="settings",  color="grey")],
        [cb("Production Reports", 4),
         lnk("Daily Production Summary", "Report", "Daily Production Summary", ob=1),
         lnk("Press Efficiency Report",  "Report", "Press Efficiency Report"),
         lnk("Shift Summary Report",     "Report", "Shift Summary Report"),
         lnk("Input vs Output Analysis", "Report", "Input vs Output Analysis"),
         cb("Die & Equipment Reports", 3),
         lnk("Die Performance Report", "Report", "Die Performance Report", ob=1),
         lnk("Die Health Dashboard",   "Report", "Die Health Dashboard"),
         lnk("Aging Oven Tracker",     "Report", "Aging Oven Tracker"),
         cb("Sales & Order Reports", 2),
         lnk("Customer Order Status",     "Report", "Customer Order Status",     ob=1),
         lnk("Order to Dispatch Tracker", "Report", "Order to Dispatch Tracker"),
         cb("Scrap & Inventory Reports", 3),
         lnk("Scrap Analysis Report", "Report", "Scrap Analysis Report"),
         lnk("Scrap Value Report",    "Report", "Scrap Value Report"),
         lnk("Stock Ledger Summary",  "Report", "Stock Ledger Summary")],
        [hdr("Reports and Analytics"), sp(0),
         sct("Daily Production Summary", 4), sct("Customer Order Status", 4), sct("Die Health Dashboard", 4),
         sp(1),
         crd("Production Reports", 4), crd("Die & Equipment Reports", 4), crd("Sales & Order Reports", 4),
         sp(2),
         crd("Scrap & Inventory Reports", 12)]
    )

    # 11. MASTERS AND SETUP
    apply_workspace(
        "Masters and Setup", "Masters and Setup", "Masters and Setup",
        "tools", "darkgrey", 10.0, "Aluminium Manufacturing",
        [sc("Item",     "DocType", link_to="Item",     icon="stock",  color="blue"),
         sc("Customer", "DocType", link_to="Customer", icon="user",   color="green"),
         sc("Supplier", "DocType", link_to="Supplier", icon="buying", color="orange")],
        [cb("Items & BOM", 3),
         lnk("Item",       "DocType", "Item",       ob=1),
         lnk("Item Group", "DocType", "Item Group"),
         lnk("BOM",        "DocType", "BOM"),
         cb("Facilities", 2),
         lnk("Warehouse",   "DocType", "Warehouse"),
         lnk("Workstation", "DocType", "Workstation"),
         cb("Parties", 2),
         lnk("Customer", "DocType", "Customer", ob=1),
         lnk("Supplier", "DocType", "Supplier"),
         cb("Company Settings", 2),
         lnk("Company",  "DocType", "Company"),
         lnk("Currency", "DocType", "Currency")],
        [hdr("Masters and Setup"), sp(0),
         sct("Item", 4), sct("Customer", 4), sct("Supplier", 4),
         sp(1),
         crd("Items & BOM", 3), crd("Facilities", 3), crd("Parties", 3), crd("Company Settings", 3)]
    )

    frappe.db.commit()
    print("All 11 workspaces updated and committed.")
