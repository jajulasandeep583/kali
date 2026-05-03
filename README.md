# Kali - Aluminium Extrusion Manufacturing ERP

A custom Frappe/ERPNext app for managing aluminium extrusion manufacturing operations — from billet receipt to dispatch.

## Features

- **17 Custom DocTypes** covering the full production cycle
- **Production Tracking** — Extrusion Job Cards, Press Logs, Billet Receipts, Billet Cutting Logs
- **Quality Control** — Quality Checks with pass/fail results, Customer Drawings
- **Die Management** — Die Master, Die Maintenance Logs, Die Health Dashboard
- **Furnace & Aging** — Furnace Logs with temperature readings, Aging Oven Logs
- **Surface Treatment** — Surface Treatment Orders
- **Shift Reporting** — Production Shift Reports, Shift Job Card Details
- **Scrap Management** — Scrap Records
- **4 Custom Dashboards** — Plant Home, Aluminium Dashboard, Kanban Board, Die Room Dashboard
- **9 Reports** — Daily Production Summary, Press Efficiency, Scrap Analysis, Order-to-Dispatch Tracker, and more
- **Workspace** — Dedicated Aluminium Manufacturing workspace with shortcuts

## Installation

### On a self-hosted bench

```bash
cd /path/to/frappe-bench
bench get-app https://github.com/jajulasandeep583/kali.git
bench --site your-site.local install-app kali
bench --site your-site.local migrate
```

### On Frappe Cloud

1. Go to your Frappe Cloud dashboard
2. Add this app via **Apps > Add App**
3. Use the repository URL: `https://github.com/jajulasandeep583/kali.git`
4. Install the app on your site

## Requirements

- Frappe Framework v16+
- ERPNext v16+ (recommended for Sales Order integration)

## Custom DocTypes

| DocType | Description |
|---------|-------------|
| Extrusion Job Card | Main production job tracking |
| Billet Receipt | Raw material intake |
| Billet Cutting Log | Billet cutting operations |
| Press Log | Extrusion press run data |
| Furnace Log | Furnace operation records |
| Furnace Temp Reading | Temperature readings (child table) |
| Aging Oven Log | Aging oven operation records |
| Aging Temp Reading | Aging temperature readings (child table) |
| Die Master | Die inventory and specifications |
| Die Maintenance Log | Die repair and maintenance |
| Quality Check | QC results per job |
| Customer Drawing | Customer-supplied drawings |
| Surface Treatment Order | Anodising/powder coating orders |
| Production Shift Report | Shift-level production summary |
| Shift Job Card Detail | Job details per shift (child table) |
| Scrap Record | Scrap material tracking |
| Test Employee | Test/demo doctype |

## License

MIT — see [license.txt](license.txt)