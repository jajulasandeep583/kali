# Aluminium Extrusion Manufacturing ERP — Complete Guide & SOP

> **Built on:** ERPNext v16 + Frappe v16 | **Custom App:** kali | **Last updated:** 2026-05-12

---

## Site Access

| Item | Value |
|------|-------|
| URL | http://kali.local:8000 |
| Username | Administrator |
| Password | admin |
| GitHub | https://github.com/jajulasandeep583/kali.git |

---

## What Is This System?

This ERP tracks the **complete aluminium extrusion manufacturing cycle** — from the moment a customer places an order to when finished profiles are dispatched. Every operation is recorded: billet temperatures, press pressures, die shot counts, QC results, scrap weights, shift reports.

**A new person opening this system should follow the workspace top to bottom — the sections are in the exact order of operations.**

---

## First Time Login — What You See

1. Open `http://kali.local:8000`
2. Login with `Administrator / admin`
3. The left sidebar shows **Aluminium Manufacturing** workspace — click it
4. You will see 11 sections, arranged in production sequence:

```
🏠 Live Dashboards          ← Start here every morning
📋 Step 1: Sales & Orders
📅 Step 2: Production Planning
📦 Step 3: Incoming Materials
✂️  Step 4: Billet Preparation
⚡ Step 5: Extrusion
🔥 Step 6: Heat Treatment & Finishing
✅ Step 7: Quality Control
📝 Step 8: Shift Operations
🔧 Masters & Setup          ← One-time setup items
📈 Reports & Analytics      ← View all reports here
```

---

## Workspace — All 11 Sections

### 🏠 Live Dashboards
Quick-access pages. Open these first thing every morning.

| Link | Purpose |
|------|---------|
| Plant Home Dashboard | Single-screen plant overview — KPIs, process pipeline, job cards, die health |
| Production Dashboard | Daily output charts, yield trend, die alerts |
| Job Card Kanban | Visual board — all jobs by status column |
| Die Room Dashboard | Grid of all dies with shot-life progress bars |

### 📋 Step 1: Sales & Customer Orders
Start here when a new customer order arrives.

| DocType | Purpose |
|---------|---------|
| Customer | Customer master record |
| Sales Order | ERPNext sales order — links to all production |
| Customer Requirement Sheet | Captures exact production requirements from customer |
| Customer Drawing | Profile drawing register with approval tracking |

### 📅 Step 2: Production Planning
Plan how to fulfil the order.

| DocType | Purpose |
|---------|---------|
| Production Planning Sheet | Calculates billets and logs needed, links order to press schedule |

### 📦 Step 3: Incoming Materials
Manage raw material stock.

| DocType | Purpose |
|---------|---------|
| Billet Receipt | Record billet batches received from supplier |
| Log Master | Track aluminium log inventory by batch |
| Log to Billet Conversion | Record billet cutting from logs — captures yield |

### ✂️ Step 4: Billet Preparation
Prepare billets for pressing.

| DocType | Purpose |
|---------|---------|
| Billet Cutting Log | Saw cutting records per shift |
| Furnace Log | Billet heating — temperatures, soak times, fuel |

### ⚡ Step 5: Extrusion
Core production — the press run.

| DocType | Purpose |
|---------|---------|
| Extrusion Job Card | Main production record — die, billet, output, yield (90+ fields) |
| Press Log | Per-stroke press data — pressure, speed, temperature, defects |

### 🔥 Step 6: Heat Treatment & Finishing
Post-extrusion processing.

| DocType | Purpose |
|---------|---------|
| Aging Oven Log | T5/T6/T66 aging cycle records |
| Surface Treatment Order | Anodizing / powder coating / polishing orders |

### ✅ Step 7: Quality Control
Inspection and scrap.

| DocType | Purpose |
|---------|---------|
| Quality Check | 24-field QC inspection — dimensional, surface, hardness |
| Scrap Record | Track all scrap by type — butt end, front cut, rejection |

### 📝 Step 8: Shift Operations
End-of-shift records and die upkeep.

| DocType | Purpose |
|---------|---------|
| Production Shift Report | Shift-level KPIs — efficiency auto-calculated |
| Die Maintenance Log | Routine cleaning, nitriding, repair, condemned tracking |

### 🔧 Masters & Setup
One-time setup items. Create these before starting production.

| DocType | Purpose |
|---------|---------|
| Item | Product/profile item master (ERPNext) |
| Die Master | Die registry — shape, alloy compatibility, shot life limit |

### 📈 Reports & Analytics
All 9 custom reports with charts. See the Reports section below for details.

---

## Complete Production SOP — Step by Step

### Before You Start — One-Time Setup

These must be set up before production begins:

**1. Create Customer**
- Path: Step 1 → Customer → New
- Fill: customer_name, customer_group, customer_type, address, contact

**2. Create Items / Profiles**
- Path: Masters → Item → New
- Fill: item_code, item_name, item_group = Products, stock_uom = Kg

**3. Create Dies**
- Path: Masters → Die Master → New
- Fill: die_number, die_description, alloy_grade, max_shots_allowed (typically 5000–8000 based on alloy), die_status = New

**4. Add Log Inventory**
- Path: Step 3 → Log Master → New
- Fill: log_batch, log_diameter_inch, alloy_grade, total_weight_kg, status = Available

---

### STEP 1 — Sales & Customer Orders

**When:** A customer places an order.

#### 1A. Create Sales Order (ERPNext)
- Path: Step 1 → Sales Order → New
- Fill: customer, delivery_date, items (profile, qty, rate)
- Submit the Sales Order

#### 1B. Create Customer Requirement Sheet
- Path: Step 1 → Customer Requirement Sheet → New

| Field | What to Enter |
|-------|--------------|
| req_date | Today's date |
| customer | Select customer |
| sales_order | Link the Sales Order above |
| profile_weight_required_tons | How many tons needed |
| die_required | Which die to use |
| profile_length_mm | Required profile length |
| alloy_grade | 6063 / 6061 / 6082 / 6005 |
| temper_required | T5 / T6 / T66 |
| surface_finish | Mill Finish / Anodizing / Powder Coating |
| press_size_required | 6 inch / 7 inch / 8 inch |
| special_requirements | Any notes |
| status | Received |

- Save.

#### 1C. Add Customer Drawing (if applicable)
- Path: Step 1 → Customer Drawing → New
- Upload drawing file, link to customer and sales order
- Set status = Approved once drawing is confirmed

---

### STEP 2 — Production Planning

**When:** You know the order requirements and have selected a die.

#### 2A. Create Production Planning Sheet
- Path: Step 2 → Production Planning Sheet → New

| Field | What to Enter |
|-------|--------------|
| plan_date | Today |
| customer_req | Link to Customer Requirement Sheet |
| sales_order | Link Sales Order |
| die | Select die from Die Master |
| press | Select press workstation |
| alloy_grade | Must match requirement |
| profile_tons_planned | Tons to produce |
| log_batch | Select log batch from Log Master |
| billet_cut_length_mm | Required billet length (typically 480–520mm) |
| planned_date | Target production date |
| status | Approved |

**Auto-calculated fields:**
- single_billet_weight_kg — calculated from diameter + length
- billets_needed — tons required ÷ billet weight ÷ 0.83
- logs_needed — billets needed ÷ (log length ÷ billet length)
- total_billet_weight_needed_kg — billets × single billet weight

**Key formula reference:**
```
Single billet weight (kg) = π/4 × diameter(m)² × length(m) × 2700
Billets needed            = (tons × 1000) / billet_weight / 0.83
Logs needed               = billets_needed / (log_length / billet_length)
```

- Save.

---

### STEP 3 — Incoming Materials

**When:** Raw material (billets or logs) arrives from supplier.

#### 3A. Record Billet Receipt
- Path: Step 3 → Billet Receipt → New
- Fill: receipt_date, supplier, alloy_grade, billet_dia_inch, no_of_billets, total_weight_kg, batch_no, coc_number (Certificate of Conformance)
- This batch_no will be linked in the Extrusion Job Card

#### 3B. Check Log Master
- Path: Step 3 → Log Master
- Verify the log batch you will use has:
  - Sufficient total_weight_kg
  - Correct alloy_grade matching requirement
  - status = Available
  - log_diameter_inch matching press size

#### 3C. Log to Billet Conversion
**When:** You cut logs into billets at the saw station.

- Path: Step 3 → Log to Billet Conversion → New

| Field | What to Enter |
|-------|--------------|
| conversion_date | Today |
| shift | Morning / Evening / Night |
| log_batch | Select log batch being cut |
| press_size_inch | Match press size |
| log_original_length_mm | Actual log length measured |
| billet_cut_length_mm | Target billet length |
| no_of_logs_used | Count of logs cut |
| no_of_billets_produced | Billets produced (count) |
| single_billet_weight_kg | Weigh one billet |
| total_billet_weight_kg | Total weight of billets |
| butt_end_loss_kg | Weight of butt end scrap |
| saw_cut_loss_kg | Material lost in saw cuts |
| cutting_yield_percentage | **Auto-calculated** |
| operator | Saw operator name |

- Save.

> **Target:** Cutting yield should be 92–96%. If below 92%, check saw blade and settings immediately.

---

### STEP 4 — Billet Preparation

**When:** Billets are being prepared for the press — cutting to size and heating.

#### 4A. Billet Cutting Log
- Path: Step 4 → Billet Cutting Log → New
- Fill: shift_date, shift, cut_length_mm, no_pieces_cut, butt_end_weight_kg, scrap_from_cutting_kg
- Link to job card if cutting for a specific job

#### 4B. Furnace Log
**When:** Billets are being heated in the furnace.

- Path: Step 4 → Furnace Log → New

| Field | What to Enter |
|-------|--------------|
| furnace_no | Which furnace |
| job_card | Link to Extrusion Job Card |
| log_date | Today |
| billet_batch | Which billet batch heating |
| no_billets_loaded | Count loaded in furnace |
| target_temp_c | 470–490°C for 6063 alloy |
| actual_temp_achieved_c | Actual temperature reading |
| heat_up_time_mins | Time taken to reach target |
| soak_time_mins | Time held at target temperature |
| fuel_consumed_units | Fuel used |
| operator | Furnace operator name |

- Add temperature readings every 30 minutes in the **Temp Readings child table** (zone, time, temperature)
- Save.

> **Note:** 6063 target: 470–490°C. If actual is below 460°C, billet is too cold — press will show high pressure.

---

### STEP 5 — Extrusion

**When:** Billet is loaded in the press and extrusion begins. This is the most important record in the system.

#### 5A. Extrusion Job Card
- Path: Step 5 → Extrusion Job Card → New

**Section 1 — Basic Info:**

| Field | What to Enter |
|-------|--------------|
| shift_date | Today |
| shift | Morning / Evening / Night |
| press | 1500T or 2500T |
| shift_supervisor | Supervisor name |
| press_operator | Operator name |
| sales_order_ref | Link to Sales Order |

**Section 2 — Die Details:**

| Field | What to Enter |
|-------|--------------|
| die_number | Select from Die Master |
| die_status | Auto fills from Die Master |
| profile_description | Profile type/code |

> **System checks automatically:**
> - If die has >90% shot life used → warning popup
> - If die_status = Condemned → blocking alert, cannot proceed

**Section 3 — Billet Details:**

| Field | What to Enter |
|-------|--------------|
| log_batch | Link to Log Master batch |
| log_to_billet | Link to Log to Billet Conversion record |
| billet_batch | Select billet receipt batch |
| alloy_grade | Auto fills from billet batch |
| press_size_inch | Must match die size |
| billet_cut_length_mm | From conversion record |
| billet_weight_used_kg | Actual weight loaded into press |

**Section 4 — Press Parameters:**

| Field | What to Enter | Target Range |
|-------|--------------|-------------|
| billet_temp_celsius | Billet temperature before loading | 470–490°C |
| die_temp_c | Die temperature | 440–460°C |
| ram_pressure_tons | Actual breakthrough pressure | Per die spec |
| extrusion_speed_mpm | Ram/extrusion speed | Per profile spec |
| profile_exit_temp_c | Temperature of profile exiting die | 500–520°C |

**Section 5 — Output (fill after pressing):**

| Field | What to Enter |
|-------|--------------|
| gross_output_kg | Total weight before trimming |
| butt_scrap_kg | Butt end weight (target: 5–8%) |
| front_scrap_kg | Front cut weight (target: 2–3%) |
| net_output_kg | Final good profile weight |
| yield_percentage | **Auto-calculated** — target >85% |
| discard_weight_kg | Discard/runout pieces |

> **Auto-alert:** If yield drops below 80%, an orange flash alert appears. Investigate before saving.

**Section 6 — Stretching & Cutting:**

| Field | What to Enter |
|-------|--------------|
| stretching_done | Check if stretching performed |
| stretch_percentage | Usually 0.5–2% |
| pieces_before_cut | Count of profiles before saw |
| pieces_after_cut | Count after cutting to length |
| pieces_rejected | Rejected pieces count |

**Section 7 — Aging (if required):**

| Field | What to Enter |
|-------|--------------|
| aging_required | Check if T5/T6 required |
| temper_required | T5 / T6 / T66 |
| aging_oven | Which oven |
| aging_start_time | Start datetime |
| aging_end_time | End datetime |
| aging_temp_celsius | T5=185°C / T6=175°C / T66=165°C |
| hardness_after_aging_hv | Test reading after aging |

**Update Status as Job Progresses:**
```
Draft
  → Billet Loaded          (billet is in the press container)
  → Extrusion Running      (ram has started)
  → Quenching              (profile cooling after press)
  → Stretching             (stretcher operation)
  → Cutting                (saw cutting to length)
  → Aging                  (in aging oven)
  → Surface Treatment      (at surface treatment)
  → Quality Check          (QC inspection)
  → Completed              (approved and ready for dispatch)
                  → Rejected / Quality Hold (if QC fails)
```

- Save at each stage update.

#### 5B. Press Log (Every Stroke)
- Path: Step 5 → Press Log → New
- Record for **every stroke** on the press

| Field | What to Enter |
|-------|--------------|
| job_card | Link to current Extrusion Job Card |
| log_time | Exact time of this stroke |
| stroke_no | Stroke number (1, 2, 3...) |
| ram_pressure_tons | Actual ram pressure reading |
| ram_speed_mmps | Ram speed |
| container_temp_c | Container/liner temperature |
| die_temp_c | Die temperature |
| profile_exit_temp_c | Exit temperature of profile |
| defect_observed | Check if any defect on this stroke |
| defect_type | Select type if defect found |
| action_taken | What was done |

> **Warning:** If ram_pressure_tons suddenly spikes, die may be blocked. Stop press immediately.

---

### STEP 6 — Heat Treatment & Finishing

#### 6A. Aging Oven Log
**When:** Profiles are loaded into the aging oven for temper treatment.

- Path: Step 6 → Aging Oven Log → New

| Field | What to Enter | Target |
|-------|--------------|--------|
| oven_no | Which oven | — |
| job_card | Link to Job Card | — |
| temper_target | T5 / T6 / T66 | — |
| set_temp_c | Oven setpoint | T5=185°C / T6=175°C / T66=165°C |
| profiles_loaded_kg | Total weight loaded | — |
| actual_start | Start datetime | — |
| actual_end | End datetime | T5=4h / T6=8h / T66=12h |
| final_hardness_hv | Brinell/Vickers test after aging | T5=60–70HV / T6=80–90HV |
| result | Pass / Fail / Re-age | — |

- Add zone temperature readings every hour in the **Temp Readings child table**
- Save.

> If result = Re-age: load back into oven at same temperature for 2 additional hours.

#### 6B. Surface Treatment Order
**When:** Profiles need anodizing, powder coating, or polishing.

- Path: Step 6 → Surface Treatment Order → New

| Field | What to Enter |
|-------|--------------|
| job_card | Link to Extrusion Job Card |
| treatment_type | Mill Finish / Anodizing / Powder Coating / Polishing |
| color_shade | Customer required color |
| ral_code | RAL code (if powder coat) |
| film_thickness_micron | Target thickness — Anodizing: 15–25μm, Powder Coat: 60–80μm |
| qty_kg | Weight to treat |
| vendor | Surface treatment vendor name |
| status | Pending → In Process → Completed |

- Save. Update status as treatment progresses.

---

### STEP 7 — Quality Control

#### 7A. Quality Check
**When:** Profiles are ready for inspection before dispatch.

- Path: Step 7 → Quality Check → New

| Field | What to Enter |
|-------|--------------|
| qc_date | Today |
| job_card | Link to Extrusion Job Card |
| inspector | QC inspector name |
| sample_qty | Number of pieces sampled |

**Dimensional Check:**

| Field | How to Check |
|-------|-------------|
| wall_thickness_actual | Measure with vernier caliper |
| wall_thickness_spec | From customer drawing |
| wall_thickness_result | Pass if within ±0.1mm of spec |

**Surface Check:**
- Check for: die lines, scoring, blistering, scratches, discoloration
- surface_finish_result: Pass / Fail

**Hardness Check:**
- hardness_hv: Test using hardness tester
- T5 target: 60–70 HV | T6 target: 80–90 HV
- hardness_result: Pass / Fail

**Overall Result (set automatically by system):**
```
All checks Pass  → overall_result = Approved
Any check Fails  → overall_result = Rejected
Mixed results    → overall_result = Hold
```

- If Rejected: fill rejection_reason and corrective_action
- Save.

#### 7B. Scrap Record
**When:** Any scrap material is generated (butt end, front cut, QC rejection, surface defect).

- Path: Step 7 → Scrap Record → New
- Fill: scrap_date, job_card, scrap_type, weight_kg, notes
- All scrap goes to recycling — record it every shift

**Scrap types and normal ranges:**
| Type | Normal Range |
|------|-------------|
| Butt End | 5–8% of billet |
| Front Cut | 2–3% |
| Rejection | <2% |
| Surface Defect | <1% |

> If butt end exceeds 8%, check press ram settings. If rejection exceeds 2%, check die condition.

---

### STEP 8 — Shift Operations

#### 8A. Production Shift Report
**Fill this at the end of every shift — mandatory.**

- Path: Step 8 → Production Shift Report → New

| Field | What to Enter |
|-------|--------------|
| shift_date | Today |
| shift | Morning / Evening / Night |
| press | Which press |
| shift_incharge | Shift supervisor name |
| planned_production_kg | Target kg for this shift |
| actual_production_kg | Actual kg produced |
| efficiency_percentage | **Auto-calculated** |
| shift_yield_percentage | **Auto-calculated** |
| total_downtime_mins | Total downtime in minutes |
| no_of_die_changes | Dies changed this shift |
| no_of_strokes | Total press strokes |
| total_billet_used_kg | Total billet weight consumed |
| total_scrap_kg | Total scrap generated |
| issues_faced | Problems encountered |
| safety_incidents | Check if any accident occurred |
| safety_details | **Mandatory if safety_incidents is checked** |
| next_shift_handover | Notes for the incoming shift team |

- Add job cards run in this shift in the **Shift Job Card Detail child table**
- Save.

> **Target:** efficiency_percentage > 85%. If below 75% for 3 consecutive shifts, investigate press/die/material issues.

#### 8B. Die Maintenance Log
**When:** A die needs maintenance, nitriding, repair, or is condemned.

- Path: Step 8 → Die Maintenance Log → New

| Field | What to Enter |
|-------|--------------|
| die | Select from Die Master |
| maintenance_date | Today |
| maintenance_type | Routine Cleaning / Nitriding / Polishing / Repair / Condemned |
| before_condition | Good / Fair / Poor / Damaged |
| after_condition | Condition after maintenance |
| nitriding_done | Check if nitriding was done |
| nitriding_cycles | Number of nitriding cycles |
| cost | Maintenance cost |
| vendor | Vendor if sent outside |
| notes | Any additional notes |

- Save. Update die_status in Die Master accordingly.

**Die Maintenance Schedule:**
| Interval | Action |
|----------|--------|
| Every 500 shots | Routine Cleaning |
| Every 1000 shots | Nitriding |
| When surface quality drops | Polishing |
| If cracked or damaged | Repair / Condemned |
| At end of shot life | Condemned |

---

## Masters & Setup — Reference

### Die Master
- Path: Masters → Die Master

**Key fields to monitor:**

| Field | Meaning | Action |
|-------|---------|--------|
| die_status | New / Active / Under Repair / Condemned / In Press | Update after each use |
| total_shots_used | Shots used so far | Increment after each job |
| max_shots_allowed | Shot life limit | Set at creation (5000–8000) |
| last_used_date | Last press date | Auto-updates |

**Shot life thresholds:**
- < 75% → Normal, use freely
- 75–90% → Monitor closely, plan replacement
- > 90% → **Plan replacement NOW** — system shows red alert
- Condemned → **System blocks selection** — die cannot be used

### Item Master
- Path: Masters → Item
- item_group: Products
- stock_uom: Kg
- Create one item per profile code

---

## Reports & Analytics — All 9 Reports

**How to open any report:** Click the report name in the **Reports and Analytics** section of the workspace.

### Daily Production Summary
**Shows:** All Extrusion Job Cards with output and yield per shift.

| Column | What it means |
|--------|--------------|
| Shift Date | Date of production |
| Job Card | EJC reference |
| Press | Which press |
| Net Output kg | Good profile produced |
| Yield % | Output ÷ Billet × 100 |
| Yield Badge | Green >85%, Blue 80–85%, Yellow 75–80%, Red <75% |

**How to use:** Filter by date range to see daily/weekly output trends. Red yield badges need investigation.

---

### Customer Order Status
**Shows:** All active Sales Orders and their current production progress.

| Column | What it means |
|--------|--------------|
| Sales Order | SO reference |
| Customer | Customer name |
| Ordered Kg | Total order quantity |
| Produced Kg | Quantity produced so far |
| Progress % | Produced ÷ Ordered |
| Status | Active / Overdue / Completed |

**How to use:** Overdue orders highlighted in red. Use for customer follow-up calls.

---

### Order to Dispatch Tracker
**Shows:** End-to-end order progress from order date to dispatch.

| Column | What it means |
|--------|--------------|
| Sales Order | Reference |
| Customer | Name |
| Order Date | When order was placed |
| Delivery Date | Promised date |
| Current Stage | Where the job is right now |
| Dispatch Progress | Overall % complete |
| Overdue Flag | Red if past delivery date |

**How to use:** Any red row needs immediate attention — escalate to production manager.

---

### Press Efficiency Report
**Shows:** Efficiency % per press per day over a date range.

| Badge | Efficiency |
|-------|-----------|
| Excellent (Green) | > 90% |
| Good (Blue) | 80–90% |
| Average (Yellow) | 70–80% |
| Poor (Red) | < 70% |

**How to use:** Track press performance trends. Consecutive poor days = maintenance or die issue.

---

### Shift Summary Report
**Shows:** 30-day heatmap view — Morning / Evening / Night shifts by date.

- Green cell = Good shift (>85%)
- Yellow cell = Average (70–85%)
- Red cell = Poor (<70%) or safety incident

**How to use:** Spot patterns — which shift consistently underperforms? Which press has more downtime?

---

### Die Performance Report
**Shows:** All dies with shot-life progress bars and per-die production history.

| Column | What it means |
|--------|--------------|
| Die Number | Reference |
| Total Shots Used | Cumulative shots |
| Max Shots Allowed | Shot life limit |
| Shot Life % | Used ÷ Max × 100 |
| Condition | Progress bar — Red >90%, Orange >75%, Green <75% |

**How to use:** Sort by Shot Life % descending. Any die >90% must be scheduled for replacement.

---

### Die Health Dashboard
**Shows:** Bar chart comparing all dies — shots used vs maximum allowed.

**How to use:** Visual quick-check. Bars near the max line need action. Use in morning review meeting.

---

### Scrap Analysis Report
**Shows:** Scrap weight by type (butt end, front cut, rejection, surface defect) with a donut chart.

| Column | What it means |
|--------|--------------|
| Scrap Type | Category |
| Weight kg | Total scrap in period |
| % of Total | Share of total scrap |
| Cost | Estimated scrap cost |

**How to use:** If butt end % is rising, check ram settings. High rejection % = QC or die issue.

---

### Aging Oven Tracker
**Shows:** All active aging oven loads with remaining soak time.

| Column | What it means |
|--------|--------------|
| Job Card | Reference |
| Temper | T5 / T6 / T66 |
| Start Time | When loaded |
| Target End | When to remove |
| Result | Pass / Fail / Re-age |

**How to use:** Check before removing any load. Re-age entries need a second cycle.

---

## Live Dashboards — Detailed Guide

### 🏭 Plant Home Dashboard (`/app/alum-home`)
**Open every morning.** This is the plant-wide overview.

**Alert Bar (top of page):**
| Color | Meaning | Action |
|-------|---------|--------|
| 🔴 Red | Die with >90% shot life | Send die for repair, get backup ready |
| 🟠 Orange | Sales Order past delivery date | Prioritize in press schedule |
| 🔵 Blue | Quality Check awaiting decision | Open QC list, approve or reject |

**KPI Cards (Row 1):**
- Press 1 / Press 2 — RUNNING or IDLE + active job count
- Today's Output — kg produced in all shifts today
- Active Orders — Sales Orders currently in production
- Delayed Orders — Orders past delivery date (target: zero)
- Month Revenue — Sales Invoice total this month

**Process Flow Pipeline (Row 2):**
```
Orders → Die Ready → Billet Prep → Pressing → Quenching →
Stretching → Cutting → Aging → Surface → QC → Completed → Dispatch
```
Each stage shows live job count. Click any stage to open a filtered list. High count at one stage = bottleneck.

**Active Job Cards Table:** Live table of all in-progress jobs with yield bars.

**Die Shot-Life Grid:** 12 dies with progress bars. Red = critical (>90%), orange = warning (>75%).

**14-Day Trend Chart:** Daily production kg trend line.

**Auto-refreshes every 60 seconds.**

---

### Production Dashboard (`/app/alum-dashboard`)
- Today output, active jobs, 30-day average yield, critical die count
- Daily output bar chart + yield trend line (last 14 days)
- Die alerts table (dies >75% shot life)
- Recent jobs table with yield badges

---

### Job Card Kanban (`/app/alum-kanban`)
- Color-coded columns: one column per job status
- Each card shows: job no, profile, yield%, press, date
- Click any card to open the full Extrusion Job Card form
- Use this to check what is stuck at which stage

---

### Die Room Dashboard (`/app/die-room-dashboard`)
- Grid of all dies with shot-life progress bars
- Red border = >90% critical, yellow border = >75% warning
- Summary: Total dies / Active / In Maintenance / Critical / Condemned
- Click any die to open Die Master form

---

## Key Auto-Calculations

The system calculates these automatically — you just enter the raw numbers:

| Form | Field | Calculation |
|------|-------|------------|
| Extrusion Job Card | yield_percentage | net_output_kg ÷ billet_weight_used_kg × 100 |
| Extrusion Job Card | scrap_weight_kg | billet_weight_used_kg − net_output_kg |
| Extrusion Job Card | scrap_percentage | scrap_weight_kg ÷ billet_weight_used_kg × 100 |
| Extrusion Job Card | recovery_percentage | same as yield |
| Production Shift Report | efficiency_percentage | actual_production_kg ÷ planned_production_kg × 100 |
| Production Shift Report | shift_yield_percentage | actual_production_kg ÷ total_billet_used_kg × 100 |
| Production Planning Sheet | billets_needed | (tons × 1000) ÷ billet_weight ÷ 0.83 |
| Log to Billet Conversion | cutting_yield_percentage | total_billet_weight_kg ÷ (logs × log_weight) × 100 |

---

## System Alerts & Validations

### Extrusion Job Card
| Trigger | Alert | Action |
|---------|-------|--------|
| Die selected with >90% shots | Warning popup — "Die near end of life" | Plan replacement, use with caution |
| Die selected with Condemned status | **Blocking alert** — cannot proceed | Select a different die |
| yield_percentage < 80% | Orange flash alert on screen | Check billet temp, die condition, press pressure |
| net_output > billet_weight | Validation error — cannot save | Recheck measurements |

### Die Master
| Trigger | Display |
|---------|---------|
| Shot life > 95% | Red banner at top of form |
| Shot life > 80% | Yellow banner at top of form |

### Quality Check
| Trigger | Auto-set |
|---------|---------|
| All checks = Pass | overall_result = Approved |
| Any check = Fail | overall_result = Rejected |
| Mix of Pass/Fail | overall_result = Hold |

### Production Shift Report
- If safety_incidents is checked → safety_details field becomes mandatory (cannot save without it)

---

## Formulas Reference

```
# Extrusion
Yield %       = Net Output / Billet Weight × 100          (target >85%)
Scrap %       = Scrap Weight / Billet Weight × 100        (target <15%)
Discard %     = Discard Weight / Billet Weight × 100      (target 5–8%)

# Billet Planning
Billet weight = π/4 × diameter(m)² × length(m) × 2700 kg/m³
Billets needed = (tonnes required × 1000) / billet_weight / 0.83
Logs needed    = billets_needed / (log_length / billet_cut_length)

# Cutting
Cutting yield = Total Billet Output / (Logs × Log Weight) × 100  (target 92–96%)

# Shift
Efficiency %  = Actual Production / Planned Production × 100     (target >85%)
```

---

## Morning Routine Checklist

```
07:00 — Login → Aluminium Manufacturing workspace
         ↓
         Open Plant Home Dashboard
         ↓
         Check Alert Bar:
           🔴 Die critical?  → Arrange replacement
           🟠 Order delayed? → Prioritize in press
           🔵 QC pending?    → Review and decide
         ↓
         Check KPI Cards:
           Press 1, Press 2 — Running or Idle?
           Today Output — on track?
           Delayed Orders — must be zero
         ↓
         Check Process Flow Pipeline:
           Any stage with HIGH count = bottleneck → investigate
         ↓
         Open Shift Summary Report → confirm all shift reports submitted
         ↓
         Open Order to Dispatch Tracker → check for red rows
         ↓
         Brief team → start production
```

---

## 5-Minute Client Demo Script

**Step 1 — Plant Home Dashboard (90 seconds)**
- Open: `http://kali.local:8000/app/alum-home`
- Show: Alert bar, 6 KPI cards, process flow pipeline with live counts
- Say: *"This is what the production manager sees every morning — entire plant on one screen, live counts at every stage."*

**Step 2 — Walk Through One Order (2 minutes)**

| Stage | Form | What to show |
|-------|------|-------------|
| 1 | Customer Requirement Sheet | Customer needs 5T of T5 6063 profile |
| 2 | Production Planning Sheet | System calculates 280 billets, 45 logs |
| 3 | Log to Billet Conversion | Cut billets, 94.5% yield |
| 4 | Extrusion Job Card | Press run — yield auto-calculated, alert if <80% |
| 5 | Quality Check | QC form — overall result auto-set |
| 6 | Surface Treatment Order | Anodizing order sent to vendor |
| 7 | Sales Order | Dispatch and invoice |

**Step 3 — Reports (90 seconds)**

| Report | What to highlight |
|--------|-----------------|
| Order to Dispatch Tracker | Every order, every stage, delays in red |
| Die Performance Report | Red bars = dies needing replacement |
| Shift Summary Report | 30-day heatmap — green/yellow/red shifts |
| Press Efficiency Report | Which press is underperforming |
| Scrap Analysis Report | Scrap breakdown — find cost savings |

*Close: "Every process in your plant — tracked, calculated, alerted. We can customize any field or report for your specific requirements."*

---

## Troubleshooting

| Problem | Solution |
|---------|---------|
| Site not opening | Open Ubuntu/WSL → `cd ~/frappe-bench && bench start` → wait 30s |
| Login not working | Username: Administrator / Password: admin |
| Report showing error | Check if date filters are set, try clearing and refreshing |
| Workspace links not working | Run `bench --site kali.local clear-cache` in terminal |
| DocType "not found" error | Run `bench --site kali.local migrate` then clear cache |
| Bench not starting | Check `bench status` and look for port conflicts |

---

## DocTypes Reference — Complete List

| Workspace Step | DocType | Records Tracked |
|----------------|---------|----------------|
| Step 1 | Customer | Customer master |
| Step 1 | Sales Order | Customer orders |
| Step 1 | Customer Requirement Sheet | Order requirements |
| Step 1 | Customer Drawing | Profile drawings |
| Step 2 | Production Planning Sheet | Production plans |
| Step 3 | Billet Receipt | Incoming billets |
| Step 3 | Log Master | Log inventory |
| Step 3 | Log to Billet Conversion | Billet cutting yield |
| Step 4 | Billet Cutting Log | Saw cutting records |
| Step 4 | Furnace Log | Billet heating |
| Step 5 | Extrusion Job Card | Main press production record |
| Step 5 | Press Log | Per-stroke press data |
| Step 6 | Aging Oven Log | T5/T6/T66 aging cycles |
| Step 6 | Surface Treatment Order | Anodizing / powder coat |
| Step 7 | Quality Check | QC inspections |
| Step 7 | Scrap Record | Scrap tracking |
| Step 8 | Production Shift Report | Shift summaries |
| Step 8 | Die Maintenance Log | Die maintenance records |
| Masters | Item | Profile items |
| Masters | Die Master | Die inventory & shot life |

**Supporting child tables:**
- Furnace Temp Reading (child of Furnace Log)
- Aging Temp Reading (child of Aging Oven Log)
- Shift Job Card Detail (child of Production Shift Report)

---

## Reports Reference — Complete List

| Report | Section | Shows |
|--------|---------|-------|
| Daily Production Summary | Reports | Output & yield per job, per shift |
| Customer Order Status | Reports | Per-order production progress |
| Order to Dispatch Tracker | Reports | End-to-end order tracking |
| Press Efficiency Report | Reports | Per-press efficiency trend |
| Shift Summary Report | Reports | 30-day shift heatmap |
| Die Performance Report | Reports | Per-die shot life & production |
| Die Health Dashboard | Reports | Bar chart — all dies shot life |
| Scrap Analysis Report | Reports | Scrap by type, weight, cost |
| Aging Oven Tracker | Reports | Active aging loads & remaining time |

---

---

## STOCK & MANUFACTURING FLOW

### What is a Profile Item?
Each die produces one profile shape. In ERPNext each profile = one Item.
- DIE-001 → PRO-T-40X40 (T Section 40x40)
- DIE-002 → PRO-SQ-50X50 (Square Hollow 50x50)
- DIE-003 → PRO-RECT-100X50 (Rectangle 100x50)
- DIE-004 → PRO-ANG-50X50 (Angle 50x50x3)
- DIE-006 → PRO-DOOR-001 (Door Frame Profile)
- DIE-007 → PRO-WIN-001 (Window Frame Profile)
- DIE-008 → PRO-SOL-001 (Solar Panel Frame)
- DIE-009 → PRO-CW-001 (Curtain Wall Profile)
- DIE-010 → PRO-H-001 (Custom H Section)

### What is a BOM?
Bill of Materials = Recipe for making a profile.
Shows: **1.18 Kg Billet → 1 Kg Profile**
The 0.18 Kg difference = scrap/losses (butt end + front cut + discard)

### Stock Entry - Manufacture
This is the KEY transaction that tracks every kg:



### Yield Calculation

- Industry target: **82–85%**
- Below 80% = investigate immediately (die issue / press problem)

### Scrap Types Explained

| Type | Code | Description | Typical % |
|------|------|-------------|-----------|
| Butt End | SCRAP-BUTT | Last piece in press — cannot extrude | 6–8% |
| Front Cut | SCRAP-FRONT | First piece out — not full profile shape | 1–2% |
| Discard | SCRAP-DISC | Short/bent pieces from stretch & cut stage | 2–4% |
| QC Reject | SCRAP-REJ | Failed quality inspection | 0.5–2% |

### Scrap Value
Scrap is **NOT** waste — it has cash value!
- Butt End & Front Cut: Rs 85/Kg
- Discard & QC Reject: Rs 75/Kg
- Sold to scrap dealers monthly (customer: Aluminium Scrap Traders)

### New Reports Available
| Report | Shows |
|--------|-------|
| Input vs Output Analysis | Per-job: billet in, profile out, each scrap type, yield %, recovery value |
| Scrap Value Report | Monthly scrap breakdown with value and % of production |
| Stock Ledger Summary | Current stock in Billet Store / Finished Goods / Scrap Yard with values |

### Colour Coding in Input vs Output Analysis
- 🟢 Yield ≥ 85% — Green (excellent)
- 🟡 Yield 80–84% — Orange (acceptable)
- 🔴 Yield < 80% — Red (investigate)

---

## Installation (For Developers)

```bash
cd /path/to/frappe-bench
bench get-app https://github.com/jajulasandeep583/kali.git
bench --site your-site.local install-app kali
bench --site your-site.local migrate
bench --site your-site.local clear-cache
```

**Tech stack:** ERPNext v16 + Frappe v16 | Python 3.14 | MariaDB | Redis | Frappe Charts + Chart.js v4

---

*kali app v5.0 | Workspace redesigned with process-flow layout | Last updated: 2026-05-12*
