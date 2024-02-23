import pymongo
from fastapi.encoders import jsonable_encoder
import json

def alreadyBooked(classname, day, session):

    # Define the class name you want to query
    class_name = classname
    day = parseDay(day)

    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://admin:hello123@cluster0.obs63zv.mongodb.net/")  # Update the connection string as per your MongoDB configuration
    db = client["test"]  # Replace "your_database_name" with the name of your MongoDB database
    collection_timetable = db["timetables"]  # Replace "timetables" with the name of your collection
    collection_halls = db["hallschemas"]

    # Query documents based on the class name
    responseTT = collection_timetable.find_one({"className": class_name})

    classAssigned = []

    isAssigned = responseTT['TimeTable'][day]['Halls'][session]
    if isAssigned != '0':
        classAssigned.append(isAssigned)
        response = {
            "isAllocated": "true",
            "halls": classAssigned,
            "session": session
        }

    else:
        responseH = collection_halls.find()
        for hall in responseH:
            print(hall)
            if hall['schedule'][day]['sessions'][session] == '0':
                classAssigned.append(hall['hallId'])
        response = {
            "isAllocated": "false",
            "halls": classAssigned
        }

    print(response)
    client.close()

    return response


# {'_id': ObjectId('65d847935ce8994156670fbf'), 
#  'hallId': 'Y301', 
#  'status': 'active', 
#  'block': 'Y', 
#  'floor': 3, 
#  'schedule': [
    #             {'day': 'Monday', 
    #              'sessions': [], 
    #              '_id': ObjectId('65d84e3d04f21e2dace19069')
    #              }
    # ], 
#  '__v': 0}



def parseDay(day: str) -> int:
    switcher = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }

    return switcher.get(day, -1)


