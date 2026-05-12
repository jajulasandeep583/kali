# PRODUCTION MANAGER - DAILY SOP
# Aluminium Extrusion Plant ERP
# Site: http://kali.local:8000 | Login: Administrator / admin

---

## MORNING ROUTINE (7:00 AM)

1. Open http://kali.local:8000
2. Login: Administrator / admin
3. Click "Aluminium Manufacturing" workspace
4. Click "Plant Home Dashboard"

CHECK ALERT BAR:
- Red Alert = Die needs replacement NOW
  Action: Go to Die Master, send die for repair, arrange replacement die immediately
- Orange Alert = Order delayed
  Action: Open Order to Dispatch Tracker, check which order is delayed, prioritize in press
- Blue Alert = QC pending approval
  Action: Open Quality Check list, review and approve/reject

CHECK KPI CARDS:
- Press 1 (1500T) = RUNNING or IDLE?
- Press 2 (2500T) = RUNNING or IDLE?
- Today Output KG = meeting target?
- Active Orders = how many in pipeline?
- Delayed Orders = must be ZERO
- Month Revenue = tracking target?

CHECK PROCESS FLOW PIPELINE:
Customer Order -> Die Ready -> Billet Prep -> Pressing -> Quenching -> Stretching
-> Cutting -> Aging -> Surface -> QC -> Completed -> Dispatch

WARNING: If one stage shows HIGH count = BOTTLENECK
Action: Investigate that stage immediately

---

## PLANNING NEW PRODUCTION

When customer order comes in:

### STEP 1: Customer Requirement Sheet

Path: Pre-Production -> Customer Requirement Sheet -> New

Fill these fields:
- req_date: Today's date
- customer: Select customer name
- sales_order: Link sales order
- profile_weight_required_tons: How many tons customer needs
- die_required: Which die to use
- profile_length_mm: What length profiles needed
- alloy_grade: 6063 / 6061 / 6082 / 6005
- temper_required: T5 or T6 or T66
- surface_finish: Mill Finish / Anodizing / Powder Coating
- press_size_required: 6 inch / 7 inch / 8 inch
- special_requirements: Any special notes
- status: Received

Save.

### STEP 2: Production Planning Sheet

Path: Pre-Production -> Production Planning Sheet -> New

Fill these fields:
- plan_date: Today
- customer_req: Link to requirement sheet above
- customer: Auto fills
- sales_order: Link sales order
- die: Select die from Die Master
- press: Select press workstation
- press_size_inch: Must match die size
- alloy_grade: Must match requirement
- profile_tons_planned: Tons to produce
- log_batch: Select available log batch
- logs_allocated_nos: How many logs to use
- billet_cut_length_mm: What size to cut billets
- billets_needed: System calculates
- single_billet_weight_kg: System calculates
- total_billet_weight_needed_kg: System calculates
- planned_date: When to produce
- status: Approved

Save.

KEY CALCULATION:
```
Single billet weight (kg) = pi/4 x diameter(m)^2 x length(m) x 2700
Billets needed            = (tons x 1000) / billet weight / 0.83
Logs needed               = billets needed / (log length / billet length)
```

### STEP 3: Check Log Stock

Path: Pre-Production -> Log Master

Check:
- log_diameter_inch matches press size
- alloy_grade matches requirement
- status = Available
- sufficient total_weight_kg available

### STEP 4: Log to Billet Conversion

Path: Pre-Production -> Log to Billet Conversion -> New

Fill:
- conversion_date: Today
- shift: Morning / Evening / Night
- log_batch: Select log batch
- press_size_inch: Match to press
- log_original_length_mm: Actual log length
- billet_cut_length_mm: Required billet length
- no_of_logs_used: How many logs cutting
- no_of_billets_produced: Count after cutting
- single_billet_weight_kg: Weigh one billet
- total_billet_weight_kg: Total weight
- butt_end_loss_kg: Weight of butt end scrap
- saw_cut_loss_kg: Weight lost in saw cuts
- total_cutting_scrap_kg: Total cutting loss
- cutting_yield_percentage: Auto calculated
- operator: Who did the cutting

Save.

WARNING: Cutting yield should be 92-96%.
If below 92% investigate saw settings immediately.

---

## PRODUCTION - EXTRUSION JOB CARD

Path: Daily Operations -> Extrusion Job Card -> New

SECTION 1 - Basic Info:
- shift_date: Today
- shift: Morning / Evening / Night
- press: Select press (1500T or 2500T)
- shift_supervisor: Supervisor name
- press_operator: Operator name

SECTION 2 - Die Details:
- die_number: Select from Die Master
  WARNING: System warns if die is over 90% shots used
  WARNING: System blocks if die is Condemned
  Check die_status = Active before selecting

SECTION 3 - Billet Details:
- log_batch: Link to Log Master
- log_to_billet: Link to conversion record
- billet_batch: Select billet receipt
- alloy_grade: Auto fills
- press_size_inch: Must match die
- billet_cut_length_mm: From conversion record
- billet_weight_used_kg: Actual weight loaded

SECTION 4 - Press Parameters:
- billet_temp_celsius: Target 470-490 deg C
- die_temp_c: Target 440-460 deg C
- ram_pressure_tons: Record actual pressure
- extrusion_speed_mpm: Record speed
- profile_exit_temp_c: Record exit temp

SECTION 5 - Output:
- gross_output_kg: Total before cutting
- butt_scrap_kg: Butt end weight
- front_scrap_kg: Front end weight
- net_output_kg: Final good output
- yield_percentage: AUTO CALCULATED
  Good yield: >85%
  Acceptable: 80-85%
  Investigate: <80%
- discard_weight_kg: Discard pieces
- discard_percentage: Should be 5-8%

SECTION 6 - Stretching and Cutting:
- stretching_done: Check if done
- stretch_percentage: Usually 1-2%
- pieces_before_cut: Count before saw
- pieces_after_cut: Count after saw
- pieces_rejected: Rejected pieces count

SECTION 7 - Aging:
- aging_required: Check if needed
- temper_required: T5 or T6 or T66
- aging_oven: Select oven
- aging_start_time: Record start
- aging_end_time: Record end
- aging_temp_celsius: T6 = 175 deg C / T5 = 185 deg C
- hardness_after_aging_hv: Test and record

UPDATE STATUS as production moves:
```
Draft
  -> Billet Loaded     (when billet in press)
  -> Extrusion Running (press started)
  -> Quenching         (after press)
  -> Stretching
  -> Cutting
  -> Aging
  -> Surface Treatment
  -> Quality Check
  -> Completed
```

---

## PRESS LOG (Every Stroke)

Path: Daily Operations -> Press Log -> New

- job_card: Link to current job card
- log_time: Exact time
- stroke_no: Stroke number
- ram_pressure_tons: Actual pressure
- ram_speed_mmps: Actual speed
- container_temp_c: Container temperature
- die_temp_c: Die temperature
- profile_exit_temp_c: Exit temperature
- defect_observed: Check if any defect seen
- defect_type: Select type if defect
- action_taken: What was done

Record for EVERY stroke.
WARNING: If pressure suddenly increases, die may be blocked. Stop press immediately.

---

## FURNACE LOG (Every Heating Cycle)

Path: Daily Operations -> Furnace Log -> New

- furnace_no: Which furnace
- job_card: Link to job card
- log_date: Today
- billet_batch: Which billets heating
- no_billets_loaded: Count loaded
- target_temp_c: Usually 480 deg C for 6063
- actual_temp_achieved_c: Actual reading
- heat_up_time_mins: Time to reach temp
- soak_time_mins: Time held at temp
- operator: Furnace operator name

Record temperature every 30 minutes in the temp readings table.

---

## AGING OVEN LOG

Path: Daily Operations -> Aging Oven Log -> New

- oven_no: Which oven
- job_card: Link to job card
- temper_target: T5 / T6 / T66
- set_temp_c:
  T5  = 185 deg C for 4 hours
  T6  = 175 deg C for 8 hours
  T66 = 165 deg C for 12 hours
- profiles_loaded_kg: Total KG in oven
- actual_start: Start datetime
- actual_end: End datetime
- final_hardness_hv: Test after aging
  T5 target: 60-70 HV
  T6 target: 80-90 HV
- result: Pass / Fail / Re-age

Record zone temperatures every hour in the temp readings table.

---

## QUALITY CHECK

Path: Quality & Tracking -> Quality Check -> New

- qc_date: Today
- job_card: Link to job card
- inspector: QC person name
- sample_qty: How many pieces checked

DIMENSION CHECK:
- wall_thickness_actual: Measure with vernier
- wall_thickness_spec: From drawing
- wall_thickness_result: Pass if within +/- 0.1mm

SURFACE CHECK:
- surface_finish: Pass / Fail
  Check for: scratches, die lines, blistering

HARDNESS CHECK:
- hardness_hv: Test with hardness tester
  T6 must be: 80-90 HV
  T5 must be: 60-70 HV
- hardness_result: Pass / Fail

OVERALL RESULT (set by system):
  All Pass  = Approved
  Any Fail  = Rejected
  Mixed     = Hold

If Rejected:
- rejection_reason: Write exact reason
- corrective_action: What to do next

---

## SURFACE TREATMENT ORDER

Path: Quality & Tracking -> Surface Treatment Order -> New

- job_card: Link to job card
- treatment_type:
  Mill Finish    = no treatment, direct dispatch
  Anodizing      = corrosion resistance
  Powder Coating = color coating
  Polishing      = mirror finish
- color_shade: Customer required color
- ral_code: RAL color code if powder coat
- film_thickness_micron: Target thickness
  Anodizing:    15-25 micron
  Powder Coat:  60-80 micron
- qty_kg: Weight to treat
- vendor: If sending outside
- status: Pending -> In Process -> Completed

---

## DIE MANAGEMENT

Path: Masters -> Die Master

Check die before every job:
1. die_status must be = Active
2. Check total_shots_used vs max_shots_allowed
   >90% = Plan replacement NOW
   >75% = Monitor closely
   <75% = OK to use

After every job:
- Update total_shots_used (add shots used)
- Update last_used_date

When die needs maintenance:
Path: Masters -> Die Maintenance Log -> New

- maintenance_type:
  Routine Cleaning = after every 500 shots
  Nitriding        = every 1000 shots
  Polishing        = when surface quality drops
  Repair           = if die damaged
  Condemned        = end of life
- before_condition: Good / Fair / Poor / Damaged
- after_condition: After maintenance
- cost: Maintenance cost

---

## SCRAP RECORD

Path: Quality & Tracking -> Scrap Record -> New

Types of scrap:
- Butt End:       End piece from press (5-8% of billet)
- Front Cut:      First piece cut off (2-3%)
- Rejection:      Failed QC pieces
- Surface Defect: Surface treatment rejects
- Other:          Any other scrap

Record every day. All scrap goes to recycling.
WARNING: If butt end exceeds 8%, check press settings.

---

## END OF SHIFT REPORT

Path: Daily Operations -> Production Shift Report -> New

Fill EVERY shift end:
- shift_date: Today
- shift: Morning / Evening / Night
- press: Which press
- shift_incharge: Supervisor name
- planned_production_kg: Target for shift
- actual_production_kg: Actual achieved
- efficiency_percentage: AUTO CALCULATED (target >85%)
- total_downtime_mins: Any downtime during shift
- no_of_die_changes: Dies changed this shift
- no_of_strokes: Total strokes
- total_billet_used_kg: Billets consumed
- total_scrap_kg: Total scrap generated
- issues_faced: Any problems faced
- safety_incidents: Any accidents
- next_shift_handover: What next shift must know

---

## KEY REPORTS AND WHAT THEY SHOW

| Report | What It Shows | Action Trigger |
|--------|--------------|----------------|
| Order to Dispatch Tracker | Every order and current stage | Red row = delayed >7 days, prioritize |
| Die Performance Report | All dies with shot life % | Red >90% shots = replace now |
| Daily Production Summary | All job cards with yield % | Red yield <80% = investigate |
| Press Efficiency Report | Per press efficiency trend | Target >85% efficiency |
| Scrap Analysis Report | Scrap by type and weight | High butt end % = check press |
| Shift Summary Report | 30-day shift heatmap | Green = good shift, Red = bad |
| Die Health Dashboard | Bar chart of all dies shot life | Visual quick check |
| Aging Oven Tracker | What is currently in aging ovens | Shows remaining hours |
| Customer Order Status | Per customer order progress | Customer follow-up tool |

---

## ALERTS AND ACTIONS

### DIE CRITICAL (>90% shots used):
1. Finish current job only
2. Remove die from press
3. Send for nitriding or replacement
4. Update die_status = Under Repair
5. Arrange backup die before next job

### ORDER DELAYED (>7 days):
1. Open that sales order
2. Check which stage it is stuck at
3. Prioritize in press schedule
4. Inform customer if dispatch date missed

### LOW YIELD (<80%):
1. Check billet temperature (must be 470-490 deg C)
2. Check die condition for wear or blockage
3. Check press ram pressure
4. Check billet quality and alloy grade
5. Record findings in job card notes

### QC REJECTED:
1. Segregate rejected material physically
2. Create Scrap Record
3. Decide: rework or scrap
4. If die issue, send for maintenance
5. Re-run production if customer permits

---

## 5-MINUTE CLIENT DEMO SCRIPT

Step 1 - Login (30 seconds):
  Say: "This is our Aluminium Extrusion ERP built on ERPNext.
  Let me show you how the plant runs from one screen."

Step 2 - Plant Home Dashboard (1 minute):
  Open: http://kali.local:8000/app/alum-home
  Show: Alert bar at top, KPI cards, live process flow
  Say: "This is the morning view for the production manager.
  Every stage of production visible in real time."

Step 3 - Order Tracking (1 minute):
  Open: Order to Dispatch Tracker report
  Say: "Every customer order, where it is right now,
  how many KG produced, any delays highlighted in red."

Step 4 - Die Management (30 seconds):
  Open: Die Room Dashboard
  Say: "All dies at a glance. Red means needs replacement today.
  System auto-alerts when 90% of shot life is used."

Step 5 - Job Card (1 minute):
  Open: Any Extrusion Job Card
  Say: "This is one complete production record.
  Billet temperature, press pressure, yield auto-calculated,
  instant alert if yield drops below 80%."

Step 6 - Reports (1 minute):
  Show: Die Performance -> Shift Summary -> Scrap Analysis
  Say: "9 reports with charts. Shift heatmap, die life,
  scrap breakdown, press efficiency - all in one place."

Close: "Any process in your plant, this system tracks it.
We can customize further based on your specific requirements."

---

## TROUBLESHOOTING

**Site not opening:**
1. Open Ubuntu / WSL terminal
2. Run: cd ~/frappe-bench && bench start
3. Wait 30 seconds
4. Try http://kali.local:8000 again

**Report showing error:**
1. Open Claude Code terminal
2. Describe the error
3. Claude will diagnose and fix automatically

**Forgot password:**
- Username: Administrator
- Password: admin

**GitHub repository:**
https://github.com/jajulasandeep583/kali.git

---

## DOCTYPES REFERENCE (All 20)

| Workspace Section | DocType | Purpose |
|------------------|---------|---------|
| Pre-Production | Customer Requirement Sheet | Capture customer order requirements |
| Pre-Production | Production Planning Sheet | Plan production with billet/log calc |
| Pre-Production | Log Master | Track aluminium log batches |
| Pre-Production | Log to Billet Conversion | Record billet cutting and yield |
| Daily Operations | Extrusion Job Card | Main production record per job |
| Daily Operations | Press Log | Per-stroke press data |
| Daily Operations | Furnace Log | Billet heating records |
| Daily Operations | Aging Oven Log | Heat treatment records |
| Daily Operations | Billet Cutting Log | Saw cutting records |
| Daily Operations | Production Shift Report | End of shift summary |
| Masters | Die Master | Die inventory and shot life |
| Masters | Billet Receipt | Billet purchase receipt |
| Masters | Customer Drawing | Profile drawings |
| Masters | Die Maintenance Log | Die repair and maintenance |
| Quality & Tracking | Quality Check | QC inspection record |
| Quality & Tracking | Surface Treatment Order | Anodizing / powder coat orders |
| Quality & Tracking | Scrap Record | Scrap tracking and weighing |
| Supporting | Aging Temp Reading | Oven temp log (child table) |
| Supporting | Furnace Temp Reading | Furnace temp log (child table) |
| Supporting | Shift Job Card Detail | Shift report job details (child table) |


---

## STOCK ENTRY PROCEDURE (MANUFACTURE)

### When to Create a Manufacture Stock Entry
After each production run is complete, create a Manufacture Stock Entry to record all material movements.

### Step-by-Step

1. **Go to:** Stock > Stock Entry > New
2. **Set type:** Manufacture
3. **Add INPUT row:** Item: ALU-BILLET-6063, Source: Billet Store, Qty: actual kg consumed
4. **Add SCRAP rows:** SCRAP-BUTT, SCRAP-FRONT, SCRAP-DISC, SCRAP-REJ -> Scrap Yard
5. **Add FINISHED GOODS row:** Profile item -> Finished Goods Warehouse (Is Finished Item: YES)
6. **Verify:** Total Output = Total Input
7. **Submit** the entry

### Yield Target
- Target: 82-85% yield
- Formula: Good Profile Kg / Total Billet Kg x 100
- Below 80%: report to Production Manager immediately

---

*SOP Version 1.0 | Aluminium Extrusion ERP*
*Built on ERPNext v16 | kali custom app*
*Last updated: 2026-05-10*
