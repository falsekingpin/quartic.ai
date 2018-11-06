# count_of_errors = []

# for obj in collection.find():
#         if obj[timestamp]:
#             if type(obj[timestamp]) is not datetime:
#                 time = datetime.strptime(obj[timestamp],date_format)
#                 collection.update({'_id':obj['_id']},{'$set':{timestamp : time}})

# for obj in collection.find():
#         if obj[responsetime]:
#             if type(obj[responsetime]) is not str:
#                 rtime = int(obj[responsetime])
#                 collection.update({'_id':obj['_id']},{'$set':{responsetime : rtime}})

# for find in db.collection.find({$and:[{"loglevel":"ERROR"},
#     {"timestamp": {"$gte":from_date,"$lt": to_date}}]}):
#     count_of_errors.append(find)


# for doc in db.collection.find(
#     {"timestamp": {"$gte":from_date,"$lt": to_date}}):
#     pprint(doc)
# print("Count of errors : {}".format((count_of_errors)))

# count_errors = collection.find({"$and":[{"loglevel":"ERROR"},
#     {"timestamp": {"$gte":from_date,"$lt": to_date}}]}).distinct("timestamp").count()
# print(count_errors)

# for single_collection in collection.find({"$and":[{"loglevel":"ERROR"},
#     {"timestamp": {"$gte":from_date,"$lt": to_date}}]}):
#     pprint.pprint(single_collection)

# for single_collection in collection.find({"$and":[{"loglevel":"ERROR"},
#     {"timestamp": {"$gte":from_date,"$lt": to_date}}]}).distinct("timestamp"):
#     pprint.pprint(single_collection)