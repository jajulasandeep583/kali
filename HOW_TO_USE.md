# Aluminium Extrusion Manufacturing ERP — Complete Guide

## Site Details
| Field | Value |
|-------|-------|
| **URL** | http://kali.local:8000 |
| **Login** | Administrator |
| **Password** | admin |
| **ERPNext Version** | v16 |
| **Custom App** | kali (github.com/jajulasandeep583/kali) |

---

## Quick Start — Factory Demo Script (5 minutes)

**Step 1:** Login → You'll see **Aluminium Manufacturing** workspace with 28 shortcuts in 7 sections.

**Step 2:** Click **Production Dashboard** → Live KPI cards showing today's output, active jobs, 30-day yield%, die alerts, month total.

**Step 3:** Click **Job Card Kanban** → Color-coded cards across 9 status columns (Pending → Billet Loaded → Heating → Extruding → Stretching → Aging → QC → Completed → On Hold).

**Step 4:** Click **Die Room Dashboard** → Visual grid of all 10 dies with shot-life progress bars. Red border = critical.

**Step 5:** Click **Die Health Dashboard** (report) → Bar chart + color-coded table showing each die's shot consumption.

**Step 6:** Click **Shift Summary Report** → Heatmap-style daily table with Morning/Evening/Night efficiency badges.

---

## System Architecture

### Custom DocTypes (17 total)

#### Core Operational
| DocType | Purpose | Key Fields |
|---------|---------|------------|
| **Extrusion Job Card** | Heart of production — 90+ fields, 12 sections | die_number, billet_batch, yield_percentage (auto-calc), press parameters, quench/stretch/aging, downtime |
| **Press Log** | Stroke-by-stroke monitoring | stroke_no, ram_pressure_tons, die_temp_c, profile_exit_temp_c, defect_observed |
| **Furnace Log** | Billet heating records | furnace_no, target_temp_c, actual_temp_achieved_c, fuel_consumed_units, temp_readings (child table) |
| **Aging Oven Log** | T5/T6/T66 aging cycles | oven_no, temper_target, soak_hours, final_hardness_hv, result (Pass/Fail/Re-age) |
| **Production Shift Report** | Shift-level KPIs | shift_date, shift (Morning/Evening/Night), planned_production_kg, actual_production_kg, efficiency_% (auto-calc), safety_incidents |
| **Billet Cutting Log** | Billet saw operations | cut_length_mm, no_pieces_cut, butt_end_weight_kg, scrap_from_cutting_kg |

#### Masters
| DocType | Purpose |
|---------|---------|
| **Die Master** | 21 fields — die shape, alloy, shot count, condition, nitriding dates |
| **Billet Receipt** | Incoming billet batches with COC details |
| **Customer Drawing** | Drawing register with approval workflow |
| **Die Maintenance Log** | Routine/Nitriding/Polishing/Repair/Condemned tracking |
| **Quality Check** | 24-field QC record with dimensional, surface, mechanical checks |
| **Surface Treatment Order** | Anodizing/powder coat orders |
| **Scrap Record** | Butt end, front end, handling loss tracking |

---

## Live Dashboard Pages

### Production Dashboard (`/app/alum-dashboard`)
- **5 KPI cards:** Today output, Active jobs, 30-day avg yield, Critical dies, Month output
- **Charts:** Daily output bar + Yield trend line (last 14 days)
- **Die Alerts table:** Dies >75% shot life with progress bars
- **Recent Jobs table:** Last 8 job cards with yield badges
- **Auto-refreshes every 60 seconds**

### Job Card Kanban (`/app/alum-kanban`)
- 9 status columns with color coding
- Each card shows: job no, profile, yield%, press, date/shift
- Click any card to open the full form

### Die Room Dashboard (`/app/die-room-dashboard`)
- Grid of all dies with shot-life progress bars
- Red border = >90% critical, yellow border = >75% warning
- Summary KPIs: Total, Active, In Maintenance, Critical, Condemned
- Click any die card to open Die Master form

---

## Reports (9 total with charts + color coding)

| Report | Where to Find | Key Feature |
|--------|--------------|-------------|
| **Daily Production Summary** | Analytics section | Yield badges (green/blue/yellow/red), axis-mixed chart |
| **Press Efficiency Report** | Analytics | Excellent/Good/Average/Poor status badges, line+bar chart |
| **Shift Summary Report** | Analytics | Day-view heatmap with M/E/N efficiency, safety incident flag |
| **Die Performance Report** | Analytics | Shot-life progress bars, per-die bar chart |
| **Die Health Dashboard** | Analytics | Shot life vs max comparison, condition badges |
| **Scrap Analysis Report** | Analytics | Type badges, donut chart by scrap type |
| **Aging Oven Tracker** | Analytics | Pass/Fail/Re-age badges, donut chart |
| **Customer Order Status** | Analytics | Progress bars per order, overdue highlight red |
| **Order to Dispatch Tracker** | Analytics | Dispatch progress bar, overdue flag |

---

## Client Scripts (Auto-Calculations)

### Extrusion Job Card
- **Yield auto-calc:** Enter billet weight + net output → yield% and recovery% fill automatically
- **Low yield alert:** If yield drops below 80%, orange flash-alert appears on screen
- **Die shot warning:** When die_number is entered, checks shot life — popup if >90%
- **Condemned die block:** Popup warning if selected die is condemned
- **Billet batch → Alloy:** Selecting billet batch auto-fills alloy grade

### Die Master
- **Shot life headline alert:** Red banner if >95% used, yellow if >80%
- **Quick buttons:** "View Maintenance Logs" and "View Job Cards" added to toolbar

### Quality Check
- **Auto-overall result:** All 4 check results auto-set Overall Result (Pass/Fail/Conditional)

### Production Shift Report
- **Efficiency calc:** Actual ÷ Planned × 100 fills Efficiency% automatically
- **Yield calc:** Actual ÷ Billet × 100 fills Shift Yield% automatically
- **Safety incident:** Makes Safety Details mandatory when safety flag is checked

---

## Dummy Data Summary (3 months: Feb–Apr 2025)

| Entity | Count |
|--------|-------|
| Customers | 10 (7 new + 3 from Phase 1-8) |
| Dies | 10 (DIE-001 to DIE-010) |
| Billet Batches | 6 (BILLET-2025-001 to 006) |
| Extrusion Job Cards | 8 (EJC-2025-001 to 008) |
| Press Logs | 20 (for EJC-2025-001, strokes 1-20, defects on #8 & #14) |
| Furnace Logs | 5 |
| Aging Oven Logs | 3 (2 Pass, 1 Re-age) |
| Die Maintenance Logs | 8 (DIE-001: 2 nitriding + 1 polish; DIE-005: condemned) |
| Customer Drawings | 5 |
| Production Shift Reports | 90 (30 days × 3 shifts, Feb–Mar 2025) |

---

## Standard Operating Procedure

### Daily Start-Up
1. Login → Aluminium Manufacturing workspace
2. Open **Production Dashboard** → check die alert count and active jobs
3. Open **Shift Summary Report** → verify previous shift data is complete

### Creating a Job Card
1. Masters → **Die Master** → confirm die condition and shot count
2. Masters → **Billet Receipt** → confirm batch has sufficient weight
3. Daily Ops → **Extrusion Job Card** → New
4. Fill: die_number, billet_batch, shift_date, shift, press
5. After extrusion: enter billet_weight_used_kg + net_output_kg → yield auto-calculates
6. If yield < 80%: alert fires → investigate before saving

### Recording Press Strokes
1. Daily Ops → **Press Log** → New
2. Link to Job Card, set log_time and stroke_no
3. Fill ram_pressure_tons, ram_speed_mmps, container_temp_c, die_temp_c
4. If defect: check defect_observed → select defect_type → add notes

### Recording Furnace Cycle
1. Daily Ops → **Furnace Log** → New
2. Link to Job Card, set furnace_no, target_temp_c
3. Add zone temperature readings in the Temp Readings child table
4. Record actual_temp_achieved_c, heat_up_time_mins, soak_time_mins

### Recording Aging Cycle
1. Daily Ops → **Aging Oven Log** → New
2. Set temper_target (T5/T6/T66), set_temp_c, soak_hours
3. After cycle: enter final_hardness_hv, set result (Pass/Fail/Re-age)

### Closing a Shift
1. Daily Ops → **Production Shift Report** → New
2. Fill shift_date, shift, planned_production_kg, actual_production_kg
3. Efficiency% and Shift Yield% auto-calculate
4. Add Job Cards in the table, fill downtime, die changes, strokes
5. Check safety_incidents if any incident occurred (Safety Details become mandatory)
6. Next Shift Handover Notes → fill for the incoming team

### Die Maintenance Workflow
1. Masters → **Die Maintenance Log** → New
2. Select die (from Die Master), set maintenance_type
3. Fill before_condition, after_condition
4. For nitriding: check nitriding_done, set nitriding_cycles
5. Enter cost → used for total maintenance cost tracking

### QC Sign-Off
1. Tracking → **Quality Check** → New
2. Link to Job Card, fill dimensional/surface/mechanical/visual check results
3. Overall Result auto-sets to Pass/Fail/Conditional
4. Enter inspector_name and sign off

---

## GitHub Repository

- **Repo:** https://github.com/jajulasandeep583/kali.git
- **Branch:** main
- **Install:** `bench get-app https://github.com/jajulasandeep583/kali.git && bench --site <site> install-app kali`

## Tech Stack
- ERPNext v16 + Frappe Framework v16
- Python 3.14 (pyenv) on Ubuntu (WSL2)
- MariaDB InnoDB, Redis, Gunicorn
- Frappe Charts (built-in), Bootstrap 5 CSS

---

*Last updated: 2025-05-02 | kali app v2.0 — Phase A-H complete*
