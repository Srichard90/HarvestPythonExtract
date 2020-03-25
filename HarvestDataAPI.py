import requests
import json
import pyodbc
import time

start_time = time.time()

# Establish Date Ranges, Enter End Date, auto finds first date of that month
BookMonth = '2020-02-29'
DateGet = BookMonth.split('-')
StartDate = DateGet[0] + "-" + DateGet[1] + "-01"
EndDate = BookMonth

# SQL Server parameters
server = 'XXX Server IP XXX'
username='sa'
password='XXX PASS XXX'
database='XXX SQL DataBase Name XXX'
driver='{SQL Server}'
conn_string='DRIVER=%s;SERVER=%s;UID=%s;PWD=%s;DATABASE=%s' % (driver,server,username,password,database)
authToken = "Bearer " + "XXX AUTH TOKEN FROM HARVEST XXX"
accountID = "XXX HARVEST ACCOUNT ID XXX"

# Establish link to JSON through headers and parameters
url_address = "https://api.harvestapp.com/v2/time_entries/"
headers = {
    "Authorization": authToken,
    "Harvest-Account-ID": accountID
}
params = {
    "from": StartDate,
    "to": EndDate
}

# Establish connection to SQL Server and clear old data
conn = pyodbc.connect(conn_string)
cursor = conn.cursor()
exec_string = "DELETE FROM HarvestData WHERE date >= '{}' AND date <= '{}'".format(StartDate,EndDate)
cursor.execute(exec_string)
conn.commit()

# Grab total pages to cycle through
r = requests.get(url=url_address, headers=headers, params=params).json()
total_pages = (int(r['total_pages']) +1)

# Loop through all pages, push to SQL Server
for page in range(1, total_pages):
    url = "https://api.harvestapp.com/v2/time_entries?page="+str(page)
    response = requests.get(url=url, headers=headers, params=params).json()
    for data in response['time_entries']:
        date = data['spent_date']
        PeriodGet = date.split('-')
        BookPeriod = PeriodGet[0] + PeriodGet[1]
        client = data['client']['name'].replace("'","")
        projectName = data['project']['name'].replace("'","")
        projectCode = data['project']['code'].replace("'","")
        task = data['task']['name'].replace("'", "")
        hours = data['hours']
        billable = data['billable']
        employeeName = data['user']['name'].replace("'","")
        depConv = projectName.replace(".","")
        department = depConv[-3:]
        if data['billable_rate'] is None:
            billRate = 0
            billAmt = 0
        else:
            billRate = data['billable_rate']
            billAmt = (billRate * hours)
        if data['cost_rate'] is None:
            costRate = 0
            costAmt = 0
        else:
            costRate = data['cost_rate']
            costAmt = (costRate * hours)
        exec_string = "EXEC RefreshHarvestPython '{}', '{}', '{}', '{}', '{}', '{}', {:.2f}, '{}', '{}', '{}', {:.2f}, {:.2f}, {:.2f}, {:.2f}".format\
            (BookPeriod,date,client,projectName,projectCode,task,hours,billable,employeeName,department,billRate,billAmt,costRate,costAmt)
        cursor.execute(exec_string)
        conn.commit()

run_time = ("--- %s seconds ---" % (time.time() - start_time))

print("Run time: " + run_time)