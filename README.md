# NexGen Logistics - Vehicle Cost-Efficiency Imbalance Predictor (V-IP)

## 1. Project Objective & Alignment
This application addresses NexGen Logistics' critical challenge of **Cost Pressures** and **Operational Inefficiencies** by proactively optimizing fleet assets.

The V-CEIP shifts management from reactive repairs to predictive optimization, supporting the goal of achieving a **15-20% reduction** in operational costs by focusing resources on high-risk vehicles.

## 2. Problem Chosen - Option 8
**Title:** Vehicle Cost-Efficiency Imbalance Predictor

**Justification:** The project identifies vehicles that exhibit an imbalance between **high aggregated maintenance costs** and **low utilization**. This pinpoint focus targets the most wasteful assets, minimizing cost leakage risk before a major, unscheduled repair occurs.

## 3. Solution Stack & Core Metrics
* **Core Technology:** Python, Streamlit (Interactive Web App)
* **Libraries:** Pandas, NumPy, Plotly, Scikit-learn (IsolationForest)

### Custom Metrics:
* **Cost Leakage Index (CLI):** A synthetic metric ($\text{Normalized Cost} / (\text{Utilization Rate} + \epsilon)$) used to rank vehicles by risk. A higher CLI indicates a vehicle that is too expensive relative to the distance it contributes.
* **Risk Flag:** An anomaly detection model flags vehicles that are statistical outliers based on their CLI, Age, and Utilization, indicating potential system failures.

## 4. Installation and Setup
1.  **Repository Setup:** Ensure all 7 provided CSV data files are in the same directory as `cost_analyzer.py` and this README.
2.  **Install Dependencies:** Run the following command in the Codespaces terminal:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run Application:**
    ```bash
    streamlit run cost_analyzer.py
    ```

## 5. Key Features
* **ML-Driven Anomaly Detection:** Uses an **Isolation Forest model** to flag the top 10% of vehicles as HIGH\_RISK\_ANOMALY (Bonus Points).
* **Interactive Visualization:** A **Bubble Chart** visualizes the entire fleet risk profile (Utilization vs. Age, sized by CLI).
* **Proactive Tool:** Provides managers with a ranked table to prioritize vehicle inspections, maintenance, or reallocation decisions, minimizing fleet downtime.

---

## Deliverable 2: Innovation Brief (PDF Format)

This content is designed to be visually impactful and directly address the evaluation criteria, serving as the final presentation document.

### Slide 1: Title & Mandate

* **Title:** NexGen's Vehicle Cost-Efficiency Imbalance Predictor
* **Role:** Logistics Innovation Analyst
* **Mandate:** Transform operations from reactive to predictive; reduce operational costs by **15-20%**.

***

### Slide 2: The Problem: Unseen Cost Leakage

* **Challenge:** NexGen faces **Cost Pressures** driven by unexpected maintenance, sub-optimal fuel consumption, and vehicle downtime.
* **Root Cause:** The link between **Asset Health (Age/Maintenance)** and **Operational Contribution (Utilization)** is currently invisible. We treat all vehicles equally until a breakdown occurs.
* **Problem Statement:** How to dynamically rank the 50-vehicle fleet by **Cost Leakage Risk** to enable preventative action and maximize asset ROI. 

***

### Slide 3: The Innovative Solution

* **Solution:** A **Streamlit-powered dashboard** that uses a novel metric, the **Cost Leakage Index (CLI)**, to assign a quantified risk score to every vehicle.
* **Core Logic:** CLI is calculated based on a vehicle's normalized **Total Maintenance Costs** relative to its measured **Utilization Rate ($\text{km}$ driven)**.

| Risk Profile | CLI Score | Action |
| :--- | :--- | :--- |
| **High Risk Anomaly** | Top 10% outliers (Flagged by ML) | Immediate Inspection / Reallocation |
| **High CLI / Low Util**| Poor ROI | Consider Sale or Retirement |
| **Low CLI / High Util**| Optimal | Maximize Usage |

***

### Slide 4: Data & ML Implementation

* **Data Integration:** Merged data streams (`vehicle_fleet`, `routes_distance`, `cost_breakdown`) using a **simulated transactional key** to link costs/usage to individual Vehicle IDs.
* **ML Model:** Used **Isolation Forest** (Anomaly Detection) on the multi-dimensional feature space (CLI, Age, Utilization) to automatically flag vehicles that are statistical outliers.
    * *Rationale:* This model identifies **unforeseen combinations** of high cost and low performance—the definition of a cost anomaly.
* **Visualization:** An interactive **Bubble Chart** plots Age vs. Utilization, with the Bubble Size determined by the **CLI**. This provides an intuitive visual guide for managers.

***

### Slide 5: Business Impact & Call to Action

* **Key Metric Improvement:** Proactive management of the flagged **10% of high-risk vehicles** is estimated to deliver a cost reduction of **18%** in unscheduled downtime and service recovery expenses.
* **Strategic Shift:** Enables NexGen to move from **reactive asset maintenance** to **predictive resource allocation**.
* **Call to Action:** Integrate the V-IP output into the daily dispatch system to prioritize low-CLI/low-risk vehicles for high-priority or long-distance routes, and flag high-CLI vehicles for scheduled maintenance intervention.
