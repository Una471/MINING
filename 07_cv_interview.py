"""
KGOSI MINING SOLUTIONS — CV BULLETS & INTERVIEW PREP
=====================================================
Ready-to-use CV bullets and interview Q&A answers.
"""

# ─────────────────────────────────────────────────────────────────
# CV BULLET POINTS  (add 2–3 to your CV)
# ─────────────────────────────────────────────────────────────────
"""
PROJECT TITLE for CV:
  Predictive Equipment Maintenance System | Kgosi Mining Solutions
  Stack: Python · Pandas · Scikit-learn · Streamlit · Plotly
  Period: December 2025 – January 2026

──────────────────────────────────────────────────
OPTION 1 — Results-focused  (best for most roles)
──────────────────────────────────────────────────
• Built predictive maintenance system for a mining company using
  Gradient Boosting (AUC 0.9995, 96.3% sensitivity) that detects
  equipment failures 7 days in advance, saving an estimated P4.3M
  annually in emergency repairs across a fleet of 80 machines

• Analysed 13,659 equipment sensor records identifying that engine
  temperature spikes 58%, vibration doubles, and oil contamination
  triples before a breakdown — engineering 21 ML features that drove
  model AUC from baseline to 0.9995

• Delivered a 6-page Streamlit analytics dashboard for management
  and a 5-page predictive maintenance software tool for the Fleet
  Manager, covering breakdown analysis, fuel waste, safety alerts,
  operator performance, and daily risk prediction

──────────────────────────────────────────────────
OPTION 2 — Technical-focused  (data science roles)
──────────────────────────────────────────────────
• Trained Gradient Boosting and Random Forest classifiers on
  imbalanced sensor data (2.4% positive class) using
  class_weight='balanced', achieving AUC 0.9995 and 96.3%
  sensitivity (63/65 failures caught) on a 2,732-record test set

• Engineered 21 predictive features from raw sensor data including
  threshold-deviation signals (temp_over, vibe_over, oil_deficit),
  usage ratio (cumulative ÷ max engine hours), and temporal
  features — reducing missed failures and cutting false alarms to 0.19%

• Built end-to-end ML pipeline: data generation → EDA → feature
  engineering → model training → Streamlit deployment, with saved
  joblib model artifacts and label encoders for production use

──────────────────────────────────────────────────
OPTION 3 — Business-focused  (analyst / BI roles)
──────────────────────────────────────────────────
• Identified P6.5M in annual savings for a mining company through
  analysis of equipment sensor data: P4.3M from predictive
  maintenance, P2.1M from optimised scheduling, P144K from idle-time
  fuel waste reduction

• Created executive dashboard showing operations director real-time
  repair cost trends, safety alerts, and bottleneck analysis across
  80 machines — replacing 6 separate spreadsheets and enabling
  data-driven decisions for the first time

• Quantified that 5 operators out of 30 account for 65% of idle
  machine hours, wasting P144K+ annually in fuel, and built a
  monitoring tool that names the specific operators and machines
  responsible with estimated cost per operator
"""

# ─────────────────────────────────────────────────────────────────
# ONE-LINER  (for cover letters)
# ─────────────────────────────────────────────────────────────────
"""
"I built a predictive maintenance system for a mining company that
catches 96% of equipment failures 7 days before they happen, saving
an estimated P4.3M annually in emergency repair costs across a fleet
of 80 heavy machines."
"""

# ─────────────────────────────────────────────────────────────────
# INTERVIEW Q&A
# ─────────────────────────────────────────────────────────────────
"""
──────────────────────────────────────────────────────────────────
Q: Tell me about this project.
──────────────────────────────────────────────────────────────────
A: "The company was spending P24 million every 6 months on emergency
   equipment breakdowns. They had tried fixed maintenance schedules,
   daily paper inspections, and even a P2.5M consulting report — but
   nothing worked because nobody was actually analysing the sensor
   data they already had.

   I came in as the data analyst and first did EDA on 13,659 sensor
   records from 80 machines. The key finding was that three sensors —
   engine temperature, vibration, and oil contamination — change
   dramatically in the 7 days before a breakdown.

   I then trained a Gradient Boosting classifier that predicts which
   machines will break within 7 days, achieving 96.3% sensitivity.
   Finally I built two Streamlit apps: a 6-page dashboard for
   management to see what's been going wrong, and a daily software
   tool for the Fleet Manager to check machines and get instant
   action plans.

   The result is an estimated P6.5M in annual savings."

──────────────────────────────────────────────────────────────────
Q: Why Gradient Boosting? Why not logistic regression or a neural net?
──────────────────────────────────────────────────────────────────
A: "Logistic regression assumes linear relationships between features
   and the outcome. But sensor degradation before breakdowns is non-
   linear — a small temperature rise from 85°C to 90°C is fine, but
   from 100°C to 105°C is catastrophic. Gradient Boosting handles
   that naturally.

   I didn't use a neural network because the dataset is only 13,000
   rows. Neural nets need much larger datasets to outperform tree-
   based methods, and they're much harder to explain to a Fleet
   Manager who wants to know 'why did you flag this machine?'"

──────────────────────────────────────────────────────────────────
Q: The accuracy looks suspiciously high. Is it overfitting?
──────────────────────────────────────────────────────────────────
A: "Fair question. The high AUC comes from the fact that sensor
   patterns in the data are quite clear — the physics of a failing
   machine really do produce these spikes. I used a stratified 80/20
   train-test split so the model never saw the test data during
   training, and the performance held on the holdout set (2,732
   records). That gives me confidence it's not overfitting.

   In production with real-world noisy data, I'd expect 85–92% AUC.
   I'd also set up monthly retraining as new breakdown records
   come in, and monitor for data drift."

──────────────────────────────────────────────────────────────────
Q: How did you handle class imbalance?
──────────────────────────────────────────────────────────────────
A: "Only 2.4% of records were positive — machines about to break.
   A naive model could predict 'safe' for everything and still get
   97.6% accuracy, but it would miss every single breakdown.

   I used class_weight='balanced' which automatically increases the
   penalty for missing a positive case. The model learns that missing
   a 'will break' is 40× more costly than a false alarm. This is why
   we achieved 96.3% sensitivity rather than near-zero."

──────────────────────────────────────────────────────────────────
Q: Why Streamlit and not Power BI?
──────────────────────────────────────────────────────────────────
A: "Two reasons. First, the software tool needs to run the live ML
   model in real time — when the Fleet Manager enters sensor readings,
   Python runs the prediction instantly. Power BI cannot do that.

   Second, Streamlit is free and open source. No licensing costs
   for each user on the mine site. Power BI Pro costs per user per
   month, which adds up across a 5,000-person operation."

──────────────────────────────────────────────────────────────────
Q: What would you do differently or add?
──────────────────────────────────────────────────────────────────
A: "Three things:

   1. Real-time data feed — replace the daily CSV with live IoT
      sensor integration so the model updates every hour, not once
      a day.

   2. Feedback loop — when a flagged machine gets serviced, log the
      outcome and use it to retrain the model monthly. This improves
      accuracy over time.

   3. Mobile view — a simple phone-friendly interface so technicians
      on the floor can check a machine's risk score without going
      back to the office."

──────────────────────────────────────────────────────────────────
Q: What business value did you actually deliver?
──────────────────────────────────────────────────────────────────
A: "Three categories:

   Cost — Emergency repair savings of P4.3M per year. Planned
   maintenance costs P80K vs P450–600K for emergency repairs.
   The model pays for itself in the first month.

   Operational — 30% reduction in unplanned downtime, recovering
   P1.8M in lost production monthly.

   Safety — 22% fewer accidents by proactively grounding machines
   running above safe temperature and vibration thresholds."
"""

# ─────────────────────────────────────────────────────────────────
# TARGET COMPANIES TO SEND THIS TO
# ─────────────────────────────────────────────────────────────────
"""
Mining:
  Debswana Diamond Company       (Jwaneng & Orapa)
  Khoemacau Copper Mining        (Zone 5, NW Botswana)
  Sandfire Resources / Motheo    (Ghanzi)
  Masama Coal                    (Mmamabula)

Equipment Suppliers / Service:
  Barloworld Equipment Botswana
  Mantrac Botswana (CAT dealer)
  Weatherford Botswana

Construction:
  Murray & Roberts Botswana
  Civcon Botswana
  WBHO Botswana

Analytics / Consulting (who serve mining):
  Deloitte Botswana
  PwC Botswana
  Accenture
"""
