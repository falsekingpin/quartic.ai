# -*- coding: utf-8 -*-
__author__ = "Akshay Nar"

from pygrok import Grok
from pymongo import MongoClient
from datetime import datetime,timedelta

class ProcessLogFiles:
    filename = "/home/user/Personal-Work/log_problem/out.log"
    # infile = r"/home/user/Personal-Work/log_problem/out.log"
    client = MongoClient()
    db = client.log_database
    collection = db.log_collection
    line_collection = db.line_no_collection
    keep_phrases = ["ERROR","INFO","DEBUG"]

    date_format = "%Y-%m-%d %H:%M:%S.%f"
    timestamp = "timestamp"
    responsetime = "responsetime"
    filename_key = "filename"

    def process_logic(self):
        self.insert_data_from_file(self.filename)
        self.format_data()
        self.insert_file_no(self.filename)

    def format_data(self):
        for obj in self.collection.find():
            print(obj[self.timestamp])
            if obj[self.timestamp]:
                if type(obj[self.timestamp]) is not datetime:
                    time = datetime.strptime(obj[self.timestamp],self.date_format)
                    self.collection.update({'_id':obj['_id']},{'$set':{self.timestamp : time}})

        for obj in self.collection.find():
            if obj[self.responsetime]:
                if type(obj[self.responsetime]) is not str:
                    rtime = int(obj[self.responsetime])
                    self.collection.update({'_id':obj['_id']},{'$set':{self.responsetime : rtime}})


    def insert_file_no(self,filename):
        num_lines = sum(1 for line in open(self.filename))
        print(num_lines)
        post_id = self.line_collection.insert_one(
            { filename.split('.')[0] : num_lines}).inserted_id
        print("insert file no id : {} ".format(post_id))

    def insert_data_from_file(self,filename):
        with open(filename) as f:
            text = f.readlines()

        for line in text:
            for phrase in self.keep_phrases:
                if phrase in line:
                    pattern = '%{TIMESTAMP_ISO8601:timestamp}%{SPACE}(\[%{WORD:pid}%{SPACE}%{POSINT:pid}])%{SPACE}(\[%{NUMBER:responsetime}?ms])%{SPACE}(\[%{WORD:uid}\s+%{WORD:uidname}])%{SPACE}(\[%{LOGLEVEL:loglevel}])%{SPACE}(%{URIPATHPARAM:request})%{SPACE}%{GREEDYDATA:syslog_message}'
                    grok = Grok(pattern)
                    grok_json = grok.match(line)
                    post_id = self.insert_data(grok_json)
                    # post_id = self.collection.insert_one(grok_json).inserted_id
                    print(post_id)

    def insert_data(self,data):
        doc_id = None
        if(data[self.timestamp]):
            doc_id = self.collection.insert_one(data).inserted_id
        elif(data[self.filename_key]):
            print("Found filename key")
        return doc_id

    def format_single_doc(self,doc_id):
        self.collection.update({'_id':doc_id},{'$set':{self.timestamp : time}})
        self.collection.update({'_id':doc_id},{'$set':{self.responsetime : rtime}})

if __name__ == '__main__':
    ProcessLogFiles().process_logic()