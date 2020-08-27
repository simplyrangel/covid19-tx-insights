"""Plot Texas COVID-19 data."""
import numpy as np
import pandas as pd
import datetime
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

def mark_event(timeline, df, xloc, param="case"):
    for date in timeline.index:
        if date == timeline.index[-1]:
            label="statewide health policy event"
            va="top"
        else:
            label=""
            va="bottom"
        plt.axhline(
            date, 
            linestyle="-", 
            color="red", 
            label=label,
            linewidth=1)
        text = """%s\n%s\n7 day rolling %s average: %d"""%(
            date.strftime("%Y-%m-%d"), 
            timeline.loc[date, "event"], 
            param,
            df.loc[date, "weekly_average"])
        plt.text(
            xloc,
            date,
            text,
            va=va,
            ha="right",
            fontsize=10,
            color="red")

def metadata(date_pulled):
    return """Data pulled %s from the
Texas Department of State Health Services:
https://dshs.texas.gov/coronavirus/additionaldata.aspx

Code available on Github:
https://github.com/simplyrangel/covid19-tx-insights"""%date_pulled

# -------------------------------------------------------
# Read and manipulate data.
# -------------------------------------------------------
data_dir = "bin/data-2020-08-26"
case_count_file = "%s/TexasCOVID19DailyCountyCaseCountData.xlsx" %data_dir
death_count_file = "%s/TexasCOVID19DailyCountyFatalityCountData.xlsx" %data_dir
case_count_df = dshstexas.read(case_count_file, datetime_header=True)
death_count_df = dshstexas.read(death_count_file, datetime_header=True)

# deaths data on the Texas dashboard says all deaths past 
# 2020-08-12 are incomplete so let's ignore them:
complete_deaths = [x for x in death_count_df.columns if x <= datetime.datetime(year=2020,month=8,day=11)]
death_count_df = death_count_df.loc[:, complete_deaths]

# timeline:
timeline = pd.read_excel("data/timeline.xlsx", comment="#", index_col="date")
short_timeline = timeline[timeline.include == 1].sort_values(by="date", axis=0)

# get totals for state of Texas:
tx_cases_df = pd.DataFrame(case_count_df.sum(axis=0), columns=["cumulative"])
tx_cases_df["daily"] = tx_cases_df.cumulative.diff()
tx_deaths_df = pd.DataFrame(death_count_df.sum(axis=0), columns=["cumulative"])
tx_deaths_df["daily"] = tx_deaths_df.cumulative.diff()

# calculate 7-week rolling average:
tx_cases_df["weekly_average"] = tx_cases_df.daily.rolling(7).mean()
tx_deaths_df["weekly_average"] = tx_deaths_df.daily.rolling(7).mean()

# -------------------------------------------------------
# Plot setup.
# -------------------------------------------------------
hede = "Texas COVID-19 data\n"
fig_props = {"figsize": (10,6)}
landscape_props = {"figsize": (7,10)}

# dates misc:
latest_case_date = tx_cases_df.index[-1]
latest_death_date = tx_deaths_df.index[-1]
xaxis_dates = xaxis_labels(case_count_df)

# create pdf to store long portrait figure:
pdf = PdfPages("figures/2020-08-26-timeline.pdf")

# -------------------------------------------------------
# Plot daily cases for entire state.
# Portrait figure.
# -------------------------------------------------------
# plot case data:
plt.figure(**landscape_props)
plt.title("%sdaily state cases through %s" %(
    hede, 
    latest_case_date.strftime("%Y-%m-%d")))
plt.plot(
    tx_cases_df.daily, 
    tx_cases_df.index, 
    label="daily case count",
    alpha=0.3,
    color="blue",
    linewidth=2)
plt.plot(
    tx_cases_df.weekly_average, 
    tx_cases_df.index, 
    label="7-day rolling average",
    alpha=1,
    color="blue",
    linestyle="--")

# timeline:
mark_event(short_timeline, tx_cases_df, 17e3)

# metadata box:
plt.text(
    17e3,
    tx_cases_df.index[0]-datetime.timedelta(days=4),
    metadata("2020-08-26"),
    ha="right",
    va="top",
    fontsize=10)

# finish plot:
plt.yticks(xaxis_dates, rotation=60)
plt.gca().invert_yaxis()
plt.xticks(rotation=60)
plt.xlim([0, 17e3])
plt.legend(loc="lower right",fontsize=10)
plt.xlabel("cases per day")
plt.ylabel("date")
plt.tight_layout()
pdf.savefig()
plt.close()

# -------------------------------------------------------
# Plot daily deaths for entire state.
# Portrait figure.
# -------------------------------------------------------
# plot deaths data:
plt.figure(**landscape_props)
plt.title("%sdaily state deaths through %s" %(
    hede, 
    latest_death_date.strftime("%Y-%m-%d")))
plt.plot(
    tx_deaths_df.daily, 
    tx_deaths_df.index, 
    label="daily death count",
    alpha=0.3,
    color="black",
    linewidth=2)
plt.plot(
    tx_deaths_df.weekly_average, 
    tx_deaths_df.index, 
    label="7-day rolling average",
    alpha=1,
    color="black",
    linestyle="--")

# timeline:
mark_event(short_timeline, tx_deaths_df, 400, param="death")

# metadata box:
plt.text(
    400,
    tx_deaths_df.index[0]-datetime.timedelta(days=4),
    metadata("2020-08-26"),
    ha="right",
    va="top",
    fontsize=10)

# finish plot:
plt.yticks(xaxis_dates, rotation=60)
plt.gca().invert_yaxis()
plt.xticks(rotation=60)
plt.xlim([0, 400])
plt.legend(loc="lower right",fontsize=10)
plt.xlabel("deaths per day")
plt.ylabel("date")
plt.tight_layout()
pdf.savefig()
plt.close()

# -------------------------------------------------------
# close pdf:
# -------------------------------------------------------
pdf.close()




