# Predictive Forecasting of Care Load & Placement Demand

## Project Overview
This project explores historical data from the Unaccompanied Alien Children (UAC) Program to understand changes in children entering, remaining in, and leaving federal care. It builds simple, explainable forecasting baselines for HHS care load and discharges.

## Objectives
- Clean and inspect the source CSV.
- Explore HHS care load, CBP transfers, and HHS discharges.
- Compare naive, moving-average, and Random Forest forecasting approaches.
- Evaluate predictions using MAE, RMSE, and MAPE.
- Generate baseline 30-day projections.
- Document data-quality issues and limitations.

## Dataset
The dataset contains:
- `Date`
- `Children apprehended and placed in CBP custody*`
- `Children in CBP custody`
- `Children transferred out of CBP custody`
- `Children in HHS Care`
- `Children discharged from HHS Care`

The available reporting dates span January 2023 to December 2025. The cleaned data contains 720 reporting dates across a 1,075-day calendar range, leaving 355 dates (33.02%) without a reporting record.

## Tools
- Python
- Jupyter Notebook
- pandas
- NumPy
- Matplotlib
- scikit-learn

## Workflow
1. Inspect and clean the data: parse dates, convert numeric fields, remove fully blank rows, and sort chronologically.
2. Check data quality: duplicate dates, missing values, and missing calendar dates.
3. Perform EDA: summary statistics and historical charts for HHS care load, transfers, and discharges.
4. Engineer lag, rolling-average, and calendar features.
5. Build baseline models: naive forecast, moving average, and Random Forest.
6. Evaluate with MAE, RMSE, and MAPE.
7. Export baseline 30-day forecasts and model-comparison tables.

## Models
- **Naive Forecast:** repeats the latest training observation.
- **Moving Average:** forecasts using the average of recent observations.
- **Random Forest Regressor:** learns patterns from lag, rolling-average, and calendar features.

## Initial HHS Care Load Results
The current notebook evaluation reported:

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Naive Forecast | 186.51 | 227.23 | 8.76% |
| Moving Average | 33.25 | 40.61 | 1.48% |
| Random Forest | 62.72 | 85.17 | 2.91% |

These are preliminary results. The evaluation procedures are not fully consistent: the moving-average model uses actual test observations for rolling one-step-ahead predictions, while the Random Forest uses historical lag features. Re-evaluate all models on the same dates and with the same forecasting protocol before selecting a final model. Add discharge-model results from the notebook's `discharge_comparison` table when available.

## Forecast Outputs
When the notebook cells run successfully, the `project_outputs/` folder is intended to contain:
- `HHS_Care_Forecast.csv`
- `HHS_Discharge_Forecast.csv`
- `HHS_Care_Model_Comparison.csv`
- `HHS_Discharge_Model_Comparison.csv`

## Limitations
- **Missing reporting dates:** 355 of 1,075 calendar dates (33.02%) have no record. Missing dates should not automatically be treated as zero activity.
- **Irregular time steps:** `shift(7)` means seven available observations, not necessarily seven calendar days.
- **Discharge counts vs. demand:** Recorded discharges do not directly measure unmet placement demand or available placement capacity.
- **Baseline forecasts:** The current 30-day moving-average projection repeats a constant recent average and is not a validated changing-trend forecast.
- **Uncertainty:** Confidence intervals and capacity-breach probabilities have not yet been implemented or validated.
- **Operational decisions:** Treat forecasts as exploratory until data quality and evaluation are improved; do not use them alone for staffing or placement decisions.

## How to Run
1. Make sure the source CSV path in `unified.ipynb` is correct.
2. Open `unified.ipynb` in Jupyter Notebook.
3. Run cells in order from data loading through cleaning, EDA, modeling, evaluation, and export.
4. Confirm the expected CSVs appear in `project_outputs/`.

## Suggested Repository Structure
```text
Predictive_Forecasting_Project/
├── unified.ipynb
├── HHS_Unaccompanied_Alien_Children_Program.csv
├── README.md
└── project_outputs/
    ├── HHS_Care_Forecast.csv
    ├── HHS_Discharge_Forecast.csv
    ├── HHS_Care_Model_Comparison.csv
    └── HHS_Discharge_Model_Comparison.csv
```

## Conclusion
This notebook demonstrates an initial workflow for historical analysis and baseline forecasting of HHS care load and discharges. The most important next improvement is to address missing reporting dates and evaluate all models consistently before interpreting forecasts as reliable operational guidance.
