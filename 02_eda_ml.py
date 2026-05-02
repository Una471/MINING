"""
KGOSI MINING SOLUTIONS — EDA & ML MODEL TRAINING
Run this SECOND after 01_generate_data.py
Analyses the data and trains the breakdown prediction model.
"""

import pandas as pd
import numpy as np
import os, json, joblib, warnings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import LabelEncoder
warnings.filterwarnings("ignore")

print("=" * 60)
print("KGOSI MINING — EDA & MODEL TRAINING")
print("=" * 60)

df  = pd.read_csv("equipment_data.csv")
print(f"\n📂 Loaded {len(df):,} records | {df['machine_id'].nunique()} machines")

# ─── PART 1: EDA ─────────────────────────────────────────────────
print("\n" + "─"*60)
print("PART 1 — EXPLORATORY DATA ANALYSIS")
print("─"*60)

print(f"\n[1] Shape        : {df.shape}")
print(f"[1] Date range   : {df['date'].min()} → {df['date'].max()}")
print(f"[1] Missing vals : {df.isnull().sum().sum()}")

print(f"\n[2] BREAKDOWNS")
print(f"    Total events     : {df['breakdown'].sum()}")
print(f"    Breakdown rate   : {df['breakdown'].mean()*100:.2f}%")
print(f"    Total repair cost: P{df['repair_cost_bwp'].sum():,.0f}")
print(f"    Avg cost/event   : P{df[df['breakdown']==1]['repair_cost_bwp'].mean():,.0f}")

print(f"\n[3] BREAKDOWNS BY MACHINE TYPE:")
bd = df.groupby("machine_type").agg(
    count=("record_id","count"),
    breakdowns=("breakdown","sum"),
    repair_cost=("repair_cost_bwp","sum")
).sort_values("breakdowns", ascending=False)
print(bd.to_string())

print(f"\n[4] SENSOR READINGS — NORMAL vs BREAKDOWN:")
sensors = ["engine_temp_c","vibration","oil_pressure_psi","oil_contamination_ppm","days_since_maintenance"]
for s in sensors:
    nm = df[df["breakdown"]==0][s].mean()
    bk = df[df["breakdown"]==1][s].mean()
    ch = (bk-nm)/nm*100
    arrow = "↑" if ch > 0 else "↓"
    print(f"    {s:<35} Normal: {nm:>7.2f}  | Breakdown: {bk:>7.2f}  {arrow}{abs(ch):.0f}%")

print(f"\n[5] FUEL & IDLE ANALYSIS:")
total_idle = df["idle_hours"].sum()
idle_waste = total_idle * 35 * 14.50 * 0.35
print(f"    Total idle hours   : {total_idle:,.1f} hrs")
print(f"    Estimated wasted   : P{idle_waste:,.0f}")
print(f"    Total fuel cost    : P{df['fuel_cost_bwp'].sum():,.0f}")

print(f"\n[6] SAFETY RISK:")
for r in ["Critical","High","Medium","Low"]:
    c = (df["safety_risk"]==r).sum()
    print(f"    {r:<10}: {c:>6,}  ({c/len(df)*100:.1f}%)")

print(f"\n[7] MAINTENANCE OVERDUE (>150 days):")
od = df[df["days_since_maintenance"] > 150]
print(f"    Overdue records    : {len(od):,}")
print(f"    Unique machines    : {od['machine_id'].nunique()}")
print(f"    Avg days overdue   : {od['days_since_maintenance'].mean():.0f}")

print(f"\n[8] TOP 5 OPERATORS BY IDLE HOURS:")
op_idle = df.groupby("operator_id")["idle_hours"].sum().sort_values(ascending=False).head(5)
for op, hrs in op_idle.items():
    waste = hrs * 35 * 14.50 * 0.35
    print(f"    {op}: {hrs:.0f} hrs  →  P{waste:,.0f} wasted")

# ─── PART 2: FEATURE ENGINEERING ─────────────────────────────────
print("\n" + "─"*60)
print("PART 2 — FEATURE ENGINEERING")
print("─"*60)

df["date_dt"]       = pd.to_datetime(df["date"])
df["day_of_week"]   = df["date_dt"].dt.dayofweek
df["month"]         = df["date_dt"].dt.month
df["is_night"]      = df["shift"].str.startswith("Night").astype(int)
df["temp_over"]     = (df["engine_temp_c"] - 90).clip(lower=0)
df["vibe_over"]     = (df["vibration"] - 4.0).clip(lower=0)
df["oil_deficit"]   = (60 - df["oil_pressure_psi"]).clip(lower=0)
df["contam_flag"]   = (df["oil_contamination_ppm"] > 3.0).astype(int)

TYPE_MAX = {"Excavator":5000,"Haul Truck":8000,"Drill Rig":4000,"Loader":6000,
            "Crusher":7000,"Dozer":5500,"Grader":5000,"Water Truck":6000,
            "Compressor":4500,"Conveyor Belt":9000}
df["usage_ratio"] = df.apply(
    lambda r: min(r["cumulative_hours"] / TYPE_MAX.get(r["machine_type"], 6000), 1.0), axis=1)

le_type = LabelEncoder(); df["type_enc"] = le_type.fit_transform(df["machine_type"])
le_site = LabelEncoder(); df["site_enc"] = le_site.fit_transform(df["site"])

print("  ✅ Created: day_of_week, month, is_night")
print("  ✅ Created: temp_over, vibe_over, oil_deficit, contam_flag")
print("  ✅ Created: usage_ratio, type_enc, site_enc")

# ─── PART 3: ML MODEL ────────────────────────────────────────────
print("\n" + "─"*60)
print("PART 3 — MACHINE LEARNING")
print("─"*60)

FEATURES = [
    "age_years","hours_today","cumulative_hours","days_since_maintenance",
    "engine_temp_c","vibration","oil_pressure_psi","oil_contamination_ppm",
    "battery_voltage","idle_hours","maintenance_due","type_enc","site_enc",
    "day_of_week","month","is_night","temp_over","vibe_over","oil_deficit",
    "contam_flag","usage_ratio",
]
TARGET = "will_break_7days"

X, y = df[FEATURES], df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

print(f"\n  Train: {len(X_train):,}  |  Test: {len(X_test):,}")
print(f"  Positives: {y.sum():,}  ({y.mean()*100:.2f}%)")

print("\n  Training Gradient Boosting...")
gb = GradientBoostingClassifier(n_estimators=150, learning_rate=0.08, max_depth=5, random_state=42)
gb.fit(X_train, y_train)
gb_pred  = gb.predict(X_test)
gb_proba = gb.predict_proba(X_test)[:,1]
gb_auc   = roc_auc_score(y_test, gb_proba)

print("\n  Training Random Forest...")
rf = RandomForestClassifier(n_estimators=200, max_depth=12, class_weight="balanced", random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_pred  = rf.predict(X_test)
rf_proba = rf.predict_proba(X_test)[:,1]
rf_auc   = roc_auc_score(y_test, rf_proba)

# Pick best
if gb_auc >= rf_auc:
    best, best_pred, best_proba, best_auc, best_name = gb, gb_pred, gb_proba, gb_auc, "GradientBoosting"
else:
    best, best_pred, best_proba, best_auc, best_name = rf, rf_pred, rf_proba, rf_auc, "RandomForest"

print(f"\n  GB AUC : {gb_auc:.4f}")
print(f"  RF AUC : {rf_auc:.4f}")
print(f"  Winner : {best_name}")
print(f"\n{classification_report(y_test, best_pred, target_names=['Safe','Will Break'])}")

cm = confusion_matrix(y_test, best_pred)
tn,fp,fn,tp = cm.ravel()
print(f"  Sensitivity: {tp/(tp+fn)*100:.1f}%  (of machines about to break, we catch this many)")
print(f"  False alarms: {fp/(fp+tn)*100:.2f}%")

print(f"\n  TOP 10 FEATURES:")
fi = pd.DataFrame({"feature":FEATURES,"importance":best.feature_importances_}).sort_values("importance",ascending=False)
for _,r in fi.head(10).iterrows():
    bar = "█" * int(r["importance"]*150)
    print(f"  {r['feature']:<30} {bar}  {r['importance']:.4f}")

# ─── PART 4: SCORE ALL MACHINES ──────────────────────────────────
print("\n" + "─"*60)
print("PART 4 — SCORING ALL MACHINES")
print("─"*60)

latest = df.sort_values("date").groupby("machine_id").last().reset_index()
latest["fail_prob"] = best.predict_proba(latest[FEATURES])[:,1]
latest["risk_level"] = pd.cut(latest["fail_prob"],
    bins=[0,0.25,0.55,0.80,1.0], labels=["Low","Medium","High","Critical"])

rc = latest["risk_level"].value_counts()
print(f"\n  🔴 Critical : {rc.get('Critical',0)}")
print(f"  🟠 High     : {rc.get('High',0)}")
print(f"  🟡 Medium   : {rc.get('Medium',0)}")
print(f"  🟢 Low      : {rc.get('Low',0)}")

# ─── PART 5: SAVE ────────────────────────────────────────────────
print("\n" + "─"*60)
print("PART 5 — SAVING")
print("─"*60)

joblib.dump(best,    "model.pkl")
joblib.dump(le_type, "le_type.pkl")
joblib.dump(le_site, "le_site.pkl")

with open("features.json","w") as f: json.dump(FEATURES, f)

meta = {"model":best_name,"auc":round(best_auc,4),"sensitivity":round(tp/(tp+fn),4),
        "features":FEATURES,"trained":str(pd.Timestamp.now().date())}
with open("model_meta.json","w") as f: json.dump(meta, f, indent=2)

latest[["machine_id","machine_type","site","age_years","cumulative_hours",
        "days_since_maintenance","engine_temp_c","vibration","oil_pressure_psi",
        "fail_prob","risk_level","idle_hours","fuel_cost_bwp","safety_risk"]
      ].to_csv("risk_scores.csv", index=False)

print("  ✅ model.pkl")
print("  ✅ le_type.pkl  /  le_site.pkl")
print("  ✅ features.json  /  model_meta.json")
print("  ✅ risk_scores.csv")
print("\nNext:")
print("  streamlit run 03_dashboard.py --server.port 8501")
print("  streamlit run 04_software.py  --server.port 8502")
print("=" * 60)
