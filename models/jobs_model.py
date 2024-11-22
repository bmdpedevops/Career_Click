from flask import jsonify
from database import mongo
from bson.objectid import ObjectId
from bson import json_util
import json

from models.common_model import getAllRecordsWithJoinsPagenation, getSingleRecord

table = "jobs"

def getAllJobsWithFiltersAndPagination(page,limit,search_term):
    pass




