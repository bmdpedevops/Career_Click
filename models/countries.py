import json
from database import mongo
from bson.objectid import ObjectId
from bson import json_util
from utils.jithu_helper import convertTimeStampToDate

def getCountries():
    
    pipeline = [
        {
            "$group": {
                "_id": "$country"  # Group by the 'country' field
            }
        },
        {
            "$project": {
                "_id": 0,  # Exclude the _id field from the output
                "country": "$_id"  # Rename '_id' to 'country'
            }
        }
    ]
    resultList = mongo.db.locations.aggregate(pipeline)
    all = list(json.loads(json_util.dumps(resultList)))

    return all

def getStates():
    country = "India"
    pipeline = [
         {"$match": {
                "country": country
            }
        }, 
         {
            "$sort": {
                "_id": 1  # Sort by city name in ascending order
            }
        },
        {
            "$group": {
                "_id": "$state_name"  # Group by the 'country' field
            }
        },
        {
            "$project": {
                "_id": 0,  # Exclude the _id field from the output
                "state_name": "$_id"   # Rename '_id' to 'country'
            }
        }
    ]
    resultList = mongo.db.locations.aggregate(pipeline)
    all = list(json.loads(json_util.dumps(resultList)))

    return all


def getCities(state):
    stateName = state
    
    pipeline = [
        {"$match": {
                "state_name": stateName
            }
        },
        {
            "$group": {
                "_id": "$city",
                "lat": {"$first": "$lat"}, 
                "lng": {"$first": "$lng"}, 
                "location": {"$first": "$location"}  
            }
        },
        {
            "$sort": {
                "_id": 1  
            }
        },
        {
            "$project": {
                "_id": 0,  
                "state_name": {"$literal": stateName},  
                "lat": 1,
                "lng": 1,
                "location": 1,
                "city": "$_id"   
            }
        }
    ]
    
    resultList = mongo.db.locations.aggregate(pipeline)
    all = list(json.loads(json_util.dumps(resultList)))

    return all