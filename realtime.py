import sys
import os
from pymongo import MongoClient


class RealTimeProcessing:

    client = MongoClient()
    db = client.test_database
    collection = db.test_collection
    filename = "/home/user/Personal-Work/log_problem/out-copy.log"

    def process_logic(self):
        last_line = self.get_file_no(self.filename)

        for obj in last_line:
            print(obj)
        # print("Last line : {}".format((last_line)))
        
    def update_line_no(self,filename):
        num_lines = sum(1 for line in open(self.filename))
        self.collection.updateupdate(
                {"filename" : filename},
                {"$set": { "lastline" : num_lines}})
        print(num_lines)

    def get_file_no(self,filename):
        return self.db.collection.find({"filename":{"$eq":filename}})

if __name__ == '__main__':
    RealTimeProcessing().process_logic()


