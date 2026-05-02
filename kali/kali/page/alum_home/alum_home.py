
import frappe
from frappe.utils import today, add_days, flt, get_first_day

@frappe.whitelist()
def get_home_data():
    d = {}

    def q(sql, *a):
        try:
            r = frappe.db.sql(sql, a, as_dict=True)
            return r
        except Exception:
            return []

    def cnt(dt, filters=None):
        try:
            return frappe.db.count(dt, filters or {})
        except Exception:
            return 0

    # KPIs
    r = q("SELECT COALESCE(SUM(actual_production_kg),0) v FROM `tabProduction Shift Report` WHERE shift_date=%s", today())
    d['today_kg'] = flt(r[0].v) if r else 0

    first = get_first_day(today())
    r = q("SELECT COALESCE(SUM(actual_production_kg),0) v FROM `tabProduction Shift Report` WHERE shift_date>=%s", first)
    d['month_kg'] = flt(r[0].v) if r else 0

    d['active_orders'] = cnt('Sales Order', [['status','in',['To Deliver and Bill','To Bill','To Deliver']]])

    r = q("SELECT COUNT(*) c FROM `tabSales Order` WHERE status IN ('To Deliver and Bill','To Deliver') AND delivery_date<%s AND docstatus=1", today())
    d['delayed_orders'] = int(r[0].c) if r else 0

    d['qc_pending'] = cnt('Quality Check', [['overall_result','in',['','None',None]]])

    r = q("SELECT COUNT(*) c FROM `tabDie Master` WHERE die_status!='Condemned' AND max_shots_allowed>0 AND (total_shots_used/max_shots_allowed)>=0.90")
    d['critical_dies'] = int(r[0].c) if r else 0

    # Revenue
    r = q("SELECT COALESCE(SUM(grand_total),0) v FROM `tabSales Invoice` WHERE docstatus=1 AND posting_date>=%s", first)
    d['monthly_revenue'] = flt(r[0].v) if r else 0

    # Press activity (top 2 presses by active jobs)
    presses = q("SELECT press, COUNT(*) c FROM `tabExtrusion Job Card` WHERE status NOT IN ('Completed','Rejected','Draft') AND press IS NOT NULL GROUP BY press ORDER BY c DESC LIMIT 2")
    d['press1_active'] = int(presses[0].c) if len(presses) > 0 else 0
    d['press2_active'] = int(presses[1].c) if len(presses) > 1 else 0
    d['press1_name']   = presses[0].press if len(presses) > 0 else 'Press 1'
    d['press2_name']   = presses[1].press if len(presses) > 1 else 'Press 2'

    # Flow counts by EJC status
    rows = q("SELECT status, COUNT(*) c FROM `tabExtrusion Job Card` GROUP BY status")
    flow = {r.status: int(r.c) for r in rows}
    flow['sales_orders'] = cnt('Sales Order', [['status','in',['To Deliver and Bill','To Bill','To Deliver','Draft']]])
    flow['die_active']   = cnt('Die Master',  [['die_status','in',['Active','In Press']]])
    try:
        flow['dispatch'] = cnt('Delivery Note', [['status','in',['Draft','To Bill']]])
    except Exception:
        flow['dispatch'] = 0
    d['flow'] = flow

    # Active jobs for table
    jobs = q("""
        SELECT name, status, press,
               COALESCE(yield_percentage,0)  yield_pct,
               COALESCE(net_output_kg,0)     output_kg,
               sales_order_ref               sales_order,
               shift_date
        FROM `tabExtrusion Job Card`
        WHERE status NOT IN ('Completed','Rejected')
        ORDER BY modified DESC LIMIT 10
    """)
    d['jobs'] = [dict(j) for j in jobs]

    # Dies for grid
    dies = q("""
        SELECT name, die_number, die_status,
               COALESCE(total_shots_used,0)   total_shots_used,
               COALESCE(max_shots_allowed,500) max_shots_allowed
        FROM `tabDie Master`
        WHERE die_status != 'Condemned'
        ORDER BY IF(max_shots_allowed>0, total_shots_used/max_shots_allowed, 0) DESC
        LIMIT 12
    """)
    d['dies'] = [dict(x) for x in dies]

    # 14-day trend
    start = add_days(today(), -13)
    rows = q("SELECT shift_date, SUM(actual_production_kg) kg FROM `tabProduction Shift Report` WHERE shift_date>=%s GROUP BY shift_date ORDER BY shift_date", start)
    d['trend'] = [{'date': str(r.shift_date), 'kg': flt(r.kg)} for r in rows]

    d['user'] = (frappe.session.user or 'User').split('@')[0]
    return d
