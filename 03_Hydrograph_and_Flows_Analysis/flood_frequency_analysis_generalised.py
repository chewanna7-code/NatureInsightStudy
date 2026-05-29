# -*- coding: utf-8 -*-
"""
Flood frequency comparison script

Purpose:
    Fits GEV and Gumbel distributions to annual maximum flow data and compares
    the fitted estimates with NatureInsight/SCALGO modelled peak flows.

How to use:
    1. Upload your AMAX Excel/CSV file to Colab or place it in the working folder.
    2. Edit the USER SETTINGS section below.
    3. Run the script.

Notes:
    - This script is intended for reproducible dissertation analysis.
    - Raw datasets are not included in the GitHub repository if they are large,
      licensed, or unsuitable for public sharing.
"""

# =============================================================================
# 0. IMPORT PACKAGES
# =============================================================================

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import genextreme, gumbel_r


# =============================================================================
# 1. USER SETTINGS
# =============================================================================

# File containing the annual maximum flow series.
# In Google Colab, upload the file and use something like:
# DATA_FILE = Path("/content/AMAX_mitford.xlsx")
DATA_FILE = Path("AMAX_mitford.xlsx")

# Excel sheet name or index. Use 0 for the first sheet.
SHEET_NAME = 0

# Column containing AMAX flow values.
# Use either a column name, e.g. "Flow", or a zero-based column index, e.g. 5.
FLOW_COLUMN = 5

# Return periods to estimate.
RETURN_PERIODS = np.array([10, 20, 50, 100, 200])

# NatureInsight/modelled baseline peak flows for equivalent return periods.
# Edit these values for a different catchment, outlet, or scenario.
NATUREINSIGHT_FLOWS = {
    10: 109.6069437,
    20: 125.1541477,
    50: 147.2691265,
    100: 165.4509013,
    200: 185.0643024,
}

# Optional observed/historic flood peaks to display as horizontal reference lines.
# Format: "label": flow_value
OBSERVED_PEAKS = {
    "Observed peak (2012)": 228,
    "Observed peak (2008)": 335,
}

# Output file names.
OUTPUT_TABLE = Path("Flood_Frequency_Comparison.xlsx")
OUTPUT_FIGURE = Path("Flood_Frequency_Comparison.png")


# =============================================================================
# 2. LOAD AND CLEAN FLOW DATA
# =============================================================================

def load_flows(file_path: Path, flow_column, sheet_name=0) -> pd.Series:
    """Load a flow series from an Excel or CSV file and remove non-numeric values."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Could not find {file_path}. Upload the file or update DATA_FILE."
        )

    if file_path.suffix.lower() in [".xlsx", ".xls"]:
        data = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    elif file_path.suffix.lower() == ".csv":
        data = pd.read_csv(file_path, header=None)
    else:
        raise ValueError("Unsupported file type. Use .xlsx, .xls, or .csv.")

    flows = pd.to_numeric(data[flow_column], errors="coerce").dropna()

    if flows.empty:
        raise ValueError("No numeric flow values were found. Check FLOW_COLUMN.")

    return flows


flows = load_flows(DATA_FILE, FLOW_COLUMN, SHEET_NAME)

print("Data loaded successfully.")
print(flows.describe())


# =============================================================================
# 3. ESTIMATE RETURN PERIOD FLOWS
# =============================================================================

# Exceedance probability formulation for return period estimates.
probabilities = 1 - (1 / RETURN_PERIODS)

# Generalised Extreme Value distribution fitted using maximum likelihood.
gev_params = genextreme.fit(flows)
gev_estimates = genextreme.ppf(probabilities, *gev_params)

# Gumbel distribution fitted using maximum likelihood.
gumbel_params = gumbel_r.fit(flows)
gumbel_mle_estimates = gumbel_r.ppf(probabilities, *gumbel_params)

# Gumbel estimates using the method of moments.
mean_flow = flows.mean()
std_flow = flows.std()
reduced_variate = -np.log(-np.log(1 - 1 / RETURN_PERIODS))
frequency_factor = (reduced_variate - 0.5772) / 1.2825
gumbel_moment_estimates = mean_flow + frequency_factor * std_flow

# NatureInsight values aligned with the selected return periods.
natureinsight_estimates = [NATUREINSIGHT_FLOWS[rp] for rp in RETURN_PERIODS]


# =============================================================================
# 4. CREATE COMPARISON TABLE
# =============================================================================

comparison_table = pd.DataFrame(
    {
        "Return Period (years)": RETURN_PERIODS,
        "GEV Flow (m³/s)": gev_estimates,
        "Gumbel MLE (m³/s)": gumbel_mle_estimates,
        "Gumbel Moments (m³/s)": gumbel_moment_estimates,
        "NatureInsight (m³/s)": natureinsight_estimates,
    }
).round(0)

print("\nComparison table:")
print(comparison_table)


# =============================================================================
# 5. PLOT RESULTS
# =============================================================================

plt.figure(figsize=(8, 5))

plt.plot(RETURN_PERIODS, gev_estimates, marker="o", label="GEV")
plt.plot(RETURN_PERIODS, gumbel_mle_estimates, marker="o", label="Gumbel (MLE)")
plt.plot(
    RETURN_PERIODS,
    gumbel_moment_estimates,
    marker="o",
    linestyle="--",
    label="Gumbel (Moments)",
)
plt.plot(RETURN_PERIODS, natureinsight_estimates, marker="o", label="NatureInsight")

for label, value in OBSERVED_PEAKS.items():
    plt.axhline(y=value, linestyle="--", label=label)

plt.xlabel("Return period (years)")
plt.ylabel("Peak flow (m³/s)")
plt.title("Flood Frequency Comparison")
plt.xscale("log")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(OUTPUT_FIGURE, dpi=300)
plt.show()


# =============================================================================
# 6. EXPORT OUTPUTS
# =============================================================================

comparison_table.to_excel(OUTPUT_TABLE, index=False)

print(f"\nTable exported to: {OUTPUT_TABLE}")
print(f"Figure exported to: {OUTPUT_FIGURE}")
