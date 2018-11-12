import sys
import os
from pymongo import MongoClient
import log_processing
import linecache
import io
import subprocess
import time

class RealTimeProcessing:

    client = MongoClient()
    db = client.log_database
    collection = db.log_collection
    line_collection = db.line_no_collection
    filename = "/home/user/Personal-Work/log_problem/out.log"
    obj_id = None

    def process_logic(self):
        # closed_line_no = self.get_file_no(self.filename)
        # print("Closed line no : {}".format(closed_line_no))
        # last_line_no = log_processing.ProcessLogFiles().get_total_number_of_lines(self.filename)
        # print("last_line_no : {}".format(last_line_no))
        # self.process_lines(closed_line_no,last_line_no,self.filename)
        while True:
            closed_line = self.get_file_no(self.filename)
            last_line = log_processing.ProcessLogFiles().get_total_number_of_lines(self.filename)
            if(closed_line == last_line):
                time.sleep(10)
            else:
                self.process_lines(closed_line,last_line,self.filename)
                time.sleep(10)
        # line = io.open(self.filename, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True)
        # print(line)
        # for line in self.tail(self.filename):
        #     print(line)
        
    def update_line_no(self,last_line,filename):
        cur = self.db.line_no_collection.update({"_id":self.obj_id},
                {"$set": { filename : last_line}})

    def get_file_no(self,filename):
        number_of_lines = None 
        for obj in self.db.line_no_collection.find():
            number_of_lines = (obj[self.filename.split('.')[0]])
            self.obj_id = obj['_id']
        return number_of_lines
    
    def process_lines(self,closed_line_no,last_line_no,filename):
        print("closed line no : {}".format(closed_line_no))
        print("last line no : {}".format(last_line_no))
        for line_no in range(closed_line_no,last_line_no):
            line = linecache.getline(filename,line_no)
            print("Data in process_lines : {}".format(line))
            log_processing.ProcessLogFiles().insert_log_data(line)
        self.update_line_no(log_processing.ProcessLogFiles().get_total_number_of_lines(filename),filename.split('.')[0])

    def tail(self,filename):
        ## get existing lines
        for line in filename:
            yield line
        ## follow the remaining lines
        filename.seek(0, os.SEEK_END)
        while True:
            line = filename.readline()
            print(line)
            if not line:
                time.sleep(0.1)
                continue
            yield line

if __name__ == '__main__':
    RealTimeProcessing().process_logic()


