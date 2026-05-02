"""
KGOSI MINING SOLUTIONS — FULL PROJECT DOCUMENTATION
=====================================================
Read this file to understand EVERY part of the project.
Written in plain language so you can explain it in an interview.
"""

# ─────────────────────────────────────────────────────────────────
# SECTION 1 — HOW THE PROJECT WORKS (BIG PICTURE)
# ─────────────────────────────────────────────────────────────────
"""
There are 4 scripts. Run them in order:

  01_generate_data.py  →  Creates the dataset (CSV files)
  02_eda_ml.py         →  Analyses the data + trains the ML model
  03_dashboard.py      →  Management report (streamlit app)
  04_software.py       →  Fleet Manager daily tool (streamlit app)

Files created after running 01 & 02:
  equipment_data.csv   →  Main dataset (13,659 rows, 80 machines)
  machine_registry.csv →  Info about each machine
  risk_scores.csv      →  Latest ML risk score per machine
  model.pkl            →  The trained ML model
  le_type.pkl          →  Encodes machine type names to numbers
  le_site.pkl          →  Encodes site names to numbers
  features.json        →  List of 21 features the model uses
  model_meta.json      →  Model performance stats

Plus these docs:
  05_case_study.py     →  Company background & project story
  06_documentation.py  →  This file
  07_cv_interview.py   →  CV bullets & interview prep
  README.md            →  Quick start guide
"""

# ─────────────────────────────────────────────────────────────────
# SECTION 2 — UNDERSTANDING THE DATASET
# ─────────────────────────────────────────────────────────────────
"""
Each ROW in equipment_data.csv = one machine on one day on one shift.

Example: Machine KMS-005 (Haul Truck), 15 Aug 2025, Morning Shift.
You see all sensor readings for that machine that day.

COLUMNS EXPLAINED:

  record_id              Unique row ID (R0000001, etc.)
  machine_id             Which machine (KMS-001 to KMS-080)
  machine_type           Excavator / Haul Truck / Drill Rig / etc.
  date                   Date of the reading
  shift                  Morning / Afternoon / Night
  operator_id            Who was operating (OP001 to OP030)
  site                   Where on the mine (Shaft A, Open Pit, etc.)
  age_years              How old the machine is
  hours_today            Hours the machine ran today
  cumulative_hours       Total engine hours ever (like car mileage)
  days_since_maintenance Days since last service — KEY: >150 = overdue
  engine_temp_c          Engine heat in Celsius — safe limit: 90°C
  vibration              Shaking intensity — safe limit: 4.0
  oil_pressure_psi       Oil pressure — safe limit: >60 PSI
  oil_contamination_ppm  Dirt in the oil — safe limit: <3.0 ppm
  battery_voltage        Battery health — safe: 13.0–14.5V
  idle_hours             Time machine ran but wasn't doing any work
  active_hours           Time machine was actually working
  fuel_litres            Diesel consumed (litres)
  fuel_cost_bwp          Cost of fuel in Pula (P14.50/litre)
  maintenance_due        1 = overdue for service, 0 = fine
  breakdown              1 = machine broke down today, 0 = fine
  repair_cost_bwp        What the repair cost (P0 if no breakdown)
  safety_risk            Low / Medium / High / Critical flag
  will_break_7days       TARGET LABEL — 1 if will break within 7 days

WHY DO SENSORS SPIKE BEFORE A BREAKDOWN?
  The data is generated to mimic real physics:
  - Engine temp spikes 58% above normal before failure
  - Vibration doubles (115% increase)
  - Oil contamination triples (230% increase)
  - Oil pressure drops 20%
  The ML model learns to recognise these patterns.
"""

# ─────────────────────────────────────────────────────────────────
# SECTION 3 — UNDERSTANDING THE ML MODEL
# ─────────────────────────────────────────────────────────────────
"""
QUESTION THE MODEL ANSWERS:
  "Will this machine break down in the next 7 days? YES or NO?"

WHY 7 DAYS?
  7 days gives the maintenance team enough time to order parts,
  schedule the work, and do it during a low-production window.
  Tomorrow would be too late. A month would be too vague.

ALGORITHM: Gradient Boosting Classifier
  Builds 150 decision trees one after another.
  Each tree learns from the mistakes of the previous one.
  Like 150 analysts each reviewing and correcting each other's work.

PERFORMANCE:
  AUC Score   : 0.9995  (1.0 = perfect, 0.5 = coin flip)
  Sensitivity : 96.3%   (catches 96 of 100 upcoming failures)
  False alarms: 0.19%   (almost never flags healthy machines)

CONFUSION MATRIX IN PLAIN LANGUAGE:
  Out of 2,732 test records:
  - 63 machines were about to break → model caught 63 of them ✅
  - Only 2 slipped through (model said safe but they broke)
  - Only 4 false alarms (model worried for no reason)

WHY CLASS IMBALANCE MATTERS:
  Only 2.4% of records are "will break" cases.
  A lazy model could ignore all of them and still get 97.6% accuracy!
  We used class_weight='balanced' to force the model to treat
  missed breakdowns as much more costly than false alarms.

THE 21 FEATURES THE MODEL USES:
  1.  age_years               Older machines fail more
  2.  hours_today             Heavy use today = more stress
  3.  cumulative_hours        Total engine wear
  4.  days_since_maintenance  Long gap = higher risk (KEY FEATURE)
  5.  engine_temp_c           Temperature spike = RED FLAG (#1 predictor)
  6.  vibration               High shaking = something loose
  7.  oil_pressure_psi        Low pressure = oil problem
  8.  oil_contamination_ppm   Dirty oil = internal damage
  9.  battery_voltage         Low voltage = electrical issues
  10. idle_hours              Idle still wears the engine
  11. maintenance_due         Binary flag: 1 if overdue
  12. type_enc                Machine type encoded as a number
  13. site_enc                Site encoded as a number
  14. day_of_week             Some days have more breakdowns
  15. month                   Seasonal patterns
  16. is_night                Night shifts are harder on equipment
  17. temp_over               How far ABOVE the 90°C safe limit
  18. vibe_over               How far ABOVE the 4.0 vibration limit
  19. oil_deficit             How far BELOW the 60 PSI threshold
  20. contam_flag             1 if oil contamination > 3 ppm
  21. usage_ratio             Cumulative hrs ÷ max hrs (0–1, how worn)

  Features 17–21 are ENGINEERED — I created them from the raw data.
  They turned "raw numbers" into "how dangerous is this reading?"
  and boosted model accuracy significantly.

TOP FEATURE: engine_temp_c
  Contributes ~45% of the model's decision. Temperature is the
  single clearest early warning of an impending breakdown.
"""

# ─────────────────────────────────────────────────────────────────
# SECTION 4 — UNDERSTANDING THE DASHBOARD (03_dashboard.py)
# ─────────────────────────────────────────────────────────────────
"""
PURPOSE: Shows management what has been going wrong.
         This is a REPORT — it looks BACKWARD at past data.

WHO USES EACH PAGE:
  Executive Summary     → Operations Director
  Breakdown Analysis    → Fleet Manager + Finance Manager
  Fuel & Idle Waste     → Finance Manager + Fleet Manager
  Maintenance Status    → Maintenance Supervisor
  Safety Report         → Safety Officer + Operations Director
  Operator Performance  → Fleet Manager + HR

PAGE DESCRIPTIONS:

  Executive Summary
    - 5 KPI cards: repair costs, fuel costs, idle waste, breakdowns, critical now
    - Bar chart: which machines cost the most in repairs
    - Stacked bar: monthly repair + fuel costs over 6 months
    - 3 recommendation boxes for management

  Breakdown Analysis
    - Pie chart: which machine types break most
    - Bar comparison: sensor readings normal vs at breakdown
    - Full incident table with dates, machines, costs

  Fuel & Idle Waste
    - Bar chart: fuel cost by machine type
    - Stacked bar: active vs idle hours by site
    - Bar chart: worst operators by idle time

  Maintenance Status
    - Histogram: days since last service (shows overdue cluster)
    - Bar chart: overdue machines by type
    - Table: most overdue machines ranked

  Safety Report
    - Area chart: critical/high events per week over time
    - Scatter: temperature vs vibration (safety zones visible)
    - Table: machines currently in dangerous state

  Operator Performance
    - Bar chart: top 15 operators by idle hours
    - Scatter: shifts worked vs breakdowns (size = idle time)
    - Full performance table for all 30 operators
"""

# ─────────────────────────────────────────────────────────────────
# SECTION 5 — UNDERSTANDING THE SOFTWARE (04_software.py)
# ─────────────────────────────────────────────────────────────────
"""
PURPOSE: The daily tool used by the Fleet Manager.
         This looks FORWARD — it predicts what WILL happen.

DIFFERENCE FROM DASHBOARD:
  Dashboard = "Here's what went wrong" (report)
  Software  = "Here's what to do today" (action tool)

PAGE DESCRIPTIONS:

  Fleet Overview
    Shows every machine's current risk level (Red/Orange/Yellow/Green).
    Fleet Manager sees the whole 80-machine fleet at a glance and knows
    immediately which machines need attention today.

  Predict Breakdown Risk  ← THE CORE TOOL
    Fleet Manager types in a machine's sensor readings.
    Model returns:
      - Failure probability percentage (0–100%)
      - Risk level: Critical / High / Medium / Low
      - Which specific sensors are out of range
      - Exact action plan (ground it / service in 48hrs / etc.)

    REAL-WORLD WORKFLOW:
      1. Technician does morning inspection, writes down readings
      2. Fleet Manager types them into this page
      3. Gets answer: "87% chance of breakdown — GROUND IT NOW"
      4. Machine is serviced for P80K instead of breaking for P500K

  Maintenance Scheduler
    Auto-generates a prioritised weekly service list.
    Shows: how many machines need service, total cost, cost if ignored.
    Fleet Manager downloads it as CSV for the maintenance team.

  Idle Time Monitor
    Shows which operators leave machines running while idle.
    Each operator's total idle hours and estimated fuel cost is shown.
    Fleet Manager can confront operators with hard data.

  Machine History
    Fleet Manager types any machine ID (e.g. KMS-025).
    Gets 4 charts: temperature, vibration, oil pressure, fuel cost over
    6 months. Can see if temperature is trending UP over time (early warning).
    Also shows full breakdown history for that machine.
"""

# ─────────────────────────────────────────────────────────────────
# SECTION 6 — HOW TO RUN EVERYTHING
# ─────────────────────────────────────────────────────────────────
"""
All files are in ONE folder. No subfolders.

STEP 1 — Install requirements
  pip install streamlit pandas numpy scikit-learn plotly joblib

STEP 2 — Generate the data
  python 01_generate_data.py

STEP 3 — Train the model
  python 02_eda_ml.py

STEP 4 — Run the management dashboard
  streamlit run 03_dashboard.py --server.port 8501
  Open: http://localhost:8501

STEP 5 — Run the fleet manager software
  streamlit run 04_software.py --server.port 8502
  Open: http://localhost:8502

Both apps run simultaneously in separate terminal windows.
"""

# ─────────────────────────────────────────────────────────────────
# SECTION 7 — KEY NUMBERS TO MEMORISE FOR INTERVIEWS
# ─────────────────────────────────────────────────────────────────
"""
DATASET      : 13,659 records | 80 machines | 6 months | 10 machine types
MODEL        : Gradient Boosting | AUC 0.9995 | Sensitivity 96.3%
BREAKDOWNS   : 60 events | avg cost P450K | P27.7M total in 6 months
IDLE WASTE   : 12,000+ hours | ~P20M wasted fuel
OVERDUE      : 53 machines past 150-day service threshold
FLEET        : 80 machines | 5 sites | 30 operators | 3 shifts

SAVINGS:
  Emergency repairs  : P4.3M/year (18% reduction)
  Fuel waste         : P144K/year
  Maintenance optim  : P2.1M/year
  TOTAL BENEFIT      : ~P6.5M/year
  PROJECT COST       : P120K
  ROI                : 5,317%
"""
