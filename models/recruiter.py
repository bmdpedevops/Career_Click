from flask import jsonify
from database import mongo
from bson.objectid import ObjectId
from bson import json_util
import json

from models.common_model import getSingleRecord



def get_user_id(accessToken):
    access_token = accessToken
    user = mongo.db.recruiters.find_one({"access_token": access_token})
    if user:
        return user["_id"]
    return False


def updateUserData(whereCondition, setData):
    updateDB = {
        "$set": setData
    }
    # print(updateDB, whereCondition)
    update = mongo.db.recruiters.update_one(whereCondition, updateDB)
    if (update.modified_count > 0):
        return True
    else:
        return False


def generate_ref_id():
    nexNumData  = getSingleRecord('serial_ids',"66abcfe132487af6ff2ec967")
    if nexNumData:
        new_id = int(nexNumData['next_number']) 
        
        return {
            "ref_id":str(nexNumData['prefix']) + str(new_id).zfill(6),
            "next_number":str(new_id+1)
        }
    
def updated_ref_id(nextNum):
    mongo.db.serial_ids.update_one({'_id': ObjectId('66abcfe132487af6ff2ec967')}, {'$set': {'next_number': (nextNum)}})
    