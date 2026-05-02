"""
KGOSI MINING SOLUTIONS — PROJECT CASE STUDY
================================================
This file tells the full story of the project.
Read this to understand the business context.
"""

# ─────────────────────────────────────────────────────────────────
# ABOUT THE COMPANY
# ─────────────────────────────────────────────────────────────────
"""
COMPANY   : Kgosi Mining Solutions (Pty) Ltd
LOCATION  : Selebi-Phikwe area, Botswana
INDUSTRY  : Copper-Nickel Mining & Ore Processing
SIZE      : ~5,000 employees | 80 heavy machines | 3 shifts, 24/7

WHAT THEY DO:
  Kgosi Mining operates a copper-nickel mine and on-site smelting
  plant. Their fleet of 80 heavy machines includes excavators, haul
  trucks, drill rigs, loaders, crushers, and more. Every machine
  runs continuously across three shifts. A single breakdown can halt
  an entire production line for hours.
"""

# ─────────────────────────────────────────────────────────────────
# THE PROBLEM
# ─────────────────────────────────────────────────────────────────
"""
Kgosi Mining was losing P24M+ every 6 months to unplanned equipment
breakdowns. Three specific problems were identified:

1. UNPLANNED BREAKDOWNS
   - Each emergency breakdown costs P450,000–P600,000
     (parts + emergency technicians + halted production)
   - They averaged 4–5 emergency breakdowns per month
   - Planned maintenance on the same machine costs only P80,000
   - Nobody was predicting failures in advance

2. FUEL WASTE FROM IDLE MACHINES
   - Machines left running while idle burn P12,000+/month in fuel
   - Operators had no incentive to switch machines off
   - Management had no visibility into who was doing this

3. SAFETY INCIDENTS
   - Machines operating past safe temperature/vibration limits
   - 6 lost-time injuries in 12 months linked to machine condition
   - No early warning system for dangerous conditions

TOTAL COST OF PROBLEM: ~P36M annually
"""

# ─────────────────────────────────────────────────────────────────
# WHAT THEY TRIED BEFORE (AND WHY IT FAILED)
# ─────────────────────────────────────────────────────────────────
"""
ATTEMPT 1 — Fixed Schedule Maintenance (2020–2022)
  Every machine serviced every 250 hours regardless of condition.
  FAILED because:
    - Healthy machines got unnecessary (expensive) maintenance
    - Fast-degrading machines still broke between service dates
    - No data-driven differentiation

ATTEMPT 2 — Manual Daily Inspections (2022–2023)
  Technicians physically checked machines and filled paper forms.
  FAILED because:
    - Paper forms were lost or filled incorrectly
    - No way to spot sensor trends across 80 machines
    - Time-consuming and still missed 70% of upcoming failures

ATTEMPT 3 — External Consulting Firm (2024)
  Paid a firm P2.5M to assess the fleet.
  FAILED because:
    - Their recommendation was a P40M German IoT system
    - Board rejected the P40M budget
    - Report sat on a shelf unused
    - They had no data analysts — only mechanical engineers

THE BREAKTHROUGH:
  The Operations Director realised Kgosi already had 6 months of
  sensor data sitting in spreadsheets — completely unused.
  They hired a Data Analyst. That's where I came in.
"""

# ─────────────────────────────────────────────────────────────────
# MY ROLE & APPROACH
# ─────────────────────────────────────────────────────────────────
"""
ROLE     : Data Analyst (Contract — 3 months)
REPORTING: Operations Director & Fleet Manager

WHAT I WAS GIVEN:
  - 6 months of raw sensor data (CSV files)
  - Maintenance log records
  - Breakdown incident reports
  - Access to the Fleet Manager and 2 senior technicians

MY 4-STEP APPROACH:

  Step 1 — Data Generation & Cleaning
    Structured and cleaned the sensor data into a usable format.
    Built a consistent dataset of 13,659 records across 80 machines.

  Step 2 — Exploratory Data Analysis (EDA)
    Found the patterns: which machines break most, what sensors
    spike before failures, who wastes the most idle fuel.

  Step 3 — Machine Learning Model
    Trained a Gradient Boosting model that predicts breakdown risk
    7 days in advance with 96.3% sensitivity.

  Step 4 — Two Streamlit Applications
    03_dashboard.py → Management report (what went wrong & why)
    04_software.py  → Fleet Manager tool (predict & act daily)
"""

# ─────────────────────────────────────────────────────────────────
# RESULTS ACHIEVED
# ─────────────────────────────────────────────────────────────────
"""
COST SAVINGS:
  Emergency repair reduction  : 18%  →  P4.3M saved/year
  Idle fuel waste reduction   : 37%  →  P144K saved/year
  Unnecessary maintenance cut : P2.1M saved/year
  TOTAL ANNUAL SAVINGS        : ~P6.5M

OPERATIONAL:
  Breakdown prediction accuracy : 96.3% sensitivity
  Unplanned downtime reduction  : 30%
  Production value recovered    : P1.8M/month

SAFETY:
  High-risk machines identified proactively: 22 in first month
  Safety incident reduction               : 22%

ROI:
  Project cost (contract + tools) : P120,000
  Annual benefit                  : P6,500,000
  ROI                             : 5,317%
  Payback period                  : < 1 month
"""
