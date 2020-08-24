"""Plot Texas COVID-19 data."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dshstexas

# set plot stuff:
from matplotlib.backends.backend_pdf import PdfPages
plt.rcParams.update(
    {"font.size": 14, 
     #"figure.figsize": (8,6),
    "lines.linewidth": 3})
    
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
# Read and manipulate data.
# -------------------------------------------------------
data_dir = "bin/data-2020-08-23"
case_count_file = "%s/TexasCOVID19DailyCountyCaseCountData.xlsx" %data_dir
case_count_df = dshstexas.read(case_count_file, datetime_header=True)

# timeline:
timeline = pd.read_excel("data/timeline.xlsx", comment="#", index_col="date")
short_timeline = timeline[timeline.include == 1].sort_values(by="date", axis=0)

# get total for state of Texas:
tx_df = pd.DataFrame(case_count_df.sum(axis=0), columns=["cumulative"])
tx_df["daily"] = tx_df.cumulative.diff()

# calculate 7-week rolling average:
tx_df["weekly_average"] = tx_df.daily.rolling(7).mean()

# -------------------------------------------------------
# Plot setup.
# -------------------------------------------------------
hede = "Texas COVID-19 data\n"
fig_props = {"figsize": (10,6)}
landscape_props = {"figsize": (8,16)}

# dates misc:
latest_date = tx_df.index[-1]
xaxis_dates = xaxis_labels(case_count_df)

# -------------------------------------------------------
# Plot daily cases for entire state.
# Portrait figure.
# -------------------------------------------------------
# create pdf to store long portrait figure:
pdf = PdfPages("2020-08-22-cases-timeline.pdf")

# plot figure:
plt.figure(**landscape_props)
plt.title("%sdaily state cases through %s" %(
    hede, 
    latest_date.strftime("%Y-%m-%d")))
plt.plot(
    tx_df.daily, 
    tx_df.index, 
    label="daily",
    alpha=0.3,
    color="blue")
plt.plot(
    tx_df.weekly_average, 
    tx_df.index, 
    label="7-day rolling average",
    alpha=1,
    color="blue",
    linestyle="--")

# timeline:
for date in short_timeline.index:
    if date == short_timeline.index[-1]:
        label="major health policy event"
    else:
        label=""
    plt.axhline(date, linestyle="--", color="black", linewidth=1, label=label)

plt.yticks(xaxis_dates)
plt.gca().invert_yaxis()
plt.xticks(rotation=45)
plt.xlim([0, 20e3])
plt.grid()
plt.legend(loc="upper right")
plt.xlabel("cases per day")
plt.ylabel("date")
plt.tight_layout()
pdf.savefig()

# close pdf:
pdf.close()

# -------------------------------------------------------
# Plot daily cases for entire state.
# Landscape figure.
# -------------------------------------------------------
# plot figure:
plt.figure(**fig_props)
plt.title("%sdaily state cases through %s" %(
    hede, 
    latest_date.strftime("%Y-%m-%d")))
plt.scatter(tx_df.index, tx_df.daily, label="daily")
plt.plot(tx_df.index, tx_df.weekly_average, label="7-day rolling average")
plt.xticks(xaxis_dates, rotation=45)
plt.grid()
plt.legend()
plt.xlabel("date")
plt.ylabel("cases per day")
plt.tight_layout()
plt.close()

# -------------------------------------------------------
# Plot cumulative cases for entire state.
# -------------------------------------------------------
# plot figure:
plt.figure(**fig_props)
plt.title("%scumulative state cases as of %s" %(
    hede, 
    latest_date.strftime("%Y-%m-%d")))
plt.scatter(tx_df.index, tx_df.cumulative, label="state cumulative")
plt.xticks(xaxis_dates, rotation=45)
plt.grid()
plt.legend()
plt.xlabel("date")
plt.ylabel("cumulative count")
plt.tight_layout()
plt.close()

# -------------------------------------------------------
# Show plots.
# -------------------------------------------------------
plt.show()





