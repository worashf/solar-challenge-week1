
## 📊 Task 2: Data Profiling, Cleaning & EDA

### 🎯 Objective

Perform an end-to-end exploratory data analysis (EDA) and cleaning workflow for a specific country's solar dataset. Prepare the data for downstream tasks such as comparison and region-ranking.

---

### 🗂️ Branch Naming Convention

Create a separate branch for each country’s EDA:

```
eda-[benin | togo |sierraleone]   # Example: eda-benin
```

---

### 📓 Notebook Naming Convention

Each country's notebook should follow the format:

```
<country>_eda.ipynb   # Example: benin_eda.ipynb
```

---

### 🔧 EDA Steps

#### 1. Summary Statistics & Missing Values

* Use `df.describe()` for numeric summary.
* Check for missing values:
  `df.isna().sum()`
* Flag any column with **>5% null values**.

#### 2. Outlier Detection & Basic Cleaning

* Focus on columns: `GHI`, `DNI`, `DHI`, `ModA`, `ModB`, `WS`, `WSgust`
* Compute **Z-scores** and flag outliers (`|Z| > 3`)
* Handle missing values:

  * Drop rows or impute using **median**
* Save cleaned data:

  * `data/<country>_clean.csv`
  * ⚠️ Ensure the `data/` directory is listed in `.gitignore` (do not commit raw or cleaned CSVs)

#### 3. Time Series Analysis

* Line/bar plots: `GHI`, `DNI`, `DHI`, `Tamb` vs. `Timestamp`
* Analyze trends by:

  * Day
  * Month
  * Peak/off-peak periods

#### 4. Cleaning Impact

* Compare `ModA`, `ModB` readings **pre/post-cleaning** using:

  ```python
  df.groupby('Cleaning')[['ModA', 'ModB']].mean()
  ```

#### 5. Correlation & Relationship Analysis

* Correlation heatmap:

  * Columns: `GHI`, `DNI`, `DHI`, `TModA`, `TModB`
* Scatter plots:

  * `WS`, `WSgust`, `WD` vs. `GHI`
  * `RH` vs. `Tamb`, `RH` vs. `GHI`

#### 6. Wind & Distribution Analysis

* Create wind rose or radial plots for `WS` and `WD`
* Plot histograms:

  * `GHI`
  * Another relevant variable (e.g., `WS`)

#### 7. Temperature & Humidity Interaction

* Explore how **relative humidity (`RH`)** affects:

  * Temperature (`Tamb`)
  * Solar radiation (`GHI`, `DNI`, etc.)

#### 8. Bubble Chart

* `GHI` vs. `Tamb`, with bubble size representing:

  * `RH` (Relative Humidity)
  * or `BP` (Barometric Pressure)



