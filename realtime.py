import sys
import os
from pymongo import MongoClient


class RealTimeProcessing:

    client = MongoClient()
    db = client.log_database
    collection = db.log_collection
    line_collection = db.line_no_collection
    filename = "/home/user/Personal-Work/log_problem/out-copy.log"

    def process_logic(self):
        last_line = self.get_file_no(self.filename)
        print(last_line)
        # print("Last line : {}".format((last_line)))

        # for obj in self.db.line_collection.find():
        #     print("andarr aya")
        #     print(obj[self.filename.split('.')[0]])
        # while last_line.hasNext():
        #     print(last_line.next())
        # print("Last line : {}".format((last_line)))
        
    def update_line_no(self,filename):
        num_lines = sum(1 for line in open(self.filename))
        self.collection.updateupdate(
                {"filename" : filename},
                {"$set": { "lastline" : num_lines}})
        print(num_lines)

    def get_file_no(self,filename):
        print("FileName : {}".format(filename))
        # result = db.collection.distinct("result")
        # find( { "text": { "search" : filename.split('.')[0] } } )
        return self.db.line_collection.find()

if __name__ == '__main__':
    RealTimeProcessing().process_logic()


