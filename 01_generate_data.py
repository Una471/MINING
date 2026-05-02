"""
KGOSI MINING SOLUTIONS — DATA GENERATOR
Run this FIRST before anything else.
Generates 6 months of realistic equipment sensor data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random, os

np.random.seed(42)
random.seed(42)

print("=" * 60)
print("KGOSI MINING — GENERATING EQUIPMENT DATA")
print("=" * 60)

EQUIPMENT = {
    "Excavator":     {"count": 12, "fuel_rate": 35, "max_hours": 5000, "base_vibe": 2.1},
    "Haul Truck":    {"count": 20, "fuel_rate": 55, "max_hours": 8000, "base_vibe": 1.8},
    "Drill Rig":     {"count": 8,  "fuel_rate": 28, "max_hours": 4000, "base_vibe": 3.5},
    "Loader":        {"count": 10, "fuel_rate": 30, "max_hours": 6000, "base_vibe": 2.0},
    "Crusher":       {"count": 4,  "fuel_rate": 45, "max_hours": 7000, "base_vibe": 4.2},
    "Dozer":         {"count": 8,  "fuel_rate": 32, "max_hours": 5500, "base_vibe": 2.3},
    "Grader":        {"count": 6,  "fuel_rate": 22, "max_hours": 5000, "base_vibe": 1.6},
    "Water Truck":   {"count": 6,  "fuel_rate": 25, "max_hours": 6000, "base_vibe": 1.5},
    "Compressor":    {"count": 4,  "fuel_rate": 18, "max_hours": 4500, "base_vibe": 3.8},
    "Conveyor Belt": {"count": 2,  "fuel_rate": 8,  "max_hours": 9000, "base_vibe": 2.9},
}

SITES    = ["Shaft A", "Shaft B", "Open Pit", "Processing Plant", "Waste Dump"]
SHIFTS   = ["Morning (06:00-14:00)", "Afternoon (14:00-22:00)", "Night (22:00-06:00)"]
OPS      = [f"OP{str(i).zfill(3)}" for i in range(1, 31)]

# Build machine list
machines, mid = [], 1
for etype, cfg in EQUIPMENT.items():
    for n in range(cfg["count"]):
        yr = random.randint(2012, 2021)
        machines.append({
            "machine_id":   f"KMS-{str(mid).zfill(3)}",
            "machine_type": etype,
            "age_years":    2026 - yr,
            "site":         random.choice(SITES),
            "fuel_rate":    cfg["fuel_rate"],
            "max_hours":    cfg["max_hours"],
            "base_vibe":    cfg["base_vibe"],
            "failure_risk": min(0.02 + (2026 - yr) * 0.008, 0.18),
        })
        mid += 1

machine_df = pd.DataFrame(machines)
records    = []
START, END = datetime(2025, 7, 1), datetime(2025, 12, 31)

for _, m in machine_df.iterrows():
    cur_date          = START
    cum_hours         = random.randint(200, int(m["max_hours"] * 0.6))
    days_since_maint  = random.randint(0, 120)
    oil_press_base    = random.uniform(55, 75)
    fail_countdown    = 0

    while cur_date <= END:
        if random.random() < 0.07:
            cur_date += timedelta(days=1); continue

        hours_today       = round(random.uniform(6, 12), 1)
        cum_hours        += hours_today
        days_since_maint += 1
        maint_factor      = min(days_since_maint / 180, 1.0)

        if fail_countdown > 0:
            fail_countdown -= 1; pre_fail = True
        else:
            pre_fail = False

        if not pre_fail and random.random() < (m["failure_risk"] + maint_factor * 0.04) / 30:
            fail_countdown = random.randint(5, 10); pre_fail = True

        if pre_fail:
            sp = fail_countdown / 10
            temperature        = round(random.uniform(95 + (1-sp)*20, 130), 1)
            vibration          = round(m["base_vibe"] + random.uniform(2.0, 5.0)*(1-sp), 2)
            oil_pressure       = round(oil_press_base - random.uniform(8, 20)*(1-sp), 1)
            oil_contamination  = round(random.uniform(3.5, 8.0), 2)
            battery_voltage    = round(random.uniform(11.0, 12.5), 2)
        else:
            temperature        = round(random.uniform(65, 88), 1)
            vibration          = round(m["base_vibe"] + random.uniform(-0.3, 0.8), 2)
            oil_pressure       = round(oil_press_base + random.uniform(-5, 5), 1)
            oil_contamination  = round(random.uniform(0.5, 2.5), 2)
            battery_voltage    = round(random.uniform(13.0, 14.5), 2)

        op_idx      = int(random.choice(OPS)[2:])
        idle_tend   = 0.4 if op_idx % 5 == 0 else 0.15
        idle_hours  = round(random.uniform(0, hours_today * idle_tend), 2)
        active_hrs  = hours_today - idle_hours
        fuel_lit    = round((active_hrs * m["fuel_rate"]) + (idle_hours * m["fuel_rate"] * 0.35) + random.uniform(-10,10), 1)
        fuel_cost   = round(fuel_lit * 14.50, 2)

        breakdown = 0
        if pre_fail and fail_countdown == 0:
            breakdown = 1; days_since_maint = 0; oil_press_base = random.uniform(55,75)

        will_break = 1 if (pre_fail and 0 < fail_countdown <= 7) else 0

        safety = ("Critical" if temperature > 115 or vibration > 6.5 else
                  "High"     if temperature > 105 or vibration > 5.0 else
                  "Medium"   if temperature > 95  or vibration > 4.0 else "Low")

        records.append({
            "record_id":               f"R{str(len(records)+1).zfill(7)}",
            "machine_id":              m["machine_id"],
            "machine_type":            m["machine_type"],
            "date":                    cur_date.strftime("%Y-%m-%d"),
            "shift":                   random.choice(SHIFTS),
            "operator_id":             random.choice(OPS),
            "site":                    m["site"],
            "age_years":               m["age_years"],
            "hours_today":             hours_today,
            "cumulative_hours":        round(cum_hours, 1),
            "days_since_maintenance":  days_since_maint,
            "engine_temp_c":           temperature,
            "vibration":               vibration,
            "oil_pressure_psi":        oil_pressure,
            "oil_contamination_ppm":   oil_contamination,
            "battery_voltage":         battery_voltage,
            "idle_hours":              idle_hours,
            "active_hours":            round(active_hrs, 2),
            "fuel_litres":             fuel_lit,
            "fuel_cost_bwp":           fuel_cost,
            "maintenance_due":         int(days_since_maint > 150),
            "breakdown":               breakdown,
            "repair_cost_bwp":         round(random.uniform(350000, 600000), 2) if breakdown else 0.0,
            "safety_risk":             safety,
            "will_break_7days":        will_break,
        })
        cur_date += timedelta(days=1)

df = pd.DataFrame(records)
df.to_csv("equipment_data.csv", index=False)
machine_df.to_csv("machine_registry.csv", index=False)

print(f"\n✅  Records     : {len(df):,}")
print(f"✅  Machines    : {df['machine_id'].nunique()}")
print(f"✅  Date range  : {df['date'].min()}  →  {df['date'].max()}")
print(f"✅  Breakdowns  : {df['breakdown'].sum()}")
print(f"✅  Safety flags: {(df['safety_risk'].isin(['High','Critical'])).sum():,}")
print(f"✅  Repair costs: P{df['repair_cost_bwp'].sum():,.0f}")
print(f"✅  Fuel costs  : P{df['fuel_cost_bwp'].sum():,.0f}")
print(f"\n💾  Saved: equipment_data.csv  &  machine_registry.csv")
print("\nNext: run  python 02_eda_ml.py")
print("=" * 60)
