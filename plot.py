"""Plot Texas COVID-19 data."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dshstexas

# -------------------------------------------------------
# Local functions.
# -------------------------------------------------------
def xaxis_labels(df, n_ticks=6):
    n_dates = len(df.columns) - 1
    dates_ii = np.linspace(0, n_dates, n_ticks)
    dates_ii = [int(x) for x in dates_ii]
    xaxis_dates = [df.columns[x] for x in dates_ii]
    return xaxis_dates

# -------------------------------------------------------
# Read data.
# -------------------------------------------------------
data_dir = "bin/data-2020-08-17"
case_count_file = "%s/TexasCOVID19DailyCountyCaseCountData.xlsx" %data_dir
deaths_file = "%s/TexasCOVID19DailyCountyFatalityCountData.xlsx" %data_dir
active_cases_file = "%s/TexasCOVID-19ActiveCaseDatabyCounty.xlsx" %data_dir
tests_file = "%s/TexasCOVID-19CumulativeTestsOverTimebyCounty.xlsx" %data_dir
case_count_df = dshstexas.read(case_count_file)
deaths_df = dshstexas.read(deaths_file)
active_cases_df = dshstexas.read(active_cases_file)
tests_df = dshstexas.read(tests_file)

# -------------------------------------------------------
# Plot setup.
# -------------------------------------------------------
hede = "Texas COVID-19 data\n"
fig_props = {"figsize": (10,6)}

# -------------------------------------------------------
# Plot cumulative cases.
# -------------------------------------------------------
# sort counties by cumulative number of cases:
current_date = "2020-08-16"
case_count_df = case_count_df.sort_values(
    by=current_date,
    ascending=False)

# get x axis labels:
xaxis_dates = xaxis_labels(case_count_df)

# plot figure:
plt.figure()
plt.title("%stop 5 county cumulative case counts as of 2020-08-16" %hede)
for county in case_count_df.index[:5]:
    plt.scatter(
        case_count_df.columns,
        case_count_df.loc[county, :],
        label=county)
plt.xticks(xaxis_dates, rotation=45)
plt.grid()
plt.legend()
plt.xlabel("date")
plt.ylabel("cumulative count")
plt.tight_layout()
plt.savefig("bin/cumulative_cases.png", dpi=200)
plt.close()

# -------------------------------------------------------
# Plot cumulative deaths.
# -------------------------------------------------------
# sort counties by cumulative number of cases:
current_date = deaths_df.columns[-1]
deaths_df = deaths_df.sort_values(
    by=current_date,
    ascending=False)

# get x axis labels:
xaxis_dates = xaxis_labels(deaths_df)

# plot figure:
plt.figure()
plt.title("%stop 5 county cumulative death counts as of 2020-08-15" %hede)
for county in deaths_df.index[:5]:
    label="%s: %d total deaths" %(county, deaths_df.loc[county, current_date])
    plt.scatter(
        deaths_df.columns,
        deaths_df.loc[county, :],
        label=label)
plt.xticks(xaxis_dates, rotation=45)
plt.grid()
plt.legend()
plt.xlabel("date")
plt.ylabel("cumulative count")
plt.tight_layout()
plt.savefig("bin/cumulative_deaths.png", dpi=200)
plt.close()

