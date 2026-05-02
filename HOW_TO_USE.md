# Aluminium Extrusion Manufacturing ERP - How To Use Guide

## Site Details
- **URL:** http://kali.local:8000  
- **Login:** Administrator  
- **Password:** admin  
- **ERPNext Version:** v16  

---

## 1. How to Start the Site Every Day

Open **WSL (Ubuntu)** terminal and run these commands:

```bash
# Start Redis (cache + queue)
redis-server ~/frappe-bench/config/redis_cache.conf --daemonize yes
redis-server ~/frappe-bench/config/redis_queue.conf --daemonize yes

# Start Web Server (keep this terminal open or use nohup)
cd ~/frappe-bench
nohup bench serve --port 8000 > logs/web.log 2>&1 &

# Start SocketIO
nohup node apps/frappe/socketio.js > logs/socketio.log 2>&1 &

# Start background workers
nohup bench schedule > logs/schedule.log 2>&1 &
nohup bench worker > logs/worker.log 2>&1 &
```

**Or use bench start (recommended for development):**
```bash
cd ~/frappe-bench
bench start
```

Open browser → http://kali.local:8000

---

## 2. Daily Workflow for Production Team

### Morning Checklist:
1. Log in → Go to **Aluminium Manufacturing** workspace
2. Check pending **Work Orders** (Manufacturing module)
3. Check **Die Master** - any dies due for maintenance?
4. Verify **Billet Receipt** stock availability
5. Create **Extrusion Job Card** for each production run

### End of Day:
1. Update all Job Card statuses
2. Record scrap in **Scrap Record**
3. Run **Daily Production Summary** report
4. Update completed **Quality Check** records

---

## 3. How to Create a New Job Card

**Path:** Kali Module → Extrusion Job Card → New

Fill these fields:
1. **Job Card No** - e.g., EJC-2025-002 (auto or manual)
2. **Shift** - Morning / Evening / Night
3. **Shift Date** - Today's date
4. **Press** - Select Extrusion Press 1500T or 2500T
5. **Die Number** - Select from Die Master (e.g., DIE-001)
6. **Billet Batch** - Select from Billet Receipt
7. **Profile Item** - Select the profile being extruded
8. **Work Order Ref** - Link to production Work Order
9. Fill in process parameters:
   - Billet Temp (°C), Ram Pressure (tons), Speed (mpm)
10. After extrusion: Fill weights (billet used, gross output, scrap)
11. **Net Output** = Gross - Butt End - Front End Scrap
12. **Yield %** = (Net Output / Billet Used) × 100
13. Set **Status** → Update as production progresses
14. Save and track through stages

---

## 4. How to Track Order from Sale to Dispatch

**Full workflow:**

```
Sales Order → Work Order → Extrusion Job Card → Quality Check 
→ Surface Treatment Order → Stock Entry → Delivery Note → Sales Invoice → Payment
```

**Step by step:**
1. **Sales Order** (Selling → Sales Order)
   - Create with customer, profile item, quantity, rate, delivery date
   - Submit it
2. **Work Order** (Manufacturing → Work Order)
   - Create from Sales Order or directly
   - Select BOM (BOM-ALU-PROFILE-T-6063-001)
   - Submit it
3. **Extrusion Job Card** - Create and track production
4. **Quality Check** - Record QC results, note approved qty
5. **Surface Treatment Order** - If powder coating / anodizing needed
6. **Stock Entry (Manufacture)** - Transfer FG to Finished Goods Warehouse
7. **Delivery Note** - Against Sales Order, from Finished Goods Warehouse
8. **Sales Invoice** - Against Delivery Note
9. **Payment Entry** - Record customer payment

**Tracking report:** Run **Order to Dispatch Tracker** report to see all orders status.

---

## 5. How to Check Die Performance

**Path:** Kali Module → Reports → Die Performance Report

This report shows:
- Each die's total shots used vs max allowed
- Remaining shots and % utilization
- Alert status (Green/Yellow/Red)

**Alert levels:**
- 🟢 OK - Below 75% utilized
- 🟡 WARNING - 75-90% utilized (plan maintenance)
- 🔴 CRITICAL - Above 90% (replace soon)

**To update die shots:** Go to Die Master → Find your die → Update **Total Shots Used** after each production run.

**Die Maintenance:** When a die goes for repair → Change **Die Status** to "Under Repair"

---

## 6. How to Record Scrap

**Path:** Kali Module → Scrap Record → New

Fill:
1. **Scrap No** - e.g., SCRAP-2025-003
2. **Scrap Date** - Date of generation
3. **Job Card** - Link to the Extrusion Job Card
4. **Scrap Type:**
   - Butt End (from press)
   - Front Cut (from runout)
   - Rejection (quality failure)
   - Surface Defect (from surface treatment)
   - Other
5. **Alloy Grade** - 6063 or 6061
6. **Weight (Kg)** - Actual scrap weight
7. **Recovery Amount** - Value from scrap dealer

**Types of scrap in extrusion:**
| Type | Source | Typical % |
|------|--------|-----------|
| Butt End | Extrusion press | 7-10% |
| Front Cut | Runout table | 1-3% |
| Rejection | QC failure | <2% |
| Surface Defect | After coating | <1% |

---

## 7. How to Run Reports

**Path:** Kali Module → Reports section

Available reports:

### Daily Production Summary
- Shows all job cards by date
- Filter by: From Date, To Date, Shift
- Key metrics: Billet Used, Output, Scrap, Yield%

### Die Performance Report
- Lists all dies with shot count and health status
- Highlights dies needing attention
- No filters needed - shows all dies

### Scrap Analysis Report
- Breakdown of all scrap by type
- Filter by: From Date, To Date, Scrap Type
- Shows recovery value totals

### Order to Dispatch Tracker
- End-to-end order fulfillment status
- Shows: Ordered → Produced → Dispatched → Pending
- Filter by: Customer, Date range

**To run a report:** Click on report name → Set filters → Click "Run"

---

## 8. Key DocTypes Reference

| DocType | Purpose | Navigation |
|---------|---------|-----------|
| Die Master | Track dies - shots, status, maintenance | Kali → Die Master |
| Billet Receipt | Incoming billet batches with QC data | Kali → Billet Receipt |
| Extrusion Job Card | Daily production records per shift | Kali → Extrusion Job Card |
| Quality Check | QC results - dimensions, hardness, finish | Kali → Quality Check |
| Surface Treatment Order | Powder coat / anodize tracking | Kali → Surface Treatment Order |
| Scrap Record | Record and track all scrap | Kali → Scrap Record |

---

## 9. Important Item Codes

| Item Code | Description | UOM |
|-----------|-------------|-----|
| ALU-BILLET-6063 | Aluminium Billet 6063 | Kg |
| ALU-BILLET-6061 | Aluminium Billet 6061 | Kg |
| ALU-PROFILE-T-6063 | T-Section Profile 6063 | Kg |
| ALU-PROFILE-SQ-6063 | Square Hollow Profile | Kg |
| ALU-PROFILE-RECT-6063 | Rectangle Profile | Kg |
| ALU-SCRAP | Aluminium Scrap | Kg |

---

## 10. Warehouses

| Warehouse | Use |
|-----------|-----|
| Billet Store - A | Incoming billets storage |
| Die Store - A | Die storage |
| WIP - Press Floor - A | Material at press |
| WIP - Heat Treatment Room - A | Aging oven area |
| WIP - Surface Finishing Area - A | Coating area |
| Finished Goods Warehouse - A | Ready stock |
| Scrap Yard - A | Collected scrap |
| Rejection Store - A | Rejected material |

---

## 11. Trouble-Shooting

**Site not loading?**
```bash
# Check if web server is running
ss -tlnp | grep 8000
# If not, restart:
cd ~/frappe-bench && nohup bench serve --port 8000 > logs/web.log 2>&1 &
```

**Redis connection error?**
```bash
redis-cli -p 13000 ping  # Should return PONG
redis-cli -p 11000 ping  # Should return PONG
# If not:
redis-server ~/frappe-bench/config/redis_cache.conf --daemonize yes
redis-server ~/frappe-bench/config/redis_queue.conf --daemonize yes
```

**Clear cache if pages look wrong:**
```bash
cd ~/frappe-bench
bench --site kali.local clear-cache
bench --site kali.local clear-website-cache
```

---

*Generated for Aluminium Extrusion Manufacturing ERP on ERPNext v16*  
*GitHub: https://github.com/jajulasandeep583/kali.git*
