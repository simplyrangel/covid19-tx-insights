"""Get the latest COVID-19 data from the web. Texas COVID-19 data 
provided by the Texas Department of State Health Services.

Texas DSHS COVID-19 website:
https://dshs.texas.gov/coronavirus/additionaldata.aspx
"""
import requests
import datetime
import subprocess

# -------------------------------------------------------------
# Local functions.
# -------------------------------------------------------------
def create_daily_dir():
	today = datetime.date.today().strftime("%Y-%m-%d")
	subprocess.Popen(["mkdir", "data/%s" %today])

# -------------------------------------------------------------
# Local functions.
# -------------------------------------------------------------
dshs_urls = [
	"https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyCaseCountData.xlsx",
	"https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyFatalityCountData.xlsx",
	"https://dshs.texas.gov/coronavirus/TexasCOVID-19ActiveCaseDatabyCounty.xlsx",
	"https://dshs.texas.gov/coronavirus/TexasCOVID-19CumulativeTestsOverTimebyCounty.xlsx"]
create_daily_dir()
today = datetime.date.today().strftime("%Y-%m-%d")
for url in dshs_urls:
	spreadsheet = url.split("/")[-1]
	r = requests.get(url)
	with open("data/%s/%s" %(today, spreadsheet), "wb") as of:
		of.write(r.content)

