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

**Step 1:** Login → You'll see **Aluminium Manufacturing** workspace with **29 shortcuts in 7 sections**. Click **🏭 Plant Home Dashboard** first — it is the single-page overview of the entire plant.

**Step 2:** On the **Plant Home Dashboard** (`/app/alum-home`) you see live KPI cards, process flow pipeline, active job cards table, die shot-life grid, and 14-day production trend — all auto-refreshing every 60 seconds.

**Step 3:** Click **Production Dashboard** (`/app/alum-dashboard`) → Dedicated KPI cards showing today's output, active jobs, 30-day yield%, die alerts, month total.

**Step 4:** Click **Job Card Kanban** (`/app/alum-kanban`) → Color-coded cards across job status columns (Draft → Billet Loaded → Extrusion Running → Quenching → Stretching → Cutting → Aging → Surface Treatment → Quality Check → Completed).

**Step 5:** Click **Die Room Dashboard** (`/app/die-room-dashboard`) → Visual grid of all dies with shot-life progress bars. Red border = >90% critical.

**Step 6:** Click **Die Health Dashboard** (report) → Bar chart + color-coded table showing each die's shot consumption.

**Step 7:** Click **Shift Summary Report** → Heatmap-style daily table with Morning/Evening/Night efficiency badges.

---

## System Architecture

### Custom DocTypes (17 total)

#### Core Operational
| DocType | Purpose | Key Fields |
|---------|---------|------------|
| **Extrusion Job Card** | Heart of production — 90+ fields, 12 sections | die_number, billet_batch, yield_percentage (auto-calc), press, status, billet_weight_used_kg, net_output_kg, sales_order_ref |
| **Press Log** | Stroke-by-stroke monitoring | stroke_no, ram_pressure_tons, die_temp_c, profile_exit_temp_c, defect_observed |
| **Furnace Log** | Billet heating records | furnace_no, target_temp_c, actual_temp_achieved_c, fuel_consumed_units, temp_readings (child table) |
| **Aging Oven Log** | T5/T6/T66 aging cycles | temper_target, soak_hours, final_hardness_hv, result (Pass/Fail/Re-age) |
| **Production Shift Report** | Shift-level KPIs | shift_date, shift (Morning/Evening/Night), planned_production_kg, actual_production_kg, efficiency_percentage (auto-calc), safety_incidents |
| **Billet Cutting Log** | Billet saw operations | cut_length_mm, no_pieces_cut, butt_end_weight_kg, scrap_from_cutting_kg |

#### Masters
| DocType | Purpose | Key Fields |
|---------|---------|------------|
| **Die Master** | Die registry — shape, alloy, shot life | die_number, die_status (New/Active/Under Repair/Condemned/In Press), total_shots_used, max_shots_allowed |
| **Billet Receipt** | Incoming billet batches with COC details | — |
| **Customer Drawing** | Drawing register with approval workflow | — |
| **Die Maintenance Log** | Routine/Nitriding/Polishing/Repair/Condemned tracking | — |
| **Quality Check** | 24-field QC record with dimensional, surface, mechanical checks | overall_result (Approved/Rejected/Hold) |
| **Surface Treatment Order** | Anodizing/powder coat orders | status (Pending/In Process/Completed/Rejected) |
| **Scrap Record** | Butt end, front end, handling loss tracking | — |

#### Extrusion Job Card — Full Status Flow
```
Draft → Billet Loaded → Extrusion Running → Quenching → Stretching →
Cutting → Aging → Surface Treatment → Quality Check → Completed
                                                       ↘ Rejected / Quality Hold
```

---

## Live Dashboard Pages (4 total)

### 🏭 Plant Home Dashboard (`/app/alum-home`) ← NEW — START HERE
The **single-icon entry point** for the entire plant. Built with a dark neon theme.

**Header:** Gradient header (#1a1a2e → #16213e), live clock, date, user greeting.

**Alert Bar** (auto-hides if no alerts):
- 🔴 Red — Dies with shot life ≥ 90% (need replacement)
- 🟠 Orange — Sales Orders past delivery date
- 🔵 Blue — Quality Checks awaiting result

**Row 1 — KPI Cards (6 cards):**
| Card | What it shows |
|------|--------------|
| ⚡ Press 1 | RUNNING / IDLE + active job count |
| ⚡ Press 2 | RUNNING / IDLE + active job count |
| 📦 Today's Output | kg produced in today's shifts |
| 📋 Active Orders | Sales Orders in production pipeline |
| ⚠️ Delayed Orders | SOs past delivery date |
| 💰 Month Revenue | Sales Invoice total this month |

**Row 2 — 12-Stage Process Flow (clickable pipeline):**
```
📄 Orders → 🔩 Die Ready → 🟫 Billet Prep → ⚡ Pressing → 💧 Quenching →
🔧 Stretching → ✂️ Cutting → 🔥 Aging → 🎨 Surface Tx → 🔍 QC →
📦 Completed → 🚚 Dispatch
```
Each stage shows the live count of jobs at that stage. Green = normal, Orange = high volume. Click any stage → opens filtered list.

**Row 3 — Two Columns:**
- **Left:** Active Job Cards table — Job | Sales Order | Press | Stage | Output kg | Yield% bar
- **Right:** Die Shot-Life Grid — 12 dies with progress bars (red ≥90%, orange ≥75%, green <75%)

**14-Day Production Trend:** Chart.js line chart of daily production kg.

**Quick Action Buttons:**
`+ New Job Card` · `+ Sales Order` · `+ Quality Check` · `+ Shift Report` · `📊 Full Dashboard` · `📈 Reports`

**Footer Navigation (15 icons, 3 rows):**
- Row 1 — Operations: Job Cards, Press Log, Furnace Log, Aging Log, Shift Report
- Row 2 — Quality & Masters: QC Check, Surface Tx, Scrap, Die Master, Billet
- Row 3 — Sales & Reports: Sales Order, Purchase, Delivery, Prod Report, Order Tracker

**Auto-refreshes every 60 seconds.**

---

### Production Dashboard (`/app/alum-dashboard`)
- **5 KPI cards:** Today output, Active jobs, 30-day avg yield, Critical dies, Month output
- **Charts:** Daily output bar + Yield trend line (last 14 days)
- **Die Alerts table:** Dies >75% shot life with progress bars
- **Recent Jobs table:** Last 8 job cards with yield badges
- **Auto-refreshes every 60 seconds**

### Job Card Kanban (`/app/alum-kanban`)
- Status columns with color coding
- Each card shows: job no, profile, yield%, press, date/shift
- Click any card to open the full form

### Die Room Dashboard (`/app/die-room-dashboard`)
- Grid of all dies with shot-life progress bars
- Red border = >90% critical, yellow border = >75% warning
- Summary KPIs: Total, Active, In Maintenance, Critical, Condemned
- Click any die card to open Die Master form

---

## Workspace — Aluminium Manufacturing
**29 shortcuts in 7 sections** (accessible from the main Frappe sidebar):

| Section | Shortcuts |
|---------|-----------|
| **Dashboards** (4) | 🏭 Plant Home Dashboard, Production Dashboard, Job Card Kanban, Die Room Dashboard |
| **Daily Operations** (6) | Extrusion Job Card, Press Log, Furnace Log, Aging Oven Log, Billet Cutting Log, Production Shift Report |
| **Masters** (4) | Die Master, Billet Receipt, Customer Drawing, Die Maintenance Log |
| **Quality & Tracking** (3) | Quality Check, Surface Treatment Order, Scrap Record |
| **Analytics** (7) | Daily Production Summary, Press Efficiency Report, Shift Summary Report, Die Performance Report, Die Health Dashboard, Scrap Analysis Report, Aging Oven Tracker |
| **Orders & Customers** (2) | Customer Order Status, Order to Dispatch Tracker |
| **ERPNext** (3) | Customer, Item, Sales Order |

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
- **Yield auto-calc:** Enter billet_weight_used_kg + net_output_kg → yield_percentage and recovery_percentage fill automatically
- **Low yield alert:** If yield drops below 80%, orange flash-alert appears on screen
- **Die shot warning:** When die_number is entered, checks total_shots_used/max_shots_allowed — popup if >90%
- **Condemned die block:** Popup warning if selected die has die_status = Condemned
- **Billet batch → Alloy:** Selecting billet_batch auto-fills alloy_grade

### Die Master
- **Shot life headline alert:** Red banner if >95% used, yellow if >80%
- **Quick buttons:** "View Maintenance Logs" and "View Job Cards" added to toolbar

### Quality Check
- **Auto-overall result:** All check results auto-set overall_result (Approved/Rejected/Hold)

### Production Shift Report
- **Efficiency calc:** actual_production_kg ÷ planned_production_kg × 100 fills efficiency_percentage automatically
- **Yield calc:** Actual ÷ Billet × 100 fills shift_yield_percentage automatically
- **Safety incident:** Makes safety_details mandatory when safety_incidents is checked

---

## Live Data Snapshot (as of 2026-05-02)
| Metric | Value |
|--------|-------|
| Active Sales Orders | 16 |
| Active EJCs (not completed) | 7 |
| Dies active | 8 |
| Dies critical (≥90% shot life) | 2 (DIE-002 at 95%, DIE-009 at 90%) |
| Monthly Revenue (invoiced) | ₹32.1 lakhs |
| QC pending | 0 |

---

## Standard Operating Procedure

### Daily Start-Up
1. Login → Aluminium Manufacturing workspace
2. Click **🏭 Plant Home Dashboard** → scan alert bar for critical dies and delayed orders
3. Check the 12-stage process flow for any bottlenecks (high counts at one stage)
4. Open **Production Dashboard** → verify active jobs and die alerts
5. Open **Shift Summary Report** → confirm previous shift data is complete

### Creating a Job Card
1. Masters → **Die Master** → confirm die_status = Active and total_shots_used < max_shots_allowed
2. Masters → **Billet Receipt** → confirm batch has sufficient weight
3. Daily Ops → **Extrusion Job Card** → New
4. Fill: die_number, billet_batch, shift_date, shift, press, sales_order_ref
5. After extrusion: enter billet_weight_used_kg + net_output_kg → yield_percentage auto-calculates
6. If yield < 80%: alert fires → investigate before saving
7. Update status through the flow: Billet Loaded → Extrusion Running → Quenching → Stretching → Cutting → Aging → Surface Treatment → Quality Check → Completed

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
3. efficiency_percentage and shift_yield_percentage auto-calculate
4. Add Job Cards in the job_cards table, fill downtime, die changes, strokes
5. Check safety_incidents if any incident occurred (safety_details become mandatory)
6. Fill next_shift_handover for the incoming team

### Die Maintenance Workflow
1. Masters → **Die Maintenance Log** → New
2. Select die (from Die Master), set maintenance_type
3. Fill before_condition, after_condition
4. For nitriding: check nitriding_done, set nitriding_cycles
5. Enter cost → used for total maintenance cost tracking

### QC Sign-Off
1. Tracking → **Quality Check** → New
2. Link to job_card, fill dimensional/surface/mechanical/visual check results
3. overall_result auto-sets to Approved/Rejected/Hold
4. Enter inspector and sign off

---

## Dummy Data Summary (3 months: Feb–Apr 2025)

| Entity | Count |
|--------|-------|
| Customers | 10 |
| Dies | 10 (DIE-001 to DIE-010; DIE-005 condemned, DIE-002 & DIE-009 critical) |
| Billet Batches | 6 (BILLET-2025-001 to 006) |
| Extrusion Job Cards | 15 (EJC-2025-001 to 015) |
| Press Logs | 20 (for EJC-2025-001, strokes 1-20, defects on #8 & #14) |
| Furnace Logs | 5 |
| Aging Oven Logs | 3 (2 Pass, 1 Re-age) |
| Die Maintenance Logs | 8 (DIE-001: 2 nitriding + 1 polish; DIE-005: condemned) |
| Customer Drawings | 5 |
| Production Shift Reports | 90 (30 days × 3 shifts, Feb–Mar 2025) |
| Sales Orders (active) | 16 |

---

## GitHub Repository

- **Repo:** https://github.com/jajulasandeep583/kali.git
- **Branch:** main
- **Install:**
  ```bash
  bench get-app https://github.com/jajulasandeep583/kali.git
  bench --site <site> install-app kali
  bench --site <site> migrate
  ```

## Tech Stack
- ERPNext v16 + Frappe Framework v16
- Python 3.14 (pyenv) on Ubuntu (WSL2)
- MariaDB InnoDB, Redis, Gunicorn, Screen
- Frappe Charts (built-in), Chart.js v4 (CDN), Bootstrap 5

---

*Last updated: 2026-05-02 | kali app v3.0 — Plant Home Dashboard added*

## 🚀 Extrusion Job Card Enhancements

### ✅ Features Implemented
- Scrap Weight Auto Calculation
- Scrap Percentage
- Recovery Percentage
- Validation for incorrect production entries

### 📊 Business Logic
- Scrap Weight = Billet Weight - Net Output
- Scrap % = (Scrap / Billet) × 100
- Recovery % = (Output / Billet) × 100

### ⚠️ Validation
- System prevents saving if:
  - Net Output > Billet Weight

### 🧪 Example

| Billet | Output | Scrap | Recovery |
|--------|--------|-------|----------|
| 1000   | 850    | 150   | 85%      |

### 🛠 Setup

Run after pulling latest changes:

```bash
bench migrate
bench restart
```

### 📌 Usage Steps

1. Go to Extrusion Job Card
2. Enter:
   - Billet Weight
   - Net Output
3. System auto-calculates:
   - Scrap
   - Scrap %
   - Recovery %
4. Save the document

---

## Complete Process Flow

Log Receipt → Homogenizing → Log to Billet Cutting → Billet Loading → Extrusion Press → Quenching → Stretching → Cutting → Aging → Surface Treatment → QC → Packing → Dispatch

---

## Pre-Production Workflow

1. Customer places requirement
2. Create **Customer Requirement Sheet** — captures alloy, temper, surface finish, tonnage needed
3. Create **Production Planning Sheet** — system calculates billets and logs needed
4. Allocate logs from **Log Master** (linked to batch received from supplier)
5. Create **Log to Billet Conversion** record — captures saw cutting yield, butt-end loss
6. Billets are now ready for loading into the press

---

## Key Calculations



---

## Demo Script for Client Presentation

### Step 1 — Plant Home Dashboard
- Open http://kali.local:8000/app/alum-home
- Show live KPI cards: Today Output, Active Jobs, Yield %, Die Alerts
- Show process flow pipeline (clickable stages)
- Show active job cards table with live status
- Show die shot-life grid (red = critical dies)

### Step 2 — Walk Through One Complete Order

| Stage | DocType | Action |
|-------|---------|--------|
| 1 | Customer Requirement Sheet | Customer requests 5 tons of T5 profile |
| 2 | Production Planning Sheet | System calculates 280 billets, 45 logs needed |
| 3 | Log Master | Allocate LOG-2025-001 (6063, 6 inch, homogenized) |
| 4 | Log to Billet Conversion | Cut 480mm billets, yield 94.5% |
| 5 | Extrusion Job Card | Run press, capture billet weight, output, scrap |
| 6 | Quality Check | Hardness, dimensions, visual — Approved |
| 7 | Surface Treatment Order | Mill Finish / Anodizing / Powder Coat |
| 8 | Delivery Note | Dispatch to customer |
| 9 | Sales Invoice | Invoice raised and payment received |

### Step 3 — Show Reports

| Report | What to Highlight |
|--------|-------------------|
| Order to Dispatch Tracker | End-to-end order status in one view |
| Die Performance Report | Red badges on dies nearing shot limit |
| Daily Production Summary | Shift-wise tonnage and yield |
| Press Efficiency Report | OEE and downtime per press |
| Scrap Analysis Report | Scrap cost breakdown by category |

---

*Last updated: 2026-05-10 | kali app v4.0 — Log Master, Billet Conversion, Planning docs added*


---

## Complete Process Flow

Log Receipt → Homogenizing → Log to Billet Cutting → Billet Loading → Extrusion Press → Quenching → Stretching → Cutting → Aging → Surface Treatment → QC → Packing → Dispatch

---

## Pre-Production Workflow

1. Customer places requirement
2. Create **Customer Requirement Sheet** — captures alloy, temper, surface finish, tonnage needed
3. Create **Production Planning Sheet** — system calculates billets and logs needed
4. Allocate logs from **Log Master** (linked to batch received from supplier)
5. Create **Log to Billet Conversion** record — captures saw cutting yield, butt-end loss
6. Billets are now ready for loading into the press

---

## Key Calculations

```
Single billet weight (kg) = pi/4 x (diameter in m)^2 x length (m) x 2700

Billets needed = (tons required x 1000) / billet weight / 0.83

Logs needed = billets needed / (log length / billet cut length)

Cutting Yield % = Total Billet Output / (Logs Used x Single Log Weight) x 100

Extrusion Yield % = Net Profile Output / Billet Input x 100

Discard % = Discard Weight / Billet Input x 100
```

---

## Demo Script for Client Presentation

### Step 1 — Plant Home Dashboard
- Open http://kali.local:8000/app/alum-home
- Show live KPI cards: Today Output, Active Jobs, Yield %, Die Alerts
- Show process flow pipeline (clickable stages)
- Show active job cards table with live status
- Show die shot-life grid (red = critical dies)

### Step 2 — Walk Through One Complete Order

| Stage | DocType | Action |
|-------|---------|--------|
| 1 | Customer Requirement Sheet | Customer requests 5 tons of T5 profile |
| 2 | Production Planning Sheet | System calculates 280 billets, 45 logs needed |
| 3 | Log Master | Allocate LOG-2025-001 (6063, 6 inch, homogenized) |
| 4 | Log to Billet Conversion | Cut 480mm billets, yield 94.5% |
| 5 | Extrusion Job Card | Run press, capture billet weight, output, scrap |
| 6 | Quality Check | Hardness, dimensions, visual — Approved |
| 7 | Surface Treatment Order | Mill Finish / Anodizing / Powder Coat |
| 8 | Delivery Note | Dispatch to customer |
| 9 | Sales Invoice | Invoice raised and payment received |

### Step 3 — Show Reports

| Report | What to Highlight |
|--------|-------------------|
| Order to Dispatch Tracker | End-to-end order status in one view |
| Die Performance Report | Red badges on dies nearing shot limit |
| Daily Production Summary | Shift-wise tonnage and yield |
| Press Efficiency Report | OEE and downtime per press |
| Scrap Analysis Report | Scrap cost breakdown by category |

---

*Last updated: 2026-05-10 | kali app v4.0 — Log Master, Billet Conversion, Planning docs added*
