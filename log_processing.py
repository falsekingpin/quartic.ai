# -*- coding: utf-8 -*-
__author__ = "Akshay Nar"

from pygrok import Grok
from pymongo import MongoClient
from datetime import datetime,timedelta
import subprocess

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
        line_no = self.get_total_number_of_lines(self.filename)
        nos_of_line = self.file_len(self.filename)
        print("No of lines : {}".format(nos_of_line))
        print("Total no of lines : {}".format(line_no))
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
        num_lines = self.get_total_number_of_lines(filename)
        print(num_lines)
        post_id = self.line_collection.insert_one(
            { filename.split('.')[0] : num_lines}).inserted_id
        print("insert file no id : {} ".format(post_id))

    def insert_data_from_file(self,filename):
        with open(filename) as f:
            text = f.readlines()
        self.insert_log_data(text)
    
    def insert_log_data(self,data):
        print("Line ------ : {}".format(data))
        for line in data:
            for phrase in self.keep_phrases:
                if phrase in line:
                    pattern = '%{TIMESTAMP_ISO8601:timestamp}%{SPACE}(\[%{WORD:pid}%{SPACE}%{POSINT:pid}])%{SPACE}(\[%{NUMBER:responsetime}?ms])%{SPACE}(\[%{WORD:uid}\s+%{WORD:uidname}])%{SPACE}(\[%{LOGLEVEL:loglevel}])%{SPACE}(%{URIPATHPARAM:request})%{SPACE}%{GREEDYDATA:syslog_message}'
                    grok = Grok(pattern)
                    grok_json = grok.match(line)
                    post_id = self.insert_data(grok_json)
                    print("Grok json : {}".format(grok_json))
                    # post_id = self.collection.insert_one(grok_json).inserted_id
                    print(post_id)
                    self.format_single_doc(post_id,grok_json)

    def insert_data(self,data):
        doc_id = None
        if(data[self.timestamp]):
            doc_id = self.collection.insert_one(data).inserted_id
        elif(data[self.filename_key]):
            print("Found filename key")
        return doc_id

    def format_single_doc(self,doc_id,obj):
        time = datetime.strptime(obj[self.timestamp],self.date_format)
        rtime = int(obj[self.responsetime])
        self.collection.update({'_id':doc_id},{'$set':{self.timestamp : time}})
        self.collection.update({'_id':doc_id},{'$set':{self.responsetime : rtime}})

    def file_len(self,fname):
        p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                                                stderr=subprocess.PIPE)
        result, err = p.communicate()
        if p.returncode != 0:
            raise IOError(err)
        return int(result.strip().split()[0])
    
    def get_total_number_of_lines(self,filename):
        return sum(1 for line in open(filename))


if __name__ == '__main__':
    ProcessLogFiles().process_logic()