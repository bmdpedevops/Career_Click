from flask import jsonify
from database import mongo
from bson.objectid import ObjectId
from bson import json_util
import json

from models.common_model import getSingleRecord



def get_user_id(accessToken):
    access_token = accessToken
    user = mongo.db.users.find_one({"access_token": access_token})
    if user:
        return user["_id"]
    return False


def updateUserData(whereCondition, setData):
    updateDB = {
        "$set": setData
    }
    # print(updateDB, whereCondition)
    update = mongo.db.users.update_one(whereCondition, updateDB)
    if (update.modified_count > 0):
        return True
    else:
        return False

def getMembersList(company_id): 
    fetch_data = mongo.db.users.find().sort('_id', -1)
    # Convert ObjectId to string for serialization
    data_fetched = list(json.loads(json_util.dumps(fetch_data)))
    return data_fetched

def generate_ref_id():
    nexNumData  = getSingleRecord('serial_ids',"66a408bba70c7a8d9ca471c9")
    if nexNumData:
        new_id = int(nexNumData['next_number']) 
        
        return {
            "ref_id":str(nexNumData['prefix']) + str(new_id).zfill(6),
            "next_number":str(new_id+1)
        }
    
def updated_ref_id(nextNum):
    mongo.db.serial_ids.update_one({'_id': ObjectId('66a408bba70c7a8d9ca471c9')}, {'$set': {'next_number': (nextNum)}})
    