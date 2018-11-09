# -*- coding: utf-8 -*-
__author__ = "Akshay Nar"

# import pymongo
import pprint
from pymongo import MongoClient
from pymongo import ASCENDING
# import datetime
from datetime import datetime,timedelta
import matplotlib.pyplot as plot
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches


class GetData:  
    client = MongoClient()
    db = client.log_database
    collection = db.log_collection
    slots = 10
    plot_data = []
    x_axis_data = []
    y_axis_data = []
    day = None

    date_format = "%Y-%m-%d %H:%M:%S.%f"
    timestamp = "timestamp"
    responsetime = "responsetime"
    from_date = datetime(2018, 8, 30, 15, 24, 46, 846066)
    to_date = datetime(2018, 8, 30, 16, 24, 46, 846066)

    def process_logic(self):
        self.get_data()

    def get_data(self):
        initital_time = self.collection.find_one(sort=[(self.timestamp, 1)])[self.timestamp]
        print(initital_time)
        # hour_after = initital_time + timedelta(minutes=30)
        # print(hour_after) 

        for i in range(self.slots):
            plot_info = {}
            print(type(initital_time))
            day = initital_time.strftime("%Y-%m-%d")
            plot_info["day"] = day
            half_hour_after = initital_time + timedelta(minutes=30)
            count_errors = self.collection.find({"$and":[{"loglevel":"ERROR"},
                {self.timestamp: {"$gte":initital_time,"$lt": half_hour_after}}]}).count()
            plot_info["from_time"] = initital_time.strftime("%Y-%m-%d %H:%M:%S")
            plot_info["to_time"] = half_hour_after.strftime("%Y-%m-%d %H:%M:%S")
            plot_info["count_of_errors"] = count_errors
            plot_info[self.timestamp] = '{0} - {1}'.format(initital_time.strftime("%H:%M"),half_hour_after.strftime("%H:%M"))
            self.plot_data.append(plot_info)
            initital_time = half_hour_after


        for data in self.plot_data:
            x_axis = data[self.timestamp]
            y_axis = data["count_of_errors"]
            self.x_axis_data.append(x_axis)
            self.y_axis_data.append(y_axis)
            day = data["day"]


        # print(x_axis_data)
        # print(y_axis_data)
        # df = pd.DataFrame({
        #      'length': y_axis_data,
        #      }, index= x_axis_data)
        # hist = df.hist(bins=3)

        # plot.hist(y_axis_data,density=1, bins=20) 
        # plot.axis(x_axis_data)
        # plot.axis([10000, 99, 0, 0])  
        # plot.xlabel('Date')
        # plot.ylabel('Count')
        # plot.show()

        # for data in collection.find().sort("responsetime",pymongo.ASCENDING):
        #     print(data['responsetime'])


        response_time_count = self.collection.find({"loglevel": {"$not":{"$eq" : "ERROR" }}}).sort(self.responsetime,ASCENDING).count()
        print(response_time_count)

        response_time_list = []
        response_list_data = []
        for data in self.collection.find({"loglevel": {"$not":{"$eq" : "ERROR" }}}).sort(self.responsetime,ASCENDING):
            response_time_list.append(data)
            # print(data)
            
        print(response_time_list[response_time_count/2][self.responsetime])
        print(response_time_list[response_time_count/2 + response_time_count/3][self.responsetime])
        print(response_time_list[response_time_count - response_time_count/10][self.responsetime])

        plot.plot(self.x_axis_data,self.y_axis_data)
        red_patch = mpatches.Patch(color='red', label=day)
        plot.legend(handles=[red_patch])
        plot.xlabel('time')
        plot.ylabel('count')
        plot.show()

if __name__ == '__main__':
    GetData().process_logic()



