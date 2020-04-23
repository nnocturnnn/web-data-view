from spyre import server
import csv
import pandas as pd

uniqRegion = []
uniqTemp = ["VCI","TCI","VHI"]

def csv_read(file):
    reader = csv.DictReader(file, delimiter=',')
    for line in reader:
        if line["Region"] not in uniqRegion:
            uniqRegion.append(line["Region"])


with open("alldata.csv",encoding='utf-8') as f_obj:
    csv_read(f_obj)

def csv_region(file, region, year, f_week, s_week):
    lst = []
    reader = csv.DictReader(file, delimiter=',')
    for line in reader:
        if line["Region"] == region:
            if line["year"] == year:
                if float(line["week"]) > f_week and  float(line["week"]) < s_week:
                    lst.append(line)
    return lst

def fApp(listname):
    listy = []
    for i in range(len(listname)):
        listy.append(dict({'label' : listname[i],
                           'value' : listname[i]}))
    return listy

RegionforApp = fApp(uniqRegion)
TmpforApp = fApp(uniqTemp)


class SimpleApp(server.App):
    title = "Vertolet"
    inputs = [{
        "type": 'dropdown',
        "label": 'Region',
        "options": RegionforApp,
        "value": 'GOOG',
        "key": 'region',
        "action_id": "update_data"
    },
    {
        "type": 'dropdown',
        "label": 'Time series',
        "options": TmpforApp,
        "value": 'GOOG',
        "key": 'vh',
        "action_id": "update_data"
    },
   {
        "type":'text',
        "label": 'Index',
        "value" : '2016 12-32',
        "key": 'title',
        "action_id" : "refresh",
    }]

    tabs = ["Plot", "Table"]

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]


    def getData(self, params):
        region = params['region']
        data = params['title']
        year = data.split(' ')[0]
        weeks = data.split(' ')[1]
        f_week = int(weeks.split('-')[0])
        s_week = int(weeks.split('-')[1])
        with open("alldata.csv",encoding='utf-8') as t_obj:
            regionData = csv_region(t_obj,region,year,f_week,s_week)
        df = pd.DataFrame.from_records(regionData)
        del df['Region']
        del df['week']
        return df

    def getPlot(self, params):
        vh = params['vh']
        df = self.getData(params).set_index('year').drop([vh], axis=1)
        df=df.astype(float) 
        plt_obj = df.plot()
        plt_obj.set_ylabel(vh)
        plt_obj.set_xlabel("Date")
        plt_obj.set_title(params['region'])
        fig = plt_obj.get_figure()
        return fig
    
app = SimpleApp()
app.launch(port=9093)