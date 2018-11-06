# -*- coding: utf-8 -*-
__author__ = "Akshay Nar"

from pygrok import Grok
from pymongo import MongoClient

class ProcessLogFiles:
    infile = r"/home/user/Personal-Work/log_problem/out.log"
    client = MongoClient()
    db = client.test_database
    collection = db.test_collection
    keep_phrases = ["ERROR","INFO","DEBUG"]

    date_format = "%Y-%m-%d %H:%M:%S.%f"
    timestamp = "timestamp"
    responsetime = "responsetime"

    def process_logic(self):
        with open(self.infile) as f:
            text = f.readlines()

        for line in text:
            for phrase in self.keep_phrases:
                if phrase in line:
                    pattern = '%{TIMESTAMP_ISO8601:timestamp}%{SPACE}(\[%{WORD:pid}%{SPACE}%{POSINT:pid}])%{SPACE}(\[%{NUMBER:responsetime}?ms])%{SPACE}(\[%{WORD:uid}\s+%{WORD:uidname}])%{SPACE}(\[%{LOGLEVEL:loglevel}])%{SPACE}(%{URIPATHPARAM:request})%{SPACE}%{GREEDYDATA:syslog_message}'
                    grok = Grok(pattern)
                    grok_json = grok.match(line)
                    post_id = self.collection.insert_one(grok_json).inserted_id

    def format_data(self):
        for obj in self.collection.find():
            if obj[self.timestamp]:
                if type(obj[self.timestamp]) is not datetime:
                    time = datetime.strptime(obj[self.timestamp],self.date_format)
                    self.collection.update({'_id':obj['_id']},{'$set':{self.timestamp : time}})

        for obj in self.collection.find():
            if obj[self.responsetime]:
                if type(obj[self.responsetime]) is not str:
                    rtime = int(obj[self.responsetime])
                    self.collection.update({'_id':obj['_id']},{'$set':{self.responsetime : rtime}})

if __name__ == '__main__':
    ProcessLogFiles().process_logic()